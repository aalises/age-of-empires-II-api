import pandas as pd
import os
from db import db

from api.models.factory import get_model

def populate_db():
    for filename in os.listdir(os.path.abspath('./data')):
        if not filename.endswith('.csv'):
            continue

        data = load_data('data/{}'.format(filename))
        filename = filename.split(".")[0]
        for row in data:
            item = get_model(filename, row)
            db.session.add(item)
            db.session.commit()


def load_data(file_name):
    data = pd.read_csv(file_name, sep=',',header=0, skipinitialspace=True)  
    return data.where(pd.notnull(data), None).values.tolist()
