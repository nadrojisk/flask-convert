from flask import Flask, render_template, request
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', ascii_text='', hex_text='', x='')


@app.route('/', methods=['POST'])
def encrypt():
    conversion = ''
    hex_text = ''
    ascii_text = ''
    if 'ascii' in request.form:
        conversion = 'ascii'
        text = request.form[f'{conversion}_text']
        ascii_text = text
    elif 'hex' in request.form:
        conversion = 'hex'
        text = request.form[f'{conversion}_text']
        hex_text = text

    output = globals()[f"{conversion}_conversion"](request.form, text)
    # output = hex_conversion(request.form, text)
    if hex_text == '':
        hex_text = output
    elif ascii_text == '':
        ascii_text = output

    return render_template('index.html', ascii_text=ascii_text, hex_text=hex_text, x='test')

# TODO: cant handle newline characters


def hex_conversion(form, text):
    text = text.split(' ')
    output = ''
    for x in text:
        try:
            output += chr(int(x, 16))
        except ValueError:
            continue
    return output


def ascii_conversion(form, text):
    output = ''
    for x in text:
        output += hex(ord(x)) + " "
    return output


if __name__ == '__main__':
    app.run()
