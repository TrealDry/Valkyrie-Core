from . import web
from config import HCAPTCHA_SITE_KEY
from flask import render_template, request
from utils import passwd, regex, hcaptcha as hc, \
    database as db, request_get as rg


@web.route("/change_prefix", methods=("POST", "GET"))
def change_prefix():
    message = ""

    try:
        login = regex.char_clean(rg.main("login"))
        password = rg.main("password")

        prefix = rg.main("prefix")

        if request.method != "POST":
            raise

        if len(login) > 15 or len(password) > 20:
            message = "Incorrect login or password!"
            raise

        if len(prefix) > 20:
            message = "Prefix exceeds 20 characters!"
            raise

        if not hc.hcaptcha.verify():
            message = "Captcha failed!"
            raise

        account_id = tuple(db.account.find(
            {"username": {"$regex": f"^{login}$", '$options': 'i'}}
        ))

        if not bool(account_id):
            message = "Incorrect login or password!"
            raise
        else:
            account_id = account_id[0]["_id"]

        if not passwd.check_password(
            account_id, password, is_gjp=False
        ):
            message = "Incorrect login or password!"
            raise

        vip_status = db.account_stat.find_one({"_id": account_id})["vip_status"]

        if not bool(vip_status):
            message = "Vip status is required to change prefix (more details in discord server)!"
            raise

        db.account_stat.update_one({"_id": account_id}, {"$set": {
            "prefix": prefix
        }})

        return "Prefix has been successfully changed!"

    except:
        return render_template('change_prefix.html', SITE_KEY=HCAPTCHA_SITE_KEY, message=message)
