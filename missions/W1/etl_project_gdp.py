import pandas as pd
import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup
from country_converter import CountryConverter
from typing import List, Dict, Union
import logging
import os
import sqlite3

"""
Variable
-----
url : string
    ETL 과정을 수행할 url 주소

keys : list
    데이터에 존재하는 Column 리스트

default_store_path : string
    Load 시 json 파일이 저장될 경로

default_log_path : string
    log가 저장될 경로
"""
url = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29"
keys = ['Country/Territory', 'IMFForecast', 'IMFYear', 'WorldBankEstimate', 'WorldBankYear',
        'UnitedNationsEstimate', 'UniteNationsYear']
default_store_path = '/Users/admin/Desktop/Softeer_DE/data/Countries_by_GDP.json'
default_log_path = '/Users/admin/Desktop/Softeer_DE/log/etl_project_log.txt'

def extract_data(
    url:str
) -> List[Dict[str, str]]:
    """
    url(GDP Page)에 존재하는 테이블의 데이터를 추출하는 함수입니다.

    Parameter
    -----
    url : string
        추출하고자 하는 페이지의 url

    Return
    -----
    List[Dict[str, str]]
        딕셔너리 리스트 형태의 데이터를 반환
    """
    try:
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('table', {"class": 'wikitable'})
        tbody = table.find('tbody')
        rows = tbody.find_all('tr')

        data = []
        for row in rows:
            data_row = []
            cols = row.find_all("td")
            for col in cols:
                text = col.text.strip()
                if text == '—':
                    data_row.append(None)
                    data_row.append(None)
                else:
                    data_row.append(text)

            data_row_dict = dict(zip(keys, data_row))
            data.append(data_row_dict)

        return data[2:]
    except Exception as e:
        raise Exception(f"Extract failed: {e}")

def transform_data(
    data:List[Dict[str, str]]
) -> List[Dict[str, Union[str, int, float]]]:
    """
    data를 입력 받아 분석을 위해 전처리하는 함수입니다.

    Parameter
    -----
    data : List[Dict[str, str]]
        전처리 과정을 수행할 딕셔너리 리스트

    Return
    -----
    List[Dict[str, Union[str, int, float]]]
        value가 type에 맞게 변환된 딕셔너리 리스트 반환
    """
    try:
        data = pd.DataFrame(data[1:])
        print(data.head())
        data = data[['Country/Territory', 'IMFForecast', 'IMFYear']]
        for k in ['IMFForecast', 'IMFYear']:
            data[k] = data[k].apply(
                lambda x: x[x.index(']') + 1:] if isinstance(x, str) and ']' in x else x
            )
            if data[k].dtypes == 'object':
                data[k] = data[k].apply(
                    lambda x: int(x.replace(',', '')) if x is not None else x
                )
                data[k] = data[k].astype('Int64')
                if k == 'IMFForecast':
                    data[k] = round(data[k] / 1000 - 0.005, 2)
    
        cc = CountryConverter()
        data['region'] = cc.pandas_convert(series=data['Country/Territory'], to='continent')
    
        return data
    except Exception as e:
        raise Exception(f"Transform failed: {e}")

def load_data(
    data: Dict[str, Union[str, int, float]],
    file_name: str = default_store_path
) -> None:
    """
    data를 json 형태로 저장하는 함수입니다.

    Parameter
    -----
    data : List[Dict[str, Union[str, int, float]]]
        json 형태로 저장할 딕셔너리 리스트

    Return
    -----
    None
        json 형태로 저장 과정만 수행
    """
    data.to_json(file_name, orient='records')

def print_country_over_100B(
    data: Dict[str, Union[str, int, float]]
) -> None:
    """
    data의 IMFForecast 컬럼의 값이 100이 넘는 나라를 내림차순으로 정렬해 출력합니다.

    Parameter
    -----
    data : List[Dict[str, Union[str, int, float]]]
        전처리가 완료된 딕셔너리 리스트

    Return
    -----
    None
    """
    over_100B = data[data['IMFForecast'] >= 100].sort_values('IMFForecast', ascending=False)
    print('Country for Higher Than 100B of GCP')
    print(over_100B['Country/Territory'])

def print_mean_of_top5(
    data: Dict[str, Union[str, int, float]]
) -> None:
    """
    data의 region 기준으로 상위 5개 나라의 평균을 내림차순으로 정렬해 출력합니다.

    Parameter
    -----
    data : List[Dict[str, Union[str, int, float]]]
        전처리가 완료된 딕셔너리 리스트

    Return
    -----
    None
    """
    region = data['region'].unique()
    for r in region:
        if r == 'not found':
            continue
        
        GDP_top_5_for_region = data[data['region'] == r].sort_values('IMFForecast', ascending=False)[:5]
        GDP_top_5_for_region = GDP_top_5_for_region['IMFForecast']
        print(f'region : {r}')
        print(f'GDP Mean (Top 5) : {round(GDP_top_5_for_region.mean(), 2)}')
        print()

"""
Log Format
-----
Year-Monthname-Day-Hour-Minute-Second, {message}
ex) 2025-07-09-15-06-30, Transform 완료
"""
logging.basicConfig(filename=default_log_path, level=logging.INFO,
                    format="%(asctime)s, %(message)s", 
                    datefmt="%Y-%m-%d-%H-%M-%S", force=True)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    logger.info('Extract 시작')
    data = extract_data(url)
    logger.info('Extract 완료')

    logger.info('Transform 시작')
    data = transform_data(data)
    logger.info('Transform 완료')

    logger.info('Load 시작')
    load_data(data)
    logger.info('Load 완료')

    print_country_over_100B(data)
    print_mean_of_top5(data)