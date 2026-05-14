import os

from dotenv import load_dotenv

load_dotenv()

from app import create_app, db   # noqa: E402
from app.models import Role, User # noqa: E402

app = create_app(os.getenv('FLASK_CONFIG') or 'default')



@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)