import psycopg2

class Postgres:
    def __init__(self, connection):
        #verify the architecture of Python

        print(connection)

        host = connection['host']
        database = connection['database']
        user = connection['user']
        password = connection['password']

        try :
            #Initialize your connection
            self.conn = psycopg2.connect(
                host=host,
                database=database,
                user=user,
                password=password,
            )
        except:
            print('Connect failed, exiting')
            exit()

        #If no errors, print connected
        print('connected')

    def dbSelect(self, query):
        conn = self.conn.cursor()
        conn.execute(query)
        column_names = list(map(lambda x: x.lower(), [
            d[0] for d in conn.description]))
        # list of data items
        rows = list(conn.fetchall())
        result = [dict(zip(column_names, row)) for row in rows]
        # print(result)
        conn.close()

        # print(rows)
        return result

    def selectDb(self, query):
        conn = self.conn.cursor()
        conn.execute(query)
        column_names = list(map(lambda x: x.lower(), [
            d[0] for d in conn.description]))
        # list of data items
        rows = list(conn.fetchall())
        result = [dict(zip(column_names, row)) for row in rows]
        # print(result)
        conn.close()

        # print(rows)
        return result

    def executeDb(self, query):
        try:
            conn = self.conn.cursor()
            conn.execute(query)
            self.conn.commit()
            conn.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error: %s" % error)
            self.conn.close()
            return 1


if __name__ == '__main__':
    connection = {
        "host": "192.168.1.229",  # Exemplo de DSN (IP:Porta/SID ou Service Name)
        "database": "crestani",
        "user": "postgres",
        "password": "crest@ni2900"
    }

    query = f"""
        SELECT distinct 
          itens_averbados -> 0 ->> 'numero_due' numero_due,
          itens_averbados -> 0 ->> 'data_embarque' data_embarque,
          itens_averbados -> 0 ->> 'data_averbacao' data_averbacao,
          itens_averbados -> 0 ->> 'motivo_alteracao' motivo_alteracao,
          '1' as natureza,
          entidadeid,
          null as nro_declaracao,
          null as tipo_documento,
          null as tipo_conhecimento,
          null as data_declaracao,
          null as pais_destino
      FROM 
          sap.due_eventos
      where
          itens_averbados -> 0 ->> 'numero_due' not in (select d."NumeroDeclaracao" from sap.due_dados d)
    """

    nf_remessas = Postgres(connection).selectDb(query)

    print(nf_remessas)