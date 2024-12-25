from Scraper.enumerators import DamageSusceptibilityTypes


class InfoCard:
    def __init__(self, url):
        self.url = url                           # TEXT NOT NULL

        self.name = None                         # TEXT NOT NULL,
        self.name_translated = None              # TEXT NOT NULL,

        self.name_uppercase = None               # TEXT NOT NULL,
        self.name_translated_uppercase = None    # TEXT NOT NULL,

        self.size = None                     # (string) int fkey not null, from table creature_sizes
        self.type_ = None                    # (string) int fkey not null, from table creature_types
        self.alignment = None                # (string) int fkey not null, from table creature_alignments
        self.is_named = None                 # int (bool) not null

        self.armor_class = None              # int not null
        self.armor_class_type = None         # (string) int fkey not null, from table creature_types

        self.average_hitpoints = None        # int not null
        self.hit_die_type = None             # INTEGER NOT NULL CHECK(hit_die_type > 0),
        self.hit_dice = None                 # INTEGER NOT NULL CHECK(hit_dice > 0),
        self.hitpoints_bonus = None          # INTEGER NOT NULL,

        self.walking_speed = None            # INTEGER,
        self.flying_speed = None             # INTEGER,
        self.swimming_speed = None           # INTEGER,
        self.digging_speed = None            # INTEGER,
        self.climbing_speed = None           # INTEGER,

        self.strength = None                 # INTEGER NOT NULL CHECK(strength > 0 AND strength <= 30),
        self.strength_modifier = None        # INTEGER NOT NULL CHECK(strength_modifier >= -5 AND strength_modifier <= 10),
        self.dexterity = None                # INTEGER NOT NULL CHECK(dexterity > 0 AND dexterity <= 30),
        self.dexterity_modifier = None       # INTEGER NOT NULL CHECK(dexterity_modifier >= -5 AND dexterity_modifier <= 10),
        self.constitution = None             # INTEGER NOT NULL CHECK(constitution > 0 AND constitution <= 30),
        self.constitution_modifier = None    # INTEGER NOT NULL CHECK(constitution_modifier >= -5 AND constitution_modifier <= 10),
        self.intelligence = None             # INTEGER NOT NULL CHECK(intelligence > 0 AND intelligence <= 30),
        self.intelligence_modifier = None    # INTEGER NOT NULL CHECK(intelligence_modifier >= -5 AND intelligence_modifier <= 10),
        self.wisdom = None                   # INTEGER NOT NULL CHECK(wisdom > 0 AND wisdom <= 30),
        self.wisdom_modifier = None          # INTEGER NOT NULL CHECK(wisdom_modifier >= -5 AND wisdom_modifier <= 10),
        self.charisma = None                 # INTEGER NOT NULL CHECK(charisma > 0 AND charisma <= 30),
        self.charisma_modifier = None        # INTEGER NOT NULL CHECK(charisma_modifier >= -5 AND charisma_modifier <= 10),

        self.strength_saving_throw = None        # INTEGER NOT NULL CHECK(strength_saving_throw >= -5 AND strength_saving_throw <= 19),
        self.dexterity_saving_throw = None       # INTEGER NOT NULL CHECK(strength_saving_throw >= -5 AND strength_saving_throw <= 19),
        self.constitution_saving_throw = None    # INTEGER NOT NULL CHECK(strength_saving_throw >= -5 AND strength_saving_throw <= 19),
        self.intelligence_saving_throw = None    # INTEGER NOT NULL CHECK(strength_saving_throw >= -5 AND strength_saving_throw <= 19),
        self.wisdom_saving_throw = None          # INTEGER NOT NULL CHECK(strength_saving_throw >= -5 AND strength_saving_throw <= 19),
        self.charisma_saving_throw = None        # INTEGER NOT NULL CHECK(strength_saving_throw >= -5 AND strength_saving_throw <= 19),
        self.strength_saving_throw = None        # INTEGER NOT NULL CHECK(strength_saving_throw >= -5 AND strength_saving_throw <= 19),

        self.acrobatics = None                   # INTEGER NOT NULL CHECK(acrobatics >= -5 AND acrobatics <= 28),
        self.animal_handling = None              # INTEGER NOT NULL CHECK(animal_handling >= -5 AND animal_handling <= 28),
        self.arcana = None                       # INTEGER NOT NULL CHECK(arcana >= -5 AND arcana <= 28),
        self.athletics = None                    # INTEGER NOT NULL CHECK(athletics >= -5 AND athletics <= 28),
        self.deception = None                    # INTEGER NOT NULL CHECK(deception >= -5 AND deception <= 28),
        self.history = None                      # INTEGER NOT NULL CHECK(history >= -5 AND history <= 28),
        self.insight = None                      # INTEGER NOT NULL CHECK(insight >= -5 AND insight <= 28),
        self.intimidation = None                 # INTEGER NOT NULL CHECK(intimidation >= -5 AND intimidation <= 28),
        self.investigation = None                # INTEGER NOT NULL CHECK(investigation >= -5 AND investigation <= 28),
        self.medicine = None                     # INTEGER NOT NULL CHECK(medicine >= -5 AND medicine <= 28),
        self.nature = None                       # INTEGER NOT NULL CHECK(nature >= -5 AND nature <= 28),
        self.perception = None                   # INTEGER NOT NULL CHECK(perception >= -5 AND perception <= 28),
        self.performance = None                  # INTEGER NOT NULL CHECK(performance >= -5 AND performance <= 28),
        self.persuasion = None                   # INTEGER NOT NULL CHECK(persuasion >= -5 AND persuasion <= 28),
        self.religion = None                     # INTEGER NOT NULL CHECK(religion >= -5 AND religion <= 28),
        self.sleight_of_hand = None              # INTEGER NOT NULL CHECK(sleight_of_hand >= -5 AND sleight_of_hand <= 28),
        self.stealth = None                      # INTEGER NOT NULL CHECK(stealth >= -5 AND stealth <= 28),
        self.survival = None                     # INTEGER NOT NULL CHECK(survival >= -5 AND survival <= 28),
        self.passive_perception = None           # INTEGER NOT NULL CHECK(passive_perception >= 5 AND passive_perception <= 38),


        self.darkvision = None                # INTEGER,
        self.blindsight = None                # INTEGER,
        self.truesight = None                 # INTEGER,
        self.tremorsense = None               # INTEGER,
        self.telepathy = 0                    # INTEGER NOT NULL,

        self.nonmagical_slashing = DamageSusceptibilityTypes.normal.value          # INTEGER NOT NULL,
        self.silver_slashing = DamageSusceptibilityTypes.normal.value              # INTEGER NOT NULL,
        self.adamntine_slashing = DamageSusceptibilityTypes.normal.value           # INTEGER NOT NULL,
        self.magical_slashing = DamageSusceptibilityTypes.normal.value             # INTEGER NOT NULL,
        self.nonmagical_piercing = DamageSusceptibilityTypes.normal.value          # INTEGER NOT NULL,
        self.silver_piercing = DamageSusceptibilityTypes.normal.value              # INTEGER NOT NULL,
        self.adamntine_piercing = DamageSusceptibilityTypes.normal.value           # INTEGER NOT NULL,
        self.magical_piercing = DamageSusceptibilityTypes.normal.value             # INTEGER NOT NULL,
        self.nonmagical_bludgeoning = DamageSusceptibilityTypes.normal.value       # INTEGER NOT NULL,
        self.silver_bludgeoning = DamageSusceptibilityTypes.normal.value           # INTEGER NOT NULL,
        self.adamntine_bludgeoning = DamageSusceptibilityTypes.normal.value        # INTEGER NOT NULL,
        self.magical_bludgeoning = DamageSusceptibilityTypes.normal.value          # INTEGER NOT NULL,

        self.acid = DamageSusceptibilityTypes.normal.value                         # INTEGER NOT NULL,
        self.cold = DamageSusceptibilityTypes.normal.value                         # INTEGER NOT NULL,
        self.fire = DamageSusceptibilityTypes.normal.value                         # INTEGER NOT NULL,
        self.force = DamageSusceptibilityTypes.normal.value                        # INTEGER NOT NULL,
        self.lightning = DamageSusceptibilityTypes.normal.value                    # INTEGER NOT NULL,
        self.necrotic = DamageSusceptibilityTypes.normal.value                     # INTEGER NOT NULL,
        self.poison = DamageSusceptibilityTypes.normal.value                       # INTEGER NOT NULL,
        self.psychic = DamageSusceptibilityTypes.normal.value                      # INTEGER NOT NULL,
        self.radiant = DamageSusceptibilityTypes.normal.value                      # INTEGER NOT NULL,
        self.thunder = DamageSusceptibilityTypes.normal.value                      # INTEGER NOT NULL,

        self.unconscious_immunity = False         # INTEGER NOT NULL,
        self.frightened_immunity = False          # INTEGER NOT NULL,
        self.invisible_immunity = False           # INTEGER NOT NULL,
        self.incapacitated_immunity = False       # INTEGER NOT NULL,
        self.deafened_immunity = False            # INTEGER NOT NULL,
        self.petrified_immunity = False           # INTEGER NOT NULL,
        self.restrained_immunity = False          # INTEGER NOT NULL,
        self.blinded_immunity = False             # INTEGER NOT NULL,
        self.poisoned_immunity = False            # INTEGER NOT NULL,
        self.charmed_immunity = False             # INTEGER NOT NULL,
        self.stunned_immunity = False             # INTEGER NOT NULL,
        self.paralyzed_immunity = False           # INTEGER NOT NULL,
        self.prone_immunity = False               # INTEGER NOT NULL,
        self.grappled_immunity = False            # INTEGER NOT NULL,


        self.cr = None                           # INTEGER NOT NULL CHECK (cr >= 0 AND cr <= 30),
        self.proficiency_bonus = None            # INTEGER NOT NULL CHECK(proficiency_bonus >= 2 AND proficiency_bonus <= 9),

        self.source = None                       # INTEGER NOT NULL,

        self.legendary_resistance = None         # INTEGER,
        self.habitat = None                      # TEXT,
        self.actions = None                      # TEXT NOT NULL,
        self.bonus_actions = None                # TEXT,
        self.reactions = None                    # TEXT,
        self.legendary_actions = None            # TEXT,
        self.mythic_actions = None               # TEXT,
        self.lair_actions = None                 # TEXT,
        self.description = None                  # TEXT,
        self.properties = None                   # TEXT,

