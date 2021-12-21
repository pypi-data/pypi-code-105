from case import uppercase_to_pascalcase

class Biome:
    # might be outdated
    def __init__(self, biome: int):
        names = {
            0: {
                "name": " Ocean",
                "name_id": "ocean"
            },
            1: {
                "name": " Plains",
                "name_id": "plains"
            },
            2: {
                "name": " Desert",
                "name_id": "desert"
            },
            3: {
                "name": " Windswept Hills",
                "name_id": "windswept_hills"
            },
            4: {
                "name": " Forest",
                "name_id": "forest"
            },
            5: {
                "name": " Taiga",
                "name_id": "taiga"
            },
            6: {
                "name": " Swamp",
                "name_id": "swampland"
            },
            7: {
                "name": " River",
                "name_id": "river"
            },
            8: {
                "name": " Nether Wastes",
                "name_id": "hell"
            },
            9: {
                "name": " The End",
                "name_id": "the_end"
            },
            10: {
                "name": " Frozen Ocean",
                "name_id": "frozen_ocean"
            },
            11: {
                "name": " Frozen River",
                "name_id": "frozen_river"
            },
            12: {
                "name": " Snowy Plains",
                "name_id": "ice_plains"
            },
            13: {
                "name": " Snowy Mountains",
                "name_id": "ice_mountains"
            },
            14: {
                "name": " Mushroom Fields",
                "name_id": "mushroom_island"
            },
            15: {
                "name": " Mushroom Field Shore",
                "name_id": "mushroom_island_shore"
            },
            16: {
                "name": " Beach",
                "name_id": "beach"
            },
            17: {
                "name": " Desert Hills",
                "name_id": "desert_hills"
            },
            18: {
                "name": " Wooded Hills",
                "name_id": "forest_hills"
            },
            19: {
                "name": " Taiga Hills",
                "name_id": "taiga_hills"
            },
            20: {
                "name": " Mountain Edge",
                "name_id": "extreme_hills_edge"
            },
            21: {
                "name": " Jungle",
                "name_id": "jungle"
            },
            22: {
                "name": " Jungle Hills",
                "name_id": "jungle_hills"
            },
            23: {
                "name": " Jungle Edge",
                "name_id": "jungle_edge"
            },
            24: {
                "name": " Deep Ocean",
                "name_id": "deep_ocean"
            },
            25: {
                "name": " Stony Shore",
                "name_id": "stone_beach"
            },
            26: {
                "name": " Snowy Beach",
                "name_id": "cold_beach"
            },
            27: {
                "name": " Birch Forest",
                "name_id": "birch_forest"
            },
            28: {
                "name": " Birch Forest Hills",
                "name_id": "birch_forest_hills"
            },
            29: {
                "name": " Dark Forest",
                "name_id": "roofed_forest"
            },
            30: {
                "name": " Snowy Taiga",
                "name_id": "cold_taiga"
            },
            31: {
                "name": " Snowy Taiga Hills",
                "name_id": "cold_taiga_hills"
            },
            32: {
                "name": " Old Growth Pine Taiga",
                "name_id": "mega_taiga"
            },
            33: {
                "name": " Giant Tree Taiga Hills",
                "name_id": "mega_taiga_hills"
            },
            34: {
                "name": " Windswept Forest",
                "name_id": "windswept_forest"
            },
            35: {
                "name": " Savanna",
                "name_id": "savanna"
            },
            36: {
                "name": " Savanna Plateau",
                "name_id": "savanna_plateau"
            },
            37: {
                "name": " Badlands",
                "name_id": "mesa"
            },
            38: {
                "name": " Badlands Plateau",
                "name_id": "mesa_plateau"
            },
            39: {
                "name": " Wooded Badlands Plateau",
                "name_id": "mesa_plateau_stone"
            },
            40: {
                "name": " Warm Ocean",
                "name_id": "warm_ocean"
            },
            41: {
                "name": " Lukewarm Ocean",
                "name_id": "lukewarm_ocean"
            },
            42: {
                "name": " Cold Ocean",
                "name_id": "cold_ocean"
            },
            43: {
                "name": " Deep Warm Ocean",
                "name_id": "deep_warm_ocean"
            },
            44: {
                "name": " Deep Lukewarm Ocean",
                "name_id": "deep_lukewarm_ocean"
            },
            45: {
                "name": " Deep Cold Ocean",
                "name_id": "deep_cold_ocean"
            },
            46: {
                "name": " Deep Frozen Ocean",
                "name_id": "deep_frozen_ocean"
            },
            47: {
                "name": " Legacy Frozen Ocean",
                "name_id": "legacy_frozen_ocean"
            },
            129: {
                "name": " Sunflower Plains",
                "name_id": "sunflower_plains"
            },
            130: {
                "name": " Desert Lakes",
                "name_id": "desert_mutated"
            },
            131: {
                "name": " Windswept Gravelly Hills",
                "name_id": "windswept_gravelly_hills"
            },
            132: {
                "name": " Flower Forest",
                "name_id": "flower_forest"
            },
            133: {
                "name": " Taiga Mountains",
                "name_id": "taiga_mutated"
            },
            134: {
                "name": " Swamp Hills",
                "name_id": "swampland_mutated"
            },
            140: {
                "name": " Ice Spikes",
                "name_id": "ice_plains_spikes"
            },
            149: {
                "name": " Modified Jungle",
                "name_id": "jungle_mutated"
            },
            151: {
                "name": " Modified Jungle Edge",
                "name_id": "jungle_edge_mutated"
            },
            155: {
                "name": " Old Growth Birch Forest",
                "name_id": "birch_forest_mutated"
            },
            156: {
                "name": " Tall Birch Hills",
                "name_id": "birch_forest_hills_mutated"
            },
            157: {
                "name": " Dark Forest Hills",
                "name_id": "roofed_forest_mutated"
            },
            158: {
                "name": " Snowy Taiga Mountains",
                "name_id": "cold_taiga_mutated"
            },
            160: {
                "name": " Old Growth Spruce Taiga",
                "name_id": "redwood_taiga_mutated"
            },
            161: {
                "name": " Giant Spruce Taiga Hills",
                "name_id": "redwood_taiga_hills_mutated"
            },
            162: {
                "name": " Gravelly Mountains+",
                "name_id": "extreme_hills_plus_trees_mutated"
            },
            163: {
                "name": " Windswept Savanna",
                "name_id": "savanna_mutated"
            },
            164: {
                "name": " Shattered Savanna Plateau",
                "name_id": "savanna_plateau_mutated"
            },
            165: {
                "name": " Eroded Badlands",
                "name_id": "mesa_bryce"
            },
            166: {
                "name": " Modified Badlands Plateau",
                "name_id": "mesa_plateau_mutated"
            },
            167: {
                "name": " Modified Wooded Badlands Plateau",
                "name_id": "mesa_plateau_stone_mutated"
            },
            168: {
                "name": " Bamboo Jungle",
                "name_id": "bamboo_jungle"
            },
            169: {
                "name": " Bamboo Jungle Hills",
                "name_id": "bamboo_jungle_hills"
            },
            178: {
                "name": " Soul Sand Valley",
                "name_id": "soulsand_valley"
            },
            179: {
                "name": " Crimson Forest",
                "name_id": "crimson_forest"
            },
            180: {
                "name": " Warped Forest",
                "name_id": "warped_forest"
            },
            181: {
                "name": " Basalt Deltas",
                "name_id": "basalt_deltas"
            },
            182: {
                "name": " Jagged Peaks",
                "name_id": "jagged_peaks"
            },
            183: {
                "name": " Frozen Peaks",
                "name_id": "frozen_peaks"
            },
            184: {
                "name": " Snowy Slopes",
                "name_id": "snowy_slopes"
            },
            185: {
                "name": " Grove",
                "name_id": "grove"
            },
            186: {
                "name": " Meadow",
                "name_id": "meadow"
            },
            187: {
                "name": " Lush Caves",
                "name_id": "lush_caves"
            },
            188: {
                "name": " Dripstone Caves",
                "name_id": "dripstone_caves"
            },
            189: {
                "name": " Stony Peaks",
                "name_id": "stony_peaks"
            }
        }
        self.name = names[biome]["name"]
        self.name_id = names[biome]["name_id"]
        self.id = biome
    
    def __int__(self) -> int:
        return self.id
    
    def __str__(self) -> str:
        return self.name
    
    def __in__(self, other) -> bool:
        if isinstance(other, int):
            return self.id == other
        
        if isinstance(other, str):
            return other in (self.name, self.name_id)

class Difficulty:
    def __init__(self, difficulty):
        names = {
            "PEACEFUL": {
                "short": "p",
                "name": "peaceful",
                "id": 0
            },
            "EASY": {
                "short": "e",
                "name": "easy",
                "id": 1
            },
            "NORMAL": {
                "short": "n",
                "name": "normal",
                "id": 2
            },
            "HARD": {
                "short": "h",
                "name": "hard",
                "id": 3
            }
        }
        self.short = names[difficulty]["short"]
        self.name = names[difficulty]["name"]
        self.id = names[difficulty]["id"]
    
    def __int__(self) -> int:
        return self.id
    
    def __str__(self) -> str:
        return self.name
    
    def __in__(self, other) -> bool:
        if isinstance(other, int):
            return self.id == other
        
        if isinstance(other, str):
            return other in (self.short, self.name)

class Gamemode:
    def __init__(self, gamemode: int):
        names = (
            {
                "short": "s",
                "name": "survival",
                "id": 0
            },
            {
                "short": "c",
                "name": "creative",
                "id": 1
            },
            {
                "short": "a",
                "name": "adventure",
                "id": 2
            },
        )
        self.short = names[gamemode]["short"]
        self.name = names[gamemode]["name"]
        self.id = names[gamemode]["id"]
    
    def __int__(self) -> int:
        return self.id
    
    def __str__(self) -> str:
        return self.name
    
    def __in__(self, other) -> bool:
        if isinstance(other, int):
            return self.id == other
        
        if isinstance(other, str):
            return other in (self.short, self.name)