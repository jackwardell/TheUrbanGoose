# FOOD = "food"
# DRINK = "drink"
# BOTH = "both"
# EITHER = "either"


class FoodOrDrink:
    FOOD = "food"
    DRINK = "drink"
    BOTH = "both"
    EITHER = "either"

    CHOICES = (FOOD, DRINK, BOTH, EITHER)

    def __init__(self, food_or_drink):
        self.value = food_or_drink

    # @classmethod
    # def from_value(cls, value):
    #     if value.lower() not in cls.CHOICES:
    #         raise ValueError(f"{value} not in {cls.CHOICES}")
    #     else:
    #         if value == cls.FOOD:
    #             return
    #
    # @classmethod
    # def is_food(cls, value):
    #     return cls.FOOD.lower() == str(value).lower()
    #
    # @classmethod
    # def is_drink(cls, value):
    #     return cls.DRINK.lower() == str(value).lower()
    #
    # @classmethod
    # def is_either(cls, value):
    #     return cls.BOTH.lower() == str(value).lower()
    #
    # @classmethod
    # def is_both(cls, value):
    #     return cls.EITHER.lower() == str(value).lower()


class QueryOrder:
    ASC = "asc"
    DESC = "desc"

    # @classmethod
    # def is_asc(cls, value):
    #     return cls.ASC.lower() == str(value).lower()
    #
    # @classmethod
    # def is_desc(cls, value):
    #     return cls.DESC.lower() == str(value).lower()
