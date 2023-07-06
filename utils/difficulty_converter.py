demon_type_dict = {
    0: 0,
    1: 3,
    2: 4,
    3: 0,
    4: 5,
    5: 6
}

difficulty_type_dict = {
    1: 1,
    2: 1,
    3: 2,
    4: 3,
    5: 3,
    6: 4,
    7: 4,
    8: 5,
    9: 5,
    10: 5
}


def demon_conv(demon_type):
    return demon_type_dict[int(demon_type)]


def diff_conv(diff_type):
    return difficulty_type_dict[int(diff_type)]
