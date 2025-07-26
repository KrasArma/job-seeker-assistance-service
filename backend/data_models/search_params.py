# from dataclasses import dataclass, field
# from typing import Any, Dict, Callable, Optional
# from enum import Enum
# from datetime import datetime
# import uuid
# from custom_logger import logger

# EXPERIENCE_CATEGORIES = ["noExperience", "between1And3", "between3And6", "moreThan6"]
# EMPLOYMENT_CATEGORIES = ["full", "part", "project", "volunteer", "probation"]
# SCHEDULE_CATEGORIES = ["fullDay", "shift", "flexible", "remote", "flyInFlyOut"]
# EDUCATION_CATEGORIES = ["not_required_or_not_specified", "special_secondary", "higher"]
# HOST_CATEGORIES = ["hh.ru", "rabota.by", "hh1.az", "hh.uz", "hh.kz", "headhunter.ge", "headhunter.kg"]

# class SearchParam(str, Enum):
#     PAGE = "page"
#     PER_PAGE = "per_page"
#     TEXT = "text"
#     SEARCH_FIELD = "search_field"
#     EXPERIENCE = "experience"
#     EMPLOYMENT = "employment"
#     SCHEDULE = "schedule"
#     AREA = "area"
#     METRO = "metro"
#     PROFESSIONAL_ROLE = "professional_role"
#     INDUSTRY = "industry"
#     EMPLOYER_ID = "employer_id"
#     CURRENCY = "currency"
#     SALARY = "salary"
#     LABEL = "label"
#     ONLY_WITH_SALARY = "only_with_salary"
#     PERIOD = "period"
#     DATE_FROM = "date_from"
#     DATE_TO = "date_to"
#     TOP_LAT = "top_lat"
#     BOTTOM_LAT = "bottom_lat"
#     LEFT_LNG = "left_lng"
#     RIGHT_LNG = "right_lng"
#     ORDER_BY = "order_by"
#     SORT_POINT_LAT = "sort_point_lat"
#     SORT_POINT_LNG = "sort_point_lng"
#     CLUSTERS = "clusters"
#     DESCRIBE_ARGUMENTS = "describe_arguments"
#     NO_MAGIC = "no_magic"
#     PREMIUM = "premium"
#     RESPONSES_COUNT_ENABLED = "responses_count_enabled"
#     PART_TIME = "part_time"
#     ACCEPT_TEMPORARY = "accept_temporary"
#     EMPLOYMENT_FORM = "employment_form"
#     WORK_SCHEDULE_BY_DAYS = "work_schedule_by_days"
#     WORKING_HOURS = "working_hours"
#     WORK_FORMAT = "work_format"
#     EXCLUDED_TEXT = "excluded_text"
#     EDUCATION = "education"
#     LOCALE = "locale"
#     HOST = "host"
#     QUERY = "query"
#     SUBMODE = "submode"
#     VACANCY = "vacancy"
#     RESUME = "resume"
#     WISHES = "wishes"
#     CATEGORY = "category"

# ValidationSearchCard = {
#     SearchParam.PAGE: {
#         "type_cast": lambda v: int(v) if v not in (None, '') else 0,
#         "validator": lambda v: None if (isinstance(v, int) and v >= 0) else "Номер страницы должен быть целым числом не меньше 0",
#     },
#     SearchParam.PER_PAGE: {
#         "type_cast": lambda v: int(v) if v not in (None, '') else 10,
#         "validator": lambda v: None if (isinstance(v, int) and 1 <= v <= 100) else "Количество элементов per_page должно быть от 1 до 100",
#     },
#     SearchParam.TEXT: {
#         "type_cast": lambda v: str(v) if v is not None else None,
#         "validator": lambda v: None,
#     },
#     SearchParam.SEARCH_FIELD: {
#         "type_cast": lambda v: str(v) if v is not None else None,
#         "validator": lambda v: None,
#     },
#     SearchParam.EXPERIENCE: {
#         "type_cast": lambda v: v,
#         "validator": lambda v: None if (v is None or v in EXPERIENCE_CATEGORIES) else "Опыт работы должен быть id из справочника experience (/dictionaries)",
#     },
#     SearchParam.EMPLOYMENT: {
#         "type_cast": lambda v: v,
#         "validator": lambda v: None if (v is None or v in EMPLOYMENT_CATEGORIES) else "Тип занятости должен быть id из справочника employment (/dictionaries)",
#     },
#     SearchParam.SCHEDULE: {
#         "type_cast": lambda v: v,
#         "validator": lambda v: None if (v is None or v in SCHEDULE_CATEGORIES) else "График работы должен быть id из справочника schedule (/dictionaries)",
#     },
#     SearchParam.AREA: {
#         "type_cast": lambda v: str(v) if v is not None else None,
#         "validator": lambda v: None,
#     },
#     SearchParam.METRO: {
#         "type_cast": lambda v: v,
#         "validator": lambda v: None,
#     },
#     SearchParam.PROFESSIONAL_ROLE: {
#         "type_cast": lambda v: str(v) if v is not None else None,
#         "validator": lambda v: None,
#     },
#     SearchParam.INDUSTRY: {
#         "type_cast": lambda v: str(v) if v is not None else None,
#         "validator": lambda v: None,
#     },
#     SearchParam.EMPLOYER_ID: {
#         "type_cast": lambda v: str(v) if v is not None else None,
#         "validator": lambda v: None,
#     },
#     SearchParam.CURRENCY: {
#         "type_cast": lambda v: str(v) if v is not None else None,
#         "validator": lambda v: None,
#     },
#     SearchParam.SALARY: {
#         "type_cast": lambda v: int(v) if v not in (None, '') else None,
#         "validator": lambda v: None if (v is None or (isinstance(v, int) and v >= 0)) else "Размер заработной платы должен быть неотрицательным числом",
#     },
#     SearchParam.LABEL: {
#         "type_cast": lambda v: str(v) if v is not None else None,
#         "validator": lambda v: None,
#     },
#     SearchParam.ONLY_WITH_SALARY: {
#         "type_cast": lambda v: str(v).lower() in ["true", "1", "yes"] if v is not None else False,
#         "validator": lambda v: None,
#     },
#     SearchParam.PERIOD: {
#         "type_cast": lambda v: int(v) if v not in (None, '') else None,
#         "validator": lambda v: None if (v is None or (isinstance(v, int) and v > 0)) else "Период должен быть положительным числом (количество дней)",
#     },
#     SearchParam.DATE_FROM: {
#         "type_cast": lambda v: str(v) if v is not None else None,
#         "validator": lambda v: None,
#     },
#     SearchParam.DATE_TO: {
#         "type_cast": lambda v: str(v) if v is not None else None,
#         "validator": lambda v: None,
#     },
#     SearchParam.TOP_LAT: {
#         "type_cast": lambda v: float(v) if v not in (None, '') else None,
#         "validator": lambda v: None,
#     },
#     SearchParam.BOTTOM_LAT: {
#         "type_cast": lambda v: float(v) if v not in (None, '') else None,
#         "validator": lambda v: None,
#     },
#     SearchParam.LEFT_LNG: {
#         "type_cast": lambda v: float(v) if v not in (None, '') else None,
#         "validator": lambda v: None,
#     },
#     SearchParam.RIGHT_LNG: {
#         "type_cast": lambda v: float(v) if v not in (None, '') else None,
#         "validator": lambda v: None,
#     },
#     SearchParam.ORDER_BY: {
#         "type_cast": lambda v: str(v) if v is not None else None,
#         "validator": lambda v: None,
#     },
#     SearchParam.SORT_POINT_LAT: {
#         "type_cast": lambda v: float(v) if v not in (None, '') else None,
#         "validator": lambda v: None,
#     },
#     SearchParam.SORT_POINT_LNG: {
#         "type_cast": lambda v: float(v) if v not in (None, '') else None,
#         "validator": lambda v: None,
#     },
#     SearchParam.CLUSTERS: {
#         "type_cast": lambda v: str(v).lower() in ["true", "1", "yes"] if v is not None else False,
#         "validator": lambda v: None,
#     },
#     SearchParam.DESCRIBE_ARGUMENTS: {
#         "type_cast": lambda v: str(v).lower() in ["true", "1", "yes"] if v is not None else False,
#         "validator": lambda v: None,
#     },
#     SearchParam.NO_MAGIC: {
#         "type_cast": lambda v: str(v).lower() in ["true", "1", "yes"] if v is not None else False,
#         "validator": lambda v: None,
#     },
#     SearchParam.PREMIUM: {
#         "type_cast": lambda v: str(v).lower() in ["true", "1", "yes"] if v is not None else False,
#         "validator": lambda v: None,
#     },
#     SearchParam.RESPONSES_COUNT_ENABLED: {
#         "type_cast": lambda v: str(v).lower() in ["true", "1", "yes"] if v is not None else False,
#         "validator": lambda v: None,
#     },
#     SearchParam.PART_TIME: {
#         "type_cast": lambda v: str(v) if v is not None else None,
#         "validator": lambda v: None,
#     },
#     SearchParam.ACCEPT_TEMPORARY: {
#         "type_cast": lambda v: str(v).lower() in ["true", "1", "yes"] if v is not None else False,
#         "validator": lambda v: None,
#     },
#     SearchParam.EMPLOYMENT_FORM: {
#         "type_cast": lambda v: str(v) if v is not None else None,
#         "validator": lambda v: None,
#     },
#     SearchParam.WORK_SCHEDULE_BY_DAYS: {
#         "type_cast": lambda v: str(v) if v is not None else None,
#         "validator": lambda v: None,
#     },
#     SearchParam.WORKING_HOURS: {
#         "type_cast": lambda v: str(v) if v is not None else None,
#         "validator": lambda v: None,
#     },
#     SearchParam.WORK_FORMAT: {
#         "type_cast": lambda v: str(v) if v is not None else None,
#         "validator": lambda v: None,
#     },
#     SearchParam.EXCLUDED_TEXT: {
#         "type_cast": lambda v: str(v) if v is not None else None,
#         "validator": lambda v: None,
#     },
#     SearchParam.EDUCATION: {
#         "type_cast": lambda v: v,
#         "validator": lambda v: None if (v is None or v in EDUCATION_CATEGORIES) else "Образование должно быть одним из: not_required_or_not_specified, special_secondary, higher",
#     },
#     SearchParam.LOCALE: {
#         "type_cast": lambda v: str(v) if v is not None else "RU",
#         "validator": lambda v: None,
#     },
#     SearchParam.HOST: {
#         "type_cast": lambda v: v,
#         "validator": lambda v: None if (v is None or v in HOST_CATEGORIES) else "Домен сайта должен быть одним из: hh.ru, rabota.by, hh1.az, hh.uz, hh.kz, headhunter.ge, headhunter.kg",
#     }, 
# }

# def validationSearch(data: Dict[str, Any]) -> dict:
#     method = "validationSearch"
#     request_id = data.get('request_id')
#     logger.info(f"{method} called, request_id={request_id}, input={data}")
#     status = 'done'
#     reason = None
#     validation = 'ok'
#     errors = {}
#     name = data.get('name')
#     value = data.get('value')
#     try:
#         param = SearchParam(name)
#     except ValueError as e:
#         result = {
#             'status': 'done',
#             'request_id': request_id,
#             'validation': 'fail',
#             'reason': {name: 'Unknown parameter'}
#         }
#         logger.error("ValidationError", str(e), input_data=data, output_data=result, method=method, request_id=request_id)
#         return result
#     try:
#         logger.info(f"{method} param resolved: {param}, value={value}")
#         if param in ValidationSearchCard:
#             caster = ValidationSearchCard[param].get('type_cast', lambda x: x)
#             try:
#                 casted = caster(value)
#                 logger.info(f"{method} type_cast: original={value}, casted={casted}")
#             except Exception as e:
#                 casted = value
#                 logger.error("ValidationError", f"Type cast error: {e}", input_data=data, output_data=None, method=method, request_id=request_id)
#             validator = ValidationSearchCard[param].get('validator')
#             if validator:
#                 error = validator(casted)
#                 logger.info(f"{method} validator: value={casted}, error={error}")
#                 if error:
#                     errors[name] = error
#         if errors:
#             validation = 'fail'
#             reason = errors
#         else:
#             reason = None
#         result = {
#             'status': status,
#             'request_id': request_id,
#             'validation': validation,
#             'reason': reason,
#             'input': data,
#             'casted': casted if 'casted' in locals() else None
#         }
#         logger.info(f"{method} finished, request_id={request_id}, result={result}")
#         return result
#     except Exception as e:
#         logger.error("ValidationError", str(e), input_data=data, output_data=None, method=method, request_id=request_id)
#         return {
#             'status': 'done',
#             'request_id': request_id,
#             'validation': 'fail',
#             'reason': {name: 'Validation error'},
#             'input': data
#         }
