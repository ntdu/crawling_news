from typing import Union

from fastapi import FastAPI, Query, Request
from crawler import crawler_tradingview, crawler_investing
from pydantic import BaseModel
import os

from fastapi.responses import FileResponse

app = FastAPI()
MEDIA_ROOT = 'media'


class Info(BaseModel):
    url : str


@app.post("/get_data_tradingview/")
def get_data_tradingview(request: Request, info: Info, type: str = Query("text", enum=["text", "html"])):
    for f in os.listdir(MEDIA_ROOT):
        os.remove(os.path.join(MEDIA_ROOT, f))

    url = info.dict()['url']

    result = crawler_tradingview(url, type) if url.split('/')[2].split('.')[1] == 'tradingview' else crawler_investing(url, type)
    result['download_link'] = str(request.base_url) + 'get_file'

    return result


@app.get("/get_file", response_class=FileResponse)
def get_file():
    for f in os.listdir(MEDIA_ROOT):
        return FileResponse(MEDIA_ROOT + '/' + f, media_type='application/octet-stream', filename=f)


@app.get("/")
def main():
    return 'CRAWLING NEWS'


# if __name__ == "__main__":
#     uvicorn.run(app, host=config.get("APP_HOST"), port=int(config.get("APP_PORT")))