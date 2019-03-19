from constants.Towers import souvenir_shop
from entities.towers.Tower import Tower


class SouvenirShop(Tower):
    def __init__(self, position_in_grid, square_size):
        Tower.__init__(self, position_in_grid, square_size, souvenir_shop["range"],
                       souvenir_shop["damage"], souvenir_shop["attack_speed"])
        self.tower_type = souvenir_shop
        self.image_name = "barrelBlack_side.png"
        self.set_image()
