# Books Collection

This is a simple application which allows to manage with the books from the collection.

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)


## General info:
What you can do:
* display all books (with title, authors, categories, description)
* filter books by author or/and category
* add books manually (via form)
* add books from google API using provided keywords
* additionally, manipulate with data using books_api

## Technologies:
* Python 3.7
* Django 2.2.1
* HTML5/CSS/Bootstrap4

## Setup:

```
clone the repository
pip install -r requirements.txt
create database and connect it with project in settings.py 
change debug on True
run: python manage.py makemigrations,
     python manage.py migrate,
     python manage.py createsuperuser,
     python managepy runserver.
```
Run tests:
```
pip install -r requirements.txt
run: pytest

```
## How does it look like

You can see this website in action [here](https://app-books-collection.herokuapp.com/)

![screen](https://user-images.githubusercontent.com/47001087/58012653-3d910080-7af5-11e9-8102-3ac4458f7efe.png)
