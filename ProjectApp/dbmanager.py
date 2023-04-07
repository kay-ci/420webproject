from flask import current_app, g
import os
from .db import Database

def get_db():
    if 'db' not in g:
        g.db = Database()
    return g.db
    
def close_db():
    if 'db' in g:
        g.db.close()
        g.pop('db', None)

def init_db():
    db = get_db()
    db.run_file(os.path.join(current_app.root_path, "schema.sql"))