import hashlib


def hashFunc(toHash):
    if isinstance(toHash, str):
        toHash = bytes.fromhex(toHash)
    if isinstance(toHash, int):
        toHash = toHash.to_bytes((toHash.bit_length() + 7) // 8, 'big')
    output = int(hashlib.sha256(toHash).hexdigest(), 16)
    return output
