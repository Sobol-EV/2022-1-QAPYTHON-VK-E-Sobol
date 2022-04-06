from faker import Faker


class BuilderBase:

    def __init__(self):
        self.fake = Faker()
        self.result = {}

    def update_inner_value(self, keys, value):
        """
        The function allows you to change the generated objects at any level of
        nesting, and also makes it possible to create new ones
        """
        if not isinstance(keys, list):
            self.result[keys] = value
        else:
            temp = self.result
            for item in keys[:-1]:
                if item not in temp.keys():
                    temp[item] = {}
                temp = temp[item]
            temp[keys[-1]] = value
        return self

    def build(self):
        return self.result
