# CSSE-490-lab-0

Lab 1: Photo Processing App

## Project Setup


### Cloning and Installing Dependencies

If you are on Windows, [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/install-win10).

Make sure you have Python 3.9 [installed locally](https://docs.python-guide.org/starting/installation/). To push to Heroku, you'll also need to install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)).

```sh
$ git clone <repo url>
$ cd lab-1-<your_github_username>

$ python3 -m venv venv
# Activate the venv
$ source venv/bin/activate    # Unix
$ .\venv\Scripts\Activate.ps1 # Windows

$ pip install -r requirements.txt
```

### Running Locally

If you are using Linux, Mac, or git bash on Windows:
```sh
$ FLASK_APP=simple_photo_processor.py flask run --reload
```

If you are using Windows power shell:
```sh
env:FLASK_APP=".\simple_photo_processor.py"; flask run --reload
```

Your app should now be running on [localhost:5000](http://localhost:5000/).

The `--reload` flag ensures that the server reloads your code as you make changes.

## Deploying to Heroku

### Creating the Heroku application

```sh
$ heroku create <your username>-lab1
$ git push heroku main

$ heroku open
```

### Testing in a local Heroku environment

```sh
$ heroku local
```
On windows:

```sh
heroku local web -f Procfile.windows
```

### Pushing up new updates to the existing application

```sh
$ git push heroku main
```
