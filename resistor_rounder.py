bases = [1.0,
1.1,
1.2,
1.3,
1.5,
1.6,
1.8,
2.0,
2.2,
2.4,
2.7,
3.0,
3.3,
3.6,
3.9,
4.3,
4.7,
5.1,
5.6,
6.2,
6.8,
7.5,
8.2,
9.1]

rakkie = [
    10,
    12,
    15,
    18,
    22,
    33,
    49,
    47,
    56,
    68,
    82,
    100,
    120,
    150,
    180,
    220,
    270,
    330,
    390,
    470,
    560,
    680,
    820,
    1000,
    1200,
    1800,
    2200,
    3300,
    3900,
    4700,
    5600,
    6800,
    8200,
    10000,
    12000,
    15000,
    18000,
    22000,
    27000,
    33000,
    39000,
    47000,
    68000,
    82000,
    100000,
    120000,
    150000,
    330000,
    390000,
    470000,
    560000,
    680000,
    820000,
    1000000
]

mults = [10**n for n in range(6)]


def find_closest(resistor_val):
    closest_val = 0
    smallest_dif = 2**64

    for base in bases:
        for m in mults:
            r = base*m
            dif = abs(resistor_val - r)
            if dif < smallest_dif:
                smallest_dif = dif
                closest_val = r
    return closest_val

def find_closest_rakkie(resistor_val):
    closest_val = 0
    smallest_dif = 2**64
    for r in rakkie:
        dif = abs(resistor_val - r)
        if dif < smallest_dif:
            smallest_dif = dif
            closest_val = r
    return closest_val


def round_map_vals(old_map):
    return dict(map(lambda pair: (pair[0], find_closest(pair[1])), old_map.items()))

def round_map_vals_rakkie(old_map):
    return dict(map(lambda pair: (pair[0], find_closest_rakkie(pair[1])), old_map.items()))


print("")