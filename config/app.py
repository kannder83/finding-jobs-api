from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .conf import settings


# Routes
from app.routes import router as router_jobs


def get_application():

    conf = {
        "title": "DEV: Finding Jobs",
        "description": "DEV: Finding a great job!",
        "version": settings.version,
        "root_path": "/"
    }

    if settings.debug == False:
        conf = {
            "title": "Finding Jobs",
            "description": "Finding a great job!",
            "version": settings.version,
            "root_path": settings.prod_url
        }

    app: FastAPI = FastAPI(
        title=conf["title"],
        description=conf["description"],
        docs_url="/",
        version=conf["version"],
        root_path=conf["root_path"]
    )

    origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(router_jobs)

    return app


application = get_application()
