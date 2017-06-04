import binascii, hashlib, hmac, os, time

def scramble_with_kdf(passw, salt, iters):
    return hashlib.pbkdf2_hmac('sha256', passw, salt, iters, 32)

def scramble_with_sha256(passw, salt, iters):
    passw = salt + passw
    for i in range(iters):
        passw = hashlib.sha256(passw).digest()
    return passw

def scramble_with_hmac(passw, salt, iters):
    hmac_obj = hmac.new(salt, passw, hashlib.sha256)
    for i in range(iters):
        hmac_obj.update(passw)
    return hmac_obj.digest()

iters = 10000000
passw = "hello world".encode()
salt = os.urandom(256)

start1 = time.time()
print(binascii.hexlify(scramble_with_kdf(passw, salt, iters)))
end1 = time.time()

start2 = time.time()
print(binascii.hexlify(scramble_with_sha256(passw, salt, iters)))
end2 = time.time()

start3 = time.time()
print(binascii.hexlify(scramble_with_hmac(passw, salt, iters)))
end3 = time.time()


print("scramble_with_kdf:\t{}".format(end1 - start1))
print("scramble_with_sha256:\t{}".format(end2 - start2))
print("scramble_with_hmac:\t{}".format(end3 - start3))
