from fastapi import FastAPI, Request, Depends, Form, Body
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
import os
from backend.db_manager.models import Vacancy, Resume, Base
from backend.hh_fetcher.hh_api_client import mock_search_vacancies, mock_apply_to_vacancy
from backend.agents.deepseek_api import query_to_filter
from backend.db_manager.database import db
from backend.config.config_reader import config_reader
from backend.config.data_models import DeepseekConfig, DatabaseConfig
from typing import Optional
from backend.data_models.search_params import validationSearch
from backend.custom_logger import logger


app = FastAPI()
templates = Jinja2Templates(directory="templates")

def get_request_id(request: Request):
    return request.headers.get('X-Request-ID') or None

async def get_db():
    return await db.get_session()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    method = "read_root"
    request_id = get_request_id(request)
    logger.info(f"{method} called, request_id={request_id}")
    try:
        resumes = await db.get_all_resumes()
        logger.info(f"{method} finished, request_id={request_id}, resumes_count={len(resumes)}")
        return templates.TemplateResponse("index.html", {"request": request, "resumes": resumes})
    except Exception as e:
        logger.error("InternalError", str(e), method=method, request_id=request_id)
        return JSONResponse({"error": "Internal server error", "request_id": request_id}, status_code=500)

@app.get("/vacancies_search", response_class=HTMLResponse)
async def vacancies_search(request: Request):
    method = "vacancies_search"
    request_id = get_request_id(request)
    logger.info(f"{method} called, request_id={request_id}")
    try:
        logger.info(f"{method} finished, request_id={request_id}")
        return templates.TemplateResponse("vacancies_search.html", {"request": request})
    except Exception as e:
        logger.error("InternalError", str(e), method=method, request_id=request_id)
        return JSONResponse({"error": "Internal server error", "request_id": request_id}, status_code=500)

@app.post("/search", response_class=HTMLResponse)
async def search_vacancies(request: Request, query: str = Form(...)):
    method = "search_vacancies"
    request_id = get_request_id(request)
    logger.info(f"{method} called, request_id={request_id}, query={query}")
    try:
        filter_data = query_to_filter(query)
        vacancies = mock_search_vacancies(filter_data)
        resumes = await db.get_all_resumes()
        logger.info(f"{method} finished, request_id={request_id}, vacancies_count={len(vacancies)}")
        return templates.TemplateResponse("index.html", {"request": request, "vacancies": vacancies, "resumes": resumes})
    except Exception as e:
        logger.error("InternalError", str(e), input_data={"query": query}, method=method, request_id=request_id)
        return JSONResponse({"error": "Internal server error", "request_id": request_id}, status_code=500)

@app.post("/apply")
async def apply_to_vacancies(request: Request):
    method = "apply_to_vacancies"
    request_id = get_request_id(request)
    logger.info(f"{method} called, request_id={request_id}")
    try:
        form = await request.form()
        selected_vacancies = form.getlist("vacancy")
        resume_id = int(form.get("resume_id"))
        basket = form.get("basket")
        rate = form.get("rate")
        score_match = form.get("score_match")
        score_best = form.get("score_best")
        contact1 = form.get("contact1")
        contact2 = form.get("contact2")
        comment = form.get("comment")
        vacancies = [
            {"id": int(v_id)} for v_id in selected_vacancies
        ]
        await db.save_responded_vacancies(
            vacancies,
            resume_id=resume_id,
            basket=basket,
            rate=int(rate) if rate else None,
            score_match=float(score_match) if score_match else None,
            score_best=float(score_best) if score_best else None,
            contact1=contact1,
            contact2=contact2,
            comment=comment
        )
        logger.info(f"{method} finished, request_id={request_id}, applied_vacancies={selected_vacancies}")
        return RedirectResponse("/", status_code=303)
    except Exception as e:
        logger.error("InternalError", str(e), method=method, request_id=request_id)
        return JSONResponse({"error": "Internal server error", "request_id": request_id}, status_code=500)

@app.post("/create_resume")
async def create_resume(request: Request, name: str = Form(...)):
    method = "create_resume"
    request_id = get_request_id(request)
    logger.info(f"{method} called, request_id={request_id}, name={name}")
    try:
        await db.create_resume(name)
        logger.info(f"{method} finished, request_id={request_id}, name={name}")
        return RedirectResponse("/", status_code=303)
    except Exception as e:
        logger.error("InternalError", str(e), input_data={"name": name}, method=method, request_id=request_id)
        return JSONResponse({"error": "Internal server error", "request_id": request_id}, status_code=500)


@app.on_event("startup")
async def on_startup():
    method = "on_startup"
    logger.info(f"{method} called")
    try:
        await db.create_tables()
        logger.info(f"{method} finished")
    except Exception as e:
        logger.error("InternalError", str(e), method=method) 