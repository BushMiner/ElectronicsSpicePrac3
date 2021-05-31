symbols = ["y", "z", "a", "f", "p", "n", "u", "m", "c", "d", "da", "h", "k", "M", "G", "T", "P", "E", "Z", "Y", ""]
symbol_values = {symbols[n]: 10 ** x for n, x in
                 enumerate([-24, -21, -18, -15, -12, -9, -6, -3, -2, -1, 1, 2, 3, 6, 9, 12, 15, 18, 21, 24, 0])}

thousands_only_symbols = ["y", "z", "a", "f", "p", "n", "u", "m","", "k", "M", "G", "T", "P", "E", "Z", "Y"]
thousands_only_symbol_values = {thousands_only_symbols[n]: 10 ** x for n, x in
                 enumerate([-24, -21, -18, -15, -12, -9, -6, -3,0,  3, 6, 9, 12, 15, 18, 21, 24,])}

# For use with UnitInstance Class
p_none = ("", 10 ** 0)  # deka
p_da = ("da", 10 ** 1)  # deka
p_h = ("h", 10 ** 2)  # hecto
p_k = ("k", 10 ** 3)  # kilo
p_M = ("M", 10 ** 6)  # mega
p_G = ("G", 10 ** 9)  # giga
p_T = ("T", 10 ** 12)  # tera
p_P = ("P", 10 ** 15)  # peta
p_E = ("E", 10 ** 18)  # exa
p_Z = ("Z", 10 ** 21)  # zetta
p_Y = ("Y", 10 ** 24)  # yotta

p_d = ("d", 10 ** -1)  # deci
p_c = ("c", 10 ** -2)  # centi
p_m = ("m", 10 ** -3)  # milli
p_u = ("u", 10 ** -6)  # micro
p_n = ("n", 10 ** -9)  # nano
p_p = ("p", 10 ** -12)  # pico
p_f = ("f", 10 ** -15)  # femto
p_a = ("a", 10 ** -18)  # atto
p_z = ("z", 10 ** -21)  # zepto
p_y = ("y", 10 ** -24)  # yocto

# For general use such as x = 5*k
# which equals 5000

da = 10 ** 1  # deka
h = 10 ** 2  # hecto
k = 10 ** 3  # kilo
M = 10 ** 6  # mega
G = 10 ** 9  # giga
T = 10 ** 12  # tera
P = 10 ** 15  # peta
E = 10 ** 18  # exa
Z = 10 ** 21  # zetta
Y = 10 ** 24  # yotta

d = 10 ** -1  # deci
c = 10 ** -2  # centi
m = 10 ** -3  # milli
u = 10 ** -6  # micro
n = 10 ** -9  # nano
p = 10 ** -12  # pico
f = 10 ** -15  # femto
a = 10 ** -18  # atto
z = 10 ** -21  # zepto
y = 10 ** -24  # yocto

def format_number(number:float):
    for entry in list(thousands_only_symbol_values.items())[::-1]:
        new_val = number / entry[1]
        if  abs(new_val) >=1 :
            return "%.3f%s" % (new_val, entry[0])

    
    return  "%.3f" % number
