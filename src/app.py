from flask import Flask, render_template, request
from utilities import *
from formatting import *

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def encrypt():

    input_type = choose(request.form)
    if input_type == 0:
        error = 'This shouldn\'t happen'
    else:
        input_text = request.form[f'{input_type}_text']

        # convert from input to hex
        text = input_to_hex(input_text, input_type)

        if text != 0:
            # convert to all other outputs
            text = text.strip()
            ascii_text = ascii_conversion(text)
            # convert to hex to standardize formatting
            hex_text = hex_conversion(text)
            oct_text = octal_conversion(text)
            dec_text = dec_conversion(text)
            bin_text = bin_conversion(text)
            b64_text = base64_conversion(text)
            b32_text = base32_conversion(text)
            error = 0

        else:
            # bad input character
            ascii_text = ''
            hex_text = ''
            dec_text = ''
            oct_text = ''
            bin_text = ''
            b64_text = ''
            b32_text = ''
            error = 1

    return render_template('index.html', ascii_text=ascii_text, hex_text=hex_text, dec_text=dec_text, bin_text=bin_text, b64_text=b64_text, b32_text=b32_text, oct_text=oct_text, error=error)

# TODO: cant handle newline characters


def choose(form):
    if 'ascii' in form:
        input_type = 'ascii'
    elif 'hex' in form:
        input_type = 'hex'
    elif 'dec' in form:
        input_type = 'dec'
    elif 'oct' in form:
        input_type = 'oct'
    elif 'bin' in form:
        input_type = 'bin'
    elif 'b64' in form:
        input_type = 'b64'
    elif 'b32' in form:
        input_type = 'b32'
    else:
        input_type = 0
    return input_type


if __name__ == '__main__':
    app.run(port=5000, debug=False, host='0.0.0.0')
