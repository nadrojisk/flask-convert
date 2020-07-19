from waitress import serve
from flask import Flask, render_template, request
from utilities import *
from formatting import *

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def encrypt():

    input_type = get_input_type(request.form)
    if input_type == 0:
        error = 'This shouldn\'t happen'
        return render_template('index.html', error=error)
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
            oct_text = oct_conversion(text)
            dec_text = dec_conversion(text)
            bin_text = bin_conversion(text)
            base64_text = base64_conversion(text)
            base32_text = base32_conversion(text)
            error = 0
            return render_template('index.html', ascii_text=ascii_text, hex_text=hex_text, dec_text=dec_text, bin_text=bin_text, base64_text=base64_text, base32_text=base32_text, oct_text=oct_text, error=error)

        else:
            # bad input character
            error = 1
            return render_template('index.html', error=error)


# TODO: cant handle newline characters


def get_input_type(form):
    for x in form:
        if '_text' not in x:
            return x
    return 0


if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=5000)
    # app.run(port=5000, debug=False, host='0.0.0.0')
