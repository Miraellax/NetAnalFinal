import math

import pandas as pd
import sqlite3

sql_query = """SELECT name FROM sqlite_master  
  WHERE type='table';"""

sql_select_sizes = "SELECT id, name FROM creature_sizes;"
sql_select_types = "SELECT id, name FROM creature_types;"
sql_select_alignments = "SELECT id, name FROM creature_alignments;"
sql_select_sources = "SELECT id, name FROM creature_sources;"

sql_insert_sizes = "INSERT INTO creature_sizes (name) VALUES (?) RETURNING id;"
sql_insert_types = "INSERT INTO creature_types (name) VALUES (?) RETURNING id;"
sql_insert_alignments = "INSERT INTO creature_alignments (name) VALUES (?) RETURNING id;"
sql_insert_sources = "INSERT INTO creature_sources (name) VALUES (?) RETURNING id;"

def get_db_names_column(cursor: sqlite3.Cursor, sql_query) -> dict:
    cursor.execute(sql_query)
    res = cursor.fetchall()

    # {name: id}
    return {res[i]["name"]:res[i]["id"] for i in range(len(res))}

def insert_db_names_column(cursor: sqlite3.Cursor, sql_query, value) -> int:
    cursor.execute(sql_query, [value])
    res = cursor.fetchall()

    # {name: id}
    return res[0]["id"]

def insert_creature(cursor: sqlite3.Cursor, creature_df):
    sql = f"""INSERT INTO creatures (
                                    url,
                                    name,
                                    name_translated,
                                    name_uppercase,
                                    name_translated_uppercase,
                                    size,
                                    type,
                                    alignment,
                                    is_named,
                                    armor_class,
                                    armor_class_type,
                                    average_hitpoints,
                                    hit_die_type,
                                    hit_dice,
                                    hitpoints_bonus,
                                    walking_speed,
                                    flying_speed,
                                    swimming_speed,
                                    digging_speed,
                                    climbing_speed,
                                    strength,
                                    strength_modifier,
                                    dexterity,
                                    dexterity_modifier,
                                    constitution,
                                    constitution_modifier,
                                    intelligence,
                                    intelligence_modifier,
                                    wisdom,
                                    wisdom_modifier,
                                    charisma,
                                    charisma_modifier,
                                    strength_saving_throw,
                                    dexterity_saving_throw,
                                    constitution_saving_throw,
                                    intelligence_saving_throw,
                                    wisdom_saving_throw,
                                    charisma_saving_throw,
                                    strength_saving_throw,
                                    acrobatics,
                                    animal_handling,
                                    arcana,
                                    athletics,
                                    deception,
                                    history,
                                    insight,
                                    intimidation,
                                    investigation,
                                    medicine,
                                    nature,
                                    perception,
                                    performance,
                                    persuasion,
                                    religion,
                                    sleight_of_hand,
                                    stealth,
                                    survival,
                                    passive_perception,
                                    darkvision,
                                    blindsight,
                                    truesight,
                                    tremorsense,
                                    telepathy,
                                    nonmagical_slashing,
                                    silver_slashing,
                                    adamntine_slashing,
                                    magical_slashing,
                                    nonmagical_piercing,
                                    silver_piercing,
                                    adamntine_piercing,
                                    magical_piercing,
                                    nonmagical_bludgeoning,
                                    silver_bludgeoning,
                                    adamntine_bludgeoning,
                                    magical_bludgeoning,
                                    acid,
                                    cold,
                                    fire,
                                    force,
                                    lightning,
                                    necrotic,
                                    poison,
                                    psychic,
                                    radiant,
                                    thunder,
                                    unconscious_immunity,
                                    frightened_immunity,
                                    invisible_immunity,
                                    incapacitated_immunity,
                                    deafened_immunity,
                                    petrified_immunity,
                                    restrained_immunity,
                                    blinded_immunity,
                                    poisoned_immunity,
                                    charmed_immunity,
                                    stunned_immunity,
                                    paralyzed_immunity,
                                    prone_immunity,
                                    grappled_immunity,
                                    cr,
                                    proficiency_bonus,
                                    source,
                                    legendary_resistance,
                                    habitat,
                                    actions,
                                    bonus_actions,
                                    reactions,
                                    legendary_actions,
                                    mythic_actions,
                                    lair_actions,
                                    description,
                                    properties                                  
                                    )
                            VALUES (
                                    :url,
                                    :name,
                                    :name_translated,
                                    :name_uppercase,
                                    :name_translated_uppercase,
                                    :size,
                                    :type_,
                                    :alignment,
                                    :is_named,
                                    :armor_class,
                                    :armor_class_type,
                                    :average_hitpoints,
                                    :hit_die_type,
                                    :hit_dice,
                                    :hitpoints_bonus,
                                    :walking_speed,
                                    :flying_speed,
                                    :swimming_speed,
                                    :digging_speed,
                                    :climbing_speed,
                                    :strength,
                                    :strength_modifier,
                                    :dexterity,
                                    :dexterity_modifier,
                                    :constitution,
                                    :constitution_modifier,
                                    :intelligence,
                                    :intelligence_modifier,
                                    :wisdom,
                                    :wisdom_modifier,
                                    :charisma,
                                    :charisma_modifier,
                                    :strength_saving_throw,
                                    :dexterity_saving_throw,
                                    :constitution_saving_throw,
                                    :intelligence_saving_throw,
                                    :wisdom_saving_throw,
                                    :charisma_saving_throw,
                                    :strength_saving_throw,
                                    :acrobatics,
                                    :animal_handling,
                                    :arcana,
                                    :athletics,
                                    :deception,
                                    :history,
                                    :insight,
                                    :intimidation,
                                    :investigation,
                                    :medicine,
                                    :nature,
                                    :perception,
                                    :performance,
                                    :persuasion,
                                    :religion,
                                    :sleight_of_hand,
                                    :stealth,
                                    :survival,
                                    :passive_perception,
                                    :darkvision,
                                    :blindsight,
                                    :truesight,
                                    :tremorsense,
                                    :telepathy,
                                    :nonmagical_slashing,
                                    :silver_slashing,
                                    :adamntine_slashing,
                                    :magical_slashing,
                                    :nonmagical_piercing,
                                    :silver_piercing,
                                    :adamntine_piercing,
                                    :magical_piercing,
                                    :nonmagical_bludgeoning,
                                    :silver_bludgeoning,
                                    :adamntine_bludgeoning,
                                    :magical_bludgeoning,
                                    :acid,
                                    :cold,
                                    :fire,
                                    :force,
                                    :lightning,
                                    :necrotic,
                                    :poison,
                                    :psychic,
                                    :radiant,
                                    :thunder,
                                    :unconscious_immunity,
                                    :frightened_immunity,
                                    :invisible_immunity,
                                    :incapacitated_immunity,
                                    :deafened_immunity,
                                    :petrified_immunity,
                                    :restrained_immunity,
                                    :blinded_immunity,
                                    :poisoned_immunity,
                                    :charmed_immunity,
                                    :stunned_immunity,
                                    :paralyzed_immunity,
                                    :prone_immunity,
                                    :grappled_immunity,
                                    :cr,
                                    :proficiency_bonus,
                                    :source,
                                    :legendary_resistance,
                                    :habitat,
                                    :actions,
                                    :bonus_actions,
                                    :reactions,
                                    :legendary_actions,
                                    :mythic_actions,
                                    :lair_actions,
                                    :description,
                                    :properties
                                    ) ON CONFLICT DO NOTHING RETURNING id;"""


    # print(creature_df.to_dict())
    cursor.execute(sql, creature_df.to_dict())
    res = cursor.fetchall()

    # {name: id}
    return res[0]

# 1. Чтение датафрейма из файла
df = pd.read_csv("output/bestiary.csv", )

# 2. Исправление ошибок данных
df.loc[df["source"].isna(), "source"] = "«Player's handbook»"
df.loc[df["average_hitpoints"] == 0, "average_hitpoints"] = 1
df.loc[df["hit_die_type"] == 0, "hit_die_type"] = 1
df.loc[df["hit_dice"] == 0, "hit_dice"] = 1
df.loc[df["passive_perception"].isna(), "passive_perception"] = 5
df.loc[df["cr"].isna(), "cr"] = 0
df.loc[df["proficiency_bonus"].isna(), "proficiency_bonus"] = 2
df.loc[df["proficiency_bonus"] == "0.0", "proficiency_bonus"] = 2
df.loc[df["proficiency_bonus"] == 0.0, "proficiency_bonus"] = 2

print(df.loc[df["name"] == "Дух жнеца"]["proficiency_bonus"])


# 3. Добавление в бд
with sqlite3.connect('../database/database.db') as connection:
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    for id_, row in df.iterrows():
        print(row["name"])

        size = row["size"]
        type_ = row["type_"]
        alignment = row["alignment"]
        source = row["source"]

        # 2. Проверка словарных значений, получение индексов ключей
        # или добавление значения в словарь и получение индекса ключа
        db_sizes = get_db_names_column(cursor, sql_select_sizes)
        if size in db_sizes:
            size_id = db_sizes[size]
        else:
            size_id = insert_db_names_column(cursor, sql_insert_sizes, size)

        db_types = get_db_names_column(cursor, sql_select_types)
        if type_ in db_types:
            type_id = db_types[type_]
        else:
            type_id = insert_db_names_column(cursor, sql_insert_types, type_)

        db_alignments = get_db_names_column(cursor, sql_select_alignments)
        if alignment in db_alignments:
            alignment_id = db_alignments[alignment]
        else:
            if isinstance(alignment, float) and math.isnan(alignment):
                alignment_id = None
            else:
                alignment_id = insert_db_names_column(cursor, sql_insert_alignments, alignment)

        db_sources = get_db_names_column(cursor, sql_select_sources)
        if source in db_sources:
            source_id = db_sources[source]
        else:
            source_id = insert_db_names_column(cursor, sql_insert_sources, source)

        row["size"] = size_id
        row["type_"] = type_id
        row["alignment"] = alignment_id
        row["source"] = source_id

        # Добавление карточки в бд
        insert_creature(cursor, row)
