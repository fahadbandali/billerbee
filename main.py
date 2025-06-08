from fastapi import FastAPI

app = FastAPI(title="Billerbee API", description="A simple FastAPI application", version="1.0.0")

@app.get("/")
async def read_root():
    return {"message": "Hello World", "project": "Billerbee"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q} 