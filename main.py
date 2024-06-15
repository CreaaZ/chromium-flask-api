import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_httpauth import HTTPBasicAuth
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

load_dotenv()
app = Flask(__name__)
auth = HTTPBasicAuth()

# Global variables
driver = None
window_handle = None

# Selenium setup
chrome_options = Options()
chrome_options.binary_location = os.getenv("CHROME_PATH")  
chrome_options.add_argument("--kiosk") 
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

# Path to the chromedriver executable
chrome_driver_path = os.getenv("CHROME_DRIVER_PATH")
service = Service(executable_path=chrome_driver_path)

def _get_web_driver():
    global driver
    global window_handle
    if not driver or window_handle not in driver.window_handles:
        driver = webdriver.Chrome(service=service, options=chrome_options)
        window_handle = driver.current_window_handle

    return driver

@auth.verify_password
def verify_password(username, password):
    if username == os.getenv("BASIC_AUTH_USERNAME") and password == os.getenv("BASIC_AUTH_PASSWORD"):
        return True

@app.route('/open_url', methods=['POST'])
@auth.login_required
def open_url():
    data = request.get_json()
    url = data.get('url')
    if url:
        _get_web_driver().get(url)
        return jsonify({"status": "success", "message": f"URL {url} opened in Chromium"}), 200
    else:
        return jsonify({"status": "error", "message": "URL is required"}), 400

@app.route('/refresh', methods=['POST'])
@auth.login_required
def refresh():
    _get_web_driver().refresh()
    return jsonify({"status": "success", "message": "Browser refreshed"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv("PORT"), debug=os.getenv("DEBUG"))
