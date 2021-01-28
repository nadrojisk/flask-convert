"""

Author: Jordan Sosnowski
Date: 7/16/2020

"""


from waitress import serve
from flask import Flask, render_template, request
import flask_restful
import conversions
from flask_restful import reqparse

app = Flask(__name__)
api = flask_restful.Api(app)

# global options
PREFIX = True
WIDTH = 8

TYPES = {
    "hex": conversions.hex_conversion,
    "ascii": conversions.ascii_conversion,
    "dec": conversions.dec_conversion,
    "oct": conversions.oct_conversion,
    "base32": conversions.base32_conversion,
    "base64": conversions.base64_conversion,
    "b32": "base32",
    "b64": "base64",
    "h": "hex",
    "a": "ascii",
    "unicode": "ascii",
    "u": "ascii",
    "o": "oct",
}


@app.route("/", methods=["GET"])
def index():
    """
    Default route
    """

    return render_template("index.html")


parser = reqparse.RequestParser()
parser.add_argument("output_type")
parser.add_argument("input_type")
parser.add_argument("input")


class Convert(flask_restful.Resource):
    def get(self):
        args = parser.parse_args()
        input_type = args["input_type"]
        output_type = args["output_type"]
        text = conversions.input_to_hex(args["input"], input_type)

        func = self.get_function(output_type)
        return {"conversion": func(text)}

    def get_function(self, data_type):
        func_value = TYPES[data_type]
        if callable(func_value):
            return func_value
        return self.get_function(func_value)


api.add_resource(Convert, "/convert")


def bool_to_checkbox(data):
    if data:
        return "on"
    elif not data:
        return "off"
    return None


def set_options(options):
    global PREFIX
    global WIDTH

    if "prefix_option" in options:
        PREFIX = True
    else:
        PREFIX = False

    WIDTH = options["width_option"]
    if WIDTH == "":
        WIDTH = 8


@app.route("/", methods=["POST"])
def encrypt():
    """
    Method that gets hit when hitting index via a POST

    Handles conversions of input data. Currently expects binary, octal, hex,
    and decimal to be space seperated
    """
    # TODO: make it so when changing options it doesn't wipe data from page
    input_type = get_input_type(request.form)
    if input_type == 1:
        options = get_options(request.form)

        set_options(options)
        return render_template(
            "index.html",
            prefix_option=bool_to_checkbox(PREFIX),
            width_option=WIDTH,
        )

    if input_type == 0:
        error = 1
        return render_template(
            "index.html",
            error=error,
            prefix_option=bool_to_checkbox(PREFIX),
            width_option=WIDTH,
        )

    input_text = request.form[f"{input_type}_text"]

    # convert from input to hex
    text = conversions.input_to_hex(input_text, input_type)

    if text == conversions.ERROR_BLANK:
        return render_template(
            "index.html",
            prefix_option=bool_to_checkbox(PREFIX),
            width_option=WIDTH,
        )

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
        return render_template(
            "index.html",
            ascii_text=ascii_text,
            hex_text=hex_text,
            dec_text=dec_text,
            bin_text=bin_text,
            base64_text=base64_text,
            base32_text=base32_text,
            oct_text=oct_text,
            error=error,
            prefix_option=bool_to_checkbox(PREFIX),
        )

    # bad input character
    error = 1
    return render_template(
        "index.html", error=error, prefix_option=bool_to_checkbox(PREFIX)
    )


# TODO: cant handle newline characters
# TODO: pass custom error messages


def get_input_type(form):
    """
    Iterates through values sent via POST and finds the one sent via
    the button press.

    Button press do not contain _text in them
    i.e. if the convert button for ascii is pressed `ascii` would be passed
    """
    for param in form:
        if "option" in param:
            return 1
        if "_text" not in param:
            return param
    return 0


def get_options(form):
    options = {}
    for param in form:
        if "_option" in param:
            options[param] = form[param]
    return options


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=5000)
    # app.run(port=5000, debug=False)
