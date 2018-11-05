from numpy import genfromtxt
from os import listdir
from db import db

from api.models.factory import get_model

def populate_db():
    for filename in listdir('data/'):
        if not filename.endswith('.csv'):
            continue

        data = load_data('data/{}'.format(filename))
        filename = filename.split(".")[0]
        for row in data:
            item = get_model(filename, row)
            db.session.add(item)
            db.session.commit()


def load_data(file_name):
    data = genfromtxt(file_name, delimiter=',', skip_header=1,
                      dtype='unicode', autostrip=True)
    return data.tolist()
