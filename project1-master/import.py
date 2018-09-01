import csv, os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv('DATABASE_URL'))
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open('zips.csv')
    reader = csv.reader(f)
    for Zipcode, City, State, Lat, Long, Population in reader:
        db.execute('INSERT INTO locations (zip_code, city, state, latitude, longitude, population) VALUES (:zipcode, :city, :state, :lat, :long, :population)',
                    {'zipcode': Zipcode, 'city': City, 'state': State, 'lat': Lat, 'long': Long, 'population': Population}
        )
    db.commit()

if __name__ == '__main__':
    main()
