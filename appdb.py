import urllib
from sqlalchemy import create_engine

params = urllib.parse.quote_plus('Driver={SQL Server};Server=.;Database=sample;uid=sa;pwd=Admin@12345;')
engine = create_engine("pypyodbc.connect(%s)" % params)