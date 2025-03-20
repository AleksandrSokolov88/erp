from src.key_value_collector import KeyValueCollector


class KeyValueConverter:

    def __init__(self):
        self.__collector = KeyValueCollector()

    def convert_keys_values_to_dict(self, has_two_colons, line):
        keys = self.__collector.collect_keys(has_two_colons, line)
        values = self.__collector.collect_values(has_two_colons, line, keys)
        parsed_info = {}
        if has_two_colons:
            for key, value in zip(keys, values):
                parsed_info[key] = value
        else:
            if values not in keys:
                parsed_info[keys] = values
            else:
                parsed_info[keys] = ""
        return parsed_info
