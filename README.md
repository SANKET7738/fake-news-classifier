# NewsFresh
Detecting Fake News and Misinformation!

An end-to-end Machine Learning based web-app built on top of Django and Flask to detect and classify fake news.

## Setup
 
This project requires **Python3** or above version. So first check your python version.
You can use ``` python --version ``` to check the version you are running.
  

After checking this you can clone the repo.
 

Make sure git is installed. You can proced then by the link-

```
git clone https://github.com/SANKET7738/fake-news-classifier.git
```

After cloning the repo open a terminal window to the desired location. Then, install virtualenv using ``` pip install virtualenv ``` .
 

After installation create a virtual environment. You can do that by using the command ``` virtual project-name ``` . Then activate the environment by ``` project-name/Scripts/activate```.


Next to install all the required dependedencies of the project use command ``` pip install -r requirements.txt ``` this will install all the required packages and libraries for the project. 
 

If you still get a module not found or import error. you can use the command ``` pip install package-name``` to install the required.
Next use ```python``` or ```python3``` command to open your python CLI.Then use the following commands -


```
import nltk
nltk.download("punkt")
```

use ```exit()``` to exit the CLI.


After for django app. Navigate to the location where *manage.py* is that is ```NewsFresh/django-app/newsfresh```. 


Now you will require to do the DB migrations. Which can be done by -


```
python manage.py makemigrations
python manage.py migrate
```


You can create a user-admin profile by using ``` python manage.py createsuperuser```.


Finally now use ``` python manage.py runserver ``` to activate the server.


Now you can visit the app at url ```localhost:8000``` .


Linux users use ```python3``` instead of ```python```.


You can acess the django shell by ```python manage.py shell```.


for FLask setup [click here](https://github.com/SANKET7738/fake-news-classifier/blob/master/flask-app/README.md)
 

## Usage

1. Dashboard

![landing-page](https://github.com/SANKET7738/fake-news-classifier/blob/master/demo-imgs/dashboard.png)


2. Provide the *URL* of the news as an input.

![input](https://github.com/SANKET7738/fake-news-classifier/blob/master/demo-imgs/input.png)

3. Wait for the results!

![output](https://github.com/SANKET7738/fake-news-classifier/blob/master/demo-imgs/output.png)


