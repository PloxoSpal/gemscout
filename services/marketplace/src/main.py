from fastapi import FastAPI
import uvicorn

from src.api.dictionaries import router as dictionaries_router
app = FastAPI()

app.include_router(dictionaries_router)

if __name__ == '__main__':
    uvicorn.run("src.main:app", host="0.0.0.0", port=8001, reload=True)
