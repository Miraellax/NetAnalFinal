import random
import time
from datetime import datetime
import requests

import numpy as np
import pandas as pd
from requests import RequestException

from Scraper.InfoCard import InfoCard
from Scraper.scraper import scrape_bestiary_table, scrape_beast_info

base_url = "https://dnd.su"
bestiary_url = "/bestiary/"

# # 1. Сохранение адресов к карточкам бестиария в текстовый файл
# pages = scrape_bestiary_table(url=base_url+bestiary_url, base_url=base_url)
# with open("output/card_urls.txt", "w") as file:
#     for url in pages:
#         file.write(url+"\n")

# # 2. Чтение адресов к карточкам бестиария из файла
# with open("output/card_urls.txt", "r") as file:
#     lines = file.readlines()
#     pages = [line.strip() for line in lines]


# 3. Создание и заполнение датафрейма
# info_card_columns = list(InfoCard(None).__dict__.keys())
# df = pd.DataFrame(0, index=np.arange(len(pages)), columns=info_card_columns, dtype="object")

# # 4. Чтение датафрейма из файла
# df = pd.read_csv("output/bestiary.csv")
# print(df.info())

# 5. Парсим сайт
# 709 - https://dnd.su/bestiary/8401-reaper-spirit/ с бонусом мастерства Бонус мастерства равен вашему бонусу
# 1074 - https://dnd.su/bestiary/8436-clapperclaw-the-scarecrow/
# 1087 - https://dnd.su/bestiary/13671-forlarren/
# 1121 - https://dnd.su/bestiary/5853-yestabrod/
# 1280 - https://dnd.su/bestiary/3329-captain-othelstan/
# 1769 - https://dnd.su/bestiary/8150-niv-mizzet/
# 1836 - https://dnd.su/bestiary/17352-ogre-chitterlord/
# 2465 - https://dnd.su/bestiary/4538-abyssal-wretch/
# 2511 - https://dnd.su/bestiary/17420-tecuziztecatl/

# 2569 - https://dnd.su/bestiary/3989-dancing-item/ скипнули

# 2607 - https://dnd.su/bestiary/17368-enhanced-sphinx/
# 2674 - https://dnd.su/bestiary/4916-hellenrae/
# 2693 - https://dnd.su/bestiary/5184-walking-statue-of-waterdeep/
# 2810 - https://dnd.su/bestiary/4698-escher/

# i = 2810
# pages = pages[i:]
# with requests.session() as session:
#
#     for url in pages:
#         print(url)
#         while True:
#             try:
#                 card = scrape_beast_info(url, session)
#                 break
#             except requests.exceptions.ConnectTimeout:
#                 time.sleep(random.uniform(0.5, 1))
#
#         # break
#
#         df.loc[i, card.__dict__.keys()] = list(card.__dict__.values())
#         i += 1
#         time.sleep(random.uniform(0.5, 1))
#
#         df.to_csv('output/bestiary.csv', index=False)
