"""

Author: Jordan Sosnowski
Date: 7/19/20

"""

import binascii
import base64

HEX = "hex"
BIN = "bin"
OCT = "oct"
DEC = "dec"
ASCII = "ascii"
BASE64 = "base64"
BASE32 = "base32"

ERROR_INVALID = 0
ERROR_NEG = 1
ERROR_BLANK = 2


class Conversions:
    def __init__(self, prefix=True, width=8) -> None:
        self.prefix = prefix
        self.width = width

        self.funcs = {
            "hex": self.hex_to_hex,
            "bin": self.bin_to_hex,
            "oct": self.oct_to_hex,
            "dec": self.dec_to_hex,
            "ascii": self.ascii_to_hex,
            "base64": self.base64_to_hex,
            "base32": self.base32_to_hex,
        }

    @staticmethod
    def ascii_conversion(text):
        """
        Function to handle conversion of hex to ascii.

        It is assumed that the data coming in is in a hex format
        """

        text = text.split(" ")
        try:
            output = "".join([chr(int(x, 16)) for x in text])
        except TypeError:
            output = ""
        return output.strip()

    def bin_conversion(self, text):
        """
        Function to handle conversion of hex to binary

        It is assumed that the data coming in is in a hex format
        Binary is outputted with a `0bXXXX` format
        """

        text = text.split(" ")
        if self.prefix:
            pre = "0b"
        else:
            pre = ""
        output = "".join(
            [
                pre + bin(int(x, 16))[2:].zfill(int(self.width)) + " "
                for x in text
            ]
        )
        return output.strip()

    @staticmethod
    def dec_conversion(text):
        """
        Function to handle conversion of hex to decimal

        It is assumed that data coming in is in a hex format
        """

        text = text.split(" ")
        output = "".join([str(int(x, 16)) + " " for x in text])
        return output.strip()

    def hex_conversion(self, text):
        """
        Function to handle conversion of hex to hex

        It is assumed that data coming in is in a hex format
        Mainly used to ensure output hex is in an ideal format as input may
        come in without the standard format
        Hex is outputted with a `0xXX` format
        """

        text = text.split(" ")
        if self.prefix:
            pre = "0x"
        else:
            pre = ""
        output = "".join(
            [
                pre + hex(int(x, 16))[2:].zfill(int(self.width) // 4) + " "
                for x in text
            ]
        )
        return output.strip()

    def oct_conversion(self, text):
        """
        Function to handle of hex to oct

        It is assumed the data coming in is in a hex format
        Hex is outputted with a `0oXXX` format
        """

        text = text.split(" ")
        if self.prefix:
            pre = "0o"
        else:
            pre = ""
        output = "".join(
            [pre + oct(int(x, 16))[2:].zfill(3) + " " for x in text]
        )
        return output.strip()

    def base64_conversion(self, text):
        """
        Function to handle of hex to base64

        It is assumed the data coming in is in a hex format
        """

        text = self.ascii_conversion(text)
        output = base64.b64encode(text.encode()).decode().replace("\n", "")
        return output.strip()

    def base32_conversion(self, text):
        """
        Function to handle of hex to base32

        It is assumed the data coming in is in a hex format
        """

        text = self.ascii_conversion(text)
        output = base64.b32encode(text.encode()).decode().replace("\n", "")
        return output.strip()

    @staticmethod
    def parse(text):
        text_list = text.replace(",", " ").split(" ")
        text_list = [word for word in text_list if word]

        return text_list

    def hex_to_hex(self, input_text):
        """
        Function to handle conversion of hex to hex

        It is assumed that data coming in is in a hex format
        Mainly used to ensure output hex is in an ideal format as input may
        come in without the standard format
        Hex is outputted with a `0xXX` format
        """

        # cannot handle negative values
        if "-" in input_text:
            return ERROR_NEG
        text = self.parse(input_text)
        for word in text:
            try:
                int(word, 16)
            except ValueError:
                # input is not hex
                return ERROR_INVALID
        return " ".join(text)

    def bin_to_hex(self, input_text):
        """
        Function to handle conversion of bin to hex

        Hex is outputted with a `0xXX` format
        """

        # cannot handle negative values
        if "-" in input_text:
            return ERROR_NEG
        text = self.parse(input_text)
        output = ""
        for word in text:
            try:
                output += hex(int(word, 2)) + " "
            except ValueError:
                # input is not bin
                return ERROR_INVALID
        return output

    def dec_to_hex(self, input_text):
        """
        Function to handle conversion of dec to hex

        Hex is outputted with a `0xXX` format
        """

        # crash on negative numbers
        if "-" in input_text:
            return ERROR_NEG
        text = self.parse(input_text)
        output = ""
        for word in text:
            try:

                output += hex(int(word)) + " "
            except ValueError:
                # input is not dec
                return ERROR_INVALID
        return output

    def oct_to_hex(self, input_text):
        """
        Function to handle conversion of oct to hex

        Hex is outputted with a `0xXX` format
        """

        # cannot handle negative values
        if "-" in input_text:
            return ERROR_NEG
        text = self.parse(input_text)
        output = ""
        for word in text:
            try:
                output += hex(int(word, 8)) + " "
            except ValueError:
                # input is not oct
                return ERROR_INVALID
        return output

    @staticmethod
    def ascii_to_hex(input_text):
        """
        Function to handle conversion of ascii to hex

        Hex is outputted with a `0xXX` format
        """

        output = "".join([hex(ord(x)) + " " for x in input_text])
        return output

    @staticmethod
    def base64_to_hex(input_text):
        """
        Function to handle conversion of base64 to hex

        Hex is outputted with a `0xXX` format
        """

        # add in code to handle improperly padded input
        rem = len(input_text) % 4
        if rem:
            padding = (4 - rem) * "="
            input_text += padding
        try:
            input_text = base64.b64decode(input_text).decode()
        except binascii.Error:
            return ERROR_INVALID

        if input_text == "":
            return ERROR_INVALID
        output = "".join([hex(ord(x)) + " " for x in input_text])
        return output

    @staticmethod
    def base32_to_hex(input_text):
        """
        Function to handle conversion of base32 to hex

        Hex is outputted with a `0xXX` format
        """

        # add in code to handle improperly padded input
        rem = len(input_text) % 8
        if rem:
            padding = (8 - rem) * "="
            input_text += padding
        try:
            input_text = base64.b32decode(input_text).decode()
        except binascii.Error:
            return ERROR_INVALID
        output = "".join([hex(ord(x)) + " " for x in input_text])
        return output

    def input_to_hex(self, input_text, input_type):
        """
        Function to convert input to hex to standardized inputs for other
        functions

        if any function returns 0 then it means the input characters are not
        the correct format
        i.e. inputting 0x20 in the binary field
        """

        input_text = input_text.strip()

        # cannot handle blank input data
        function = self.funcs.get(input_type, "")
        output = function if function == "" else function(input_text)

        if isinstance(output, int):
            return output

        return self.format_hex(output)

    @staticmethod
    def format_hex(hex_string):
        """
        Function to handles final hex output, formats to 0xXX minimum
        """
        hex_string = hex_string.strip().split(" ")
        output = "".join(
            ["0x" + hex(int(x, 16))[2:].zfill(2) + " " for x in hex_string]
        )
        return output.strip()
