from utils.xor import xor
from utils.base64_dec_and_enc import base64_decode


def chk_decoder(chk):
    chk = xor(base64_decode(chk[5:]), "59182")
    return chk