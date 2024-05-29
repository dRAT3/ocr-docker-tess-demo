import uvicorn
from src.app.main import app
import logging

if __name__ == "__main__":
    logging.getLogger(__name__).info("Application started")
    uvicorn.run(app, host="0.0.0.0", port=8000)
