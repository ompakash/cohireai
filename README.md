API DOCUMENTATION = https://documenter.getpostman.com/view/23480640/2sAXxMftZv

SIMPLE DJANGO APPLICATION SETUP

STEPS TO RUN THE PROJECT ON WINDOWS OS
- git clone https://github.com/ompakash/cohireai.git
- python -m venv venv_cohire
- .\venv_cohire\Scripts\activate
- cd .\PrepCV\
- pip install -r .\requirements.txt
- python .\manage.py makemigrations
- python .\manage.py migrate
- python .\manage.py createsuperuser
Email: admin@gmail.com
- python .\manage.py runserver
