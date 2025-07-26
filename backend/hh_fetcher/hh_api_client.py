from typing import List, Dict

def mock_search_vacancies(filter_data: dict) -> List[Dict]:

    return [
        {
            "id": 1,
            "link": "https://hh.ru/vacancy/1",
            "salary": "100 000-150 000 руб.",
            "company": "ООО Рога и Копыта",
            "position": "Python разработчик"
        },
        {
            "id": 2,
            "link": "https://hh.ru/vacancy/2",
            "salary": "120 000 руб.",
            "company": "ЗАО Позитив",
            "position": "Backend engineer"
        },
        {
            "id": 3,
            "link": "https://hh.ru/vacancy/3",
            "salary": "от 90 000 руб.",
            "company": "TechStars",
            "position": "Junior Python"
        }
    ]

def mock_apply_to_vacancy(vacancy_id: int, resume_id: int) -> bool:

    return True 