'''

Author: Jordan Sosnowski
Date: 7/16/2020

'''

from waitress import serve
from flask import Flask, render_template, request
import conversions


app = Flask(__name__)

# global options
PREFIX = True
WIDTH = 8


@app.route('/', methods=['GET'])
def index():
    '''
    Default route
    '''

    return render_template('index.html')


def bool_to_checkbox(data):
    if data:
        return 'on'
    elif not data:
        return 'off'
    return None


def set_options(options):
    global PREFIX
    global WIDTH

    if 'prefix_option' in options:
        PREFIX = True
    else:
        PREFIX = False

    WIDTH = options['width_option']
    if WIDTH == '':
        WIDTH = 8


@app.route('/', methods=['POST'])
def encrypt():
    '''
    Method that gets hit when hitting index via a POST

    Handles conversions of input data. Currently expects binary, octal, hex, and
    decimal to be space seperated
    '''
    # TODO: make it so when changing options it doesnt wipe data from page
    input_type = get_input_type(request.form)
    if input_type == 1:
        options = get_options(request.form)

        set_options(options)
        return render_template('index.html', prefix_option=bool_to_checkbox(PREFIX), width_option=WIDTH)

    if input_type == 0:
        error = 1
        return render_template('index.html', error=error, prefix_option=bool_to_checkbox(PREFIX), width_option=WIDTH)

    input_text = request.form[f'{input_type}_text']

    # convert from input to hex
    text = conversions.input_to_hex(input_text, input_type)

    if text == conversions.ERROR_BLANK:
        return render_template('index.html', prefix_option=bool_to_checkbox(PREFIX), width_option=WIDTH)

    if isinstance(text, str):
        # convert to all other outputs
        text = text.strip()
        ascii_text = conversions.ascii_conversion(text)
        # convert to hex to standardize formatting
        hex_text = conversions.hex_conversion(text, PREFIX, WIDTH)
        oct_text = conversions.oct_conversion(text, PREFIX)
        dec_text = conversions.dec_conversion(text)
        bin_text = conversions.bin_conversion(text, PREFIX, WIDTH)
        base64_text = conversions.base64_conversion(text)
        base32_text = conversions.base32_conversion(text)
        error = 0
        return render_template('index.html', ascii_text=ascii_text,
                               hex_text=hex_text, dec_text=dec_text,
                               bin_text=bin_text, base64_text=base64_text,
                               base32_text=base32_text, oct_text=oct_text,
                               error=error, prefix_option=bool_to_checkbox(PREFIX))

    # bad input character
    error = 1
    return render_template('index.html', error=error, prefix_option=bool_to_checkbox(PREFIX))


# TODO: cant handle newline characters
# TODO: pass custom error messages

def get_input_type(form):
    '''
    Iterates through values sent via POST and finds the one sent via
    the button press.

    Button press do not contain _text in them
    i.e. if the convert button for ascii is pressed `ascii` would be passed
    '''
    for param in form:
        if 'option' in param:
            return 1
        if '_text' not in param:
            return param
    return 0


def get_options(form):
    options = {}
    for param in form:
        if '_option' in param:
            options[param] = form[param]
    return options


if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=5000)
    # app.run(port=5000, debug=False, host='0.0.0.0')
