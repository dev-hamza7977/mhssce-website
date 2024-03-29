import os
import uuid
from datetime import datetime
from pathlib import Path

from flask import Flask, render_template, request, redirect, session
from werkzeug.utils import secure_filename

from tools import db_helper as db
from tools import common_vars as cv

app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route("/")
def index():
    _banner_db = db.get_db_from_csv_to_dict(_db_name=cv.db_HOMEPAGEBANNER)
    _event_db = db.get_db_from_csv_to_dict(_db_name=cv.db_EVENTS)
    return render_template("index.html", banner_config=_banner_db, event_db=_event_db)


@app.route("/adduser", methods=["GET", "POST"])
def adduser():
    if request.method == "POST":
        _data = {
            cv.columnname_ID: str(uuid.uuid4()),
            cv.columnname_USERNAME: request.form[cv.columnname_USERNAME].upper(),
            cv.columnname_USERID: request.form[cv.columnname_USERID],
            cv.columnname_USERPASSWORD: request.form[cv.columnname_USERPASSWORD],
            cv.columnname_ROLE: request.form["usertype"],
            cv.columnname_ENABLED: True
        }
        db.append_dict_to_csv(_data=_data, _db_name=cv.db_USERS)
        return redirect("/userlogin")


@app.route("/userlogin", methods=["GET", "POST"])
def adminlogin():
    if request.method == "GET":
        if "userid" in session:
            if session["role"] == cv.user_type_ADMINISTRATOR:
                _user_db = db.get_db_from_csv_to_df(_db_name=cv.db_USERS)
                _users_list = _user_db.loc[_user_db["role"] != cv.user_type_ADMINISTRATOR].drop(
                    [cv.columnname_ENABLED, cv.columnname_USERPASSWORD], axis=1).to_dict(
                    orient="records")
                return render_template("mhssce-admin-portal.html", users_list=_users_list)
            elif session["role"] == cv.user_type_HOMEPAGEMAINTAINER:
                _homepage_banner_db = db.get_db_from_csv_to_df(_db_name=cv.db_HOMEPAGEBANNER)
                _homepage_banner_db = _homepage_banner_db.drop([cv.columnname_ENABLED], axis=1).to_dict(
                    orient="records")
                return render_template("home-page-banner.html", banner_list=_homepage_banner_db)
            elif session["role"] == cv.user_type_EVENTINCHARGE:
                _event_db = db.get_db_from_csv_to_df(_db_name=cv.db_EVENTS)
                _event_db = _event_db.drop([cv.columnname_ENABLED], axis=1).to_dict(orient="records")
                return render_template("events-admin.html", event_db=_event_db)
        return render_template("login-form.html")
    elif request.method == "POST":
        _user_db = db.get_db_from_csv_to_df(_db_name=cv.db_USERS)
        _form_detail = dict(request.form)
        _user_detail = \
        _user_db.loc[_user_db[cv.columnname_USERID] == _form_detail[cv.columnname_USERID]].to_dict(orient="records")[0]
        if _user_detail["role"] == cv.user_type_ADMINISTRATOR:
            _users_list = _user_db.loc[_user_db["role"] != cv.user_type_ADMINISTRATOR].drop(
                [cv.columnname_ENABLED, cv.columnname_USERPASSWORD], axis=1).to_dict(
                orient="records")
            session["userid"] = _form_detail[cv.columnname_USERID]
            session["role"] = cv.user_type_ADMINISTRATOR
            return render_template("mhssce-admin-portal.html", users_list=_users_list)
        elif _user_detail["role"] == cv.user_type_HOMEPAGEMAINTAINER:
            _homepage_banner_db = db.get_db_from_csv_to_df(_db_name=cv.db_HOMEPAGEBANNER)
            _homepage_banner_db = _homepage_banner_db.drop([cv.columnname_ENABLED], axis=1).to_dict(orient="records")
            session["userid"] = _form_detail[cv.columnname_USERID]
            session["role"] = cv.user_type_HOMEPAGEMAINTAINER
            return render_template("home-page-banner.html", banner_list=_homepage_banner_db)
        elif _user_detail["role"] == cv.user_type_EVENTINCHARGE:
            _event_db = db.get_db_from_csv_to_df(_db_name=cv.db_EVENTS)
            _event_db = _event_db.drop([cv.columnname_ENABLED], axis=1).to_dict(orient="records")
            session["userid"] = _form_detail[cv.columnname_USERID]
            session["role"] = cv.user_type_EVENTINCHARGE
            return render_template("events-admin.html", event_db=_event_db)
    return render_template("login-form.html")


@app.route("/userlogout", methods=["GET"])
def userlogout():
    if "userid" in session:
        session.pop("userid")
        session.pop("role")
    return redirect(request.referrer.rsplit("/")[-1] or "/")


@app.route("/addbanner", methods=["GET", "POST"])
def addbanner():
    _desc = request.form["hpbdescription"]
    f = request.files['hpbimage']
    f.save(os.path.join(db.db_image_location, secure_filename(f.filename)))
    _data = {
        cv.columnname_ID: str(uuid.uuid4()),
        cv.columnname_TEXT: request.form["hpbdescription"].upper(),
        cv.columnname_IMAGE: f"{Path(db.db_image_location).stem}/{secure_filename(f.filename)}",
        cv.columnname_ENABLED: True
    }
    db.append_dict_to_csv(_data=_data, _db_name=cv.db_HOMEPAGEBANNER)
    return redirect("/userlogin")


@app.route("/deleteuser")
def deleteuser():
    _id = request.values[cv.columnname_ID]
    db.disable_item(_db_name=cv.db_USERS, _id=_id)
    return redirect("/userlogin")


@app.route("/deletebanner")
def deletebanner():
    _id = request.values[cv.columnname_ID]
    db.disable_item(_db_name=cv.db_HOMEPAGEBANNER, _id=_id)
    return redirect("/userlogin")


@app.route("/addevent", methods=["POST"])
def addevent():
    _eventdetail = request.form["eventdetail"]
    _eventdate = request.form["eventdate"]
    _eventdate = datetime.strptime(_eventdate, "%Y-%m-%d").strftime("%d %B %Y")
    _data = {
        cv.columnname_ID: str(uuid.uuid4()),
        cv.columnname_TEXT: _eventdetail.upper(),
        cv.columnname_DATE: _eventdate,
        cv.columnname_ENABLED: True
    }
    db.append_dict_to_csv(_data=_data, _db_name=cv.db_EVENTS)
    return redirect("/userlogin")


@app.route("/department")
def department():
    return render_template("department.html")

@app.route("/automobile")
def automobile():
    return render_template("automobile.html")

@app.route("/tpo")
def tpo():
    return render_template("tpo.html")


if __name__ == "__main__":
    # app.run(use_reloader=True, debug=False, port=5000, host="0.0.0.0")
    app.run(host="0.0.0.0", port=5000)