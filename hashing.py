import hashlib
import codecs


def hash(string):
    return codecs.encode(hashlib.sha3_256(string.encode("utf-8")).digest(), "base64").decode()


def string_to_hex(string):
    return codecs.encode(codecs.decode(string.encode("utf-8"), "base64"), "hex_codec").decode()
