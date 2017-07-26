from flask import Flask
from config import Config
from yeelight_driver import YeelightDriver as Bulb


app = Flask(__name__)


@app.route('/<string:ip>/<string:cmd>')
def index(ip,cmd):
    bulb = Bulb(ip)
    return bulb.run_command(cmd,[])

if __name__ == '__main__':
    app.run(debug=Config.debug)