import hashlib
import re

STRETCHING = 2016


def get_hash(salt, index):
    string = salt + str(index)
    hash = hashlib.md5(string.encode("utf-8"))
    hash = hash.hexdigest()

    for i in range(STRETCHING):
        hash = hashlib.md5(hash.encode("utf-8"))
        hash = hash.hexdigest()
    return hash


def find_64th_key_index(salt):
    count = 0
    index = 0
    candidates = []
    valid_indexes = set()
    quintuple = re.compile(r'(\w)\1{4}')
    triple = re.compile(r'(\w)\1{2}')

    while len(valid_indexes) < 100:

        hash = get_hash(salt, index)
        matches = quintuple.findall(hash)
        if matches:
            for back_index in range(max(index - 1000, 0), index):
                back_hash = get_hash(salt, back_index)
                trip_match = triple.search(back_hash)
                if trip_match:
                    for match in matches:
                        if match == trip_match.group(1):
                            print(back_index)
                            valid_indexes.add(back_index)

        index += 1

    indexes = sorted(valid_indexes)
    print(indexes)
    return indexes[63]


hashst = get_hash("abc", 18)
print(hashst)


hashst = get_hash("abc", 200)

# assert(find_64th_key_index("abc") == 22728)

print(find_64th_key_index("jlmsuwbz"))
