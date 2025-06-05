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
import socket

logger = logging.getLogger(__name__)


def start_server():
    app = FastAPI()

    FastAPIInstrumentor.instrument_app(app)
    RedisInstrumentor().instrument()
    PymongoInstrumentor().instrument()
    RequestsInstrumentor().instrument()
    AioHttpClientInstrumentor().instrument()
    from repository.metrics import MetricsMiddleware

    app.add_middleware(MetricsMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(short_url.router)

    @app.get("/")
    async def read_item():
        logger.info(socket.gethostname())
        return {"home_page": f"hello {socket.gethostname()}"}

    @app.get("/healthz")
    async def healthz():
        logger.info(f"health check done, {socket.gethostname()}")
        return {"ping": f"health check done {socket.gethostname()}"}

    @app.get("/metrics")
    async def metrics():
        logger.info("metrics endpoint called")

    @app.get("/{short_url_hash}", response_model=RedirectModel)
    async def redirect_to_long_url(short_url_hash: str):
        handler = Handler(short_url_hash)
        url = handler.handle()
        logger.info(f"URL to be redirected to: {url} from hash: {short_url_hash}")
        return RedirectResponse(url=url, status_code=302)

    return app
