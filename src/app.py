import codecs
import base64
from flask import Flask, render_template, request
app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', ascii_text='', hex_text='', x='')


@app.route('/', methods=['POST'])
def encrypt():
    conversion = ''
    hex_text = ''
    ascii_text = ''
    if 'ascii' in request.form:
        input_type = 'ascii'
    elif 'hex' in request.form:
        input_type = 'hex'
    elif 'oct' in request.form:
        input_type = 'oct'
    elif 'bin' in request.form:
        input_type = 'bin'
    elif 'b64' in request.form:
        input_type = 'b64'
    elif 'b32' in request.form:
        input_type = 'b32'
    else:
        return render_template('index.html', error='This shouldn\'t happen')

    input_text = request.form[f'{input_type}_text']
    # first convert from input to hex
    text = input_to_hex(input_text, input_type)
    if text != 0:
        # convert to all other outputs
        ascii_text = ascii_conversion(text)
        hex_text = text
        oct_text = octal_conversion(text)
        bin_text = bin_conversion(text)
        b64_text = base64_conversion(text)
        b32_text = base32_conversion(text)
        error = 0
    else:
        # bad input character
        ascii_text = ''
        hex_text = ''
        oct_text = ''
        bin_text = ''
        b64_text = ''
        b32_text = ''
        error = 1

    return render_template('index.html', ascii_text=ascii_text, hex_text=hex_text, bin_text=bin_text, b64_text=b64_text, b32_text=b32_text, oct_text=oct_text, error=error)

# TODO: cant handle newline characters


def input_to_hex(input_text, input_type):
    input_text = input_text.strip()
    if input_type == "hex":
        text = input_text.split(' ')
        for x in text:
            try:
                int(x, 16)
            except ValueError:
                # input is not hex
                return 0
        return input_text

    elif input_type == "bin":
        text = input_text.split(' ')
        output = ''
        for x in text:
            try:
                output += hex(int(x, 2)) + " "
            except ValueError:
                # input is not bin
                return 0
        return output

    elif input_type == "oct":
        text = input_text.split(' ')
        output = ''
        for x in text:
            try:
                output += hex(int(x, 8)) + " "
            except ValueError:
                # input is not oct
                return 0
        return output

    elif input_type == "ascii":
        output = ''
        for x in input_text:
            output += hex(ord(x)) + " "
        return output

    elif input_type == "b64":
        try:
            input_text = base64.b64decode(input_text).decode()
        except:
            return 0
        output = ''
        for x in input_text:
            output += hex(ord(x)) + " "
        return output

    elif input_type == "b32":
        try:
            input_text = base64.b32decode(input_text).decode()
        except:
            return 0
        output = ''
        for x in input_text:
            output += hex(ord(x)) + " "
        return output


def hex_to_hexstream(text):
    text = text.replace('0x', '').replace(' ', '')
    return text


def base64_conversion(text):
    text = hex_to_hexstream(text)
    output = codecs.encode(codecs.decode(text, 'hex'),
                           'base64').decode().replace('\n', '')
    return output


def base32_conversion(text):
    text = ascii_conversion(text)
    output = base64.b32encode(text.encode()).decode().replace('\n', '')
    return output


def octal_conversion(text):
    text = text.split(' ')
    output = ''
    for x in text:
        try:
            output += oct(int(x, 16)) + " "
        except ValueError:
            continue
    return output


def ascii_conversion(text):
    text = text.split(' ')
    output = ''
    for x in text:
        try:
            output += chr(int(x, 16))
        except ValueError:
            continue
    return output


def bin_conversion(text):
    output = ''
    text = text.split(' ')
    for x in text:
        try:
            output += bin(int(x, 16)) + " "
        except ValueError:
            continue
    return output


if __name__ == '__main__':
    app.run()
