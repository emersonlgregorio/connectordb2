import base64
import os.path

def encode(path):
    if(os.path.exists(path)):
        with open(path, "rb") as pdf_file:
            encoded_string = base64.b64encode(pdf_file.read())
            return encoded_string
    else:
        return "Arquivo não encontrado"



if __name__ == '__main__':
    teste = encode("\\\\srv-rds-02\\CaminhosSAP\\Anexos\\NFe\\03262185000109\\danfe\\51240103262185000109550010000257321290836637.pdf")
    print(teste)
