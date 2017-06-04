#!/usr/bin/env sage

p = random_prime(2^32)
print("p = {}".format(p))

q = random_prime(2^32)
print("q = {}".format(q))

n = p * q
print("n = {}".format(n))

phi = (p-1)*(q-1)
print("phi = {}".format(phi))

e = random_prime(phi)
print("e = {}".format(e))

d = mod(xgcd(e, phi)[1], phi)
print("d = {}".format(d))

vrf = mod(d*e, phi)
print("mod((d*e), phi) = {}".format(vrf))


def str_as_num(raw_str):
    str_num = "".join("{:02x}".format(ord(c)) for c in raw_str)
    return int(str_num, 16)

def num_as_str(num):
    str_num = "{:02x}".format(num)
    return "".join([chr(int(str_num[i:i+2], 16)) for i in range(0, len(str_num), 2)])

pt_str = "Hello"
print("pt_str = {}".format(pt_str))
pt_num = str_as_num(pt_str)
print("pt_num = {}".format(pt_num))

ct_num = power_mod(pt_num, e, n)
print("ct_num = {}".format(ct_num))
ct_str = num_as_str(ct_num)
print("ct_str = {}".format(ct_str))

pt_num_2 = power_mod(ct_num, int(d), n)
print("pt_num_2 = {}".format(pt_num_2))
pt_str_2 = num_as_str(pt_num_2)
print("pt_str_2 = {}".format(pt_str_2))
