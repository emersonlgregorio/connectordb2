import json
import datetime
import pyodbc


class SqlServer:
    def __init__(self, connection):
        server = connection['server']
        database = connection['database']
        user = connection['user']
        password = connection['password']
        driver = connection.get('driver', 'ODBC Driver 17 for SQL Server')
        port = connection.get('port', 1433)

        try:
            # Construir string de conexão
            connection_string = (
                f"DRIVER={{{driver}}};"
                f"SERVER={server},{port};"
                f"DATABASE={database};"
                f"UID={user};"
                f"PWD={password};"
            )

            # Initialize your connection
            self.conn = pyodbc.connect(connection_string)

        except pyodbc.Error as er:
            print('Connect failed, exiting')
            print(er)
            exit()

        # If no errors, print connected
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
        self.conn.commit()
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
        "server": "192.168.1.100",
        "database": "testdb",
        "user": "sa",
        "password": "password123",
        "driver": "ODBC Driver 17 for SQL Server",  # opcional
        "port": 1433  # opcional
    }

    query = f"""
        SELECT TOP 10 * FROM your_table
    """

    rsp = SqlServer(connection).selectDb(query)
    print(rsp)

    SqlServer(connection).executeDb(query)

