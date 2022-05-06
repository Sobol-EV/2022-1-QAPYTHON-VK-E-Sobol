import re
from collections import Counter


class ParserLog:

    def __init__(self, filename):
        self.filename = filename
        self.regexp_url = r'00]\s".{0,}\sHTTP\/1.'
        self.regexp_4xx_error = r"\s4[0-9]{2}\s"
        self.regexp_5xx_error = r'"\s5[0-9]{2}\s'
        self.total_request = None
        self.dict_4xx_error = {}
        self.dict_5xx_error = {}
        self.dict_number_request = {}
        self.dict_method_number = {}
        self.log_file = self.reader()
        self.get_report_values()

    def reader(self):
        with open(self.filename) as file:
            log_file = file.read()
        return log_file

    @staticmethod
    def dict_counter(dictionary: dict, key: str) -> dict:
        if key in dictionary.keys():
            dictionary[key] += 1
        else:
            dictionary[key] = 1
        return dictionary

    @staticmethod
    def ordered_values(dictinary: dict, amount: int) -> list:
        return Counter(dictinary).most_common(amount)

    def get_report_values(self):
        string_list = self.log_file.split("\n")

        for line in string_list:
            found_matches = re.findall(self.regexp_url, line)

            if found_matches:
                list_split = found_matches[0].split(" ")
                url = list_split[2]
                method = list_split[1].split('"')[1]
                if len(method) < 8:
                    self.dict_method_number = self.dict_counter(
                        self.dict_method_number, method
                    )
                self.dict_number_request = self.dict_counter(
                    self.dict_number_request, url
                )
            self.total_request = sum(self.dict_method_number.values())
            split_line = line.split(" ")

            error_4xx = re.findall(self.regexp_4xx_error, line)
            if len(error_4xx):
                length_request = len(split_line[6])
                status_code = error_4xx[0].split(" ")[1]
                request = split_line[6]
                self.dict_4xx_error[split_line[0]] = [
                    length_request, status_code, request
                ]

            error_5xx = re.findall(self.regexp_5xx_error, line)
            if len(error_5xx):
                ip_address = split_line[0]
                self.dict_5xx_error = self.dict_counter(
                    self.dict_5xx_error, ip_address
                )

    def get_report(self):
        result = [{'total_request': self.total_request}, self.dict_method_number,
                  dict(self.ordered_values(self.dict_number_request, 10)),
                  dict(self.ordered_values(self.dict_4xx_error, 5)),
                  dict(self.ordered_values(self.dict_5xx_error, 5))]

        return result

    def get_checksums_report(self):
        report = self.get_report()
        result = [len(i) for i in report]
        return result

