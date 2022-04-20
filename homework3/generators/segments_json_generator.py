from generators.builder_base import BuilderBase


class ObjectRelationJson(BuilderBase):

    def __init__(self, type_obj, params_keys_list, params_value_list):
        super().__init__()
        self.type_obj = type_obj
        assert len(params_keys_list) == len(params_value_list), \
            "Number of keys and values are not equal"
        self.keys_list = params_keys_list
        self.value_list = params_value_list
        self.reset()

    def set_object_type(self, type_obj='remarketing_player'):
        self.result['object_type'] = type_obj
        return self

    def set_params(self):
        self.result['params'] = dict(zip(self.keys_list, self.value_list))
        return self

    def reset(self):
        self.set_object_type()
        self.set_params()


class SegmentsJson(BuilderBase):

    def __init__(self):
        super().__init__()
        self.reset()

    def set_logicType(self, logic_type="or"):
        self.result["logicType"] = logic_type
        return self

    def set_name(self, name=None):
        self.result['name'] = name if name \
            else self.fake.lexify(text="Test name: ???????????????")
        return self

    def set_pass_condition(self, value=1):
        self.result['pass_condition'] = value
        return self

    def set_relations(self, mas=None):

        self.result['relations'] = mas if mas \
            else [ObjectRelationJson(
                "remarketing_player",
                ["left", "right", "type"],
                [365, 0, "positive"]
            ).build()]

    def reset(self):
        self.set_name()
        self.set_logicType()
        self.set_pass_condition()
        self.set_relations()
