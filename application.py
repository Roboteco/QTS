
from app import app as application
from flask_script import Manager, Shell

manager = Manager(application)

if __name__ == '__main__':
    manager.run()