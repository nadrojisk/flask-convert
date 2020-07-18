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
    elif 'bin' in request.form:
        input_type = 'bin'
    elif 'b64' in request.form:
        input_type = 'b64'
    input_text = request.form[f'{input_type}_text']
    # first convert from input to hex
    text = input_to_hex(input_text, input_type)
    # convert to all other outputs
    ascii_text = ascii_conversion(text)
    hex_text = text
    bin_text = bin_conversion(text)
    b64_text = base64_conversion(text)

    return render_template('index.html', ascii_text=ascii_text, hex_text=hex_text, bin_text=bin_text, b64_text=b64_text)

# TODO: cant handle newline characters


def input_to_hex(input_text, input_type):
    if input_type == "hex":
        return input_text
    elif input_type == "bin":
        text = input_text.split(' ')
        output = ''
        for x in text:
            try:
                output += hex(int(x, 2)) + " "
            except ValueError:
                continue
        return output
    elif input_type == "ascii":
        output = ''
        for x in input_text:
            output += hex(ord(x)) + " "
        return output
    elif input_type == "b64":
        input_text = base64.b64decode(input_text).decode()
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
