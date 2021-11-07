<h1 align="center">
    <strong>asgi-logger</strong>
</h1>
<p align="center">
    <a href="https://github.com/Kludex/asgi-logger" target="_blank">
        <img src="https://img.shields.io/github/last-commit/Kludex/asgi-logger" alt="Latest Commit">
    </a>
        <img src="https://img.shields.io/github/workflow/status/Kludex/asgi-logger/Test">
        <img src="https://img.shields.io/codecov/c/github/Kludex/asgi-logger">
    <br />
    <a href="https://pypi.org/project/asgi-logger" target="_blank">
        <img src="https://img.shields.io/pypi/v/asgi-logger" alt="Package version">
    </a>
    <img src="https://img.shields.io/pypi/pyversions/asgi-logger">
    <img src="https://img.shields.io/github/license/Kludex/asgi-logger">
</p>

This project was created as an alternative for the current uvicorn logger. But it can also be used with any other ASGI server.


## Installation

``` bash
pip install asgi-logger
```

## Usage

If you're using it with uvicorn, remember that you need to erase the handlers from uvicorn's logger that is writing the access logs.
To do that, just:

```python
logging.getLogger("uvicorn.access").handlers = []
```

Below you can see an example with FastAPI, but you can use it with any other ASGI application:

```python
from fastapi import FastAPI
from asgi_logger import AccessLoggerMiddleware

app = FastAPI(middleware=[Middleware(AccessLoggerMiddleware)])

@app.get("/")
async def home():
    return "Hello world!"
```

In case you want to add a custom format to the access logs, you can do it using the `format` parameter on the `AccessLoggerMiddleware`:

```python
AccessLoggerMiddleware(app, format="%(s)s")
```

For now you can verify the possible format values [here](https://github.com/Kludex/asgi-logger/blob/main/asgi_logger/middleware.py).
The documentation will be available soon.

## License

This project is licensed under the terms of the MIT license.
