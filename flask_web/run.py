import sys
sys.path.append('../')

import warnings
warnings.filterwarnings("ignore")

from flask import Flask
from views.views import view


app = Flask(__name__)
app.register_blueprint(view, url_prefix='/book')


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)