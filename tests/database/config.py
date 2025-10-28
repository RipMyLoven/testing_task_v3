import tempfile
import os

def setup_database():
    db = tempfile.NamedTemporaryFile(delete=False)
    db_path = db.name
    db.close()  
    os.environ['DB_PATH'] = db_path