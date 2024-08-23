from web3 import Web3
from eth_account import Account
from eth_keyfile import KeyFile

# Conectar al servidor RPC de Ganache
ganache_url = "http://127.0.0.1:7545"  # Cambia esto si usas otra red
web3 = Web3(Web3.HTTPProvider(ganache_url))

# Verificar si la conexión se estableció correctamente
if web3.is_connected():
    print("Conectado a Ganache!")
else:
    print("Error al conectar a Ganache.")
    exit()

def importar_cuenta():
    # Solicitar al usuario la dirección de la cuenta y la clave privada
    account_address = input("Ingrese la dirección de la cuenta: ")
    private_key = input("Ingrese la clave privada de la cuenta: ")

    # Verificar si la dirección es válida
    if not web3.is_address(account_address):
        print("Dirección de cuenta no válida.")
        return None

    # Crear un nuevo almacenamiento de claves
    keyfile = KeyFile()
    keyfile.create_keyfile("my_wallet.json", private_key)

    # Mostrar el saldo
    balance_wei = web3.eth.get_balance(account_address)
    balance_ether = web3.from_wei(balance_wei, 'ether')
    print(f"El saldo de la cuenta {account_address} es: {balance_ether} ETH")

    return account_address  # Devuelve la dirección de la cuenta

def enviar_eth(account_address):
    if not account_address:
        print("Debe importar una cuenta primero.")
        return

    # Solicitar la dirección de destino
    to_address = input("Ingrese la dirección de la cuenta de destino: ")

    # Verificar si la dirección es válida
    if not web3.is_address(to_address):
        print("Dirección de destino no válida.")
        return

    # Solicitar la cantidad de ETH a enviar
    amount = input("Ingrese la cantidad de ETH a enviar: ")

    # Convertir la cantidad de ETH a Wei
    try:
        amount_in_wei = web3.to_wei(float(amount), 'ether')
    except ValueError:
        print("Cantidad no válida.")
        return

    # Obtener la tarifa de gas estimada
    gas_price = web3.eth.gas_price
    gas_limit = 21000  # Valor predeterminado
    gas_fee = gas_price * gas_limit
    gas_fee_ether = web3.from_wei(gas_fee, 'ether')

    # Calcular el total
    total_amount = amount_in_wei + gas_fee

    # Mostrar los detalles de la transacción
    print(f"\nDetalles de la transacción:")
    print(f"Tarifa de gas estimada: {gas_fee_ether} ETH")
    print(f"Cantidad total (incluyendo tarifa de gas): {web3.from_wei(total_amount, 'ether')} ETH")

    # Confirmar la transacción
    confirm = input("¿Confirmar la transacción? (s/n): ")
    if confirm.lower() != 's':
        print("Transacción cancelada.")
        return

    # Crear la transacción
    tx = {
        'nonce': web3.eth.get_transaction_count(account_address),
        'to': to_address,
        'value': amount_in_wei,
        'gas': gas_limit,
        'gasPrice': gas_price
    }

    # Firmar la transacción con la clave privada
    try:
        # Importar la clave privada desde el almacenamiento
        keyfile = KeyFile()
        account = keyfile.load_keyfile("my_wallet.json", "your_password")

        signed_tx = web3.eth.account.sign_transaction(tx, account.privateKey)
        # Enviar la transacción
        try:
            tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            print(f"Transacción enviada con éxito. Hash de la transacción: {web3.to_hex(tx_hash)}")
            # Esperar la confirmación de la transacción (opcional)
            # tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
            # print(f"Transacción confirmada. Recibo: {tx_receipt}")
        except Exception as e:
            print(f"Error al enviar la transacción: {e}")
            return
    except Exception as e:
        print(f"Error al firmar la transacción: {e}")
        return

def consultar_saldo(account_address):
    if not account_address:
        print("Debe importar una cuenta primero.")
        return

    balance_wei = web3.eth.get_balance(account_address)
    balance_ether = web3.from_wei(balance_wei, 'ether')
    print(f"El saldo de la cuenta {account_address} es: {balance_ether} ETH")

def main_menu():
    current_account = None
    while True:
        print("\nMenú Principal:")
        if current_account:
            print(f"Cuenta actual: {current_account}")
        print("1. Importar cuenta")
        print("2. Consultar saldo")
        print("3. Enviar ETH")
        print("4. Salir")

        choice = input("Seleccione una opción (1, 2, 3 o 4): ")

        if choice == '1':
            current_account = importar_cuenta()
        elif choice == '2':
            if current_account:
                consultar_saldo(current_account)
            else:
                print("Debe importar una cuenta primero.")
        elif choice == '3':
            enviar_eth(current_account)
        elif choice == '4':
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Por favor seleccione 1, 2, 3 o 4.")

if __name__ == "__main__":
    main_menu()