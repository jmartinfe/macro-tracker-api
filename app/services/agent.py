from datetime import date
import os
from openai import OpenAI
from app.schemas.tracker import DailyTrackerState

# Initialize the OpenAI client using the API key from environment variables
def get_openai_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY environment variable is not set. Please set it to your OpenAI API key."
        )
    return OpenAI(api_key=api_key)

# Define the system prompt that guides the LLM's behavior for processing user input related to nutrition tracking.
SYSTEM_PROMPT = """
Eres un asistente experto en nutrición y seguimiento de macronutrientes.
Tu objetivo es analizar la instrucción en texto del usuario y actualizar el estado actual del registro diario (`DailyTrackerState`).

### Reglas de Negocio Específicas del Usuario:
1. **Pasta:** Si el usuario menciona "pasta" o "macarrones" sin especificar peso, asume SIEMPRE 100g en seco (aprox. 350 kcal, 12g proteína, 72g carbohidratos, 1.5g grasa).
2. **Arroz:** Si menciona "arroz", asume SIEMPRE arroz integral, 100g en seco salvo que se indique otra cosa.
3. **Huevos / Sándwiches:** 
   - Si dice "sándwich de huevo" con 2 huevos, calcula los 2 huevos E INCLUYE implícitamente el aceite de cocina para hacer los huevos y la mantequilla para tostar el pan.
4. **Comidas Genéricas:** Si no especifica cantidades exactas, realiza una estimación nutricional estándar razonable.

### Instrucciones de Modificación del JSON (`DailyTrackerState`):
- **Añadir Comida:** Si el usuario quiere registrar un nuevo alimento, genera un nuevo objeto `MealItem` con un `id` único (por ejemplo: 'meal_' seguido de un entero o sufijo corto) y añádelo a la lista `meals`.
- **Modificar Comida:** Si el usuario pide cambiar una comida ya existente en el día (ej: "en el pollo de antes no eran 200g, eran 150g"), localízala dentro de `meals`, actualiza sus valores de macros y mantén su `id`.
- **Borrar Comida:** Si el usuario pide eliminar una comida expresamente, remuévela de la lista `meals`.
- **Acción por defecto:** Si el usuario menciona un alimento o comida sin especificar acción, genera un nuevo objeto `MealItem` con un `id` único (por ejemplo: 'meal_' seguido de un entero o sufijo corto) y añádelo a la lista `meals`.
- **Inputs No Relacionados:** Si la frase del usuario no tiene nada que ver con alimentos, nutrición o comidas (ej: "Hola", "¿Qué hora es?", "Añade una reunión a mi calendario"), **NO modifiques la lista `meals`**. Devuelve exactamente el estado actual recibido sin alterar los registros.

### Reglas de Formato:
- Mantén la fecha (`date`) y los objetivos (`goals`) intactos tal como vienen en el estado actual.
- Los valores de calorías deben ir en kcal y las proteínas, carbohidratos y grasas en gramos (enteros).
"""


def run_agent(user_input: str, current_state: DailyTrackerState) -> DailyTrackerState:
    """Send the user input and current tracker state to the LLM agent for processing and return the updated state.
    """
    client = get_openai_client()
    try:
        # Prepare the messages for the LLM, including the system prompt and user input with current state
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    f"CURRENT STATE:\n{current_state.model_dump_json(indent=2)}\n\n"
                    f"USER INSTRUCTION:\n\"{user_input}\""
                ),
            },
        ]

        
        completion = client.beta.chat.completions.parse(
            model="gpt-4o-mini", # LLM model to use for processing the input
            messages=messages,
            response_format=DailyTrackerState,
            temperature=0.1,  # Low temperature for more deterministic output
        )

        
        updated_state: DailyTrackerState = completion.choices[0].message.parsed

        if updated_state is None:
            raise ValueError(
                "The LLM failed to parse the response into the expected format."
            )

        return updated_state

    except Exception as e:
        
        raise RuntimeError(
            f"Error processing input with LLM: {str(e)}"
        )