from faker import Faker
import uuid


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


class MockData(BuilderBase):

    def __init__(self):
        super().__init__()
        self.prefix = self.fake.lexify(text="?????????")
        self.reset()

    def set_id(self):
        self.result['user_id'] = uuid.uuid4()
        return self

    def set_first_name(self):
        self.result['first_name'] = self.fake.first_name() + \
                                    self.prefix
        return self

    def set_last_name(self):
        self.result['last_name'] = self.fake.last_name() + \
                                   self.prefix
        return self

    def set_new_last_name(self):
        self.result['new_last_name'] = self.fake.last_name() + \
                                       self.prefix
        return self

    def reset(self):
        self.set_id()
        self.set_first_name()
        self.set_last_name()
        self.set_new_last_name()

