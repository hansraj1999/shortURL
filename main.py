import logging.config

from fastapi import FastAPI
from routers import short_url
from fastapi.middleware.cors import CORSMiddleware
from opentelemetry.instrumentation.redis import RedisInstrumentor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.pymongo import PymongoInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.aiohttp_client import AioHttpClientInstrumentor
from fastapi.responses import RedirectResponse
from repository.redirect_to_long_url import Handler
from schemas import RedirectModel
import logging

logger = logging.getLogger(__name__)


def start_server():
    app = FastAPI()

    FastAPIInstrumentor.instrument_app(app)
    RedisInstrumentor().instrument()
    PymongoInstrumentor().instrument()
    RequestsInstrumentor().instrument()
    AioHttpClientInstrumentor().instrument()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(short_url.router)

    @app.get("/")
    async def read_item():
        return {"home_page": "hello"}

    @app.get("/{short_url_hash}", response_model=RedirectModel)
    async def redirect_to_long_url(short_url_hash: str):
        handler = Handler(short_url_hash)
        url = handler.handle()
        logger.info(f"URL to be redirected to: {url} from hash: {short_url_hash}")
        return RedirectResponse(url=url, status_code=302)
    return app
