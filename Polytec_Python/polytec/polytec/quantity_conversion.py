# Copyright (c) 2021 Polytec GmbH, Waldbronn
# Released under the terms of the GNU Lesser General Public License version 3.

import re


def __get_exponent_factor(exponent_string):
    if exponent_string is None:
        return 1
    else:
        exponent_transform_map = {
            "⁻": "-",
            "⁰": "0", "¹": "1", "²": "2", "³": "3", "⁴": "4",
            "⁵": "5", "⁶": "6", "⁷": "7", "⁸": "8", "⁹": "9"
        }
        for exponent_char, digit in exponent_transform_map.items():
            exponent_string = exponent_string.replace(exponent_char, digit)
        return pow(10, int(exponent_string))


def __get_unit_factor(unit_prefix):
    try:
        unit_factor_map = {None: 1, "G": 1e9, "M": 1e6, "k": 1e3, "m": 1e-3, "µ": 1e-6, "n": 1e-9, "p": 1e-12}
        return unit_factor_map[unit_prefix]
    except KeyError:
        raise RuntimeError(f"Unknown unit prefix: {unit_prefix}")


def value_from_quantity_string(quantity_with_unit, base_unit):
    """
    Gets the base unit value of a string containing a quantity with unit.

    Args:
        quantity_with_unit: The quantity with unit, e.g. "-1.2·10² km/s²"
        base_unit:          The base unit, e.g. "m/s²"

    Returns:
        The quantity in its base unit, e.g. -120000
    """
    re_matches = re.search(fr"([+-]?[\d.]+)\s*(?:[·*]\s*10([⁻⁰¹²³⁴⁵⁶⁷⁸⁹]+))?\s*(\w)?{base_unit}", quantity_with_unit)
    return float(re_matches[1]) * __get_exponent_factor(re_matches[2]) * __get_unit_factor(re_matches[3])
