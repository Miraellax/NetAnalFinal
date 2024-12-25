import requests
from bs4 import BeautifulSoup
import re
import pymorphy3
import pandas as pd

from Scraper.InfoCard import InfoCard
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
    # Создание объекта карточки существа
    info_card = InfoCard(url)

    # headers = {}
    # response = requests.get(url, headers=headers)
    # soup = BeautifulSoup(response.content, 'html.parser')

    # TODO заменить на запрос страницы, сейчас тест на скачанной
    with open(url, encoding="utf-8") as fp:
        soup = BeautifulSoup(fp, 'html.parser')

        name = soup.find("h2", class_="card-title").find("span").text
        name_split = re.split(r'\[|\]', name)
        ru_name, en_name = name_split[0], name_split[1]
        ru_name_upper = ru_name.upper()
        en_name_upper = en_name.upper()

        # Заполнение параметров
        info_card.name = ru_name
        info_card.name_translated = en_name
        info_card.name_uppercase = ru_name_upper
        info_card.name_translated_uppercase = en_name_upper

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

        # Нормализация размера, типа и мировоззрения
        if size is not None:
            size = morph.parse(size)[0].normal_form
        if b_type is not None:
            b_type = morph.parse(b_type)[0].normal_form
        if alignment is not None:
            alignment = morph.parse(alignment)[0].normal_form

        # Заполнение параметров
        info_card.size = size
        info_card.type_ = b_type
        info_card.alignment = alignment
        info_card.is_named = named

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

                        # Заполнение параметров
                        info_card.strength = strength_value
                        info_card.strength_modifier = strength_mod

                    case KeyAbilities.dexterity.value:
                        sp = node.text.split(" ")
                        dexterity_value = int(sp[0][3:])
                        dexterity_mod = int(sp[1][1:-1])

                        # Заполнение параметров
                        info_card.dexterity = dexterity_value
                        info_card.dexterity_modifier = dexterity_mod

                    case KeyAbilities.constitution.value:
                        sp = node.text.split(" ")
                        constitution_value = int(sp[0][3:])
                        constitution_mod = int(sp[1][1:-1])

                        # Заполнение параметров
                        info_card.constitution = constitution_value
                        info_card.constitution_modifier = constitution_mod

                    case KeyAbilities.intelligence.value:
                        sp = node.text.split(" ")
                        intelligence_value = int(sp[0][3:])
                        intelligence_mod = int(sp[1][1:-1])

                        # Заполнение параметров
                        info_card.intelligence = intelligence_value
                        info_card.intelligence_modifier = intelligence_mod

                    case KeyAbilities.wisdom.value:
                        sp = node.text.split(" ")
                        wisdom_value = int(sp[0][3:])
                        wisdom_mod = int(sp[1][1:-1])

                        # Заполнение параметров
                        info_card.wisdom = wisdom_value
                        info_card.wisdom_modifier = wisdom_mod

                    case KeyAbilities.charisma.value:
                        sp = node.text.split(" ")
                        charisma_value = int(sp[0][3:])
                        charisma_mod = int(sp[1][1:-1])

                        # Заполнение параметров
                        info_card.charisma = charisma_value
                        info_card.charisma_modifier = charisma_mod
        else: # Без навыков
            # Заполнение параметров
            info_card.strength = 0
            info_card.strength_modifier = 0
            info_card.dexterity = 0
            info_card.dexterity_modifier = 0
            info_card.constitution = 0
            info_card.constitution_modifier = 0
            info_card.intelligence = 0
            info_card.intelligence_modifier = 0
            info_card.wisdom = 0
            info_card.wisdom_modifier = 0
            info_card.charisma = 0
            info_card.charisma_modifier = 0

        # Обработка строк без класса по ключевым словам в теге <strong>
        for item in li_items_no_class:
            match item.find("strong").text:
                case KeyWords.armor_class.value:
                    # Берем всю строку, так как "обсидианово-кремневые латы дракона, щит" / "природный доспех"
                    armor_class = int(item.text.split(" ")[2])
                    sp = re.findall(r"(?<=\().*(?=\))", item.text)
                    if len(sp) > 0:
                        armor_class_type = sp[0]
                    else:
                        armor_class_type = ""

                    # Заполнение параметров
                    info_card.armor_class = armor_class
                    info_card.armor_class_type = armor_class_type

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

                    # Заполнение параметров
                    info_card.average_hitpoints = average_hitpoints
                    info_card.hit_dice = hit_dice
                    info_card.hit_die_type = hit_die_type
                    info_card.hitpoints_bonus = hitpoints_bonus

                case KeyWords.speed.value:
                    # Скорость 30 футов (40 футов в облике кабана) - удаляем то, что в скобках, так как нет возможности сохранить
                    speed_text = re.sub(r"\(.*\)", "", item.text)
                    speed_text = speed_text.split(",")
                    for speed in speed_text:
                        sp = speed.lower().strip().split(" ")
                        if SpeedTypes.swimming.value in sp:
                            info_card.swimming_speed = int(sp[-2])
                        elif SpeedTypes.flying.value in sp:
                            info_card.flying_speed = int(sp[-2])
                        elif SpeedTypes.climbing.value in sp:
                            info_card.climbing_speed = int(sp[-2])
                        elif SpeedTypes.digging.value in sp:
                            info_card.digging_speed = int(sp[-2])
                        else:
                            info_card.walking_speed = int(sp[-2])

                # !!! Перед обработкой спасов должны быть собраны значения статов для расчетов !!!
                case KeyWords.saving_throws.value:

                    # Считывание спасбросков из карточки
                    sp = item.text.replace(KeyWords.saving_throws.value, "").strip().split(", ")
                    for save in sp:
                        s_sp = save.split(" ")
                        match s_sp[0]:
                            case KeyAbilitiesShort.strength.value:
                                info_card.strength_saving_throw = int(s_sp[1])

                            case KeyAbilitiesShort.dexterity.value:
                                info_card.dexterity_saving_throw = int(s_sp[1])

                            case KeyAbilitiesShort.constitution.value:
                                info_card.constitution_saving_throw = int(s_sp[1])

                            case KeyAbilitiesShort.intelligence.value:
                                info_card.intelligence_saving_throw = int(s_sp[1])

                            case KeyAbilitiesShort.wisdom.value:
                                info_card.wisdom_saving_throw = int(s_sp[1])

                            case KeyAbilitiesShort.charisma.value:
                                info_card.charisma_saving_throw = int(s_sp[1])

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
                            info_card.nonmagical_bludgeoning = DamageSusceptibilityTypes.immunity.value
                            if DamageTypes.silver.value not in d_sp:
                                info_card.silver_bludgeoning = DamageSusceptibilityTypes.immunity.value
                            if DamageTypes.adamantine.value not in d_sp:
                                info_card.adamntine_bludgeoning = DamageSusceptibilityTypes.immunity.value
                            if DamageTypes.nonmagical.value not in d_sp:
                                info_card.magical_bludgeoning = DamageSusceptibilityTypes.immunity.value

                        # Рубящий
                        if DamageTypes.slashing.value in d_sp:
                            info_card.nonmagical_slashing = DamageSusceptibilityTypes.immunity.value
                            if DamageTypes.silver.value not in d_sp:
                                info_card.silver_slashing = DamageSusceptibilityTypes.immunity.value
                            if DamageTypes.adamantine.value not in d_sp:
                                info_card.adamntine_slashing = DamageSusceptibilityTypes.immunity.value
                            if DamageTypes.nonmagical.value not in d_sp:
                                info_card.magical_slashing = DamageSusceptibilityTypes.immunity.value

                        # Колющий
                        if DamageTypes.piercing.value in d_sp:
                            info_card.nonmagical_piercing = DamageSusceptibilityTypes.immunity.value
                            if DamageTypes.silver.value not in d_sp:
                                info_card.silver_piercing = DamageSusceptibilityTypes.immunity.value
                            if DamageTypes.adamantine.value not in d_sp:
                                info_card.adamntine_piercing = DamageSusceptibilityTypes.immunity.value
                            if DamageTypes.nonmagical.value not in d_sp:
                                info_card.magical_piercing = DamageSusceptibilityTypes.immunity.value

                        if DamageTypes.acid.value in d_sp:
                            info_card.acid = DamageSusceptibilityTypes.immunity.value
                        if DamageTypes.cold.value in d_sp:
                            info_card.cold = DamageSusceptibilityTypes.immunity.value
                        if DamageTypes.fire.value in d_sp:
                            info_card.fire = DamageSusceptibilityTypes.immunity.value
                        if DamageTypes.force.value in d_sp:
                            info_card.force = DamageSusceptibilityTypes.immunity.value
                        if DamageTypes.lightning.value in d_sp:
                            info_card.lightning = DamageSusceptibilityTypes.immunity.value
                        if DamageTypes.necrotic.value in d_sp:
                            info_card.necrotic = DamageSusceptibilityTypes.immunity.value
                        if DamageTypes.poison.value in d_sp:
                            info_card.poison = DamageSusceptibilityTypes.immunity.value
                        if DamageTypes.psychic.value in d_sp:
                            info_card.psychic = DamageSusceptibilityTypes.immunity.value
                        if DamageTypes.radiant.value in d_sp:
                            info_card.radiant = DamageSusceptibilityTypes.immunity.value
                        if DamageTypes.thunder.value in d_sp:
                            info_card.thunder = DamageSusceptibilityTypes.immunity.value

                case KeyWords.damage_vulnerability.value:
                    damage_classes = item.text.replace(KeyWords.damage_immunity.value, "").split(";")

                    # Обработка магических и остальных типов
                    for damage_class in damage_classes:
                        d_sp = re.split(r"[,| ]", damage_class)

                        # Дробящий
                        if DamageTypes.bludgeoning.value in d_sp:
                            info_card.nonmagical_bludgeoning = DamageSusceptibilityTypes.vulnerability.value
                            if DamageTypes.silver.value not in d_sp:
                                info_card.silver_bludgeoning = DamageSusceptibilityTypes.vulnerability.value
                            if DamageTypes.adamantine.value not in d_sp:
                                info_card.adamntine_bludgeoning = DamageSusceptibilityTypes.vulnerability.value
                            if DamageTypes.nonmagical.value not in d_sp:
                                info_card.magical_bludgeoning = DamageSusceptibilityTypes.vulnerability.value

                        # Рубящий
                        if DamageTypes.slashing.value in d_sp:
                            info_card.nonmagical_slashing = DamageSusceptibilityTypes.vulnerability.value
                            if DamageTypes.silver.value not in d_sp:
                                info_card.silver_slashing = DamageSusceptibilityTypes.vulnerability.value
                            if DamageTypes.adamantine.value not in d_sp:
                                info_card.adamntine_slashing = DamageSusceptibilityTypes.vulnerability.value
                            if DamageTypes.nonmagical.value not in d_sp:
                                info_card.magical_slashing = DamageSusceptibilityTypes.vulnerability.value

                        # Колющий
                        if DamageTypes.piercing.value in d_sp:
                            info_card.nonmagical_piercing = DamageSusceptibilityTypes.vulnerability.value
                            if DamageTypes.silver.value not in d_sp:
                                info_card.silver_piercing = DamageSusceptibilityTypes.vulnerability.value
                            if DamageTypes.adamantine.value not in d_sp:
                                info_card.adamntine_piercing = DamageSusceptibilityTypes.vulnerability.value
                            if DamageTypes.nonmagical.value not in d_sp:
                                info_card.magical_piercing = DamageSusceptibilityTypes.vulnerability.value

                        if DamageTypes.acid.value in d_sp:
                            info_card.acid = DamageSusceptibilityTypes.vulnerability.value
                        if DamageTypes.cold.value in d_sp:
                            info_card.cold = DamageSusceptibilityTypes.vulnerability.value
                        if DamageTypes.fire.value in d_sp:
                            info_card.fire = DamageSusceptibilityTypes.vulnerability.value
                        if DamageTypes.force.value in d_sp:
                            info_card.force = DamageSusceptibilityTypes.vulnerability.value
                        if DamageTypes.lightning.value in d_sp:
                            info_card.lightning = DamageSusceptibilityTypes.vulnerability.value
                        if DamageTypes.necrotic.value in d_sp:
                            info_card.necrotic = DamageSusceptibilityTypes.vulnerability.value
                        if DamageTypes.poison.value in d_sp:
                            info_card.poison = DamageSusceptibilityTypes.vulnerability.value
                        if DamageTypes.psychic.value in d_sp:
                            info_card.psychic = DamageSusceptibilityTypes.vulnerability.value
                        if DamageTypes.radiant.value in d_sp:
                            info_card.radiant = DamageSusceptibilityTypes.vulnerability.value
                        if DamageTypes.thunder.value in d_sp:
                            info_card.thunder = DamageSusceptibilityTypes.vulnerability.value

                case KeyWords.damage_resistance.value:
                    damage_classes = item.text.replace(KeyWords.damage_immunity.value, "").split(";")

                    # Обработка магических и остальных типов
                    for damage_class in damage_classes:
                        d_sp = re.split(r"[,| ]", damage_class)

                        # Дробящий
                        if DamageTypes.bludgeoning.value in d_sp:
                            info_card.nonmagical_bludgeoning = DamageSusceptibilityTypes.resistance.value
                            if DamageTypes.silver.value not in d_sp:
                                info_card.silver_bludgeoning = DamageSusceptibilityTypes.resistance.value
                            if DamageTypes.adamantine.value not in d_sp:
                                info_card.adamntine_bludgeoning = DamageSusceptibilityTypes.resistance.value
                            if DamageTypes.nonmagical.value not in d_sp:
                                info_card.magical_bludgeoning = DamageSusceptibilityTypes.resistance.value

                        # Рубящий
                        if DamageTypes.slashing.value in d_sp:
                            info_card.nonmagical_slashing = DamageSusceptibilityTypes.resistance.value
                            if DamageTypes.silver.value not in d_sp:
                                info_card.silver_slashing = DamageSusceptibilityTypes.resistance.value
                            if DamageTypes.adamantine.value not in d_sp:
                                info_card.adamntine_slashing = DamageSusceptibilityTypes.resistance.value
                            if DamageTypes.nonmagical.value not in d_sp:
                                info_card.magical_slashing = DamageSusceptibilityTypes.resistance.value

                        # Колющий
                        if DamageTypes.piercing.value in d_sp:
                            info_card.nonmagical_piercing = DamageSusceptibilityTypes.resistance.value
                            if DamageTypes.silver.value not in d_sp:
                                info_card.silver_piercing = DamageSusceptibilityTypes.resistance.value
                            if DamageTypes.adamantine.value not in d_sp:
                                info_card.adamntine_piercing = DamageSusceptibilityTypes.resistance.value
                            if DamageTypes.nonmagical.value not in d_sp:
                                info_card.magical_piercing = DamageSusceptibilityTypes.resistance.value

                        if DamageTypes.acid.value in d_sp:
                            info_card.acid = DamageSusceptibilityTypes.resistance.value
                        if DamageTypes.cold.value in d_sp:
                            info_card.cold = DamageSusceptibilityTypes.resistance.value
                        if DamageTypes.fire.value in d_sp:
                            info_card.fire = DamageSusceptibilityTypes.resistance.value
                        if DamageTypes.force.value in d_sp:
                            info_card.force = DamageSusceptibilityTypes.resistance.value
                        if DamageTypes.lightning.value in d_sp:
                            info_card.lightning = DamageSusceptibilityTypes.resistance.value
                        if DamageTypes.necrotic.value in d_sp:
                            info_card.necrotic = DamageSusceptibilityTypes.resistance.value
                        if DamageTypes.poison.value in d_sp:
                            info_card.poison = DamageSusceptibilityTypes.resistance.value
                        if DamageTypes.psychic.value in d_sp:
                            info_card.psychic = DamageSusceptibilityTypes.resistance.value
                        if DamageTypes.radiant.value in d_sp:
                            info_card.radiant = DamageSusceptibilityTypes.resistance.value
                        if DamageTypes.thunder.value in d_sp:
                            info_card.thunder = DamageSusceptibilityTypes.resistance.value

                case KeyWords.condition_immunity.value:
                    condition_types = item.text.replace(KeyWords.condition_immunity.value, "").split(",")
                    for c_type in condition_types:
                        c_type = c_type.replace("?", "").strip()
                        match c_type:
                            case ConditionImmunityTypes.unconscious.value:
                                info_card.unconscious_immunity = True
                            case ConditionImmunityTypes.frightened.value:
                                info_card.frightened_immunity = True
                            case ConditionImmunityTypes.invisible.value:
                                info_card.invisible_immunity = True
                            case ConditionImmunityTypes.incapacitated.value:
                                info_card.incapacitated_immunity = True
                            case ConditionImmunityTypes.deafened.value:
                                info_card.deafened_immunity = True
                            case ConditionImmunityTypes.petrified.value:
                                info_card.petrified_immunity = True
                            case ConditionImmunityTypes.restrained.value:
                                info_card.restrained_immunity = True
                            case ConditionImmunityTypes.blinded.value:
                                info_card.blinded_immunity = True
                            case ConditionImmunityTypes.poisoned.value:
                                info_card.poisoned_immunity = True
                            case ConditionImmunityTypes.charmed.value:
                                info_card.charmed_immunity = True
                            case ConditionImmunityTypes.stunned.value:
                                info_card.stunned_immunity = True
                            case ConditionImmunityTypes.paralyzed.value:
                                info_card.paralyzed_immunity = True
                            case ConditionImmunityTypes.prone.value:
                                info_card.prone_immunity = True
                            case ConditionImmunityTypes.grappled.value:
                                info_card.grappled_immunity = True
                            case ConditionImmunityTypes.exhausted.value:
                                info_card.exhausted_immunity = True

                case KeyWords.senses.value:

                    sp = item.text.replace(KeyWords.senses.value, "").strip().split(",")
                    for sense in sp:
                        if SenseTypes.passive_perception.value in sense:
                            info_card.passive_perception = int(sense.split(" ")[-1])

                        elif SenseTypes.darkvision.value in sense:
                            info_card.darkvision = int(sense.split(" ")[-2])

                        elif SenseTypes.blindsight.value in sense:
                            info_card.blindsight = int(sense.split(" ")[-2])

                        elif SenseTypes.truesight.value in sense:
                            info_card.truesight = int(sense.split(" ")[-2])

                        elif SenseTypes.tremorsense.value in sense:
                            info_card.tremorsense = int(sense.split(" ")[-2])

                case KeyWords.languages.value:
                    # Проверка на наличие Телепатии
                    sp = item.text.split(" ")
                    if SenseTypes.telepathy.value in item.text:
                        telepathy_index = sp.index(SenseTypes.telepathy.value)
                        if telepathy_index != -1:
                            telepathy = int(sp[telepathy_index+1])

                case KeyWords.challenge_rating.value:
                    # TODO поменять на хранение строки в БД
                    info_card.cr = item.text.replace(KeyWords.challenge_rating.value, "").strip().split(" ")[0]

                case KeyWords.habitat.value:
                    info_card.habitat = item.text.replace(KeyWords.habitat.value, "").strip()

                case KeyWords.source.value:
                    info_card.source = item.text.replace(KeyWords.source.value, "").strip()

                case _:
                    # Сбор данных о бонусе мастерства
                    sp = item.text.split(" ")
                    if  " ".join(sp[0:2]) == KeyWords.proficiency.value:
                        info_card.proficiency_bonus = int(sp[2])

        # Вычисление спасброска по навыку, если спас не указан в карточке (владения нет)
        if info_card.strength_saving_throw is None:
            info_card.strength_saving_throw = info_card.strength_modifier
        if info_card.dexterity_saving_throw is None:
            info_card.dexterity_saving_throw = info_card.dexterity_modifier
        if info_card.constitution_saving_throw is None:
            info_card.constitution_saving_throw = info_card.constitution_modifier
        if info_card.intelligence_saving_throw is None:
            info_card.intelligence_saving_throw = info_card.intelligence_modifier
        if info_card.wisdom_saving_throw is None:
            info_card.wisdom_saving_throw = info_card.wisdom_modifier
        if info_card.charisma_saving_throw is None:
            info_card.charisma_saving_throw = info_card.charisma_modifier

         # Навыки с владением (указанные)
        if li_skills is not None:
            sk = li_skills.find_all("span", class_="skill-bonus")
            for skill in sk:
                match skill.contents[0].strip():
                    case SkillTypes.acrobatics.value:
                        info_card.acrobatics = int(skill.find("strong", "skill-bonus-value").text)
                    case SkillTypes.animal_handling.value:
                        info_card.animal_handling = int(skill.find("strong", "skill-bonus-value").text)
                    case SkillTypes.arcana.value:
                        info_card.arcana = int(skill.find("strong", "skill-bonus-value").text)
                    case SkillTypes.athletics.value:
                        info_card.athletics = int(skill.find("strong", "skill-bonus-value").text)
                    case SkillTypes.deception.value:
                        info_card.deception = int(skill.find("strong", "skill-bonus-value").text)
                    case SkillTypes.history.value:
                        info_card.history = int(skill.find("strong", "skill-bonus-value").text)
                    case SkillTypes.insight.value:
                        info_card.insight = int(skill.find("strong", "skill-bonus-value").text)
                    case SkillTypes.intimidation.value:
                        info_card.intimidation = int(skill.find("strong", "skill-bonus-value").text)
                    case SkillTypes.investigation.value:
                        info_card.investigation = int(skill.find("strong", "skill-bonus-value").text)
                    case SkillTypes.medicine.value:
                        info_card.medicine = int(skill.find("strong", "skill-bonus-value").text)
                    case SkillTypes.nature.value:
                        info_card.nature = int(skill.find("strong", "skill-bonus-value").text)
                    case SkillTypes.perception.value:
                        info_card.perception = int(skill.find("strong", "skill-bonus-value").text)
                    case SkillTypes.performance.value:
                        info_card.performance = int(skill.find("strong", "skill-bonus-value").text)
                    case SkillTypes.persuasion.value:
                        info_card.persuasion = int(skill.find("strong", "skill-bonus-value").text)
                    case SkillTypes.religion.value:
                        info_card.religion = int(skill.find("strong", "skill-bonus-value").text)
                    case SkillTypes.sleight_of_hand.value:
                        info_card.sleight_of_hand = int(skill.find("strong", "skill-bonus-value").text)
                    case SkillTypes.stealth.value:
                        info_card.acrobatics = int(skill.find("strong", "skill-bonus-value").text)
                    case SkillTypes.survival.value:
                        info_card.survival = int(skill.find("strong", "skill-bonus-value").text)
        # Навыки без владения
        if info_card.acrobatics is None:
            info_card.acrobatics = info_card.dexterity_modifier
        if info_card.animal_handling is None:
            info_card.animal_handling = info_card.wisdom_modifier
        if info_card.arcana is None:
            info_card.arcana = info_card.intelligence_modifier
        if info_card.athletics is None:
            info_card.athletics = info_card.strength_modifier
        if info_card.deception is None:
            info_card.deception = info_card.charisma_modifier
        if info_card.history is None:
            info_card.history = info_card.intelligence_modifier
        if info_card.insight is None:
            info_card.insight = info_card.wisdom_modifier
        if info_card.intimidation is None:
            info_card.intimidation = info_card.charisma_modifier
        if info_card.investigation is None:
            info_card.investigation = info_card.intelligence_modifier
        if info_card.medicine is None:
            info_card.medicine = info_card.wisdom_modifier
        if info_card.nature is None:
            info_card.nature = info_card.intelligence_modifier
        if info_card.perception is None:
            info_card.perception = info_card.wisdom_modifier
        if info_card.performance is None:
            info_card.performance = info_card.charisma_modifier
        if info_card.persuasion is None:
            info_card.persuasion = info_card.charisma_modifier
        if info_card.religion is None:
            info_card.religion = info_card.intelligence_modifier
        if info_card.sleight_of_hand is None:
            info_card.sleight_of_hand = info_card.dexterity_modifier
        if info_card.stealth is None:
            info_card.stealth = info_card.dexterity_modifier
        if info_card.survival is None:
            info_card.survival = info_card.wisdom_modifier

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
                info_card.properties = description_node.text
                if (leg_res_index := description_node.text.find(DescriptionTitles.legendary_resistance.value)) != -1:
                    # Легендарное сопротивление (5/день)
                    re_string = fr"(?<={DescriptionTitles.legendary_resistance.value} \()\d+(?=\/.+\))"
                    a = re.findall(re_string, description_node.text)
                    info_card.legendary_resistance = int(a[0])
                else:
                    info_card.legendary_resistance = 0
            else:
                title = description_node.find("h3", "subsection-title").text
                match title:
                    case DescriptionTitles.actions.value:
                        info_card.actions = description_node.text.replace(DescriptionTitles.actions.value, "")

                    case DescriptionTitles.bonus_actions.value:
                        info_card.bonus_actions = description_node.text.replace(DescriptionTitles.bonus_actions.value, "")

                    case DescriptionTitles.reactions.value:
                        info_card.reactions = description_node.text.replace(DescriptionTitles.reactions.value, "")

                    case DescriptionTitles.legendary_actions.value:
                        info_card.legendary_actions = description_node.text.replace(DescriptionTitles.legendary_actions.value, "")

                    case DescriptionTitles.mythic_actions.value:
                        info_card.mythic_actions = description_node.text.replace(DescriptionTitles.mythic_actions.value, "")

                    case DescriptionTitles.lair_actions.value:
                        info_card.lair_actions = description_node.text.replace(DescriptionTitles.lair_actions.value, "")

                    case DescriptionTitles.lair.value:
                        info_card.lair = description_node.text.replace(DescriptionTitles.lair.value, "")

                    case DescriptionTitles.description.value:
                        if info_card.description is None:
                            info_card.description = description_node.text.replace(DescriptionTitles.description.value, "")
                        else:
                            info_card.description += description_node.text.replace(DescriptionTitles.description.value, "")

                    case DescriptionTitles.areal_effects.value:
                        if info_card.description is None:
                            info_card.description = description_node.text.replace(DescriptionTitles.areal_effects.value, "")
                        else:
                            info_card.description += description_node.text.replace(DescriptionTitles.areal_effects.value, "")

    return info_card

# scrape_bestiary_table(base_url+bestiary_url)
# scrape_beast_info("https://dnd.su/bestiary/30-aarakocra/")
# scrape_beast_info("https://dnd.su/bestiary/5519-aspect_of_tiamat/")

# # Replace 'num_pages' with the number of pages you want to scrape
# num_pages = 10
# dataset = scrape_all_reviews(product_id, num_pages)
# df = pd.DataFrame(dataset)
# df.to_csv('amazon_reviews.csv', index=False)

card = scrape_beast_info(test_html4)
for k, v in card.__dict__.items():
    print(f"{k}: {v}")

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