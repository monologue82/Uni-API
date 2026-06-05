import uvicorn


if __name__ == "__main__":
    try:
        import uvloop
        uvloop.install()
        loop = "uvloop"
        http = "httptools"
    except ImportError:
        loop = "auto"
        http = "auto"

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        workers=4,
        loop=loop,
        http=http,
        log_level="info",
    )
