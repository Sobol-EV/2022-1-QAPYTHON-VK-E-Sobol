#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import re
import os
import sys
import json
import argparse
from collections import Counter


class ParserLog:

    def __init__(self, filename):
        self.filename = filename
        self.regexp_url = r'00]\s".{0,}\sHTTP\/1.'
        self.search_mask_method = {"\"GET ": 0, "\"POST ": 0, "\"PUT ": 0,
                                   "\"DELETE ": 0, "\"HEAD ": 0, "\"OPTIONS ": 0,
                                   "\"CONNECT ": 0
                                   }
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

    def report_total_number_request(self):
        return f"---> Общее количество запросов: {self.total_request}\n"

    def report_total_count_method(self):
        result = f"---> Общее количество запросов по типу:\n"
        for elem in self.dict_method_number.keys():
            result += f"Метод {elem} - {self.dict_method_number[elem]}\n"
        return result

    def report_top_request(self):
        result = f"---> Топ 10 самых частых запросов:\n"
        for elem in self.ordered_values(self.dict_number_request, 10):
            result += f"{elem[0]} - {elem[1]} \n"
        return result

    def report_top_size_request_4xx(self):
        result = f"---> Топ 5 самых больших по размеру запросов, которые завершились клиентской (4ХХ) ошибкой:\n"
        for elem in self.ordered_values(self.dict_4xx_error, 5):
            result += f"IP:{elem[0]} - Длина:{elem[1][0]} - Статус код:{elem[1][1]}\n"
            result += f"Запрос: {elem[1][2]}\n ----------------------------\n"
        return result

    def report_top_ip_request_5xx(self):
        result = f"---> Топ 5 пользователей по количеству запросов, которые завершились серверной (5ХХ) ошибкой:\n"
        for elem in self.ordered_values(self.dict_5xx_error, 5):
            result += f"{elem[0]} - {elem[1]}\n"
        return result

    def get_report(self):
        result = f"Отчёт по лог файлу {self.filename}\n"
        result += self.report_total_number_request()
        result += self.report_total_count_method()
        result += self.report_top_request()
        result += self.report_top_size_request_4xx()
        result += self.report_top_ip_request_5xx()
        return result

    def get_report_json(self):
        result = [{'total_request': self.total_request}, self.dict_method_number,
                  dict(self.ordered_values(self.dict_number_request, 10)),
                  dict(self.ordered_values(self.dict_4xx_error, 5)),
                  dict(self.ordered_values(self.dict_5xx_error, 5))]

        return json.dumps(result)

    def export_report_txt(self, filename):
        with open(filename, 'w') as file:
            file.write(self.get_report())

    def export_report_json(self, filename):
        with open(filename, 'w') as file:
            file.write(self.get_report_json())


def console_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--log', default='access.log')
    parser.add_argument('-o', '--output', default=None)
    parser.add_argument('-j', '--json', default=None)
    return parser


if __name__ == '__main__':
    parser = console_parser()
    namespace = parser.parse_args(sys.argv[1:])

    if os.path.isfile(namespace.log):
        parser_log = ParserLog(namespace.log)
        if not (namespace.output or namespace.json):
            print("The file to save the result does not exist")
            exit(1)
        if namespace.output:
            parser_log.export_report_txt(namespace.output)
            print(f'Results successfully saved to {namespace.output}')
        if namespace.json:
            parser_log.export_report_json(namespace.json)
            print(f'Results successfully saved  {namespace.json}')
    else:
        print("Log file does not exist")
        exit(1)
