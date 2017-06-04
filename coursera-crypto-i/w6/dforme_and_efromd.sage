#!/usr/bin/env sage

# Say we have p, q, and e and need to calculate d:
p = 34345639
q = 473344229
e = 194123297627081

print("p = {}".format(p))
print("q = {}".format(q))
print("e = {}".format(e))


phi = (p-1)*(q-1)
d = mod(xgcd(e, phi)[1], phi)

print("phi = {}".format(phi))
print("d = {}".format(d))

vrf = mod(d*e, phi)
print("mod((d*e), phi) = {}".format(vrf))
print("")

# If you have p, q, and d, then e can be found the same way
e = d = p = q = phi = 0 # Resetting

p = 34345639
q = 473344229
d = 13860325261380761

print("p = {}".format(p))
print("q = {}".format(q))
print("d = {}".format(d))

phi = (p-1)*(q-1)
e = mod(xgcd(d, phi)[1], phi)

print("phi = {}".format(phi))
print("e = {}".format(e))

vrf = mod(d*e, phi)
print("mod((d*e), phi) = {}".format(vrf))