from api import create_app

'''
This is your "runner" file. Use it to run your Flask project from the command
line manually, and use it in your Heroku Procfile to run in production.

python3 run.py
'''

app = create_app()

if __name__ == '__main__':
    app.run()
