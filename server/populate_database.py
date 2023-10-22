import os
from sqlalchemy import create_engine
import pandas as pd


def populate_database():
    engine = create_engine('sqlite:///instance/database.db')
#
    df = download_format_datetime_csv('data/AHU_data/AHU_annual.csv')
    df.to_sql('AHU_data', con=engine, if_exists='replace')

    folder_path = 'data/AHU_data/'
    for f in os.listdir(folder_path):
        fname = os.path.splitext(f)[0]
        full_path = os.path.join(folder_path, f)
        df = download_format_datetime_csv(full_path)
        df.to_sql(f'{fname}', con=engine, if_exists='replace')
    

    df = pd.read_csv('data/faults.csv')
    df.to_sql('faults', con=engine, if_exists='replace', index=False)

    df = pd.read_csv('data/sensor_data.csv')
    df.to_sql('AHU_info', con=engine, if_exists='replace', index=False)



def download_format_datetime_csv(path):
    df = pd.read_csv(path)
    df['Datetime'] = pd.to_datetime(df['Datetime'])
    return df.set_index('Datetime')


if __name__ == '__main__':
    populate_database()
