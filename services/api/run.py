import uvicorn
from src.app.main import app
import logging

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
