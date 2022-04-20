from generators.builder_base import BuilderBase


class AgeJson(BuilderBase):

    def __init__(self):
        super().__init__()
        self.reset()

    def set_age_list(self, mas=None):
        self.result["age_list"] = mas if mas \
            else [i for i in range(12, self.fake.random_int(min=12, max=75))]
        return self

    def set_expand(self, flag=True):
        self.result['expand'] = flag
        return self

    def reset(self):
        self.set_age_list()
        self.set_expand()


class GeoJson(BuilderBase):

    def __init__(self):
        super().__init__()
        self.reset()

    def set_region(self, mas=None):
        mas = mas if mas else [188]
        self.result['regions'] = mas
        return self

    def reset(self):
        self.set_region()


class FullTimeJson(BuilderBase):

    def __init__(self):
        super().__init__()
        self.reset()

    def set_flags(self, flags=None):
        self.result["flags"] = flags if flags else ["use_holidays_moving", "cross_timezone"]
        return self

    def set_days_time(self, dict=None):
        dict = dict if dict else {"mon": [i for i in range(0, 20)]}
        days = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
        for day in days:
            if day in dict.keys():
                self.result[day] = dict[day]
            else:
                self.result[day] = [i for i in range(0, self.fake.random_int(min=1, max=23))]
        return self

    def reset(self):
        self.set_flags()
        self.set_days_time()


class TargetingsJson(BuilderBase):

    def __init__(self):
        super().__init__()
        self.reset()

    def set_split_audience(self, mas=None):
        self.result["split_audience"] = mas if mas \
            else [i for i in range(1, self.fake.random_int(min=2, max=10))]
        return self

    def set_sex(self, mas=None):
        self.result["sex"] = mas if mas else ["male", "female"]
        return self

    def set_interests_soc_dem(self, mas=None):
        self.result["interests_soc_dem"] = mas if mas else []
        return self

    def set_segments(self, mas=None):
        self.result["segments"] = mas if mas else []
        return self

    def set_interests(self, mas=None):
        self.result["interests"] = mas if mas else []
        return self

    def set_pads(self, mas=None):
        self.result["pads"] = mas if mas else [102643]
        return self

    def set_mobile_types(self, mas=None):
        self.result["mobile_types"] = mas if mas else ["tablets", "smartphones"]
        return self

    def set_mobile_vendors(self, mas=None):
        self.result["mobile_vendors"] = mas if mas else []
        return self

    def set_mobile_operators(self, mas=None):
        self.result["mobile_operators"] = mas if mas else []
        return self

    def reset(self):
        self.set_split_audience()
        self.set_sex()
        self.result['age'] = AgeJson().build()
        self.result['geo'] = GeoJson().build()
        self.set_interests_soc_dem()
        self.set_segments()
        self.set_interests()
        self.result['fulltime'] = FullTimeJson().build()
        self.set_pads()
        self.set_mobile_types()
        self.set_mobile_vendors()
        self.set_mobile_operators()
