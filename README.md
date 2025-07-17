DECRIPTION OF MY PROJECT
Instagram Clone with Real-Time Notifications
This project is a feature-rich Instagram clone built with Django, Django REST Framework, and Django Channels for real-time WebSocket-based notifications.

Tech Stack
-  Django, DRF, Channels
-  Redis (Channel Layer)
-  Daphne (ASGI server)
-  SQLite (or your DB)
-  HTML/CSS/JS (Frontend)

✅ Features

-  User authentication (login/register)
-  Create and delete , like, comment on posts
-  Follow/unfollow users
-  Real-time notifications using WebSockets:
   * Users receive instant alerts when they are followed, liked, or commented on
   * Notifications are sent only to authenticated users
-  WebSocket URL: ws://127.0.0.1:8000/ws/notifications/

🛠 Setup Highlights

-  Django Channels integrated in asgi.py
-  WebSocket routing via core/routing.py
-  NotificationConsumer handles real-time logic
-  Redis used for message broadcasting
-  Daphne server runs the ASGI application

Commands for running The Project
-  Create Virtual env
-  install project requirements using pip install -r requirements.txt command
-  after use command - cd instagram_clone
-  run - "python manage.py makemigrations" command. This command Creates new migration files based on the changes made to your Django models. These migration files are used to update the database schema accordingly.
-  run - "python manage.py migrate" command. This command Applies the generated migration files to the database, creating or updating tables based on your Django models.
-  last command - "daphne -b 127.0.0.1 -p 8000 instagram_clone.asgi:application".
