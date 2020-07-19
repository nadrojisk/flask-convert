import base64


def hex_to_hex(input_text):
    # function to convert from hex to hex
    # this is mainly here to ensure the input is hex
    text = input_text.split(' ')
    for x in text:
        try:
            int(x, 16)
        except ValueError:
            # input is not hex
            return 0
    output = input_text
    return output


def bin_to_hex(input_text):
    # function to convert from binary to hex
    text = input_text.split(' ')
    output = ''
    for x in text:
        try:
            output += hex(int(x, 2)) + " "
        except ValueError:
            # input is not bin
            return 0
    return output


def dec_to_hex(input_text):
    # function to convert from decimal to hex
    text = input_text.split(' ')
    output = ''
    for x in text:
        try:
            # crash on negative numbers
            if int(x) < 0:
                return 0
            output += hex(int(x)) + " "
        except ValueError:
            # input is not dec
            return 0
    return output


def oct_to_hex(input_text):
    # function to convert from octal to hex
    text = input_text.split(' ')
    output = ''
    for x in text:
        try:
            output += hex(int(x, 8)) + " "
        except ValueError:
            # input is not oct
            return 0
    return output


def ascii_to_hex(input_text):
    # function to convert from ascii to hex
    output = ''.join([hex(ord(x)) + " " for x in input_text])
    return output


def b64_to_hex(input_text):
    # function to convert from base64 to hex

    # add in code to handle improperly padded input
    rem = len(input_text) % 4
    if rem:
        padding = (4 - rem)*"="
        input_text += padding
    try:
        input_text = base64.b64decode(input_text).decode()
    except:
        return 0
    output = ''.join([hex(ord(x)) + " " for x in input_text])
    return output


def b32_to_hex(input_text):
    # function to convert from base32 to hex

    # add in code to handle improperly padded input
    rem = len(input_text) % 8
    if rem:
        padding = (8 - rem)*"="
        input_text += padding
    try:
        input_text = base64.b32decode(input_text).decode()
    except:
        return 0
    output = ''.join([hex(ord(x)) + " " for x in input_text])
    return output


def format_hex(hex_string):
    # handles final hex output, formats to 0x## minimum
    hex_string = hex_string.strip().split(' ')
    output = ''.join(
        ["0x" + hex(int(x, 16))[2:].zfill(2) + " " for x in hex_string])
    return output.strip()


def input_to_hex(input_text, input_type):
    # convert input to hex to standardized inputs for other functions
    # if any function returns 0 then it means the input characters are not the
    # correct format
    # i.e. inputting 0x20 in the binary field
    input_text = input_text.strip()
    if input_type == "hex":
        output = hex_to_hex(input_text)
    elif input_type == "bin":
        output = bin_to_hex(input_text)
    elif input_type == "dec":
        output = dec_to_hex(input_text)
    elif input_type == "oct":
        output = oct_to_hex(input_text)
    elif input_type == "ascii":
        output = ascii_to_hex(input_text)
    elif input_type == "b64":
        output = b64_to_hex(input_text)
    elif input_type == "b32":
        output = b32_to_hex(input_text)
    if output == 0:
        return 0
    else:
        return format_hex(output)
