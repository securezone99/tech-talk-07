import logging, uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv
from controllers import completeness_news_controller

load_dotenv()
logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s', handlers=[logging.StreamHandler()])
app = FastAPI(docs_url="/docs")

app.include_router(completeness_news_controller.router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
