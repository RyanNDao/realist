import sqlite3
import json
import pandas as pd


# import Pandas


class Database:
    def __init__(self):
        self.connection = sqlite3.connect('real_estate_data.db')
        self.cursor = self.connection.cursor()

    def __enter__(self):
        return self

    def __exit__(self, ext_type, exc_value, traceback):
        self.cursor.close()
        if isinstance(exc_value, Exception):
            self.connection.rollback()
        else:
            # self.connection.commit()
            pass
        self.connection.close()

    def commitChanges(self):
        self.connection.commit()

    def getTruliaTable(self):
        table = ['location TEXT PRIMARY KEY', 'address TEXT', 'asking_price INTEGER', 'city TEXT', 'state TEXT',
                 'zip TEXT',
                 'floor_sqft INTEGER', 'lot_size TEXT', 'bedrooms INTEGER', 'bathrooms INTEGER', 'neighborhood TEXT',
                 'property_type TEXT', 'parking TEXT', 'year_built TEXT', 'year_renovated TEXT', 'condition TEXT',
                 'foundation TEXT', 'basement TEXT', 'structure_type TEXT', 'architecture TEXT',
                 'house_material TEXT', 'listing_status TEXT', 'date_listed_or_sold TEXT', 'trulia_url TEXT',
                 'trulia_listing_id TEXT', 'description_keywords TEXT', 'description TEXT']
        self.cursor.execute(
            'CREATE TABLE IF NOT EXISTS trulia_listings( \
            {table} \
            ) \
            '.format(table=','.join(table))
        )
        self.setTableName('trulia_listings')

    #def MLSTable(self):
    #    table = []

    def setTableName(self, tableName):
        self.table = tableName

    def insertAndLoadTruliaData(self):
        with open('trulia_data.json', 'r') as file:
            trulia_data = json.load(file)
        for listing in trulia_data:
            # print(listing)
            if len(listing) == 27:
                self.cursor.execute(
                    'INSERT OR IGNORE INTO trulia_listings VALUES(:location, :address, :asking_price,:city,:state,:zip,:floor_sqft,:lot_size,:bedrooms,'
                    ':bathrooms,:neighborhood,:property_type,:parking,:year_built,:year_renovated,:condition,:foundation,:basement,'
                    ':structure_type,:architecture,:house_material,:listing_status,:date_listed_or_sold,:trulia_url,:trulia_listing_id,'
                    ':description_keywords,:description)', listing
                )
            elif len(listing) == 20:
                self.cursor.execute(
                    'INSERT OR IGNORE INTO trulia_listings VALUES(:location, :address, :asking_price, :city, :state, :zip, :floor_sqft, :lot_size,'
                    ':bedrooms, :bathrooms, :neighborhood, :property_type, :parking, :year_built, null, null, null, null,'
                    'null, null, null,:listing_status, :date_listed_or_sold, :trulia_url, :trulia_listing_id, :description_keywords,'
                    ':description)', listing
                )

    def getAllListings(self):
        self.cursor.execute('SELECT * FROM {tableName}'.format(tableName=self.table))
        for row in self.cursor:
            print(row)

    def getMLSTable(self):
        table = ['Address TEXT PRIMARY KEY', 'City TEXT', 'County TEXT', 'Building Units Total INTEGER',
                 'Sub Type TEXT', 'Status Contractual Search Date TEXT', 'Current Price INTEGER']

        self.cursor.execute(
            'CREATE TABLE IF NOT EXISTS MLS_listings( \
            {table} \
            ) \
            '.format(table=','.join(table))
        )
        self.setTableName('MLS_listings')

    def loadMLSData(self):
        try:
            mlsDf = pd.read_csv('MLS_data.csv')
            cols = ['Address', 'City', 'County', 'Building Units Total',
                    'Sub Type', 'Status Contractual Search Date', 'Current Price']
            mlsDf = mlsDf[cols].set_index('Address',drop=True)

            mlsDf.to_sql('MLS_listings',con=self.connection,if_exists='replace',index=True)
        except FileNotFoundError:
            print('Cannot find MLS data csv file')
        except Exception as e:
            print(e)

    def getColumnNames(self):
        self.cursor.execute('PRAGMA table_info(MLS_listings)')
        for row in self.cursor:
            print(row)


with Database() as db:
    db.getTruliaTable()
    # db.getAllListings()
    db.insertAndLoadTruliaData()
    # db.getAllListings()
    # db.commitChanges()
    #db.getMLSTable()
    #db.loadMLSData()
    db.getAllListings()
    #db.getColumnNames()
    db.commitChanges()

# cursor.execute('SELECT * FROM sqlite_master WHERE type="table"') ## find all tables


# connection.rollback()
