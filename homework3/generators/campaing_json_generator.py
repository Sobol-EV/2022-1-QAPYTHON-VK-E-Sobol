from generators.targetings_json_generator import TargetingsJson
from generators.builder_base import BuilderBase


class CampaingJson(BuilderBase):

    def __init__(self):
        super().__init__()
        self.reset()

    def set_name(self, name=None):
        self.result['name'] = name if name \
            else self.fake.lexify(text="Test name: ???????????????")
        return self

    def set_read_only(self, flag=False):
        self.result['read_only'] = flag
        return self

    def set_conversion_funnel_id(self, value=None):
        self.result['conversion_funnel_id'] = value
        return self

    def set_objective(self, type_obj="traffic"):
        self.result['objective'] = type_obj
        return self

    def set_enable_offline_goals(self, flag=False):
        self.result['enable_offline_goals'] = flag
        return self

    def set_age_restrictions(self, value=None):
        self.result['age_restrictions'] = value
        return self

    def set_date_start(self, value=None):
        self.result['date_start'] = value
        return self

    def set_date_end(self, value=None):
        self.result['date_end'] = value
        return self

    def set_autobidding_mode(self, value='second_price_mean'):
        self.result['autobidding_mode'] = value
        return self

    def set_budget_limit_day(self, value=None):
        self.result['budget_limit_day'] = value
        return self

    def set_budget_limit(self, value=None):
        self.result['budget_limit'] = value
        return self

    def set_utm(self, value=None):
        self.result['utm'] = value
        return self

    def set_mixing(self, value="fastest"):
        self.result['mixing'] = value
        return self

    def set_enable_utm(self, flag=True):
        self.result['enable_utm'] = flag
        return self

    def set_price(self, price=None):
        self.result['price'] = price if price else str(float(self.fake.random_int(min=4, max=500)))
        return self

    def set_max_price(self, price="0"):
        self.result['max_price'] = price
        return self

    def set_package_id(self, id_pack=961):
        self.result['package_id'] = id_pack
        return self

    def set_banners(self, mas=None):
        self.result['banners'] = [{
            "urls": {
                "primary": {
                    "id": 62071236
                }
            },
            "textblocks": {},
            "content": {
                "image_240x400": {
                    "id": 10381052
                }
            },
            "name": ""
        }] if not mas else mas
        return self

    def reset(self):
        self.set_name()
        self.set_read_only()
        self.set_conversion_funnel_id()
        self.set_objective()
        self.set_enable_offline_goals()
        self.result['targetings'] = TargetingsJson().build()
        self.set_age_restrictions()
        self.set_date_start()
        self.set_date_end()
        self.set_autobidding_mode()
        self.set_budget_limit_day()
        self.set_budget_limit()
        self.set_mixing()
        self.set_utm()
        self.set_enable_utm()
        self.set_price()
        self.set_max_price()
        self.set_package_id()
        self.set_banners()
