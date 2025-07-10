import sqlite3
import json
import pandas as pd

db_path = '/Users/admin/Desktop/Softeer_DE/data/World_Economies.db'
data_path = '/Users/admin/Desktop/Softeer_DE/data/Countries_by_GDP.json'

def execute_select_query(query):
    sql_command = query
    cursor.execute(sql_command)
    res = cursor.fetchall()
    print('command :',sql_command)
    for i in res:
        print(i)

if __name__ == "__main__":
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    data = pd.read_json(data_path)
    data = data.rename(columns={'IMFForecast':'GDP_USD_billion', 'Country/Territory': 'Country'})
    data['IMFYear'] = data['IMFYear'].astype('Int64')
    data.to_sql("Countries_by_GDP", connection, if_exists="replace", index=False)

    # GDP가 100B USD 이상인 국가 출력
    sql_command = "SELECT Country FROM Countries_by_GDP WHERE GDP_USD_billion >= 100;"
    execute_select_query(sql_command)

    # Region별 top5 국가의 GDP 평균 출력
    sql_command = """
    WITH base AS
    (
        SELECT Region, ROW_NUMBER() OVER(PARTITION BY Region ORDER BY GDP_USD_billion DESC) AS rn, GDP_USD_billion
        FROM Countries_by_GDP WHERE Region != "not found"
    )
    SELECT Region, ROUND(AVG(GDP_USD_billion), 2) AS GCP_average FROM base WHERE rn <= 5
    GROUP BY Region
    ORDER BY GCP_average DESC;
    """
    execute_select_query(sql_command)