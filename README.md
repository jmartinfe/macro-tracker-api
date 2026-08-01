# 🥑 Macro Tracker API
A minimalist REST API built with **FastAPI** that processes natural language inputs (written or voice-transcribed) to track daily macronutrients using an AI agent with **Pydantic Structured Outputs**.

## 🚀 Features
- **Natural Language Inputs:** Designed to digest freeform text or voice transcriptions (e.g., *"I ate 2 eggs and an avocado for breakfast"*).
- **Structured AI Agent:** Guarantees strict JSON schema responses using OpenAI (`gpt-4o-mini`) and Pydantic validation.
- **Local Persistence:** Manages daily state via a local JSON file with automatic reset logic when a new day starts.
- **Dynamic CORS & Config:** Environment-driven CORS settings for seamless deployment across different frontends.

## 🛠️ Prerequisites
- Python 3.10+
- OpenAI API Key (`OPENAI_API_KEY`)

## ⚙️ Setup & Installation

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
Create a .env file in the root directory based on the example below:
    ```
    OPENAI_API_KEY=sk-proj-your-actual-api-key
    ALLOWED_ORIGINS=http://localhost:5500,[https://your-frontend.vercel.app](https://your-frontend.vercel.app)
    ```
5. **Run the application:**

    ```
    uvicorn app.main:app --reload
    ```

Access the interactive API docs at http://127.0.0.1:8000/docs.

## 📡 API Endpoints

All tracker endpoints are prefixed with `/tracker`.

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/tracker/health` | Health check endpoint to verify API availability. |
| `GET` | `/tracker/daily_tracker_state/{id}` | Retrieves the current daily state and macros for a specific user/session ID. |
| `POST` | `/tracker/process_input` | Processes natural language text/voice input and updates the tracker state. |
| `PUT` | `/tracker/update_meal_entry?id={id}` | Updates an existing meal entry within the specified state file. |
| `DELETE` | `/tracker/delete_meal_entry?meal_id={meal_id}&id={id}` | Removes a specific meal entry by its ID. |
| `DELETE` | `/tracker/clean_old_states` | Administrative cleanup task that purges outdated state files. |

