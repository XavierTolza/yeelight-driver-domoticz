from flask import Flask
from config import Config
from yeelight_driver import YeelightDriver as Bulb


app = Flask(__name__)


@app.route('/<string:ip>/<string:cmd>', defaults={'options': []})
@app.route('/<string:ip>/<string:cmd>/<string:options>')
def index(ip,cmd,options):
    if '[' in options:
        options = list(options)
    else:
        options= [options]
    bulb = Bulb(ip)
    return bulb.run_command(cmd,options)

if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug=Config.debug)