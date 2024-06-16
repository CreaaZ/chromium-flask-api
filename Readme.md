# Flask API to control Chromium via Selenium

Exposing a simple API to control a Chrome/Chromium browser via Selenium framework.

It was developed to open a specific URL in fullscreen mode on a remote machine that has no input devices attached.

## Installation

_The app was developed and tested with Python 3.11_

Create and activate a virtual environment
```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

Install the dependencies via requirements file
```bash
pip install -r requirements.txt
```

## Configuring the environment

Copy the environment template
```bash
cp .env.template .env
```

Adjust the values accordingly

| Variable              | Description                                          |
| :-------------------- | :--------------------------------------------------- |
| `FLASK_PORT`          | The port the Flask API should be exposed on          |
| `FLASK_DEBUG`         | "True" or "False" to enable/disable Flask debug mode |
| `CHROME_PATH`         | Absolute path to the Chrome/Chromium executable      |
| `CHROME_DRIVER_PATH`  | Absolute path to the ChromeDriver executable         |
| `CHROME_PROFILE_PATH` | Absolute path to the Chrome/Chromium profiles        |
| `CHROME_PROFILE`      | Name of the profile                                  |
| `BASIC_AUTH_USERNAME` | Basic Authentication User                            |
| `BASIC_AUTH_PASSWORD` | Basic Authentication Password                        |

### Chrome Profiles

Chrome profiles are needed to share browser and session data across the lifecycle of Chromium instances.
By default, the ChromeDriver creates a complete clean profile for every new window managed.
We can set a path to the Chrome profile in order to reuse credentials, cookies, etc. across new windows.

With Linux, the profiles are typically located at `/home/myuser/.config/chromium/` with a default profile named `Default`.
It is okay to use this, however, the ChromeDriver cannot launch a new window, if there is already a window open with this profile (e.g. manually opened on the desktop).
Therefore, it is recommended to specify a new profile to be used with Selenium.
One can also use the profile manually in Chromium, e.g. to store passwords, manually log in to website, etc.

## Configuring systemd service
To start the Flask server on boot, we configure a systemd service.
Adjust the (path) values in `chromium_api.service`.
Make sure to set the `DISPLAY` environment variable to your display device, otherwise the service will not work.
Once adjusted, run the following command to copy over the file to the service directory.

```bash
sudo cp chromium_api.service /etc/systemd/system/chromium_api.service
```

You can start and stop the service via `systemctl`

```bash
sudo systemctl start chromium_api.service
sudo systemctl stop chromium_api.service
```

You can inspect the logs with journalctl
```bash
sudo journalctl -u chromium_api.service
```

## API Documentation

### Authentication

The exposed endpoints are protected by Basic Authentication.
A static user/password pair can be defined as the environment variables `BASIC_AUTH_USERNAME` and `BASIC_AUTH_PASSWORD`

### Endpoints

Currently, the following endpoints are exposed.

#### POST /url

Opens the given website in Chromium.
Launches a Chromium window if not present

```http
POST http://localhost:5005/url
content-type: application/json
```

The payload needs one parameter to be set.

| Parameter | Type     | Description                         |
| :-------- | :------- | :---------------------------------- |
| `url`     | `string` | **Required**. The URL to be opened. |

The endpoint returns status code `200` in case of success.

#### GET /url

Returns the current URL of Chromium

```http
GET http://localhost:5005/url
content-type: application/json
```

The endpoint returns status code `200` in case of success with the following payload

```json
{
    "status" : "success",
    "url" : "<url"
}
```

#### POST /refresh
Refreshes the browser page.

```http
POST http://localhost:5005/refresh
content-type: application/json
```

No payload is required.

The endpoint returns status code `200` in case of success.

#### POST /quit
Quits the browser and webdriver.

```http
POST http://localhost:5005/quit
content-type: application/json
```

No payload is required.

The endpoint returns status code `200` in case of success.