import hashlib


def get_hash(key, index):
    full_string = key + str(index)

    hash = hashlib.md5(full_string.encode())
    return hash.hexdigest()


def get_password(key):
    index = 0
    password = ""

    while (len(password) < 8):
        hash = get_hash(key, index)

        if hash[0:5] == "00000":
            print("found hash")
            password += hash[5]
        index += 1
    return password


print(get_hash("abc", 3231929))
print(get_password("abbhdwsy"))
