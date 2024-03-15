import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or b'_5#y2L"F4Q8z\n\xec]/'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://porchlink:yQfAUxKduxhxRUxGl68dSIH7mFMHmSw6@dpg-cnqbrt6n7f5s7384q00g-a.oregon-postgres.render.com/matrix_7ub1'
    #os.environ.get('DATABASE_URL') or \
        #'sqlite:///' + os.path.join(basedir, 'app.db')