**Description**
---
This is a fully functional flask app that allows users to keep track of books/articles they have read. Users can enter logs whenever they make progress on a book. The website also allows user to post publicly if they have something interesting to share.



The app was created for the Global Developer Challenge Hackathon (https://global-dev-challenge.devpost.com/?ref_content=default&ref_feature=challenge&ref_medium=portfolio).

**Live Site**
---
http://amodug1664.pythonanywhere.com/

The Flask app was hosted using a free plan from https://www.pythonanywhere.com/

**Langauges Used and Examples**
---
1) Flask: Handles all of the website logic. The application factory responsible for creating the website is stored [here](application/__init__.py)
  The main blueprint handles the functionality of the log, while the authentication blueprint deals with logging in and singign up users to the website.
2) Flask SQLAlchemy: Used to connect to the SQLite database, although other databases can also easily be used. Most used to allow the user to enter logs [here](application/routes.py).
3) Bootstrap: Front-end library to make the website look presentable and also to enhance the responsivness of the app.
4) Jinja2: HTML templating library to code dynamic HTML. Most used to [display the MyLog Page](application/templates/mylog.html).

**Demo**
---
GIF of Creating new book and adding a log entry: https://giphy.com/gifs/VGJy7uIBT43XtrCbch/html5.
There's much more! So, head to the live website [here](http://amodug1664.pythonanywhere.com/)
