from flask import jsonify
from sqlalchemy import create_engine
import pandas as pd

# Create an engine that connects to the database
engine = create_engine('sqlite:///instance/database.db')


df = pd.read_sql_query('SELECT * FROM defaults', engine, index_col=None)
output = df.to_dict(orient='index')[0]


print(output)

