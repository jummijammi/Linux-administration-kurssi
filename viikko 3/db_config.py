import pandas as pd
from sqlalchemy import create_engine

# MySQL-yhteystiedot, vaidettu käyttäjätiedot githubiin
host = "localhost"
user = "user"
password = "password"
database = "meteorites"

# Luo engine
engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}/{database}')

# Funktio datan lukemiseen
def get_meteorite_data():
    query = "SELECT * FROM landings;"
    df = pd.read_sql(query, engine)
    return df
