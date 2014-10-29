from __future__ import print_function
import aux
from datetime import date, datetime, timedelta
import statsmodels.formula.api as sm
import mysql.connector
import pandas as pd

__author__ = 'Paz'


class Excel:
    # class for converting units. E.g, turns "$10m" into 10000000

    def __init__(self, user='root', database='wrhdb'):
        self.user = user
        self.database = database

    def vc_experts(self):
        pd.set_option('display.mpl_style', 'default')
        df = pd.read_csv('/Users/Paz/Downloads/vc.csv')[:-1]  # omit last row
        # df = pd.DataFrame({"A": [10,20,30,40,50], "B": [20, 30, 10, 40, 50], "C": [32, 234, 23, 23, 42523]})
        # result = sm.ols(formula="A ~ B + C", data=df).fit()
        # print(result.params)
        # print(result.summary())

        cnx = mysql.connector.connect(self.user,self.database)
        cursor = cnx.cursor()

        try:
            query = ("INSERT INTO wrhdb.vc_experts "
                     "VALUES (%s, %s, %s, %s, %s, %s)")
            for i in df.index:
                inv_amt = aux.UnitConverter.convert(df.ix[i]['Investment Amount'])
                valuation = aux.UnitConverter.convert(df.ix[i]['Valuation'])
                query_data = (
                    df.ix[i]['Investment Date'], 'NULL', inv_amt, df.ix[i]['Round'], valuation, df.ix[i]['Name'])
                cursor.execute(query, query_data)

            cnx.commit()
            cursor.close()
            cnx.close()
            print('Success')
        except ValueError:
            print('failed updating DB')

    def ciqid(self):
        pd.set_option('display.mpl_style', 'default')
        df = pd.read_csv('/Users/Paz/Downloads/ciqid.csv')[:-1]  # omit last row

        cnx = mysql.connector.connect(self.user,self.database)
        cursor = cnx.cursor()

        try:
            query = ("INSERT INTO wrhdb.linkage VALUES (%s, %s)")
            for i in df.index:
                query_data = (df.ix[i][0], df.ix[i][3])
                cursor.execute(query, query_data)

                # self.cnx.commit()
                #  cursor.close()
                #  self.cnx.close()
            print('Success')
        except ValueError:
            print('failed updating DB')
