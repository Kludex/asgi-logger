from __future__ import annotations

import shlex
from typing import Any

import httpx
import pytest
from asgiref.typing import ASGIReceiveCallable as Receive
from asgiref.typing import ASGISendCallable as Send
from asgiref.typing import Scope

from uvicorn_logger import AccessLoggerMiddleware


class Match:
    def __eq__(self, other: Any) -> bool:
        return True


async def success_app(scope: Scope, receive: Receive, send: Send) -> None:
    await receive()
    await send({"type": "http.response.start", "status": 200, "headers": []})
    await send({"type": "http.response.body", "body": b"", "more_body": False})


async def failure_app(scope: Scope, receive: Receive, send: Send) -> None:
    raise RuntimeError()


@pytest.mark.anyio
async def test_default_format_200_response(caplog: pytest.LogCaptureFixture) -> None:
    app = AccessLoggerMiddleware(success_app)
    async with httpx.AsyncClient(app=app, base_url="http://testserver") as client:
        res = await client.get("/")
    assert res.status_code == 200
    messages = [record.msg % record.args for record in caplog.records]
    assert len(messages) == 1
    assert shlex.split(messages[0]) == [Match(), "-", "GET / HTTP/1.1", "200", "OK"]


@pytest.mark.anyio
async def test_default_format_500_response(caplog: pytest.LogCaptureFixture) -> None:
    app = AccessLoggerMiddleware(failure_app)
    async with httpx.AsyncClient(app=app, base_url="http://testserver") as client:
        with pytest.raises(RuntimeError):
            await client.get("/")
    messages = [record.msg % record.args for record in caplog.records]
    assert len(messages) == 1
    assert shlex.split(messages[0]) == [
        Match(),
        "-",
        "GET / HTTP/1.1",
        "500",
        "Internal",
        "Server",
        "Error",
    ]
