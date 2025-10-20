import json
import xmltodict
import zlib
from hdbcli import dbapi

# Conexão ao HANA
def connect_to_hana():
    conn = dbapi.connect(
        address='172.20.1.4',  # Substitua pelo endereço do seu HANA
        port=30015,            # Porta padrão do HANA
        user='SYSTEM',
        password='9Ab63^Op33'
    )
    return conn

# Recuperar o BLOB do banco de dados
def retrieve_blob(keynfe):
    conn = connect_to_hana()
    cursor = conn.cursor()

    # Query para recuperar o BLOB
    query = f"""SELECT "XmlFile" FROM SBO_CRESTANI_PRD."DocReceived" WHERE "KeyNfe" = '{keynfe}'"""
    cursor.execute(query)

    result = cursor.fetchone()
    cursor.close()
    conn.close()

    print(result)

    if result:
        if result and result[0]:
            return bytes(result[0])  # Converte para bytes
        else:
            return '999'
    else:
        return '999'

# Descompactar e analisar o BLOB
def analyze_blob(blob):
    # Verificar os primeiros bytes do BLOB
    # print("Primeiros bytes do BLOB:", blob[:20])
    # print("Hexadecimal do BLOB:", blob[:20].hex())

    if blob != '999':
        try:
            decompressed_data = zlib.decompress(blob, wbits=-zlib.MAX_WBITS)
            return decompressed_data
        except zlib.error:
            return '999'
    else:
        return '999'


# Converter XML para JSON
def convert_blob_to_json(key_nfe):
    blob = retrieve_blob(key_nfe)

    if blob != '999':
        # Analisar ou descompactar o BLOB
        data = analyze_blob(blob)

        # Tentar decodificar o XML como UTF-8
        try:
            xml_content = data.decode('utf-8')
        except UnicodeDecodeError:
            return '999'

        # Converter XML para JSON
        try:
            parsed_dict = xmltodict.parse(xml_content)
            json_content = parsed_dict
            type(json_content)
            return json_content
        except Exception as e:
            return '999'
    else:
        return {
            "status_code": "999",
            "status_message": 'XML Não localizado'
        }

# Main
if __name__ == "__main__":
    try:
        key_nfe = '51241103507415000578558900041807901113393335'

        # Converter o BLOB para JSON
        json_content = convert_blob_to_json(key_nfe)

        print(json_content)

    except Exception as e:
        print(f"Erro: {e}")