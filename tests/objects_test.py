from Objects import Hero, Berserk, Blessing, Weakness, Anger
from Settings import ObjectStatistic


class TestObjects:
    __image = "some value for image"
    __statistic = ObjectStatistic(strength=20, endurance=20, intelligence=5, luck=5)
    __default_hero_properties = {
        'fixture': __image,
        'position': [1, 1],
        'stats_strength': __statistic.strength,
        'stats_endurance': __statistic.endurance,
        'stats_intelligence': __statistic.intelligence,
        'stats_luck': __statistic.luck,
        'hp': 45,
        'max_hp': 45,
        'level': 1,
        'exp': 0,
        'next_level_exp': 100,
        'gold': 0
    }

    def test_basic_properties_of_hero(self):
        hero = self.__create_base_hero()
        desired_properties = self.__default_hero_properties

        self.__test_hero_properties(hero, desired_properties)

    def test_level_up_without_enough_exp_nothing_should_be_changed(self):
        hero = self.__create_base_hero()
        hero.exp = 0

        desired_properties = self.__default_hero_properties
        self.__test_hero_properties(hero, desired_properties)

    def test_level_up_with_enough_exp(self):
        hero = self.__create_base_hero()
        hero.exp = 1600
        hero.level_up()

        desired_properties = self.__default_hero_properties.copy()
        desired_properties['level'] = 6
        desired_properties['exp'] = 1600
        desired_properties['next_level_exp'] = 3200
        desired_properties['stats_strength'] = 30
        desired_properties['stats_endurance'] = 30
        desired_properties['hp'] = 65
        desired_properties['max_hp'] = 65

        self.__test_hero_properties(hero, desired_properties)

    def test_hp_setter_hp_less_than_max_hp(self):
        hero = self.__create_base_hero()
        hero.hp = 44

        desired_properties = self.__default_hero_properties.copy()
        desired_properties['hp'] = 44

        self.__test_hero_properties(hero, desired_properties)

    def test_multiple_effects(self):
        hero = self.__create_base_hero()

        # properties of decorator object should be changed but properties of original object shouldn't
        desired_hero_properties = self.__default_hero_properties.copy()
        self.__test_hero_properties(hero, desired_hero_properties)

        # berserk hero
        berserk = Berserk(hero)
        desired_berserk_properties = self.__default_hero_properties.copy()
        desired_berserk_properties['stats_strength'] = 27
        desired_berserk_properties['stats_endurance'] = 27
        desired_berserk_properties['stats_luck'] = 12
        desired_berserk_properties['stats_intelligence'] = 2
        desired_berserk_properties['hp'] = 45
        desired_berserk_properties['max_hp'] = 59
        self.__test_hero_properties(berserk, desired_berserk_properties)

        # blessed berserk hero
        blessed_berserk = Blessing(berserk)
        desired_blessed_berserk_properties = self.__default_hero_properties.copy()
        desired_blessed_berserk_properties['stats_strength'] = 29
        desired_blessed_berserk_properties['stats_endurance'] = 30
        desired_blessed_berserk_properties['stats_luck'] = 16
        desired_blessed_berserk_properties['stats_intelligence'] = 7
        desired_blessed_berserk_properties['hp'] = 45
        desired_blessed_berserk_properties['max_hp'] = 65
        self.__test_hero_properties(blessed_berserk, desired_blessed_berserk_properties)

        # weakened blessed berserk hero
        weakened_blessed_berserk = Weakness(blessed_berserk)
        desired_weakened_blessed_berserk_properties = self.__default_hero_properties.copy()
        desired_weakened_blessed_berserk_properties['stats_strength'] = 25
        desired_weakened_blessed_berserk_properties['stats_endurance'] = 24
        desired_weakened_blessed_berserk_properties['stats_luck'] = 16
        desired_weakened_blessed_berserk_properties['stats_intelligence'] = 5
        desired_weakened_blessed_berserk_properties['hp'] = 45
        desired_weakened_blessed_berserk_properties['max_hp'] = 53
        self.__test_hero_properties(weakened_blessed_berserk, desired_weakened_blessed_berserk_properties)

        assert 'base' not in dir(hero)
        assert berserk.base is hero
        assert blessed_berserk.base is berserk
        assert weakened_blessed_berserk.base is blessed_berserk

    def test_weakness_max_hp_and_hp_should_be_decreased(self):
        hero = self.__create_base_hero()
        weakened_hero = Weakness(hero)

        assert weakened_hero.max_hp == 33, "Maximum health points value wasn't changed after weakness applying"
        assert weakened_hero.hp == 33, "Health points value wasn't changed after weakness applying"

    def test_level_up_and_remove_effect_base_properties_should_be_changed(self):
        hero = self.__create_base_hero()
        angry_hero = Anger(hero)
        angry_hero.exp += 100
        angry_hero.level_up()

        desired_properties_with_effect = self.__default_hero_properties.copy()
        desired_properties_with_effect["stats_strength"] = 32
        desired_properties_with_effect["stats_endurance"] = 37
        desired_properties_with_effect["stats_intelligence"] = 0
        desired_properties_with_effect["stats_luck"] = 0
        desired_properties_with_effect["level"] = 2
        desired_properties_with_effect["hp"] = 79
        desired_properties_with_effect["max_hp"] = 79
        desired_properties_with_effect["exp"] = 100
        desired_properties_with_effect["next_level_exp"] = 200

        self.__test_hero_properties(angry_hero, desired_properties_with_effect)

        angry_hero = angry_hero.base
        angry_hero.update_health_points()

        desired_properties_without_effect = desired_properties_with_effect.copy()
        desired_properties_without_effect["stats_strength"] = 22
        desired_properties_without_effect["stats_endurance"] = 22
        desired_properties_without_effect["stats_intelligence"] = 5
        desired_properties_without_effect["stats_luck"] = 5
        desired_properties_without_effect["hp"] = 49
        desired_properties_without_effect["max_hp"] = 49

        self.__test_hero_properties(angry_hero, desired_properties_without_effect)

    def __create_base_hero(self):
        return Hero(self.__statistic.copy(), self.__image)

    @staticmethod
    def __test_hero_properties(hero, desired_properties):
        assert hero.fixture == desired_properties['fixture'], "Image of hero object is not equal to expected."
        assert hero.position == desired_properties['position'], "Position of hero object is different from expected one"
        assert hero.stats.strength == desired_properties[
            'stats_strength'], "Strength of hero object is different from expected one"
        assert hero.stats.endurance == desired_properties[
            'stats_endurance'], "Endurance of hero object is different from expected one"
        assert hero.stats.intelligence == desired_properties[
            'stats_intelligence'], "Intelligence of hero object is different from expected one"
        assert hero.stats.luck == desired_properties['stats_luck'], "Luck of hero object is different from expected one"
        assert hero.hp == desired_properties['hp'], "Health points value of hero object is different from expected one"
        assert hero.max_hp == desired_properties[
            'max_hp'], "Maximum health points value of hero object is different from expected one"
        assert hero.level == desired_properties['level'], "Level of hero object is different from expected one"
        assert hero.exp == desired_properties['exp'], "Experience value of hero object is different from expected one"
        assert hero.next_level_exp == desired_properties[
            'next_level_exp'], "Next level experience value of hero object is different from expected one"
        assert hero.gold == desired_properties['gold'], "Gold value of hero object is different from expected one"
