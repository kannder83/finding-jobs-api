# finding jobs API

Finding Work API - Technical Proof

## Programs

- Python3

- Docker

## Enviroment File

```bash
cp env.template .env
```

## Build Docker

```bash
docker-compose -f Developer.yml build
```

## ==============================================

## Proceso:

1. Crear el CRUD para usuarios
2. Para los skill se realiza una consulta a otra tabla donde esta el id con los nuevos valores, una relación.

## Additional info:

```py
# Function for creating database and tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
```
