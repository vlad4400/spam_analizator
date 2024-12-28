from django.apps import AppConfig
import os
from .spam_classifier import SpamClassifier

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
    
    def ready(self):
        csv_path = os.path.join(os.path.dirname(__file__), '../spam_NLP.csv')
        self.spam_classifier = SpamClassifier(csv_path)
        self.spam_classifier.train()
