# Macro Tracker API
A minimalist REST API built with **FastAPI** that processes natural language inputs (written or voice-transcribed) to track daily macronutrients using an AI agent with **Pydantic Structured Outputs**.

## Features
- **Natural Language Inputs:** Designed to digest freeform text or voice transcriptions (e.g., *"I ate 2 eggs and an avocado for breakfast"*).
- **Structured AI Agent:** Guarantees strict JSON schema responses using OpenAI (`gpt-4o-mini`) and Pydantic validation.
- **Local Persistence:** Manages daily state via a local JSON file with automatic reset logic when a new day starts.
- **Dynamic CORS & Config:** Environment-driven CORS settings for seamless deployment across different frontends.

## Prerequisites
- Python 3.10+
- OpenAI API Key (`OPENAI_API_KEY`)

## Setup & Installation

1. **Clone the repository:**
   ```
   bash
   git clone [https://github.com/your-username/macro-tracker-api.git](https://github.com/your-username/macro-tracker-api.git)
   cd macro-tracker-api
   ```

2. **Create and activate a virtual environment:**
    ```
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install dependencies:**
    ```
    pip install -r requirements.txt
    ```

4. **Environment Variables:**
Create a `.env` file in the root directory based on the example below:
    ```
    OPENAI_API_KEY=sk-proj-your-actual-api-key
    API_KEY=your-internal-api-key
    ALLOWED_ORIGINS=http://localhost:5500,https://your-frontend.vercel.app
    ENVIRONMENT=development
    APP_TITLE=Macro Tracker API
    ```

### Current environment variables

- `OPENAI_API_KEY`: Your OpenAI API key used by the AI agent.
- `API_KEY`: The API key required by frontend requests in the `X-API-Key` header.
- `ALLOWED_ORIGINS`: Comma-separated list of allowed CORS origins.
- `ENVIRONMENT`: Set to `production` to disable docs endpoints (`/docs`, `/redoc`, `/openapi.json`). Otherwise defaults to `development`.
- `APP_TITLE`: Optional API title shown in FastAPI metadata.

5. **Run the application:**

    ```
    uvicorn app.main:app --reload
    ```

Access the interactive API docs at http://127.0.0.1:8000/docs.

## API Endpoints

All tracker endpoints are prefixed with `/tracker`.

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/tracker/health` | Health check endpoint to verify API availability. |
| `GET` | `/tracker/daily_tracker_state/{id}?input_date={yyyy-mm-dd}` | Retrieves the daily tracker state for a specific user/session ID and date. |
| `POST` | `/tracker/process_input` | Processes natural language input and updates the tracker state for the given date. |
| `PUT` | `/tracker/update_meal_entry?id={id}&input_date={yyyy-mm-dd}` | Updates an existing meal entry in the specified state file for the given date. |
| `DELETE` | `/tracker/delete_meal_entry?meal_id={meal_id}&id={id}&input_date={yyyy-mm-dd}` | Removes a specific meal entry by its ID for the given date. |
| `DELETE` | `/tracker/clean_old_states?input_date={yyyy-mm-dd}` | Deletes state files older than the provided date. |

### Endpoint parameter details

- `id` (string): The user or session ID used to name the state file.
- `input_date` (YYYY-MM-DD): The date for which tracker state should be loaded or modified.

### Request body for `/tracker/process_input`

```json
{
  "id": "juan",
  "input_date": "2026-08-10",
  "user_input": "2 huevos, 100g avena"
}
```

### Request body for `/tracker/update_meal_entry`

```json
{
  "id": "meal-id-123",
  "name": "Huevos revueltos",
  "calories": 220,
  "protein": 14,
  "carbs": 2,
  "fats": 16
}
```

