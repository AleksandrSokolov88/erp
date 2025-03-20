import re


class KeyValueCollector:
    def collect_keys(self, two_colons, line):
        if two_colons:
            key_pattern = re.compile("^.+?:|[^\\s]+# :|[^\\s]+?:")
            key_list = [x.replace(":", "").strip() for x in re.findall(key_pattern, line)]
            return key_list
        else:
            key_pattern = re.compile("^.+?:")
            key = "".join(x.replace(":", "") for x in re.findall(key_pattern, line))
            return key

    def collect_values(self, two_colons, line, key_list):
        if two_colons:
            value_first_pattern = re.compile(": [^#]+? ")
            value_first = ("".join(re.findall(value_first_pattern, line))
                           .replace(":", "").strip())
            for key in key_list:
                if value_first in key or not value_first:
                    value_first = ""
            if ":" in line.rpartition(" ")[-1]:
                value_second = ""
            else:
                value_second = line.rpartition(" ")[-1].replace(":", "").strip()
            values_list = [value_first, value_second]
            return values_list
        else:
            value = line.rpartition(" ")[-1].replace(":", "")
            return value
