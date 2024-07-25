from fastapi import FastAPI
from .routes import routers
from dotenv import load_dotenv

app = FastAPI(
    title="Recommendation System API",
    description="An Insider Test Case API to serve personalized recommendations and handle user interactions.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# load_dotenv(f'env/.env.dev')

for router in routers:
    app.include_router(router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=5000)
