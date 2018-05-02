# Rentee

![](https://img.shields.io/wercker/ci/wercker/docs.svg) ![](https://img.shields.io/badge/Developer-Codegass-brightgreen.svg) ![](https://img.shields.io/badge/Flask-0.11.1-blue.svg) ![](https://img.shields.io/badge/Update-May-lightgrey.svg) 

Rentee is a open source rent mate recommendation website. You can fork the repo to build your own website.

This Website is still on developing.

## Setup

This web frame is developed with Flask, you should install the flask package first. Use the command line below to install all the package this project need.

```
pip install -r Site/requirements.txt
```

Be careful that you should `cd` to the project folder before you use this command.

After the packages are installed, you should firstly init the database. I use the sqlite to build the database, you can switch to what you like.

Use the commands below to build the database.

```
$ python manage.py db init
$ python manage.py db migrate
$ python manage.py db upgrade
```

Now you can run the website on your computer

```
$ python manage.py runserver
```

Click the http://127.0.0.1:5000 and you can see it on you computer.

 
