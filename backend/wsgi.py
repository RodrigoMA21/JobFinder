import asyncio
import os
from io import BytesIO

os.environ.setdefault("APP_ENV", "production")
os.environ.setdefault("APP_DEBUG", "false")
os.environ.setdefault("PYTHONANYWHERE", "1")

from sqlalchemy import create_engine

from app.core.config import settings
from app.models.base import Base

_sync_engine = create_engine(settings.DATABASE_URL_SYNC, echo=False)
Base.metadata.create_all(_sync_engine)
_sync_engine.dispose()

from app.main import app


def _build_scope(environ):
    headers = []
    for k, v in environ.items():
        if k.startswith("HTTP_"):
            header_name = k[5:].replace("_", "-").lower()
            headers.append((header_name.encode(), v.encode()))
        elif k in ("CONTENT_TYPE", "CONTENT_LENGTH"):
            if v:
                header_name = k.replace("_", "-").lower()
                headers.append((header_name.encode(), v.encode()))

    scope = {
        "type": "http",
        "asgi": {"version": "3.0", "spec_version": "2.1"},
        "method": environ.get("REQUEST_METHOD", "GET"),
        "path": environ.get("PATH_INFO", "/"),
        "raw_path": environ.get("PATH_INFO", "/").encode(),
        "query_string": environ.get("QUERY_STRING", "").encode(),
        "headers": headers,
        "client": None,
        "server": None,
        "scheme": "https",
    }
    return scope


class _BodyReader:
    def __init__(self, body: bytes):
        self._body = body
        self._has_both = False

    async def __call__(self):
        if not self._has_both:
            self._has_both = True
            return {"type": "http.request", "body": self._body, "more_body": False}
        while True:
            await asyncio.sleep(3600)


def _create_wsgi_app(asgi_app):
    def wsgi_app(environ, start_response):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            scope = _build_scope(environ)
            body = environ.get("wsgi.input", BytesIO()).read()
            receive = _BodyReader(body)
            send_queue = []

            async def _send(event):
                send_queue.append(event)

            loop.run_until_complete(asgi_app(scope, receive, _send))

            status = 500
            headers = []
            body = b""
            for event in send_queue:
                if event["type"] == "http.response.start":
                    status = event["status"]
                    headers = [
                        (k.decode(), v.decode()) if isinstance(k, bytes) else (k, v)
                        for k, v in event.get("headers", [])
                    ]
                elif event["type"] == "http.response.body":
                    body = event.get("body", b"")

            start_response(f"{status} {_status_text(status)}", headers)
            return [body]
        finally:
            loop.close()

    return wsgi_app


def _status_text(code: int) -> str:
    STATUS = {
        200: "OK", 201: "Created", 204: "No Content",
        301: "Moved Permanently", 302: "Found", 304: "Not Modified",
        400: "Bad Request", 401: "Unauthorized", 403: "Forbidden",
        404: "Not Found", 405: "Method Not Allowed", 409: "Conflict",
        422: "Unprocessable Entity", 429: "Too Many Requests",
        500: "Internal Server Error", 502: "Bad Gateway",
        503: "Service Unavailable",
    }
    return STATUS.get(code, "Unknown")


application = _create_wsgi_app(app)
