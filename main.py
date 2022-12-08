import uvicorn
from subprocess import run
from config.conf import settings


def main():
    """
    Main: It runs a fastapi server
    """
    if settings.debug == True:
        uvicorn.run(
            "config.app:application",
            host="0.0.0.0",
            port=8000,
            reload=True,
        )
    else:
        run("gunicorn config.app:application -w 1 -b 0.0.0.0:8000 --worker-class uvicorn.workers.UvicornWorker".split(' '))


if __name__ == "__main__":
    main()
