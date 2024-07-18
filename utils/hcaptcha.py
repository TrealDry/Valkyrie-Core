from flask_hcaptcha import hCaptcha
from config import HCAPTCHA_SITE_KEY, HCAPTCHA_SECRET_KEY


hcaptcha = hCaptcha(
    site_key=HCAPTCHA_SITE_KEY,
    secret_key=HCAPTCHA_SECRET_KEY
)


def init_hc(app):
    hcaptcha.init_app(app)
