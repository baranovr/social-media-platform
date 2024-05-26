# Social media Platform

This project was created with the goal of creating a 
**RESTful API** for a social media platform. 

The project presents seven models:<br>

**socail_media/:**

- `Hashtag`
- `Post`
- `Comment`
- `Like`
- `Dislike`
- `Subscription`

**user/:**
- `User`

The application has quite complex connections between the models, 
since it represents the interaction of a Post with likes and comments, as well as a User with Posts, likes and comments.
But it is important to note that the User model has created using **build-in Django** model and placed in separate app (`user/`).

<br>
<h2>📱 Social Media Platform</h2>

To get started with the project you need to do the following👇:

> Clone the repository
```bash
$ git clone https://github.com/baranovr/social-media-platform.git
```

<br />

> Install modules via `VENV`  
### 👉 Set Up for `Unix`, `MacOS`
```bash
$ virtualenv env
$ source env/bin/activate
$ pip3 install -r requirements.txt
```

### 👉 Set Up for `Windows`
```bash
$ virtualenv env
$ souce venv\Scripts\activate
$ pip install -r requirements.txt
```

<br />

> Set your environment variables
```bash
$ set DB_HOST=<your DB hostname>
$ set DB_NAME=<your DB name>
$ set DB_USER=<your DB username>
$ set DB_PASSWORD=<your DB user passoword>
$ set SECRET_KEY=<your secret key>
```

<br />

> Set Up Database

```bash
$ python manage.py makemigrations
$ python manage.py migrate
```

<br>

## 📑 Project general features 
📍TokenAuthentication

📍Viewing posts and comments without authorization

📍Ability to log out

📍Admin panel /admin/

📍Documentation is located at /api/doc/swagger/

📍Creating posts, setting likes/dislikes, writing comments

📍Viewing and editing personal posts

📍Viewing the number of subscribers/subscriptions

📍Viewing all posts in the application

📍Subscription option

📍Viewing posts from your subscriptions

📍Viewing a list of liked/liked posts

📍Adding hashtags to posts

<br>

<hr>

<h2>🐋📲 Social Media Platform and Docker</h2>
For convenient development and transfer of the project to other users, Docker was introduced here.
The image has been uploaded to Docker Hub:

### Link👇:
> https://hub.docker.com/repository/docker/baranovr/social_media_platform-app/general

How to use (Docker should be installed)👇:

```bash
docker-compose build
docker-compose up
```

<hr>

## 👮‍♂️ Create Super User

### ⚠️ By default, an unauthorized user does not have the rights to post or comment on anything.
To be able to interact with the platform, you need to log in.
To be able to use the full functionality, you need to be an **admin** (or `superuser`).
To create a superuser you need to run this command and follow the further instructions👇:
```bash
$ python manage.py createsuperuser
```

<br />
<hr>

## To view functionality, go to the following endpoints👇:

## 📋 Registration:

> .../api/user/register/

## 🎫 Get token:

> .../api/user/token/

## 💁‍♂️ Check your profile:

> .../api/user/me/

## 👨‍💻 View your posts:

> .../api/user/me/posts/

## 👨‍💻 View your followers/subscriptions accordingly:

> .../api/user/me/subscribers/

> .../api/user/me/subscriptions/

## 👨‍👩‍👦‍👦 View the all users:

> .../api/users/

## ➡️👨‍💻 Follow user:

> .../api/users/<user_id>/subscribe/

## 🔓 Log out:

> .../api/user/me/logout/

## Create hashtag(s):
### **❗️Only administrators can create hashtags**

> .../api/media/hashtags/

<br>

<hr>


## 📂 Code-base structure
```angular2html
< PROJECT ROOT >
   |
   |-- social_media/  
   |    |-- management/
   |    |    |-- commands/
   |    |        |-- wait_for_db.py         # Custom command for waiting db
   |    |
   |    |-- admin.py                        # Registration models in admin page 
   |    |-- apps.py
   |    |-- models.py                       # All social media models
   |    |-- serializers.py                  # All social media serializers
   |    |
   |    |-- urls.py                         # Paths for pages
   |    |-- views.py                        # All project views
   |
   |-- social_media_platform/
   |    |-- asgi.py
   |    |-- settings.py                     # Defines Global Settings
   |    |-- urls.py                         # Root paths
   |    |-- wsgi.py
   |    
   |-- media/                               # Folder for media
   |    |-- uploads/                        
   |        |-- posts_photos/                  
   |
   |-- user/                                
   |    |-- admin.py                        # Registration user in admin page
   |    |-- apps.py                         
   |    |-- models.py                       # Folder with user model
   |    |-- logout.py                       # File for log out
   |    |-- serializers.py                  # User serializers
   |    |-- urls.py                         # Urls to login and view info about current user
   |    |-- views.py                        # User view
   |
   |-- .gitignore                           # File with ignored file types to git
   |-- docker-compose.yaml                  # Docker images managing file
   |-- Dockerfile                           # Docker implementation file
   |-- manage.py                            # Start the app - Django default start script
   |-- requirements.txt                     # Development modules
   |-- sample.env                           # How to set environment variables
   |
   |-- *********************************************************************************
```
