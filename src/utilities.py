import codecs
import base64


def ascii_conversion(text):
    # helper function to convert hex to ascii
    text = text.split(' ')
    output = ''.join([chr(int(x, 16)) for x in text])
    return output.strip()


def bin_conversion(text):
    # helper function to convert hex to bin
    text = text.split(' ')
    output = ''.join(["0b" + bin(int(x, 16))[2:].zfill(8) + " " for x in text])
    return output.strip()


def hex_conversion(text):
    # helper function to convert hex to hex
    text = text.split(' ')
    output = ''.join(["0x" + hex(int(x, 16))[2:].zfill(2) + " " for x in text])
    return output.strip()


def octal_conversion(text):
    # helper function to convert hex to octal
    text = text.split(' ')
    output = ''.join(['0o' + oct(int(x, 16))[2:].zfill(3) + " " for x in text])
    return output.strip()


def base64_conversion(text):
    # helper function to convert hex to base64
    text = ascii_conversion(text)
    output = base64.b64encode(text.encode()).decode().replace('\n', '')
    return output.strip()


def base32_conversion(text):
    # helper function to convert hex to base32
    text = ascii_conversion(text)
    output = base64.b32encode(text.encode()).decode().replace('\n', '')
    return output.strip()
