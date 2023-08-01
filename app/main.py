import os.path as op
from datetime import datetime

import uvicorn
from typing import Optional
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import app.es as es

tem_dir = op.join(op.dirname(op.abspath(__file__)), "templates")

app = FastAPI()
templates = Jinja2Templates(directory=tem_dir)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """
    home
    :return:
    """
    return templates.TemplateResponse("page.html", {"request": request})


@app.post("/input")
def user_event(
    request: Request,
    uid: Optional[str] = Form(None),
    stdatetime: datetime = Form(...),
    eddatetime: datetime = Form(...),
):
    """
    user event search
    :param request:
    :param uid:
    :param stdatetime:
    :param eddatetime:
    :return:
    """
    if uid is None:
        result, docs_count, index_list,print_count = es.get_recent_data( stdatetime, eddatetime)
        uid = ""
        if print_count > docs_count :
            print_count = docs_count
    else:    
        result, docs_count, index_list,print_count = es.get_user_data(uid, stdatetime, eddatetime)
        if print_count > docs_count:
            print_count = docs_count
    
    return templates.TemplateResponse(
        "page.html",
        {
            "request": request,
            "docs": result,
            "uid": uid,
            "stdatetime": stdatetime,
            "eddatetime": eddatetime,
            "docs_count": docs_count,
            "index_list": index_list,
            "print_count":print_count,
        },
    )


@app.get("/indexes", response_class=HTMLResponse)
def get_indexes(request: Request):
    """
    All indexes list
    :param request:
    :return:
    """
    indexes = es.get_indexes()

    return templates.TemplateResponse(
        "index_list.html", {"request": request, "indexes": indexes}
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8088, reload=True)
