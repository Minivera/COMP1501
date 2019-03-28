from constants.Constants import stats, modifiers


class Character:
    base_health = 5

    def __init__(self, name):
        self.name = name
        self.health = self.base_health
        self.stats = {
            stats["BRAWN"]: 1,
            stats["SKILL"]: 1,
            stats["SMART"]: 1,
        }
        self.tools = {
            modifiers["LOCKPICK"]: 0,
            modifiers["KNIFE"]: 0,
            modifiers["BOMB"]: 0,
            modifiers["ROPE"]: 0,
        }

    def increase_stat(self, stat_name, stat_value):
        self.stats[stat_name] += stat_value
        # Also increase health if needed
        if stat_name == stats["BRAWN"]:
            self.health = self.base_health * self.stats[stat_name]
        return

    def get_stat(self, stat_name):
        return self.stats[stat_name]

    def add_tool(self, tool_name):
        self.tools[tool_name] += 1
        return

    def remove_tool(self, tool_name):
        self.tools[tool_name] = max(0, self.tools[tool_name] - 1)
        return

    def get_tool(self, tool_name):
        return self.tools[tool_name]

    def has_tool(self, tool_name):
        return self.tools[tool_name] > 0

    def get_description(self):
        text = "You are {} and your current health is {}\n".format(self.name, self.health)
        text += "\nCharacter sheet:\n"
        text += "\tABILITIES\n"
        for key in self.stats:
            text += "\t{}: {}\n".format(key.capitalize(), self.get_stat(key))
        text += "\n\tTOOLS in possession\n"
        for key in self.tools:
            text += "\t{}: {}\n".format(key.capitalize(), self.get_tool(key))
        return text
