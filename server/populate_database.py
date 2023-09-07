from sqlalchemy import create_engine
import pandas as pd

def populate_database():
    # Create an engine that connects to the database
    engine = create_engine('sqlite:///instance/database.db')
# 
    # Write the data from the DataFrame to the database
    df = pd.read_pickle('data/data.pkl')
    df.to_sql('AHU_data', con=engine, if_exists='replace')


    df = pd.read_csv('data/sensor_data.csv')
    df.to_sql('AHU_info', con=engine, if_exists='replace', index=False)

if __name__ == '__main__':
    populate_database()