from dotenv import load_dotenv
import os

load_dotenv()

class params:
    def __init__(self, database) :
        self.user = os.environ.get('DB_USER')
        self.password = os.environ.get('DB_PASSWORD')
        self.database = database
        self.port = os.environ.get('DB_PORT')
        self.host = os.environ.get('DB_HOST')