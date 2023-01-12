import hashlib


def get_hash(key, index):
    full_string = key + str(index)

    hash = hashlib.md5(full_string.encode())
    return hash.hexdigest()


def get_password(key):
    index = 0
    password_map = {}

    while (len(password_map) < 8):
        hash = get_hash(key, index)

        if hash[0:5] == "00000":
            if hash[5].isdecimal():
                position = int(hash[5])
                if position < 8:
                    if position not in password_map:
                        print(hash)
                        password_map[position] = hash[6]

        index += 1
    password_string = ""
    for i in range(8):
        password_string += password_map[i]

    return password_string


# print(get_hash("abc", 3231929))
# print(get_password("abc"))
print(get_password("abbhdwsy"))
