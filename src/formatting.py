import conversions


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
        output = conversions.hex_to_hex(input_text)
    elif input_type == "bin":
        output = conversions.bin_to_hex(input_text)
    elif input_type == "dec":
        output = conversions.dec_to_hex(input_text)
    elif input_type == "oct":
        output = conversions.oct_to_hex(input_text)
    elif input_type == "ascii":
        output = conversions.ascii_to_hex(input_text)
    elif input_type == "b64":
        output = conversions.base64_to_hex(input_text)
    elif input_type == "b32":
        output = conversions.base32_to_hex(input_text)
    if output == 0:
        return 0
    else:
        return format_hex(output)
