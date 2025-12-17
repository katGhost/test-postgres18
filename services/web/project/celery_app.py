from celery import Celery
#from project import create_app

""" Initialize Celery wit Flask app ctx""" 
celery = Celery(__name__)