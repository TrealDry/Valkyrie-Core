import hashlib


def return_hash(string):
    hash_object = hashlib.sha1(bytes(string + 'xI25fpAapCQg', 'utf-8'))
    return hash_object.hexdigest()


def return_hash2(level):
    data = ''
    l = len(level) // 40
    for i in range(40):
        data += level[i * l]
    return hashlib.sha1(bytes(data + 'xI25fpAapCQg', 'utf-8')).hexdigest()
