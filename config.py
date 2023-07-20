import os

app_dir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'DFGDYUDHGDHGDHFFDREDFDFAS56743qGDFSdghfgrweryurth4675673534fhgdD'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopementConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TESTING_DATABASE_URI') or \
			      'mysql+mysqlconnector://u1968957_default:4E4BwNjmygZ0cU6o@37.140.192.11/u1968957_default?charset=utf8'


class TestingConfig(BaseConfig):
    DEBUG = True
    #SQLALCHEMY_DATABASE_URI = os.environ.get('TESTING_DATABASE_URI') or \
	#		      'mysql+mysqlconnector://root:root@localhost/magicpanel'


class ProductionConfig(BaseConfig):
    DEBUG = True

    #SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://admin:avarxfu2wRLqup3@aa91upuub0hwl0.c6fqvd797vr9.eu-west-2.rds.amazonaws.com/magicpanel'


	#'mysql+mysqlconnector://webdev:hfdybyf@18.191.107.52/gasheet'
    #'mysql+mysqlconnector://admin:avarxfu2wRLqup3@ aa91upuub0hwl0.c6fqvd797vr9.eu-west-2.rds.amazonaws.com/gasheet'
