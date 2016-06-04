virtualenv --python=python2.7.6	myvenv
source myenv/bin/activate
python manage.py migrate
python manage.py runserver
