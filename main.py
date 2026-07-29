from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.core.logging_config import setup_logging
from app.api.routes.transcription import router as pronunciation_router
from app.services.exceptions import EmptyTextError, TextTooLongError, WordHasBlankSpacesError
from fastapi.middleware.cors import CORSMiddleware

def create_app() -> FastAPI:
    setup_logging()
    
    app = FastAPI(title="Phonetic Transcriber API",
                  description="API for transcribing English text into phonetic representations for Spanish speakers.")

    app.include_router(pronunciation_router)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app

app = create_app()

# Global Exception handlers
@app.exception_handler(EmptyTextError)
async def empty_text_exception_handler(request, exc: EmptyTextError):
    return JSONResponse(
        status_code=400,
        content={"error": "empty_text", "message": str(exc)}
    )

@app.exception_handler(TextTooLongError)
async def text_too_long_exception_handler(request, exc: TextTooLongError):
    return JSONResponse(
        status_code=400,
        content={"error": "text_too_long", "message": str(exc)}
    )

@app.exception_handler(WordHasBlankSpacesError)
async def word_has_blank_spaces_exception_handler(request, exc: WordHasBlankSpacesError):
    return JSONResponse(
        status_code=400,
        content={"error": "word_has_blank_spaces", "message": str(exc)}
    )
