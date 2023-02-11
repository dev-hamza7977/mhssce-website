from flask import Flask, render_template

from tools.db_helper import get_db_from_csv_to_json

app = Flask(__name__)


@app.route("/")
def index():
    _banner_db = get_db_from_csv_to_json(_db_name="homepage-banner")
    return render_template("index.html", banner_config=_banner_db)


@app.route("/adminlogin")
def adminlogin():
    return render_template("login-form.html")


@app.route("/adminportal")
def adminportal():
    return render_template("mhssce-admin-portal.html")


@app.route("/test")
def test():
    return render_template("home-page-banner.html")

if __name__ == "__main__":
    app.run(use_reloader=False, debug=True)
