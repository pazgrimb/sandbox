from __future__ import print_function
import aux
from datetime import date, datetime, timedelta
import statsmodels.formula.api as sm
import mysql.connector
import pandas as pd

__author__ = 'Paz'


class Excel:

    def __init__(self, user='root', database='wrhdb'):
        self.user = user
        self.database = database
        self.cnx = mysql.connector.connect(user=self.user, database=self.database)
        self.cursor = self.cnx.cursor()

    def create_vcexperts_table(self):
        pd.set_option('display.mpl_style', 'default')
        df = pd.read_csv('/Users/Paz/Downloads/vc.csv')[:-1]  # omit last row
        # df = pd.DataFrame({"A": [10,20,30,40,50], "B": [20, 30, 10, 40, 50], "C": [32, 234, 23, 23, 42523]})
        # result = sm.ols(formula="A ~ B + C", data=df).fit()
        # print(result.params)
        # print(result.summary())

        try:
            query = ("INSERT INTO wrhdb.vc_experts "
                     "VALUES (%s, %s, %s, %s, %s, %s)")
            for i in df.index:
                inv_amt = aux.UnitConverter.convert(df.ix[i]['Investment Amount'])
                valuation = aux.UnitConverter.convert(df.ix[i]['Valuation'])
                query_data = (
                    df.ix[i]['Investment Date'], 'NULL', inv_amt, df.ix[i]['Round'], valuation, df.ix[i]['Name'])
                self.cursor.execute(query, query_data)

            self.cnx.commit()
            self.cursor.close()
            self.cnx.close()
            print('Success')
        except ValueError:
            print('failed updating DB')

    def create_linkage_table(self):
        pd.set_option('display.mpl_style', 'default')
        df = pd.read_csv('/Users/Paz/Downloads/ciqid.csv')  # bug here - for some reason, skips first line of csv file. maybe it thinks its columns headers?

        unique_data = set()
        try:
            for r in df.values:
                unique_data.add((r[0],r[3]))

            query = ("INSERT INTO wrhdb.linkage VALUES (%s, %s)")
            for r in unique_data:
                self.cursor.execute(query, r)

            self.cnx.commit()
            self.cursor.close()
            self.cnx.close()
            print('Success')

        except ValueError:
            print('failed updating DB')

    def create_dealogic_table(self):
        pd.set_option('display.mpl_style', 'default')
        df = pd.read_csv('/Users/Paz/Downloads/dealogic.csv')[:-1]  # omit last row

        self.cnx.set_converter_class(aux.NumpyMySQLConverter)

        try:
            query = ("INSERT INTO wrhdb.dealogic "
                     "VALUES (" + "%s, "*51 + " %s)")
            for i in df.index:
                self.cursor.execute(query, list(df.ix[i]))

            self.cnx.commit()
            self.cursor.close()
            self.cnx.close()
            print('Success')
        except ValueError:
            print('failed updating DB')
