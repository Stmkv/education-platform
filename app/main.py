from fastapi import FastAPI

from app.infrastructure.config import get_settings

from app.presentation.api.handlers import register_exception_handlers


def create_app() -> FastAPI:
    settings = get_settings()
    print(settings)
    app = FastAPI(
        title=settings.app.title,
        debug=settings.app.debug,
    )
    register_exception_handlers(app)
    return app


app = create_app()
