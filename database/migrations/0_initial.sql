--Первичная миграция
PRAGMA foreign_keys=ON;

CREATE TABLE admins (
    userid INTEGER NOT NULL PRIMARY KEY
);

INSERT INTO admins (userid) VALUES (393113875), (1186226062);

CREATE TABLE creature_sizes (
    id INTEGER NOT NULL PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE creature_types (
    id INTEGER NOT NULL PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE creature_alignments (
    id INTEGER NOT NULL PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE creature_alignments (
    id INTEGER NOT NULL PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE damage_susceptibility (
    id INTEGER NOT NULL PRIMARY KEY,
    name TEXT NOT NULL
);

INSERT INTO damage_susceptibility
(name)
VALUES
("immunity"),
("resistance"),
("normal"),
("vulnerability");

CREATE TABLE creature_sources (
    id INTEGER NOT NULL PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE creatures (
    id INTEGER NOT NULL PRIMARY KEY,
    name TEXT NOT NULL,
    name_translated TEXT NOT NULL,
    size INTEGER NOT NULL,
    type INTEGER NOT NULL,
    alignment INTEGER NOT NULL,
    is_named INTEGER NOT NULL,
    armor_class INTEGER NOT NULL CHECK(armor_class > 0),
    armor_class_type TEXT NOT NULL,
    average_hitpoints INTEGER NOT NULL CHECK(average_hitpoints > 0),
    hit_die_type INTEGER NOT NULL CHECK(hit_die_type > 0),
    hit_dice INTEGER NOT NULL CHECK(hit_dice > 0),
    hitpoints_bonus INTEGER NOT NULL,
    walking_speed INTEGER,
    flying_speed INTEGER,
    swimming_speed INTEGER,
    digging_speed INTEGER,
    climbing_speed INTEGER,
    strength INTEGER NOT NULL CHECK(strength > 0 AND strength <= 30),
    strength_modifier INTEGER NOT NULL CHECK(strength_modifier >= -5 AND strength_modifier <= 10),
    dexterity INTEGER NOT NULL CHECK(dexterity > 0 AND dexterity <= 30),
    dexterity_modifier INTEGER NOT NULL CHECK(dexterity_modifier >= -5 AND dexterity_modifier <= 10),
    constitution INTEGER NOT NULL CHECK(constitution > 0 AND constitution <= 30),
    constitution_modifier INTEGER NOT NULL CHECK(constitution_modifier >= -5 AND constitution_modifier <= 10),
    intelligence INTEGER NOT NULL CHECK(intelligence > 0 AND intelligence <= 30),
    intelligence_modifier INTEGER NOT NULL CHECK(intelligence_modifier >= -5 AND intelligence_modifier <= 10),
    wisdom INTEGER NOT NULL CHECK(wisdom > 0 AND wisdom <= 30),
    wisdom_modifier INTEGER NOT NULL CHECK(wisdom_modifier >= -5 AND wisdom_modifier <= 10),
    charisma INTEGER NOT NULL CHECK(charisma > 0 AND charisma <= 30),
    charisma_modifier INTEGER NOT NULL CHECK(charisma_modifier >= -5 AND charisma_modifier <= 10),
    strength_saving_throw INTEGER NOT NULL CHECK(strength_saving_throw >= -5 AND strength_saving_throw <= 19),
    dexterity_saving_throw INTEGER NOT NULL CHECK(strength_saving_throw >= -5 AND strength_saving_throw <= 19),
    constitution_saving_throw INTEGER NOT NULL CHECK(strength_saving_throw >= -5 AND strength_saving_throw <= 19),
    intelligence_saving_throw INTEGER NOT NULL CHECK(strength_saving_throw >= -5 AND strength_saving_throw <= 19),
    wisdom_saving_throw INTEGER NOT NULL CHECK(strength_saving_throw >= -5 AND strength_saving_throw <= 19),
    charisma_saving_throw INTEGER NOT NULL CHECK(strength_saving_throw >= -5 AND strength_saving_throw <= 19),
    strength_saving_throw INTEGER NOT NULL CHECK(strength_saving_throw >= -5 AND strength_saving_throw <= 19),
    acrobatics INTEGER NOT NULL CHECK(acrobatics >= -5 AND acrobatics <= 28),
    animal_handling INTEGER NOT NULL CHECK(animal_handling >= -5 AND animal_handling <= 28),
    arcana INTEGER NOT NULL CHECK(arcana >= -5 AND arcana <= 28),
    athletics INTEGER NOT NULL CHECK(athletics >= -5 AND athletics <= 28),
    deception INTEGER NOT NULL CHECK(deception >= -5 AND deception <= 28),
    history INTEGER NOT NULL CHECK(history >= -5 AND history <= 28),
    insight INTEGER NOT NULL CHECK(insight >= -5 AND insight <= 28),
    intimidation INTEGER NOT NULL CHECK(intimidation >= -5 AND intimidation <= 28),
    investigation INTEGER NOT NULL CHECK(investigation >= -5 AND investigation <= 28),
    medicine INTEGER NOT NULL CHECK(medicine >= -5 AND medicine <= 28),
    nature INTEGER NOT NULL CHECK(nature >= -5 AND nature <= 28),
    perception INTEGER NOT NULL CHECK(perception >= -5 AND perception <= 28),
    performance INTEGER NOT NULL CHECK(performance >= -5 AND performance <= 28),
    persuation INTEGER NOT NULL CHECK(persuation >= -5 AND persuation <= 28),
    religion INTEGER NOT NULL CHECK(religion >= -5 AND religion <= 28),
    sleight_of_hand INTEGER NOT NULL CHECK(sleight_of_hand >= -5 AND sleight_of_hand <= 28),
    stealth INTEGER NOT NULL CHECK(stealth >= -5 AND stealth <= 28),
    survival INTEGER NOT NULL CHECK(survival >= -5 AND survival <= 28),
    passive_perception INTEGER NOT NULL CHECK(passive_perception >= 5 AND passive_perception <= 38),
    darkvision INTEGER,
    blindsight INTEGER,
    truesight INTEGER,
    tremorsight INTEGER,
    nonmagical_slashing INTEGER NOT NULL,
    silver_slashing INTEGER NOT NULL,
    adamntine_slashing INTEGER NOT NULL,
    magical_slashing INTEGER NOT NULL,
    nonmagical_piercing INTEGER NOT NULL,
    silver_piercing INTEGER NOT NULL,
    adamntine_piercing INTEGER NOT NULL,
    magical_piercing INTEGER NOT NULL,
    nonmagical_bludgeoning INTEGER NOT NULL,
    silver_bludgeoning INTEGER NOT NULL,
    adamntine_bludgeoning INTEGER NOT NULL,
    magical_bludgeoning INTEGER NOT NULL,
    acid INTEGER NOT NULL,
    cold INTEGER NOT NULL,
    fire INTEGER NOT NULL,
    force INTEGER NOT NULL,
    lightning INTEGER NOT NULL,
    necrotic INTEGER NOT NULL,
    poison INTEGER NOT NULL,
    psychic INTEGER NOT NULL,
    radiant INTEGER NOT NULL,
    thunder INTEGER NOT NULL,
    unconscious_immunity INTEGER NOT NULL,
    frightened_immunity INTEGER NOT NULL,
    invisible_immunity INTEGER NOT NULL,
    incapacitated_immunity INTEGER NOT NULL,
    deafened_immunity INTEGER NOT NULL,
    petrified_immunity INTEGER NOT NULL,
    restrained_immunity INTEGER NOT NULL,
    blinded_immunity INTEGER NOT NULL,
    poisoned_immunity INTEGER NOT NULL,
    charmed_immunity INTEGER NOT NULL,
    stunned_immunity INTEGER NOT NULL,
    paralyzed_immunity INTEGER NOT NULL,
    prone_immunity INTEGER NOT NULL,
    grappled_immunity INTEGER NOT NULL,
    telepathy INTEGER NOT NULL,
    cr INTEGER NOT NULL CHECK (cr >= 0 AND cr <= 30),
    source INTEGER NOT NULL,
    proficiency_bonus INTEGER NOT NULL CHECK(proficiency_bonus >= 2 AND proficiency_bonus <= 9),
    legendary_resistance INTEGER,
    actions TEXT NOT NULL,
    bonus_actions TEXT,
    reactions TEXT,
    legendary_actions TEXT,
    mythic_actions TEXT,
    lair_actions TEXT,
    description TEXT

    FOREIGN KEY (size) REFERENCES creature_sizes(id),
    FOREIGN KEY (type) REFERENCES creature_types(id),
    FOREIGN KEY (alignment) REFERENCES creature_alignments(id),
    FOREIGN KEY (nonmagical_slashing) REFERENCES damage_susceptibility(id),
    FOREIGN KEY (silver_slashing) REFERENCES damage_susceptibility(id),
    FOREIGN KEY (adamntine_slashing) REFERENCES damage_susceptibility(id),
    FOREIGN KEY (magical_slashing) REFERENCES damage_susceptibility(id),
    FOREIGN KEY (silver_piercing) REFERENCES damage_susceptibility(id),
    FOREIGN KEY (adamntine_piercing) REFERENCES damage_susceptibility(id),
    FOREIGN KEY (magical_piercing) REFERENCES damage_susceptibility(id),
    FOREIGN KEY (nonmagical_bludgeoning) REFERENCES damage_susceptibility(id),
    FOREIGN KEY (silver_bludgeoning) REFERENCES damage_susceptibility(id),
    FOREIGN KEY (adamntine_bludgeoning) REFERENCES damage_susceptibility(id),
    FOREIGN KEY (magical_bludgeoning) REFERENCES damage_susceptibility(id),
    FOREIGN KEY (acid) REFERENCES damage_susceptibility(id),
    FOREIGN KEY (cold) REFERENCES damage_susceptibility(id),
    FOREIGN KEY (fire) REFERENCES damage_susceptibility(id),
    FOREIGN KEY (force) REFERENCES damage_susceptibility(id),
    FOREIGN KEY (lightning) REFERENCES damage_susceptibility(id),
    FOREIGN KEY (necrotic) REFERENCES damage_susceptibility(id),
    FOREIGN KEY (poison) REFERENCES damage_susceptibility(id),
    FOREIGN KEY (psychic) REFERENCES damage_susceptibility(id),
    FOREIGN KEY (radiant) REFERENCES damage_susceptibility(id),
    FOREIGN KEY (thunder) REFERENCES damage_susceptibility(id),
    FOREIGN KEY (source) REFERENCES creature_sources(id)
);