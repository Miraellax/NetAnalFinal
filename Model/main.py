import numpy as np
import pandas as pd
import pymorphy3
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords

stopwords_ru = stopwords.words('russian')

# url,
# name,name_translated,name_uppercase,name_translated_uppercase,
# size,type_,alignment,is_named,
# armor_class,armor_class_type,
# average_hitpoints,hit_die_type,hit_dice,hitpoints_bonus,
# walking_speed,flying_speed,swimming_speed,digging_speed,climbing_speed,

# strength,dexterity,constitution,intelligence,wisdom,charisma,
# strength_saving_throw,dexterity_saving_throw,constitution_saving_throw,intelligence_saving_throw,wisdom_saving_throw,charisma_saving_throw,

# acrobatics,animal_handling,arcana,athletics,deception,history,insight,intimidation,investigation,medicine,nature,
# perception,performance,persuasion,religion,sleight_of_hand,stealth,survival,passive_perception,

# darkvision,blindsight,truesight,tremorsense,telepathy,
# nonmagical_slashing,silver_slashing,adamntine_slashing,magical_slashing,nonmagical_piercing,silver_piercing,
# adamntine_piercing,magical_piercing,nonmagical_bludgeoning,silver_bludgeoning,adamntine_bludgeoning,
# magical_bludgeoning,acid,cold,fire,force,lightning,necrotic,poison,psychic,radiant,thunder,

# unconscious_immunity,frightened_immunity,invisible_immunity,incapacitated_immunity,deafened_immunity,
# petrified_immunity,restrained_immunity,blinded_immunity,poisoned_immunity,charmed_immunity,stunned_immunity,
# paralyzed_immunity,prone_immunity,grappled_immunity,

# cr,proficiency_bonus,source,legendary_resistance,
# habitat,actions,bonus_actions,reactions,legendary_actions,mythic_actions,lair_actions,description,properties,exhausted_immunity,lair

def normalize_words(token: str, normalizer):
    res = " ".join([normalizer.parse(word)[0].normal_form for word in token.split(" ")])
    return res


def get_similar(card_url, card_df, target_index, n, cosine_sim_matrix):
    # Индекс таргета в матрице косинусных расстояний, смотрим по уникальному полю "url"
    # target_index = card_df[card_df["url"] == card_url].index[0]

    # Смотрим похожесть карточек на таргет, выбирая строку косинусных расстояний с индексом таргета
    card_scores = list(enumerate(cosine_sim_matrix[target_index]))

    # Сортировка карточек по уменьшению похожести
    sorted_cards = sorted(card_scores, key=lambda x: x[1], reverse=True)

    top_cards = []
    i = -1
    # Добавляем всех кроме самого себя
    while len(top_cards) < n:
        i += 1
        try:
            # Не добавляем элемент с индексом таргета
            if sorted_cards[i][0] != target_index:
                top_cards.append((card_df.iloc[sorted_cards[i][0]], sorted_cards[i][1]))
        except IndexError:
            break

    return top_cards


df = pd.read_csv("../Scraper/output/bestiary.csv")
columns = [ "size", "type_", "alignment", "armor_class_type", "description", "properties", "source", "actions", "lair", "lair_actions"]

for col in columns:
    df.loc[df[col].isna(), col] = ""

df.loc[:, "token"] = df.loc[:, columns].apply(lambda row: ' '.join(row.values.astype(str)), axis=1)

df_scores = pd.DataFrame(df.loc[:, "url"])
df_scores = df_scores.assign(score_1=np.nan,score_1_url=np.nan,score_2=np.nan,score_2_url=np.nan,score_3=np.nan,score_3_url=np.nan,)

morph = pymorphy3.MorphAnalyzer()
vectorizer = TfidfVectorizer(stop_words=stopwords_ru)

# for key, group in df.groupby(by=["cr"]):
#     print(key, len(group))
#
#     group.loc[:, "token"] = group["token"].apply(normalize_words, normalizer=morph)
#     print(group["token"])
#
#     # Векторизуем токен, собранный из разных параметров карточки
#     tfidf_matrix = vectorizer.fit_transform(group["token"])
#
#     cosine_sim_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)
#
#     # Выделяем для каждой карточки 3 похожих
#     index_count = 0
#     for i, row in group.iterrows():  # i will be index, row a pandas Series
#         # print(i)
#         target = group.loc[i, "url"]
#
#         res = get_similar(card_url=target, card_df=group, target_index=index_count, n=3, cosine_sim_matrix=cosine_sim_matrix)
#
#         print(f"Наиболее похожие на {target}:")
#         card_count = 1
#         for card in res:
#             print(f"{card[1]}, {card[0]['url']}")
#
#             # Сохраняем данные в датафрейм
#             df_scores.loc[i, f"score_{card_count}"] = card[1]
#             df_scores.loc[i, f"score_{card_count}_url"] = card[0]["url"]
#             card_count += 1
#
#         index_count += 1
#
#     # Сохраняем датафрейм в файл
#     df_scores.to_csv("output/bestiary_recomendations.csv")


# df_scores = pd.read_csv("output/bestiary_recomendations.csv")
#
# df.loc[df["cr"].isna(), "cr"] = -1
#
# # Обработка существ без CR
# for key, group in df.groupby(by=["cr"]):
#     if key[0] == -1:
#         print(key, len(group))
#
#         group.loc[:, "token"] = group["token"].apply(normalize_words, normalizer=morph)
#         print(group["token"])
#
#         # Векторизуем токен, собранный из разных параметров карточки
#         tfidf_matrix = vectorizer.fit_transform(group["token"])
#
#         cosine_sim_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)
#
#         # Выделяем для каждой карточки 3 похожих
#         index_count = 0
#         for i, row in group.iterrows():  # i will be index, row a pandas Series
#             # print(i)
#             target = group.loc[i, "url"]
#
#             res = get_similar(card_url=target, card_df=group, target_index=index_count, n=3, cosine_sim_matrix=cosine_sim_matrix)
#
#             print(f"Наиболее похожие на {target}:")
#             card_count = 1
#             for card in res:
#                 print(f"{card[1]}, {card[0]['url']}")
#
#                 # Сохраняем данные в датафрейм
#                 df_scores.loc[i, f"score_{card_count}"] = card[1]
#                 df_scores.loc[i, f"score_{card_count}_url"] = card[0]["url"]
#                 card_count += 1
#
#             index_count += 1
#
#         # Сохраняем датафрейм в файл
#         df_scores.to_csv("output/bestiary_recomendations_no_cr.csv")
