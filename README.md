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
GET /daily_tracker_state — Retrieves the current day's macros, daily goals, and meal log.

POST /process_input — Accepts a JSON payload ({"text": "..."}) with natural language input, updates the daily state, and returns the recalculated totals.

GET /health — Service health check endpoint.