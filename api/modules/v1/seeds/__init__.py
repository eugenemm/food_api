from .food_categories import init_food_categories
from .toppings import init_toppings
from .foods import init_foods
from .toppings_foods import init_toppings_foods


def apply_seeds():
    init_food_categories()
    init_toppings()
    init_foods()
    init_toppings_foods()


