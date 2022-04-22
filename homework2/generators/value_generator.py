from faker import Faker


class DataAuth:

    def __init__(self):
        self.fake = Faker()
        self.result = {}
        self.reset()

    def set_login(self, login=None):
        self.result['login'] = login if login else self.fake.ascii_email()
        return self

    def set_password(self, password=None):
        self.result['password'] = password if password else self.fake.password()
        return self

    def set_username(self, username=None):
        self.result['username'] = username if username else self.fake.user_name()

    def reset(self):
        self.set_login()
        self.set_password()
        self.set_username()
        return self

    def build(self):
        return self.result


class DataCampaing:

    def __init__(self):
        self.fake = Faker()
        self.result = {}
        self.reset()

    def set_link(self, link=None):
        self.result['link'] = link if link \
            else self.fake.lexify(text='https://???????????.ru')
        return self

    def set_campaing_name(self, campaing_name=None):
        self.result['campaing_name'] = campaing_name if campaing_name \
            else self.fake.catch_phrase()
        return self

    def reset(self):
        self.set_link()
        self.set_campaing_name()

    def build(self):
        return self.result


class DataSegments:

    def __init__(self):
        self.fake = Faker()
        self.result = {}
        self.reset()

    def set_segment_name(self, segment_name=None):
        self.result['segments_name'] = segment_name if segment_name \
            else self.fake.lexify(text='SEGMENTS NAME: ???????????')
        return self

    def reset(self):
        self.set_segment_name()

    def build(self):
        return self.result
