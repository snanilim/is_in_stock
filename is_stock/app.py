from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List
import shutil
from typing import Optional
from pathlib import Path
import time, os, base64
import json
import uvicorn
from grab_site import grab_site_info
from fastapi.responses import StreamingResponse





app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    result = grab_site_info()
    print("result", result["image_url"])
    print(type(result))
    return templates.TemplateResponse("index.html", {"request": request, "data": result})


@app.get("/update-url")
async def upload_file(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})



@app.get("/update-time")
async def update_time(request: Request):
    return templates.TemplateResponse("update_time.html", {"request": request})


class CaptureItem(BaseModel):
    upload_link: str


@app.post("/uploadfiles/")
async def save_capture_image(request: Request, upload_link: str = Form(...)):
    print("request", upload_link)
    f = open("site_url.txt", "w")
    f.write(upload_link)
    f.close()
    return templates.TemplateResponse("success.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)