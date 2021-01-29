"""

Author: Jordan Sosnowski
Date: 1/28/2021

"""


from flask import Flask, render_template, request
import flask_restful
import conversions
from flask_restful import reqparse
from waitress import serve


# global options
PREFIX = True
WIDTH = 8
PROD = False


app = Flask(__name__)
api = flask_restful.Api(app)

parser = reqparse.RequestParser()
parser.add_argument("output_type")
parser.add_argument("input_type")
parser.add_argument("input")


@app.route("/", methods=["GET", "POST"])
def index():
    """
    Default route
    """
    """
    Method that gets hit when hitting index via a POST

    Handles conversions of input data. Currently expects binary, octal, hex,
    and decimal to be space seperated
    """

    if request.method == "GET":
        return render_template("index.html")

    elif request.method == "POST":
        # TODO: make it so when changing options it doesn't wipe data from page
        conv = conversions.Conversions(PREFIX, WIDTH)
        input_type = get_input_type(request.form)
        if input_type == 1:

            set_options()
            return render_template(
                "index.html",
                prefix_option=bool_to_checkbox(conv.prefix),
                width_option=conv.width,
            )

        if input_type == 0:
            error = 1
            return render_template(
                "index.html",
                error=error,
                prefix_option=bool_to_checkbox(conv.prefix),
                width_option=conv.width,
            )

        input_text = request.form[f"{input_type}_text"]

        # convert from input to hex
        text = conv.input_to_hex(input_text, input_type)

        if text == conversions.ERROR_BLANK:
            return render_template(
                "index.html",
                prefix_option=bool_to_checkbox(conv.prefix),
                width_option=conv.width,
            )

        if isinstance(text, str):
            # convert to all other outputs
            text = text.strip()
            ascii_text = conv.ascii_conversion(text)
            # convert to hex to standardize formatting
            hex_text = conv.hex_conversion(text)
            oct_text = conv.oct_conversion(text)
            dec_text = conv.dec_conversion(text)
            bin_text = conv.bin_conversion(text)
            base64_text = conv.base64_conversion(text)
            base32_text = conv.base32_conversion(text)
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
                prefix_option=bool_to_checkbox(conv.prefix),
            )

        # bad input character
        error = 1
        return render_template(
            "index.html",
            error=error,
            prefix_option=bool_to_checkbox(conv.prefix),
        )


class Convert(flask_restful.Resource):
    def get(self):
        args = parser.parse_args()
        input_type = args["input_type"]
        output_type = args["output_type"]
        conv = conversions.Conversions()
        text = conv.input_to_hex(args["input"], input_type)

        func = conv.get_conversion(output_type)
        return {"output": func(text)}


api.add_resource(Convert, "/convert")


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


#######################################
# Handles Setting and Getting Options #
#######################################


def get_options():
    """ Pulls options from post request """
    options = {}
    for param in request.form:
        if "_option" in param:
            options[param] = request.form[param]
    return options


def set_options():
    """Grabs options and then sets them in App
    TODO: needs to be changed as this changes the options
    for everyone!
    """

    global PREFIX
    global WIDTH

    options = get_options()

    if "prefix_option" in options:
        PREFIX = True
    else:
        PREFIX = False

    WIDTH = options["width_option"]
    if WIDTH == "":
        WIDTH = 8


def bool_to_checkbox(data):
    """ Convert bool value to on / off"""
    if data:
        return "on"
    elif not data:
        return "off"
    return None


if __name__ == "__main__":
    if PROD:
        serve(app, host="0.0.0.0", port=5000)
    else:
        app.run(port=5000, debug=True)
