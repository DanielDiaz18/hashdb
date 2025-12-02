"""
Script de demostración automática de la mini-blockchain
Ejecuta una serie de operaciones para mostrar todas las funcionalidades
"""

import sys
from blockchain import Blockchain
import time


def demo():
    """Ejecuta una demostración completa del sistema."""

    # 1. Crear blockchain
    print("\n[1] Creando nueva blockchain...")
    blockchain = Blockchain()
    print("✅ Blockchain inicializada con bloque génesis")
    time.sleep(1)

    # 2. Agregar bloques
    print("\n" + "-" * 70)
    print("[2] Agregando bloques de ejemplo...")
    print("-" * 70)

    transactions = [
        "Transacción #1: Juan -> María $100",
        "Transacción #2: Pedro -> Ana $50",
        "Transacción #3: María -> Luis $75",
        "Evento: Nuevo usuario registrado - ID: 12345",
        "Log: Sistema actualizado a versión 2.0",
    ]

    for i, data in enumerate(transactions, 1):
        print(f"\n  Agregando bloque #{i}...")
        block = blockchain.add_block(data)
        print(f"  ✅ Bloque creado - Hash: {block.hash[:16]}...")
        time.sleep(0.5)

    # 3. Mostrar la cadena
    print("\n" + "-" * 70)
    print("[3] Mostrando toda la cadena:")
    print("-" * 70)
    blockchain.display_chain()
    time.sleep(2)

    # 4. Verificar integridad (primera vez)
    print("\n" + "-" * 70)
    print("[4] Verificando integridad de la cadena...")
    print("-" * 70)
    is_valid, errors = blockchain.verify_chain()
    if is_valid:
        print("\n✅ ¡La cadena es VÁLIDA!")
        print(
            f"   Todos los {len(blockchain.chain)} bloques están correctamente encadenados."
        )
    time.sleep(2)

    # 5. Guardar blockchain
    print("\n" + "-" * 70)
    print("[5] Guardando blockchain en archivo...")
    print("-" * 70)
    blockchain.save_to_file("demo_blockchain.json")
    time.sleep(1)

    # 6. Simular ataque
    print("\n" + "-" * 70)
    print("[6] 🔴 SIMULANDO ATAQUE - Corrompiendo bloque #2")
    print("-" * 70)
    print("\n⚠️  Un atacante modifica los datos del bloque #2...")
    blockchain.corrupt_block(
        2, "DATOS CORRUPTOS - Transacción fraudulenta: Hacker -> Hacker $999999"
    )
    time.sleep(1)

    # 7. Verificar integridad (después del ataque)
    print("\n" + "-" * 70)
    print("[7] Verificando integridad después del ataque...")
    print("-" * 70)
    is_valid, errors = blockchain.verify_chain()

    if not is_valid:
        print("\n❌ ¡CADENA CORRUPTA! - Ataque detectado")
        print(f"\n   Se encontraron {len(errors)} error(es):\n")
        for error in errors:
            print(f"   {error}\n")
    time.sleep(2)

    # 8. Mostrar bloque corrupto
    print("\n" + "-" * 70)
    print("[8] Mostrando el bloque corrupto:")
    print("-" * 70)
    corrupted_block = blockchain.get_block_by_id(2)
    print(corrupted_block)


if __name__ == "__main__":
    try:
        demo()
    except KeyboardInterrupt:
        sys.exit(0)
