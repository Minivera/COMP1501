class Character:
    def __init__(self, name):
        self.name = name
        self.health = 0
        self.stats = {}
        self.modifiers = {}

    def set_stat(self, stat_name, stat_value):
        self.stats[stat_name] = stat_value
        return

    def get_stat(self, stat_name):
        return self.stats[stat_name]

    def set_modifier(self, modifier_name, modifier_value):
        self.modifiers[modifier_name] = modifier_value
        return

    def get_modifier(self, modifier_name):
        return self.modifiers[modifier_name]

    def get_description(self):
        text = "You are {} and your current health is {}\n".format(self.name, self.health)
        text += "\nCharacter sheet:\n"
        text += "\tABILITIES\n"
        for key in self.stats:
            text += "\t{}: {}\n".format(key.capitalize(), self.get_stat(key))
        text += "\n\tMODIFIERS\n"
        for key in self.modifiers:
            text += "\t{}: +{}\n".format(key.capitalize(), self.get_modifier(key))
        return text
