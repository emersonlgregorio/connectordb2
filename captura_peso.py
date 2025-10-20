import socket
import re


def conectar_peso(ip, porta, timeout=5):
    """Estabelece conexão TCP/IP com a balança."""
    try:
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.settimeout(timeout)
        cliente.connect((ip, porta))
        print(f"Conectado à balança {ip}:{porta}")
        return cliente
    except Exception as e:
        print(f"Erro ao conectar à balança: {e}")
        return None


def obter_peso(cliente, balanca):
    """Obtém o peso da balança via TCP/IP."""
    try:
        # Enviar comando para solicitar o peso (depende do protocolo da balança)
        comando = b'REQUEST_WEIGHT\n'  # Substituir pelo comando correto
        cliente.sendall(comando)

        if balanca == 'saturno':
            dados = cliente.recv(1024).decode().strip()
        elif balanca == 'toledo':
            dados = re.sub(r'[^\d.]', '', cliente.recv(1024).decode('latin1', errors='ignore'))

        return dados

    except Exception as e:
        print(f"Erro ao obter peso: {e}")
        return None


def capturar(ip, porta, balanca):

    cliente = conectar_peso(ip, porta)

    if cliente:
        i = 0
        try:
            while i <= 10:
                i += 1
                peso = obter_peso(cliente, balanca)
                if peso:
                    if balanca == 'saturno':
                        peso_quantidade = peso[:6]
                    elif balanca == "toledo":
                        peso_quantidade = peso
                    print(f"Peso recebido: {peso}")
                else:
                    print("Nenhum dado recebido.")
        except KeyboardInterrupt:
            print("\nFinalizando conexão.")
        finally:
            cliente.close()

    return peso_quantidade



if __name__ == "__main__":
    ##192.168.11.100:23 Germinare
    ##192.168.6.41:9000 Querencia
    ##192.168.9.40:9000 Curupai
    ##192.168.202.51:30000 Armazem Tangara

    # peso = capturar('192.168.202.51', 30000, 'saturno')
    peso = capturar('192.168.6.41', 9000, 'toledo')
    print(peso)
