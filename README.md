# K-CHOME

This is a web server and interface for monitoring IoT devises and sensors. It is designed to be extensible and adaptable to the number of devices(things) and sensors that are connected to it. It is designed to be used in a home environment, but can be used in other environments as well.

This project is a work in progress and is not yet ready for use. It is developed along side it's android app counterpart [K-CHome](https://github.com/jetsup/K-CHome) that communicates with the server through a [RESTful API](k_api).

## Pre-requisites

For testing this project you will need to have set-up a Gmail account that support sending the emails through SMTP. You can find more information on how to set-up a `google app` for SMTP [here](https://gist.github.com/jetsup/a283be1e2501d84960d21a6d2ade5caf).

For testing the Android app you will need host the server on a public IP address or use a service like [ngrok](https://ngrok.com/) to tunnel the server to a public IP address. For ngrok, you will need to claim your free domain and use it to tunnel the server. This will reduce the hustle of changing the server address in the android app every time you restart the server.

## Installation

All the required dependencies are listed in the [requirements.txt](requirements.txt) file. You can install them by running the following command:

```bash
pip3 install -r requirements.txt # for linux and mac
```

or

```bash
pip install -r requirements.txt # for windows
```

## Running the server

To run the server, run the following command:

```bash
python3 manage.py runserver # default port is 8000
```

or

```bash
python3 manage.py runserver 9090 # to run the server on port 9090, change 9090 to any port you want
```

When adding a board to the database, use the [read_pid_vid.py](read_pid_vid.py) script to read the `PID` and `VID` of the board. This will help in identifying the board when it is connected to the server.
