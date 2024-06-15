# Flask API to control Chromium via Selenium

Exposing a simple API to control a Chrome/Chromium browser via Selenium framework.

It was developed to open a specific URL in kiosk mode on a remote machine that has no input devices attached.

## Installation

_The app was developed and tested with Python 3.11_

Create and activate a virtual environment
```
python3.11 -m venv .venv
source .venv/bin/activate
```

Install the dependencies via requirements file
```
pip install -r requirements.txt
```

## Configuring the environment

Copy the environment template
```
cp .env.template .env
```

Adjust the values accordingly

| Variable              | Description                                     |
| :-------------------- | :---------------------------------------------- |
| `PORT`                | The port the Flask API should be exposed on     |
| `DEBUG`               | Enable/disable Flask debug mode                 |
| `CHROME_PATH`         | Absolute path to the Chrome/Chromuim executable |
| `CHROME_DRIVER_PATH`  | Absolute path to the ChromeDriver executable    |
| `BASIC_AUTH_USERNAME` | Basic Authentication User                       |
| `BASIC_AUTH_PASSWORD` | Basic Authentication Password                   |


## API Documentation

### Authentication

The exposed endpoints are protected by Basic Authentication.
A static user/password pair can be defined as the environment variables `BASIC_AUTH_USERNAME` and `BASIC_AUTH_PASSWORD`

### Endpoints

Currently, two endpoints are exposed.
One to open a specific URL in the browser, another one to refresh the browser.

#### /open_url

```http
POST http://localhost:5005/open_url
content-type: application/json
```

The payload needs one parameter to be set.

| Parameter | Type     | Description                         |
| :-------- | :------- | :---------------------------------- |
| `url`     | `string` | **Required**. The URL to be opened. |

The endpoint returns status code `200` in case of success.

#### /refresh
```http
POST http://localhost:5005/refresh
content-type: application/json
```

No payload is required.

The endpoint returns status code `200` in case of success.
