import sqlalchemy as sa
import sqlalchemy.orm as so
from app import app, db
from app.models.user_models import *
from app.models.client_models import *
from app.models.community_models import *
from app.models.ad_models import *

@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': db, 'User': User, 'Client': Client, 'ClientNotes':ClientNotes, 'Community':Community, 'Ad':Ad}