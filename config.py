import os

class Config:
    debug=bool(os.environ['YEELIGHT_DEBUG'])