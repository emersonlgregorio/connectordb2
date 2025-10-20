#Import your dependencies
import json
from hdbcli import dbapi
import datetime

class Hana:
    def __init__(self, connection):

        address = connection['address']
        port = connection['port']
        user = connection['user']
        password = connection['password']

        try :
            #Initialize your connection
            self.conn = dbapi.connect(
                address=address,
                port=port,
                user=user,
                password=password,
            )
        except dbapi.Error as er:
            print('Connect failed, exiting')
            print(er)
            exit()

        #If no errors, print connected
        # print('connected')

    def selectDb(self, query):
        cursor = self.conn.cursor()
        cursor.execute(query)
        column_names = list(map(lambda x: x.lower(), [
            d[0] for d in cursor.description]))
        # list of data items
        rows = list(cursor.fetchall())
        result = [dict(zip(column_names, row)) for row in rows]
        cursor.close()
        self.conn.close()
        # print(type(result))
        # print(result)
        # return json.dumps(result, indent=4, cls=DateTimeEncoder, default=str)
        return result

    def executeDb(self, query):
        cursor = self.conn.cursor()
        cursor.execute(query)
        cursor.close()
        self.conn.close()

class DateTimeEncoder(json.JSONEncoder):
    def default(self, z):
        if isinstance(z, datetime.datetime):
            return (str(z))
        else:
            return super().default(z)


if __name__ == '__main__':
    connection = {
        "address": "172.20.1.4",
        "port": "30015",
        "user": "SYSTEM",
        "password": "9Ab63^Op33"
    }

    query = f"""
                    SELECT to_char(w."AvgPrice") "AvgPrice" FROM sbo_crestani_prd.oitw w
                    WHERE w."ItemCode" = '023004' AND w."WhsCode" = '03.MATR'
                  """

    rsp = Hana(connection).selectDb(query)
    print(rsp)
    avgPrice = rsp[0]['avgprice']
    print(avgPrice)

    Hana(connection).executeDb(query)