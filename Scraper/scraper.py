import enum

import requests
from bs4 import BeautifulSoup
import re
import pymorphy3
import pandas as pd

from Scraper.enumerators import (DamageSusceptibilityTypes,
                                 KeyWords,
                                 KeyAbilities,
                                 KeyAbilitiesShort,
                                 SkillTypes,
                                 DamageTypes,
                                 ConditionImmunityTypes,
                                 SenseTypes,
                                 DescriptionTitles,
                                 SpeedTypes)

# TODO, фичи перед действиями, которые не легендарные сопротивления, идут в описание существа. Например "амфибия" у дракона.
#  Скрапер высчитывает все бонусы спас бросков и бонусы навыков, независимо от того, написан ли он в карточке.

base_url = "https://dnd.su"
bestiary_url = "/bestiary/"
test_html = "Аспект Тиамат _ Бестиарий D&D 5 _ Fizban's Treasury of Dragons.htm"
test_html2 = "Вервепрь _ Бестиарий D&D 5 _ Monster manual.htm"
test_html3 = "Скелет _ Бестиарий D&D 5 _ Player's handbook, Monster manual.htm"
test_html4 = "Баллиста _ Бестиарий D&D 5 _ Dungeon master's guide.htm"
test_html5 = "Панцирница _ Бестиарий D&D 5 _ Monster manual.htm"

# Для нормализации слов
morph = pymorphy3.MorphAnalyzer()

def scrape_bestiary_table(url: str):
    headers = {}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    pages = []
    items = soup.find_all("div", class_="list-item__beast")

    for item in items:
        link = item.find("a", class_="list-item-wrapper")
        if link.has_attr("href"):
            pages.append(base_url+link["href"])

    return pages


def scrape_beast_info(url: str):
    headers = {}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # with open(url, encoding="utf-8") as fp:
    #     soup = BeautifulSoup(fp, 'html.parser')

    name = soup.find("h2", class_="card-title").find("span").text
    name_split = re.split(r'\[|\]', name)
    ru_name, en_name = name_split[0], name_split[1]
    ru_name_upper = ru_name.upper()
    en_name_upper = en_name.upper()
    print(ru_name, en_name)

    card_article_body = soup.find("ul", class_="card__article-body")

    li_size_type_alignment = card_article_body.find("li", class_="size-type-alignment")
    li_items_no_class = card_article_body.find_all("li", class_="")
    li_abilities = card_article_body.find("li", class_="abilities")
    li_skills = card_article_body.find("li", class_="skills")
    li_desc = card_article_body.find_all("li", class_="subsection desc")

    # Обработка размера, типа, мировоззрения, именной ли НИП
    size_type_alignment = li_size_type_alignment.text
    last_qmark = size_type_alignment.rindex("?")
    size = size_type_alignment[0:last_qmark].replace("?", "")
    type_alignment = size_type_alignment[last_qmark + 1:]
    size_part = re.findall("[а-я ]+", type_alignment)
    size = (size + size_part[0]).strip()
    if len(size_part[0].strip()) > 0:
        type_alignment = type_alignment.replace(size_part[0], "")

    if type_alignment.count(")") > 0:
        f = re.findall(r".+\)", type_alignment)
        b_type = (f[0]).strip()

        a = type_alignment.replace(f[0], "").replace(",", "").strip()
        if len(a) > 0:
            alignment = a
        else:
            alignment = None
    else:
        t_sp = type_alignment.split(",")
        if len(t_sp) == 1:
            b_type = t_sp[0].strip()
            alignment = None

        else:
            b_type = t_sp[0].strip()
            alignment = t_sp[1].strip()
    if "именной НИП" in size_type_alignment:
        named = True
    else:
        named = False

    print("S", size, "T", b_type, "A", alignment, "named", named)

    # Нормализация размера, типа и мировоззрения
    if size is not None:
        size = morph.parse(size)[0].normal_form
    if b_type is not None:
        b_type = morph.parse(b_type)[0].normal_form
    if alignment is not None:
        alignment = morph.parse(alignment)[0].normal_form
    print("S", size, "T", b_type, "A", alignment, "named", named)

    # Объявление сопротивлений/иммунитетов перед обработкой
    nonmagical_slashing = DamageSusceptibilityTypes.normal.value
    silver_slashing = DamageSusceptibilityTypes.normal.value
    adamntine_slashing = DamageSusceptibilityTypes.normal.value
    magical_slashing = DamageSusceptibilityTypes.normal.value
    nonmagical_piercing = DamageSusceptibilityTypes.normal.value
    silver_piercing = DamageSusceptibilityTypes.normal.value
    adamntine_piercing = DamageSusceptibilityTypes.normal.value
    magical_piercing = DamageSusceptibilityTypes.normal.value
    nonmagical_bludgeoning = DamageSusceptibilityTypes.normal.value
    silver_bludgeoning = DamageSusceptibilityTypes.normal.value
    adamntine_bludgeoning = DamageSusceptibilityTypes.normal.value
    magical_bludgeoning = DamageSusceptibilityTypes.normal.value
    acid = DamageSusceptibilityTypes.normal.value
    cold = DamageSusceptibilityTypes.normal.value
    fire = DamageSusceptibilityTypes.normal.value
    force = DamageSusceptibilityTypes.normal.value
    lightning = DamageSusceptibilityTypes.normal.value
    necrotic = DamageSusceptibilityTypes.normal.value
    poison = DamageSusceptibilityTypes.normal.value
    psychic = DamageSusceptibilityTypes.normal.value
    radiant = DamageSusceptibilityTypes.normal.value
    thunder = DamageSusceptibilityTypes.normal.value

    # Объявление отсутствия иммунитета к состояниям перед обработкой
    unconscious = False
    frightened = False
    invisible = False
    incapacitated = False
    deafened = False
    petrified = False
    restrained = False
    blinded = False
    poisoned = False
    charmed = False
    stunned = False
    paralyzed = False
    prone = False
    grappled = False
    exhausted = False

    # Определение мест обитания перед обработкой
    habitat = None

    # Определение навыка телепатии перед обработкой
    telepathy = 0

    # Обработка значений статов
    # !!! Для спасбросков и навыков используются значения статов, они должны быть собраны перед обработкой li_items_no_class !!!
    if li_abilities is not None:
        for node in li_abilities:
            match node["title"]:
                case KeyAbilities.strength.value:
                    sp = node.text.split(" ")
                    strength_value = int(sp[0][3:])
                    strength_mod = int(sp[1][1:-1])
                    print("str", strength_value, strength_mod)

                case KeyAbilities.dexterity.value:
                    sp = node.text.split(" ")
                    dexterity_value = int(sp[0][3:])
                    dexterity_mod = int(sp[1][1:-1])
                    print("dex", dexterity_value, dexterity_mod)

                case KeyAbilities.constitution.value:
                    sp = node.text.split(" ")
                    constitution_value = int(sp[0][3:])
                    constitution_mod = int(sp[1][1:-1])
                    print("const", constitution_value, constitution_mod)

                case KeyAbilities.intelligence.value:
                    sp = node.text.split(" ")
                    intelligence_value = int(sp[0][3:])
                    intelligence_mod = int(sp[1][1:-1])
                    print("int", intelligence_value, intelligence_mod)

                case KeyAbilities.wisdom.value:
                    sp = node.text.split(" ")
                    wisdom_value = int(sp[0][3:])
                    wisdom_mod = int(sp[1][1:-1])
                    print("wis", wisdom_value, wisdom_mod)

                case KeyAbilities.charisma.value:
                    sp = node.text.split(" ")
                    charisma_value = int(sp[0][3:])
                    charisma_mod = int(sp[1][1:-1])
                    print("char", charisma_value, charisma_mod)
    else: # Без навыков
        strength_value = 0
        strength_mod = 0
        dexterity_value = 0
        dexterity_mod = 0
        constitution_value = 0
        constitution_mod = 0
        intelligence_value = 0
        intelligence_mod = 0
        wisdom_value = 0
        wisdom_mod = 0
        charisma_value = 0
        charisma_mod = 0

    # Обработка строк без класса по ключевым словам в теге <strong>
    for item in li_items_no_class:
        match item.find("strong").text:
            case KeyWords.armour_class.value:
                # Берем всю строку, так как "обсидианово-кремневые латы дракона, щит" / "природный доспех"
                armour_class = int(item.text.split(" ")[2])
                sp = re.findall(r"(?<=\().*(?=\))", item.text)
                if len(sp) > 0:
                    armour_type = sp[0]
                else:
                    armour_type = ""
                print(armour_class, armour_type)

            case KeyWords.hitpoints.value:
                average_hitpoints = 0
                hit_dice = 0
                hit_die_type = 0
                hitpoints_bonus = 0

                if (av_hp := item.find("span", attrs={"data-type":"middle"})) is not None:
                    average_hitpoints = int(av_hp.text)

                if (h_dice := item.find("span", attrs={"data-type":"throw"})) is not None:
                    hit_dice = int(h_dice.text)

                if (h_dice_type := item.find("span", attrs={"data-type":"dice"})) is not None:
                    hit_die_type = int(h_dice_type.text)

                if (hitpoints_bonus_node := item.find("span", attrs={"data-type":"bonus"})) is not None:
                    hitpoints_bonus = int(hitpoints_bonus_node.text)
                print(average_hitpoints, hit_dice, hit_die_type, hitpoints_bonus)

            case KeyWords.speed.value:
                walking_speed = None
                swimming_speed = None
                flying_speed = None
                climbing_speed = None
                digging_speed = None

                # Скорость 30 футов (40 футов в облике кабана) - удаляем то, что в скобках, так как нет возможности сохранить
                speed_text = re.sub(r"\(.*\)", "", item.text)
                speed_text = speed_text.split(",")
                for speed in speed_text:
                    sp = speed.lower().strip().split(" ")
                    if SpeedTypes.swimming.value in sp:
                        swimming_speed = int(sp[-2])
                    elif SpeedTypes.flying.value in sp:
                        flying_speed = int(sp[-2])
                    elif SpeedTypes.climbing.value in sp:
                        climbing_speed = int(sp[-2])
                    elif SpeedTypes.digging.value in sp:
                        digging_speed = int(sp[-2])
                    else:
                        walking_speed = int(sp[-2])
                print(walking_speed, swimming_speed, flying_speed, climbing_speed, digging_speed)

            # !!! Перед обработкой спасов должны быть собраны значения статов для расчетов !!!
            case KeyWords.saving_throws.value:
                save_str = None
                save_dex = None
                save_con = None
                save_int = None
                save_wis = None
                save_chr = None

                # Считывание спасбросков из карточки
                sp = item.text.replace(KeyWords.saving_throws.value, "").strip().split(", ")
                for save in sp:
                    s_sp = save.split(" ")
                    match s_sp[0]:
                        case KeyAbilitiesShort.strength.value:
                            save_str = int(s_sp[1])

                        case KeyAbilitiesShort.dexterity.value:
                            save_dex = int(s_sp[1])

                        case KeyAbilitiesShort.constitution.value:
                            save_con = int(s_sp[1])

                        case KeyAbilitiesShort.intelligence.value:
                            save_int = int(s_sp[1])

                        case KeyAbilitiesShort.wisdom.value:
                            save_wis = int(s_sp[1])

                        case KeyAbilitiesShort.charisma.value:
                            save_chr = int(s_sp[1])

                    # Вычисление спасброска по навыку, если спас не указан в карточке (владения нет)
                    if save_str is None:
                        save_str = strength_mod
                    if save_dex is None:
                        save_dex = dexterity_mod
                    if save_con is None:
                        save_con = constitution_mod
                    if save_int is None:
                        save_int = intelligence_mod
                    if save_wis is None:
                        save_wis = wisdom_mod
                    if save_chr is None:
                        save_chr = charisma_mod

                print("save_str", save_str, "save_dex", save_dex, "save_con", save_con, "save_int", save_int, "save_wis", save_wis, "save_chr", save_chr)

            case KeyWords.damage_immunity.value:
                # Разбиение на магические и немагические/не посеребренные/не адамантиевые через ;
                damage_classes = item.text.replace(KeyWords.damage_immunity.value, "").split(";")

                # Обработка магических и остальных типов
                for damage_class in damage_classes:
                    d_sp = re.split(r"[,| ]", damage_class)

                    # иммунитет к дробящий от немагических = немагический-имм, магический-нормал, серебо-имм, адамантий-имм
                    # иммунитет к дробящий от немагических кроме серебра/адам = немагический-имм, магический-нормал, серебо-нормал/имм, адамантий-имм/нормал
                    # иммунитет к дробящий кроме серебра/адам = немагический-имм, магический-имм, серебо-нормал/имм, адамантий-имм/нормал
                    # иммунитет к дробящий = немагический-имм, магический-имм, серебо-имм, адамантий-имм

                    # Дробящий
                    if DamageTypes.bludgeoning.value in d_sp:
                        nonmagical_bludgeoning = DamageSusceptibilityTypes.immunity.value
                        if DamageTypes.silver.value not in d_sp:
                            silver_bludgeoning = DamageSusceptibilityTypes.immunity.value
                        if DamageTypes.adamantine.value not in d_sp:
                            adamntine_bludgeoning = DamageSusceptibilityTypes.immunity.value
                        if DamageTypes.nonmagical.value not in d_sp:
                            magical_bludgeoning = DamageSusceptibilityTypes.immunity.value

                    # Рубящий
                    if DamageTypes.slashing.value in d_sp:
                        nonmagical_slashing = DamageSusceptibilityTypes.immunity.value
                        if DamageTypes.silver.value not in d_sp:
                            silver_slashing = DamageSusceptibilityTypes.immunity.value
                        if DamageTypes.adamantine.value not in d_sp:
                            adamntine_slashing = DamageSusceptibilityTypes.immunity.value
                        if DamageTypes.nonmagical.value not in d_sp:
                            magical_slashing = DamageSusceptibilityTypes.immunity.value

                    # Колющий
                    if DamageTypes.piercing.value in d_sp:
                        nonmagical_piercing = DamageSusceptibilityTypes.immunity.value
                        if DamageTypes.silver.value not in d_sp:
                            silver_piercing = DamageSusceptibilityTypes.immunity.value
                        if DamageTypes.adamantine.value not in d_sp:
                            adamntine_piercing = DamageSusceptibilityTypes.immunity.value
                        if DamageTypes.nonmagical.value not in d_sp:
                            magical_piercing = DamageSusceptibilityTypes.immunity.value

                    if DamageTypes.acid.value in d_sp:
                        acid = DamageSusceptibilityTypes.immunity.value
                    if DamageTypes.cold.value in d_sp:
                        cold = DamageSusceptibilityTypes.immunity.value
                    if DamageTypes.fire.value in d_sp:
                        fire = DamageSusceptibilityTypes.immunity.value
                    if DamageTypes.force.value in d_sp:
                        force = DamageSusceptibilityTypes.immunity.value
                    if DamageTypes.lightning.value in d_sp:
                        lightning = DamageSusceptibilityTypes.immunity.value
                    if DamageTypes.necrotic.value in d_sp:
                        necrotic = DamageSusceptibilityTypes.immunity.value
                    if DamageTypes.poison.value in d_sp:
                        poison = DamageSusceptibilityTypes.immunity.value
                    if DamageTypes.psychic.value in d_sp:
                        psychic = DamageSusceptibilityTypes.immunity.value
                    if DamageTypes.radiant.value in d_sp:
                        radiant = DamageSusceptibilityTypes.immunity.value
                    if DamageTypes.thunder.value in d_sp:
                        thunder = DamageSusceptibilityTypes.immunity.value

            case KeyWords.damage_vulnerability.value:
                damage_classes = item.text.replace(KeyWords.damage_immunity.value, "").split(";")

                # Обработка магических и остальных типов
                for damage_class in damage_classes:
                    d_sp = re.split(r"[,| ]", damage_class)

                    # Дробящий
                    if DamageTypes.bludgeoning.value in d_sp:
                        nonmagical_bludgeoning = DamageSusceptibilityTypes.vulnerability.value
                        if DamageTypes.silver.value not in d_sp:
                            silver_bludgeoning = DamageSusceptibilityTypes.vulnerability.value
                        if DamageTypes.adamantine.value not in d_sp:
                            adamntine_bludgeoning = DamageSusceptibilityTypes.vulnerability.value
                        if DamageTypes.nonmagical.value not in d_sp:
                            magical_bludgeoning = DamageSusceptibilityTypes.vulnerability.value

                    # Рубящий
                    if DamageTypes.slashing.value in d_sp:
                        nonmagical_slashing = DamageSusceptibilityTypes.vulnerability.value
                        if DamageTypes.silver.value not in d_sp:
                            silver_slashing = DamageSusceptibilityTypes.vulnerability.value
                        if DamageTypes.adamantine.value not in d_sp:
                            adamntine_slashing = DamageSusceptibilityTypes.vulnerability.value
                        if DamageTypes.nonmagical.value not in d_sp:
                            magical_slashing = DamageSusceptibilityTypes.vulnerability.value

                    # Колющий
                    if DamageTypes.piercing.value in d_sp:
                        nonmagical_piercing = DamageSusceptibilityTypes.vulnerability.value
                        if DamageTypes.silver.value not in d_sp:
                            silver_piercing = DamageSusceptibilityTypes.vulnerability.value
                        if DamageTypes.adamantine.value not in d_sp:
                            adamntine_piercing = DamageSusceptibilityTypes.vulnerability.value
                        if DamageTypes.nonmagical.value not in d_sp:
                            magical_piercing = DamageSusceptibilityTypes.vulnerability.value

                    if DamageTypes.acid.value in d_sp:
                        acid = DamageSusceptibilityTypes.vulnerability.value
                    if DamageTypes.cold.value in d_sp:
                        cold = DamageSusceptibilityTypes.vulnerability.value
                    if DamageTypes.fire.value in d_sp:
                        fire = DamageSusceptibilityTypes.vulnerability.value
                    if DamageTypes.force.value in d_sp:
                        force = DamageSusceptibilityTypes.vulnerability.value
                    if DamageTypes.lightning.value in d_sp:
                        lightning = DamageSusceptibilityTypes.vulnerability.value
                    if DamageTypes.necrotic.value in d_sp:
                        necrotic = DamageSusceptibilityTypes.vulnerability.value
                    if DamageTypes.poison.value in d_sp:
                        poison = DamageSusceptibilityTypes.vulnerability.value
                    if DamageTypes.psychic.value in d_sp:
                        psychic = DamageSusceptibilityTypes.vulnerability.value
                    if DamageTypes.radiant.value in d_sp:
                        radiant = DamageSusceptibilityTypes.vulnerability.value
                    if DamageTypes.thunder.value in d_sp:
                        thunder = DamageSusceptibilityTypes.vulnerability.value

            case KeyWords.damage_resistance.value:
                damage_classes = item.text.replace(KeyWords.damage_immunity.value, "").split(";")

                # Обработка магических и остальных типов
                for damage_class in damage_classes:
                    d_sp = re.split(r"[,| ]", damage_class)

                    # Дробящий
                    if DamageTypes.bludgeoning.value in d_sp:
                        nonmagical_bludgeoning = DamageSusceptibilityTypes.resistance.value
                        if DamageTypes.silver.value not in d_sp:
                            silver_bludgeoning = DamageSusceptibilityTypes.resistance.value
                        if DamageTypes.adamantine.value not in d_sp:
                            adamntine_bludgeoning = DamageSusceptibilityTypes.resistance.value
                        if DamageTypes.nonmagical.value not in d_sp:
                            magical_bludgeoning = DamageSusceptibilityTypes.resistance.value

                    # Рубящий
                    if DamageTypes.slashing.value in d_sp:
                        nonmagical_slashing = DamageSusceptibilityTypes.resistance.value
                        if DamageTypes.silver.value not in d_sp:
                            silver_slashing = DamageSusceptibilityTypes.resistance.value
                        if DamageTypes.adamantine.value not in d_sp:
                            adamntine_slashing = DamageSusceptibilityTypes.resistance.value
                        if DamageTypes.nonmagical.value not in d_sp:
                            magical_slashing = DamageSusceptibilityTypes.resistance.value

                    # Колющий
                    if DamageTypes.piercing.value in d_sp:
                        nonmagical_piercing = DamageSusceptibilityTypes.resistance.value
                        if DamageTypes.silver.value not in d_sp:
                            silver_piercing = DamageSusceptibilityTypes.resistance.value
                        if DamageTypes.adamantine.value not in d_sp:
                            adamntine_piercing = DamageSusceptibilityTypes.resistance.value
                        if DamageTypes.nonmagical.value not in d_sp:
                            magical_piercing = DamageSusceptibilityTypes.resistance.value

                    if DamageTypes.acid.value in d_sp:
                        acid = DamageSusceptibilityTypes.resistance.value
                    if DamageTypes.cold.value in d_sp:
                        cold = DamageSusceptibilityTypes.resistance.value
                    if DamageTypes.fire.value in d_sp:
                        fire = DamageSusceptibilityTypes.resistance.value
                    if DamageTypes.force.value in d_sp:
                        force = DamageSusceptibilityTypes.resistance.value
                    if DamageTypes.lightning.value in d_sp:
                        lightning = DamageSusceptibilityTypes.resistance.value
                    if DamageTypes.necrotic.value in d_sp:
                        necrotic = DamageSusceptibilityTypes.resistance.value
                    if DamageTypes.poison.value in d_sp:
                        poison = DamageSusceptibilityTypes.resistance.value
                    if DamageTypes.psychic.value in d_sp:
                        psychic = DamageSusceptibilityTypes.resistance.value
                    if DamageTypes.radiant.value in d_sp:
                        radiant = DamageSusceptibilityTypes.resistance.value
                    if DamageTypes.thunder.value in d_sp:
                        thunder = DamageSusceptibilityTypes.resistance.value

            case KeyWords.condition_immunity.value:
                condition_types = item.text.replace(KeyWords.condition_immunity.value, "").split(",")
                for c_type in condition_types:
                    match c_type:
                        case ConditionImmunityTypes.unconscious.value:
                            unconscious = True
                        case ConditionImmunityTypes.frightened.value:
                            frightened = True
                        case ConditionImmunityTypes.invisible.value:
                            invisible = True
                        case ConditionImmunityTypes.incapacitated.value:
                            incapacitated = True
                        case ConditionImmunityTypes.deafened.value:
                            deafened = True
                        case ConditionImmunityTypes.petrified.value:
                            petrified = True
                        case ConditionImmunityTypes.restrained.value:
                            restrained = True
                        case ConditionImmunityTypes.blinded.value:
                            blinded = True
                        case ConditionImmunityTypes.poisoned.value:
                            poisoned = True
                        case ConditionImmunityTypes.charmed.value:
                            charmed = True
                        case ConditionImmunityTypes.stunned.value:
                            stunned = True
                        case ConditionImmunityTypes.paralyzed.value:
                            paralyzed = True
                        case ConditionImmunityTypes.prone.value:
                            prone = True
                        case ConditionImmunityTypes.grappled.value:
                            grappled = True
                        case ConditionImmunityTypes.exhausted.value:
                            exhausted = True

            case KeyWords.senses.value:
                passive_perception = 0
                darkvision = 0
                blindsight = 0
                truesight = 0
                tremorsense = 0

                sp = item.text.replace(KeyWords.senses.value, "").strip().split(",")
                for sense in sp:
                    if SenseTypes.passive_perception.value in sense:
                        passive_perception = int(sense.split(" ")[-1])

                    elif SenseTypes.darkvision.value in sense:
                        darkvision = int(sense.split(" ")[-2])

                    elif SenseTypes.blindsight.value in sense:
                        blindsight = int(sense.split(" ")[-2])

                    elif SenseTypes.truesight.value in sense:
                        truesight = int(sense.split(" ")[-2])

                    elif SenseTypes.tremorsense.value in sense:
                        tremorsense = int(sense.split(" ")[-2])

                print("passive_perception", passive_perception, "darkvision", darkvision, "blindsight", blindsight, "truesight", truesight, "tremorsense", tremorsense)

            case KeyWords.languages.value:
                # Проверка на наличие Телепатии
                sp = item.text.split(" ")
                if SenseTypes.telepathy.value in item.text:
                    telepathy_index = sp.index(SenseTypes.telepathy.value)
                    if telepathy_index != -1:
                        telepathy = int(sp[telepathy_index+1])

            case KeyWords.challenge_rating.value:
                # TODO поменять на хранение строки в БД
                challenge_rating = item.text.replace(KeyWords.challenge_rating.value, "").strip().split(" ")[0]
                print("CR", challenge_rating)

            case KeyWords.habitat.value:
                habitat = item.text.replace(KeyWords.habitat.value, "").strip()

            case KeyWords.source.value:
                source = item.text.replace(KeyWords.source.value, "").strip()
                print(source)

            case _:
                # Сбор данных о бонусе мастерства
                sp = item.text.split(" ")
                if  " ".join(sp[0:2]) == KeyWords.proficiency.value:
                    proficiency_bonus = int(sp[2])
                    print("prof_bonus", proficiency_bonus)

    # Обработка владения навыками и подсчет навыков без владения
    acrobatics = None
    animal_handling = None
    arcana = None
    athletics = None
    deception = None
    history = None
    insight = None
    intimidation = None
    investigation = None
    medicine = None
    nature = None
    perception = None
    performance = None
    persuasion = None
    religion = None
    sleight_of_hand = None
    stealth = None
    survival = None

    # Навыки с владением (указанные)
    if li_skills is not None:
        sk = li_skills.find_all("span", class_="skill-bonus")
        for skill in sk:
            match skill.contents[0].strip():
                case SkillTypes.acrobatics.value:
                    acrobatics = int(skill.find("strong", "skill-bonus-value").text)
                case SkillTypes.animal_handling.value:
                    animal_handling = int(skill.find("strong", "skill-bonus-value").text)
                case SkillTypes.arcana.value:
                    arcana = int(skill.find("strong", "skill-bonus-value").text)
                case SkillTypes.athletics.value:
                    athletics = int(skill.find("strong", "skill-bonus-value").text)
                case SkillTypes.deception.value:
                    deception = int(skill.find("strong", "skill-bonus-value").text)
                case SkillTypes.history.value:
                    history = int(skill.find("strong", "skill-bonus-value").text)
                case SkillTypes.insight.value:
                    insight = int(skill.find("strong", "skill-bonus-value").text)
                case SkillTypes.intimidation.value:
                    intimidation = int(skill.find("strong", "skill-bonus-value").text)
                case SkillTypes.investigation.value:
                    investigation = int(skill.find("strong", "skill-bonus-value").text)
                case SkillTypes.medicine.value:
                    medicine = int(skill.find("strong", "skill-bonus-value").text)
                case SkillTypes.nature.value:
                    nature = int(skill.find("strong", "skill-bonus-value").text)
                case SkillTypes.perception.value:
                    perception = int(skill.find("strong", "skill-bonus-value").text)
                case SkillTypes.performance.value:
                    performance = int(skill.find("strong", "skill-bonus-value").text)
                case SkillTypes.persuasion.value:
                    persuasion = int(skill.find("strong", "skill-bonus-value").text)
                case SkillTypes.religion.value:
                    religion = int(skill.find("strong", "skill-bonus-value").text)
                case SkillTypes.sleight_of_hand.value:
                    sleight_of_hand = int(skill.find("strong", "skill-bonus-value").text)
                case SkillTypes.stealth.value:
                    acrobatics = int(skill.find("strong", "skill-bonus-value").text)
                case SkillTypes.survival.value:
                    survival = int(skill.find("strong", "skill-bonus-value").text)
    # Навыки без владения
    if acrobatics is None:
        acrobatics = dexterity_mod
    if animal_handling is None:
        animal_handling = wisdom_mod
    if arcana is None:
        arcana = intelligence_mod
    if athletics is None:
        athletics = strength_mod
    if deception is None:
        deception = charisma_mod
    if history is None:
        history = intelligence_mod
    if insight is None:
        insight = wisdom_mod
    if intimidation is None:
        intimidation = charisma_mod
    if investigation is None:
        investigation = intelligence_mod
    if medicine is None:
        medicine = wisdom_mod
    if nature is None:
        nature = intelligence_mod
    if perception is None:
        perception = wisdom_mod
    if performance is None:
        performance = charisma_mod
    if persuasion is None:
        persuasion = charisma_mod
    if religion is None:
        religion = intelligence_mod
    if sleight_of_hand is None:
        sleight_of_hand = dexterity_mod
    if stealth is None:
        stealth = dexterity_mod
    if survival is None:
        survival = wisdom_mod

    print(
    "acrobatics", acrobatics,
    "animal_handling", animal_handling,
    "arcana", arcana,
    "athletics", athletics,
    "deception", deception,
    "history", history,
    "insight", insight,
    "intimidation", intimidation,
    "investigation", investigation,
    "medicine", medicine,
    "nature", nature,
    "perception", perception,
    "performance", performance,
    "persuasion", persuasion,
    "religion", religion,
    "sleight_of_hand", sleight_of_hand,
    "stealth", stealth,
    "survival", survival,
    )

    # Определение описаний перед обработкой
    actions = ""
    legendary_resistance = 0
    bonus_actions = ""
    reactions = ""
    legendary_actions = ""
    mythic_actions = ""
    lair_actions = ""
    lair = ""
    description = ""
    # Местные эффекты относятся к описанию - areal_effects

    for description_node in li_desc:
        # Описание без заголовка, может хранить легендарное сопротивление
        if len(description_node.find_all("h3", "subsection-title")) == 0:
            # TODO add svoistva into DB
            properties = description_node.text
            if (leg_res_index := description_node.text.find(DescriptionTitles.legendary_resistance.value)) != -1:
                # Легендарное сопротивление (5/день)
                re_string = fr"(?<={DescriptionTitles.legendary_resistance.value} \()\d+(?=\/.+\))"
                a = re.findall(re_string, description_node.text)
                legendary_resistance = int(a[0])
        else:
            title = description_node.find("h3", "subsection-title").text
            match title:
                case DescriptionTitles.actions.value:
                    actions = description_node.text.replace(DescriptionTitles.actions.value, "")

                case DescriptionTitles.bonus_actions.value:
                    bonus_actions = description_node.text.replace(DescriptionTitles.bonus_actions.value, "")

                case DescriptionTitles.reactions.value:
                    reactions = description_node.text.replace(DescriptionTitles.reactions.value, "")

                case DescriptionTitles.legendary_actions.value:
                    legendary_actions = description_node.text.replace(DescriptionTitles.legendary_actions.value, "")

                case DescriptionTitles.mythic_actions.value:
                    mythic_actions = description_node.text.replace(DescriptionTitles.mythic_actions.value, "")

                case DescriptionTitles.lair_actions.value:
                    lair_actions = description_node.text.replace(DescriptionTitles.lair_actions.value, "")

                case DescriptionTitles.lair.value:
                    lair = description_node.text.replace(DescriptionTitles.lair.value, "")

                case DescriptionTitles.description.value:
                    description += description_node.text.replace(DescriptionTitles.description.value, "")

                case DescriptionTitles.areal_effects.value:
                    description += description_node.text.replace(DescriptionTitles.areal_effects.value, "")

    print(
        "actions", actions,
        "legendary_resistance", legendary_resistance,
        "bonus_actions", bonus_actions,
        "reactions", reactions,
        "legendary_actions", legendary_actions,
        "mythic_actions", mythic_actions,
        "lair_actions", lair_actions,
        "lair", lair,
        "description", description,
    )

    # TODO Обернуть все поля в класс карточки существа, добавить ссылку на страницу существа

    print("nonmagical_slashing:", nonmagical_slashing,
          "silver_slashing:", silver_slashing,
          "adamntine_slashing:", adamntine_slashing,
          "magical_slashing:", magical_slashing,
          "nonmagical_piercing:", nonmagical_piercing,
          "silver_piercing:", silver_piercing,
          "adamntine_piercing:", adamntine_piercing,
          "magical_piercing:", magical_piercing,
          "nonmagical_bludgeoning:", nonmagical_bludgeoning,
          "silver_bludgeoning:", silver_bludgeoning,
          "adamntine_bludgeoning:", adamntine_bludgeoning,
          "magical_bludgeoning:", magical_bludgeoning,
          "acid:", acid,
          "cold:", cold,
          "fire:", fire,
          "force:", force,
          "lightning:", lightning,
          "necrotic:", necrotic,
          "poison:", poison,
          "psychic:", psychic,
          "radiant:", radiant,
          "thunder:", thunder, )
    print(
        "unconscious:",unconscious,
        "frightened:",frightened,
        "invisible:",invisible,
        "incapacitated:",incapacitated,
        "deafened:",deafened,
        "petrified:",petrified,
        "restrained:",restrained,
        "blinded:",blinded,
        "poisoned:",poisoned,
        "charmed:",charmed,
        "stunned:",stunned,
        "paralyzed:",paralyzed,
        "prone:",prone,
        "grappled:",grappled,
        "exhausted:",exhausted)

    print("habitat", habitat)
    print("telepathy", telepathy)


# scrape_bestiary_table(base_url+bestiary_url)
scrape_beast_info("https://dnd.su/bestiary/30-aarakocra/")
# scrape_beast_info("https://dnd.su/bestiary/5519-aspect_of_tiamat/")

# # Replace 'num_pages' with the number of pages you want to scrape
# num_pages = 10
# dataset = scrape_all_reviews(product_id, num_pages)
# df = pd.DataFrame(dataset)
# df.to_csv('amazon_reviews.csv', index=False)

# scrape_beast_info(test_html3)

# test = [
# "Средний? рой крошечных Конструктов, любое мировоззрение",
# "Средняя? Нежить, законно-злая",
# "Средний? рой крошечных Зверей, без мировоззрения",
# "Средний? рой крошечных Зверей",
# "Маленький? или Средний? Гуманоид, нейтрально-злой",
# "Громадный? Дракон (цветной), хаотично-злой",
# "Маленький? или Средний? Гуманоид (любой расы), хаотично-нейтральный",
# "Маленький? Гуманоид (человек, перевертыш), хаотично-нейтральный",
# "Маленький? Гуманоид (человек, перевертыш)"
# ]