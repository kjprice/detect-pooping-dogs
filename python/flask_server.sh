export FLASK_APP=server.py
lsof -ti tcp:5000 | xargs kill
flask run --host=0.0.0.0