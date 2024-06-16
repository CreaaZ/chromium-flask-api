import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_httpauth import HTTPBasicAuth
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException

load_dotenv()
app = Flask(__name__)
auth = HTTPBasicAuth()

# Global variables
driver = None
window_handle = None

# Selenium setup
chrome_options = Options()
chrome_options.binary_location = os.getenv("CHROME_PATH")
chrome_options.add_argument("--start-fullscreen")
chrome_options.add_argument(f"--user-data-dir={os.getenv('CHROME_PROFILE_PATH')}")
chrome_options.add_argument(f"--profile-directory={os.getenv('CHROME_PROFILE')}")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

# Path to the chromedriver executable
chrome_driver_path = os.getenv("CHROME_DRIVER_PATH")
service = Service(executable_path=chrome_driver_path)


def _check_alive():
    if driver:
        try:
            return window_handle in driver.window_handles
        except WebDriverException as e:
            if "disconnected: not connected to DevTools" in str(e):
                return False


def _get_web_driver():
    global driver, window_handle
    if not driver or not _check_alive():
        driver = webdriver.Chrome(service=service, options=chrome_options)
        window_handle = driver.current_window_handle

    return driver


@auth.verify_password
def verify_password(username, password):
    if username == os.getenv("BASIC_AUTH_USERNAME") and password == os.getenv(
        "BASIC_AUTH_PASSWORD"
    ):
        return True


@app.route("/url", methods=["POST"])
@auth.login_required
def post_url():
    data = request.get_json()
    url = data.get("url")
    if url:
        _get_web_driver().get(url)
        return (
            jsonify({"status": "success", "message": f"URL {url} opened in Chromium"}),
            200,
        )
    else:
        return jsonify({"status": "error", "message": "URL is required"}), 400

@app.route("/url", methods=["GET"])
@auth.login_required
def get_url():
    current_url = _get_web_driver().current_url
    return jsonify({"status": "success", "url": current_url }), 200

@app.route("/refresh", methods=["POST"])
@auth.login_required
def refresh():
    _get_web_driver().refresh()
    return jsonify({"status": "success", "message": "Browser refreshed"}), 200


@app.route("/quit", methods=["POST"])
@auth.login_required
def quit_driver():
    try:
        _get_web_driver().quit()
    except Exception as e:
        print(str(e))
    global driver, window_handle
    driver = None
    window_handle = None
    return jsonify({"status": "success", "message": "Browser quitted"}), 200


if __name__ == "__main__":
    debug = True if os.getenv("FLASK_DEBUG") == "True" else False
    app.run(host="0.0.0.0", port=os.getenv("FLASK_PORT"), debug=debug)
