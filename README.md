# ds-boilerplate-code

Install Python in Windows/Linux/MacOS.

Use: https://www.digitalocean.com/community/tutorials/install-python-windows-10 for Windows intallation.
Linux and MacOS: use package management system to install python3 and pip (apt/rpm/brew etc.)

## Clone this repo (or download and extract zip)

or even better if you **fork it** and use your own repo.
```
git clone https://github.com/dinkoosmankovic/ds-boilerplate-code my-project
```
## Setup virtual environment
```
python3 -m venv
cd my-project
mkdir venv
python3 -m venv venv
```

## Activate venv
```
. venv/bin/activate
```

## Get all the libraries
```
pip install -r requirements.txt
```

## Run the code
```
python3 main.py
```
You should get the following screen:

![App Window](/img/screenshot.png)

**You can also setup Visual Studio Code IDE with Python extensions. Then select Python interpreter inside venv folder and run main.py from VS Code.***





