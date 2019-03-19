from constants.Towers import food_shop
from entities.towers.Tower import Tower


class FoodShop(Tower):
    def __init__(self, position_in_grid, square_size):
        Tower.__init__(self, position_in_grid, square_size, food_shop["range"],
                       food_shop["damage"], food_shop["attack_speed"])
        self.effect = food_shop["slow"]
        self.tower_type = food_shop
        self.image_name = "barrelGreen_side.png"
        self.set_image()

    def upgrade(self):
        Tower.upgrade(self)
        self.effect /= 2
