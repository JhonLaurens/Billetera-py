from web3 import Web3
from eth_account import Account

# Conectar al servidor RPC de Ganache
ganache_url = "http://127.0.0.1:7545"  # Cambia esto si usas otra red
web3 = Web3(Web3.HTTPProvider(ganache_url))

# Verificar si la conexión se estableció correctamente
if web3.is_connected():
    print("Conectado a Ganache!")
else:
    print("Error al conectar a Ganache.")
    exit()

# Variable global para almacenar la cuenta actual
current_account = None

def importar_cuenta():
    global current_account
    # Solicitar al usuario la dirección de la cuenta y la clave privada
    account_address = input("Ingrese la dirección de la cuenta: ")
    print("Ingrese la clave privada de la cuenta (se ocultará después de presionar Enter):")
    private_key = input()
    print("*" * len(private_key))  # Oculta la clave privada con asteriscos

    # Verificar si la dirección es válida
    if not web3.is_address(account_address):
        print("Dirección de cuenta no válida.")
        return None

    try:
        # Verificar si la clave privada es válida creando una cuenta
        account = Account.from_key(private_key)
        if account.address.lower() != account_address.lower():
            print("La clave privada no corresponde a la dirección proporcionada.")
            return None
        
        current_account = {
            'address': account_address,
            'private_key': private_key
        }
        
        # Mostrar el saldo
        consultar_saldo()
        
        return account_address
    except ValueError:
        print("Clave privada no válida.")
        return None

def consultar_saldo():
    global current_account
    if not current_account:
        print("Debe importar una cuenta primero.")
        return

    # Extraer la dirección de la cuenta del diccionario
    account_address = current_account['address'] 

    balance_wei = web3.eth.get_balance(account_address)
    balance_ether = web3.from_wei(balance_wei, 'ether')
    print(f"El saldo de la cuenta {account_address} es: {balance_ether} ETH")

def enviar_eth():
    global current_account
    if not current_account:
        print("Debe importar una cuenta primero.")
        return

    # Solicitar la dirección de destino
    receiver_address = input("Ingrese la dirección de la cuenta de destino: ")

    # Verificar si la dirección es válida
    if not web3.is_address(receiver_address):
        print("Dirección de destino no válida.")
        return

    # Solicitar la cantidad de ETH a enviar
    amount = input("Ingrese la cantidad de ETH a enviar: ")

    try:
        # Convertir la cantidad de ETH a Wei
        amount_in_wei = web3.to_wei(float(amount), 'ether')

        # Obtener el nonce de la cuenta de envío
        nonce = web3.eth.get_transaction_count(current_account['address'])

        # Construir la transacción
        transaction = {
            'nonce': nonce,
            'to': receiver_address,
            'value': amount_in_wei,
            'gas': 21000,  # Límite de gas (puedes ajustarlo según sea necesario)
            'gasPrice': web3.eth.gas_price,  # Precio del gas
            'chainId': web3.eth.chain_id
        }

        # Calcular el costo total de la transacción
        total_cost = amount_in_wei + (transaction['gas'] * transaction['gasPrice'])

        # Verificar si hay suficiente saldo
        balance = web3.eth.get_balance(current_account['address'])
        if balance < total_cost:
            print("Saldo insuficiente para realizar la transacción.")
            return

        # Mostrar los detalles de la transacción
        print(f"\nDetalles de la transacción:")
        print(f"De: {current_account['address']}")
        print(f"Para: {receiver_address}")
        print(f"Cantidad: {amount} ETH")
        print(f"Tarifa de gas estimada: {web3.from_wei(transaction['gas'] * transaction['gasPrice'], 'ether')} ETH")
        print(f"Cantidad total (incluyendo tarifa de gas): {web3.from_wei(total_cost, 'ether')} ETH")

        # Confirmar la transacción
        confirm = input("¿Confirmar la transacción? (s/n): ")
        if confirm.lower() != 's':
            print("Transacción cancelada.")
            return

        # Firmar la transacción con la clave privada
        signed_txn = web3.eth.account.sign_transaction(transaction, current_account['private_key'])

        # Enviar la transacción
        try:
            tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
            print(f"Transacción enviada. Hash de la transacción: {web3.to_hex(tx_hash)}")

            # Esperar a que la transacción sea minada
            tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
            print("Transacción confirmada. Detalles:")
            print(f"Bloque: {tx_receipt['blockNumber']}")
            print(f"Gas usado: {tx_receipt['gasUsed']}")
            print(f"Estado: {'Éxito' if tx_receipt['status'] == 1 else 'Fallido'}")
        except Exception as e:
            print(f"Error al enviar la transacción: {e}")

    except Exception as e:
        print(f"Error al procesar la transacción: {str(e)}")

def main_menu():
    while True:
        print("\nMenú Principal:")
        if current_account:
            print(f"Cuenta actual: {current_account['address']}")
        print("1. Importar cuenta")
        print("2. Consultar saldo")
        print("3. Enviar ETH")
        print("4. Salir")

        choice = input("Seleccione una opción (1, 2, 3 o 4): ")

        if choice == '1':
            importar_cuenta()
        elif choice == '2':
            consultar_saldo()
        elif choice == '3':
            enviar_eth()
        elif choice == '4':
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Por favor seleccione 1, 2, 3 o 4.")

if __name__ == "__main__":
    main_menu()
