import json
import datetime
import oracledb

# oracledb.init_oracle_client(lib_dir=r"C:\oracle\instantclient_21_13")
# oracledb.init_oracle_client(lib_dir=r"/app/oracle/instantclient")
oracledb.init_oracle_client()

class Oracle:

    def __init__(self, connection):
        user = connection['user']
        password = connection['password']
        dsn = connection['dsn']

        try:
            self.conn = oracledb.connect(user=user,
                                          password=password,
                                          dsn=dsn
                                         )

        except oracledb.Error as er:
            print('Connect failed, exiting')
            print(er)
            exit()

        # If no errors, print connected
        print('connected')

    def selectDb(self, query):
        cursor = self.conn.cursor()
        cursor.execute(query)
        column_names = list(map(lambda x: x.lower(), [
            d[0] for d in cursor.description]))
        # list of data items
        rows = list(cursor.fetchall())
        result = [dict(zip(column_names,row)) for row in rows]
        cursor.close()
        self.conn.close()
        # print(type(result))
        # print(result)
        # return json.dumps(result, indent=4, sort_keys=True, default=str)
        return result

    def executeDB(self, query):
        cursor = self.conn.cursor()
        cursor.execute(query)
        cursor.execute('commit')
        cursor.close()
        self.conn.close()

    def callProc(self, procedure, id, json):
        try:
            cursor = self.conn.cursor()
            print(json)
            cursor.callproc(procedure, [id,json])
            code = 201
            message = 'Executado com sucesso!!!'
            return code, message

        except oracledb.DatabaseError as e:
            error, = e.args  # Desempacotando o erro
            code = error.code
            message = error.message
            return code, message

        finally:
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
        "dsn": "172.20.2.2:1521/qa",  # Exemplo de DSN (IP:Porta/SID ou Service Name)
        "user": "agnew",
        "password": "agnew"
    }

    # query = f"""
    #     SELECT * FROM AC_VW_NF_EXP_REMESSA WHERE DANFE_EXP LIKE '51241103262185000109550010000302161238966510'
    # """
    #
    # nf_remessas = Oracle(connection).selectDb(query)

    proc = Oracle(connection).callProc('zprocessaromaneio', 'bdc29093-0b52-4b2b-9d66-b02a4db3e30b','{\"pcodigo\": 6455, \"pplacaveiculo\": \"ACY5A12\", \"pplacacarreta\": \"ACY5A12\", \"ptagassociado\": null, \"pmotorista\": \"SALOMAO BARROS\", \"ptalhoes\": [{\"talhao\": \"CO-49\", \"porcentagem_carga\": 100, \"pfazenda\": \"1283848702\", \"pordermservico\": \"7433928902\"}], \"pproduto\": \"  12725502\", \"pbruto\": 55000, \"ptara\": 25000, \"pliquido\": 30000, \"ptipodocumento\": \"osg\", \"parmazem\": \"7417885002\", \"pdata\": \"21/02/2025\", \"psafra\": \"15\", \"pequipe\": \" 830877002\", \"pumidade\": \"14\", \"pimpureza\": \"1\", \"pavariados\": \"1\", \"pquebrados\": \"1\", \"pardidos\": \"1\", \"poutros\": \"1\", \"pgraosverdes\": \"1\", \"pnotaorigem\": null, \"pdataorigem\": null, \"pserieorigem\": null, \"pvalororigem\": null, \"pqtdeorigem\": null, \"pobservacao\": \"t\", \"pordemcarregamento\": 1564}')

    code, message = proc

    print(code)
    print(message)

