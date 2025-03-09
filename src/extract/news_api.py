import requests
import pandas as pd

from datetime import datetime
from pandas import json_normalize

from src.env_container import env_container

class NewsApi:
    """
    API для полученя новостных статей
    Можно было использовать NewsApiClient с библиотеки newsapi, но можно и обычными requests

    Returns:
        _type_: _description_
    """
    _new_api_url = "https://newsapi.org/v2/everything"

    def __init__(self) -> None:
        pass

    def get_articles(
        self,
        keyword: str,
        date_from: str,
        date_to: str,
    ): 
        """
        Функция получения статей с NewsApi

        Args:
            keyword (str): ключевое слово или фраза, статьи по которым необходимо найти
            date_from (str): фильтрация статей по дате
            date_to (str): фильтрация статей по дате

        Returns:
            _type_: _description_
        """
        data_df = None
        page = 1
        while True:
            print("Page: ", page)
            url = self.__get_url(keyword, date_from, date_to, page)

            print(f"Обращаемся по адресу {url}")
            response = requests.get(url)
            if response.status_code != 200:
                print(f"Получили {response.status_code}")
                return data_df
            
            data = response.json()
            # print(f"Всего {data["totalResults"]} новостных статей по данному запросу")

            data_df = pd.concat([data_df, json_normalize(data["articles"])], ignore_index=True)
            page += 1
        

    def __get_url(
        self, 
        keyword: str,
        date_from: str,
        date_to: str,
        page: int=1,
    ) -> str:
        """
        Создание URL

        Создание URL к статьям для запроса keyword с date_from до date_to
        date - дата (без времени) в iso формате

        Args:
            keyword (str): ключевое слово или фраза, статьи по которым необходимо найти
            date_from (str): фильтрация статей по дате
            date_to (str): фильтрация статей по дате
            page (int): страница

        Returns:
            url (str): url для получения необходимых статей
        """
        url = f"{self._new_api_url}?q={keyword}&from={date_from}&to={date_to}&page={page}"
        url = f"{url}&apiKey={env_container.key_api}"

        return url
