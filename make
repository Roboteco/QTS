# создание окружения
python -m venv venv
D:\WebServers_python\QTS_Logistics\venv/Scripts/Activate.ps1

# установка пакетов
pip install Flask
pip install flask_script
pip install -U Flask-SQLAlchemy
pip install -U flask-cors
pip install flask-jwt-extended
pip install mysql-connector-python

# настрока git
git init
git remote add origin git@github.com:Roboteco/QTS.git
git pull origin main

# ошибка в коде
On this specific error: from flask._compat import text_type
ModuleNotFoundError: No module named 'flask._compat' -
It happened because the python searched on Flask._compat directory and It isn't there, so I changed like on below : (on flask_script/__init__.py)
Where:
from ._compat import text_type on original flask-script file
to :
from flask_script._compat import text_type