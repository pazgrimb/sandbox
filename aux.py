__author__ = 'Paz'
import math


class UnitConverter:
    """class for converting units. E.g, turns "$10m" into 10000000"""

    def __init__(self):
        pass

    @staticmethod
    def convert(val):
        lookup = {'k': 1000, 'm': 1000000, 'b': 1000000000}
        try:
            if val is 'nan':
                return 'NULL'
            if isinstance(val, float) and math.isnan(val):
                return 'NULL'
            if len(val) == 2:
                return float(val[1:])
            if len(val) == 1:
                return float(val)
            parsed_num = float(val[1:-1].replace(",", ""))
            multiplier = 1
            unit = val[-1]
            if not unit.isdigit():
                multiplier = lookup[unit.lower()]
            number = parsed_num * multiplier
        except ValueError:
            return 'NULL'
        return number
