from constants.Towers import clothing_shop
from entities.towers.Tower import Tower


class ClothingShop(Tower):
    def __init__(self, position_in_grid, square_size):
        Tower.__init__(self, position_in_grid, square_size, clothing_shop["range"],
                       clothing_shop["damage"], clothing_shop["attack_speed"])
        self.effect = clothing_shop["slow"]
        self.tower_type = clothing_shop
        self.image_name = "barrelRed_side.png"
        self.set_image()

    def upgrade(self):
        Tower.upgrade(self)
        self.effect /= 2

