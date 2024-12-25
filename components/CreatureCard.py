import aiosqlite

async def get_creature_card_data(id: int, cursor : aiosqlite.Cursor):
    result = await cursor.execute(
        """
        SELECT
        c.name,
        c.name_translated,
        s.name AS size,
        t.name AS type,
        a.name AS alignment,
        c.cr,
        C.url
        FROM
        creatures AS c
        INNER JOIN
        creature_sizes AS s
            ON s.id = c.size
        INNER JOIN
        creature_types AS t
            ON t.id = c.type
        INNER JOIN
        creature_alignments AS a
            ON t.id = c.alignment
        WHERE c.id = ?
        """,
        (id,)
    )
    return await result.fetchone()


def create_card_markup(dict_like):
    return (
        f"{dict_like["name_translated"]} [{dict_like["name"]}]\n"
        f"{dict_like["size"]} {dict_like["type"]}, {dict_like["alignment"]}\n"
        f"CR: {dict_like["cr"]}\n"
        f"Ссылка на страницу: {dict_like["url"]}"
    )