# Billetera Ethereum con Python y Web3

Este programa en Python lo desarrollé para interactuar con la blockchain de Ethereum a través de un servidor local como Ganache utilizando la biblioteca `web3.py`. El objetivo del programa es facilitar la gestión básica de cuentas de Ethereum, permitiéndome importar cuentas, consultar saldos y enviar ETH a otras direcciones de manera sencilla desde la línea de comandos.

## Funcionalidades del Programa

### 1. Conectar a una Red Ethereum

El programa se conecta a una red Ethereum local, como Ganache, utilizando una conexión RPC. Esto me permite interactuar con la blockchain simulada en mi máquina local, lo que es ideal para pruebas y desarrollo sin costos reales.

### 2. Importar una Cuenta Ethereum

Puedo importar una cuenta de Ethereum ingresando la dirección de la cuenta y la clave privada. El programa valida que tanto la dirección como la clave privada sean correctas. Si la clave privada corresponde a la dirección ingresada, se almacena la cuenta como la cuenta actual en uso. Esta función es esencial para interactuar con la blockchain ya que cualquier operación requiere de una cuenta válida.

### 3. Consultar el Saldo de una Cuenta

Una vez que la cuenta ha sido importada, puedo consultar el saldo actual en ETH. El programa obtiene el saldo de la cuenta de la blockchain simulada (Ganache) y lo muestra en la consola. Esta funcionalidad me permite verificar si tengo suficientes fondos antes de realizar cualquier transacción.

### 4. Enviar ETH a Otra Dirección

El programa permite enviar ETH desde la cuenta importada a cualquier otra dirección de Ethereum. Para hacer esto, solicito la dirección de destino y la cantidad de ETH que quiero enviar. El programa calcula el costo total de la transacción, incluidas las tarifas de gas, y verifica si hay suficiente saldo en la cuenta para cubrir estos costos. Si todo está en orden, el programa firma y envía la transacción utilizando la clave privada de la cuenta importada, luego espera a que la transacción sea confirmada en la blockchain.

### 5. Menú Interactivo

El programa utiliza un menú interactivo basado en la consola que me permite seleccionar fácilmente las operaciones que quiero realizar. Las opciones incluyen importar una cuenta, consultar el saldo, enviar ETH y salir del programa. Este menú es útil para navegar por las diferentes funcionalidades sin necesidad de recordar comandos específicos.

## Consideraciones de Seguridad

- **Gestión de Claves Privadas**: Este programa solicita la clave privada de una cuenta de Ethereum para realizar transacciones. **Es importante nunca compartir esta clave ni almacenarla en un lugar inseguro**, ya que da acceso completo a los fondos de la cuenta.
- **Validaciones de Entrada**: El programa incluye validaciones para asegurar que las direcciones de Ethereum sean válidas y que los fondos sean suficientes antes de intentar cualquier transacción, ayudando a evitar errores comunes y pérdidas accidentales.

## Requisitos Técnicos

- **Python 3.6+**: El programa está escrito en Python, por lo que necesitaré tener una versión compatible instalada.
- **Ganache**: Utilizo Ganache para simular una red local de Ethereum, lo que facilita el desarrollo y prueba de transacciones sin costos reales.
- **web3.py**: Esta biblioteca es esencial para interactuar con la blockchain de Ethereum. Se puede instalar usando pip:

   ```bash
   pip install web3
