import os

from app import create_app, auth

config_name = os.getenv('APP_SETTINGS') # config_name = "development"
app = create_app(config_name)

users = {
    "john": "hello",
    "susan": "bye"
}


@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None


if __name__ == '__main__':
    app.run()