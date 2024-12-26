import math

import numpy as np
import pandas as pd
import sqlite3


def insert_db_recommendation(cursor: sqlite3.Cursor, base_url, similar_url, similarity) -> int:
    sql = ("INSERT INTO similar_creatures (base_id, similar_id, similarity) VALUES "
           "((SELECT id FROM creatures WHERE url = ?), "
           "(SELECT id FROM creatures WHERE url = ?), "
           "?);")

    cursor.execute(sql, [base_url, similar_url, similarity])
    res = cursor.fetchall()

# 1. Чтение датафрейма из файла
df = pd.read_csv("output/bestiary_recomendations.csv", )

# 3. Добавление в бд
with sqlite3.connect('../database/database.db') as connection:
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    for id_, row in df.iterrows():
        target_url = row["url"]

        score_1 = row["score_1"]
        score_1_url = row["score_1_url"]
        score_2 = row["score_2"]
        score_2_url = row["score_2_url"]
        score_3 = row["score_3"]
        score_3_url = row["score_3_url"]

        # Добавление рекомендации в бд
        for score, score_url in [(score_1, score_1_url),(score_2, score_2_url),(score_3, score_3_url),]:
            score = np.clip(score, 0, 1)
            insert_db_recommendation(cursor, base_url=target_url, similar_url=score_url, similarity=score)
