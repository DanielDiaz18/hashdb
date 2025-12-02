"""
Aplicación principal de la mini-blockchain
Proporciona una interfaz de línea de comandos para interactuar con la blockchain
"""

import os
import sys
from blockchain import Blockchain


def clear_screen():
    """Limpia la pantalla de la consola."""
    os.system("clear" if os.name != "nt" else "cls")


def print_menu():
    """Muestra el menú principal."""
    print("\n" + "-" * 60)
    print("  MENÚ PRINCIPAL")
    print("-" * 60)
    print("  1. Agregar nuevo registro (bloque)")
    print("  2. Mostrar toda la cadena")
    print("  3. Verificar integridad de la cadena")
    print("  4. Guardar blockchain en archivo")
    print("  5. Cargar blockchain desde archivo")
    print("  6. 🔴 SIMULAR ATAQUE - Corromper un bloque")
    print("  7. Ver estadísticas de la blockchain")
    print("  0. Salir")
    print("-" * 60)


def add_new_block(blockchain: Blockchain):
    """
    Permite al usuario agregar un nuevo bloque a la cadena.

    Args:
        blockchain: Instancia de la blockchain
    """
    print("\n" + "=" * 60)
    print("  AGREGAR NUEVO REGISTRO")
    print("=" * 60)

    # Solicitar datos al usuario
    data = input(
        "\nIngrese los datos del registro (ej. 'Transacción: Juan -> María $100'): "
    ).strip()

    if not data:
        print("❌ Error: Los datos no pueden estar vacíos.")
        return

    # Agregar el bloque
    new_block = blockchain.add_block(data)

    print("\n✅ ¡Bloque agregado exitosamente!")
    print(new_block)


def display_chain(blockchain: Blockchain):
    """
    Muestra todos los bloques de la cadena.

    Args:
        blockchain: Instancia de la blockchain
    """
    blockchain.display_chain()


def verify_chain(blockchain: Blockchain):
    """
    Verifica la integridad de la cadena y muestra los resultados.

    Args:
        blockchain: Instancia de la blockchain
    """
    print("\n" + "=" * 60)
    print("  VERIFICACIÓN DE INTEGRIDAD")
    print("=" * 60)
    print("\nAnalizando la cadena de bloques...")

    is_valid, errors = blockchain.verify_chain()

    if is_valid:
        print("\n✅ ¡La cadena es VÁLIDA!")
        print(
            f"   Todos los {len(blockchain.chain)} bloques están correctamente encadenados."
        )
        print("   No se detectaron alteraciones.")
    else:
        print("\n❌ ¡CADENA CORRUPTA!")
        print(f"   Se encontraron {len(errors)} error(es):\n")
        for error in errors:
            print(f"   {error}\n")
        print("   ⚠️  La integridad de la blockchain ha sido comprometida.")


def simulate_attack(blockchain: Blockchain) -> Blockchain:
    """
    Simula un ataque corrompiendo un bloque seleccionado por el usuario.

    Args:
        blockchain: Instancia de la blockchain

    Returns:
        La blockchain modificada
    """
    print("\n" + "=" * 60)
    print("  SIMULAR ATAQUE - CORROMPER BLOQUE")
    print("=" * 60)

    if len(blockchain.chain) < 2:
        print(
            "\n❌ Error: La blockchain debe tener al menos 2 bloques para simular un ataque."
        )
        return blockchain

    try:
        block_id = int(
            input(
                f"\nIngrese el ID del bloque a corromper (1 - {len(blockchain.chain)-1}): "
            )
        )
    except ValueError:
        print("❌ Error: ID inválido.")
        return blockchain

    if block_id < 1 or block_id >= len(blockchain.chain):
        print("❌ Error: ID fuera de rango.")
        return blockchain

    new_data = input("Ingrese los nuevos datos corruptos para el bloque: ").strip()
    if not new_data:
        print("❌ Error: Los datos no pueden estar vacíos.")
        return blockchain

    blockchain.corrupt_block(block_id, new_data)
    print(f"\n✅ Bloque #{block_id} corrompido exitosamente.")

    return blockchain


def save_blockchain(blockchain: Blockchain):
    """
    Guarda la blockchain en un archivo.

    Args:
        blockchain: Instancia de la blockchain
    """
    print("\n" + "=" * 60)
    print("  GUARDAR BLOCKCHAIN")
    print("=" * 60)

    filename = input(
        "\nNombre del archivo (presione Enter para 'blockchain.json'): "
    ).strip()
    if not filename:
        filename = "blockchain.json"

    if not filename.endswith(".json"):
        filename += ".json"

    blockchain.save_to_file(filename)


def load_blockchain(blockchain: Blockchain) -> Blockchain:
    """
    Carga la blockchain desde un archivo.

    Args:
        blockchain: Instancia actual de la blockchain

    Returns:
        La blockchain cargada o la original si falla
    """
    print("\n" + "=" * 60)
    print("  CARGAR BLOCKCHAIN")
    print("=" * 60)

    filename = input(
        "\nNombre del archivo (presione Enter para 'blockchain.json'): "
    ).strip()
    if not filename:
        filename = "blockchain.json"

    if not filename.endswith(".json"):
        filename += ".json"

    new_blockchain = Blockchain()
    if new_blockchain.load_from_file(filename):
        return new_blockchain
    else:
        print("\n⚠️  Se mantendrá la blockchain actual.")
        return blockchain


def main():
    """Función principal de la aplicación."""

    blockchain = Blockchain()

    temp_blockchain = Blockchain()
    if temp_blockchain.load_from_file("blockchain.json"):
        blockchain = temp_blockchain

    # Bucle principal
    while True:
        print_menu()

        choice = input("\nSeleccione una opción: ").strip()

        if choice == "1":
            add_new_block(blockchain)
        elif choice == "2":
            display_chain(blockchain)
        elif choice == "3":
            verify_chain(blockchain)
        elif choice == "4":
            save_blockchain(blockchain)
        elif choice == "5":
            blockchain = load_blockchain(blockchain)
        elif choice == "6":
            blockchain = simulate_attack(blockchain)
        elif choice == "0":
            blockchain.save_to_file()
            sys.exit(0)
        else:
            print("\n❌ Opción inválida. Intente nuevamente.")

        input("\nPresione Enter para continuar...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
