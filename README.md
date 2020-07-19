# Proyecto_RyC_Backend
Proyecto RyC backend con flask

### INSTALL VIRTUAL ENV
```bash
/usr/bin/python3.7 -m pip install virtualenv
virtualenv venv --python=3.7
```

### ACTIVE ENVIROMENT
```bash
cd venv/bin
source activate
cd ../..
```

### INSTALL REQUIREMENTS
```bash
/usr/bin/python3.7 -m pip install -r requirements.txt
```

### RUN FLASK
```bash
export FLASK_ENV=development
export FLASK_APP=src/app.py
flask run
```

### SOURCE DEACTIVATE
```bash
source activate
```

### Flask Migrate
```bash
flask db init

## For version update
flask db migrate

## Version upgrade
flask db upgrade

## Version before
flask db downgrade
```
