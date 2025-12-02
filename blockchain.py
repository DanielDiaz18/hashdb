"""
Módulo principal de la mini-blockchain
Implementa las clases Block y Blockchain para encadenar registros con hash
"""

import hashlib
import json
from datetime import datetime
from typing import List, Optional, Dict, Any


class Block:
    """
    Representa un bloque (registro) en la cadena.
    Cada bloque contiene datos y un hash que depende del bloque anterior.
    """
    
    def __init__(self, block_id: int, timestamp: str, data: str, prev_hash: str):
        """
        Inicializa un nuevo bloque.
        
        Args:
            block_id: Identificador único del bloque
            timestamp: Marca de tiempo de creación
            data: Datos del bloque (transacción, mensaje, etc.)
            prev_hash: Hash del bloque anterior
        """
        self.block_id = block_id
        self.timestamp = timestamp
        self.data = data
        self.prev_hash = prev_hash
        self.hash = self.calculate_hash()
    
    def calculate_hash(self) -> str:
        """
        Calcula el hash SHA-256 del bloque basado en sus atributos.
        
        Fórmula: hash = SHA256(block_id || timestamp || data || prev_hash)
        
        Returns:
            String hexadecimal del hash calculado
        """
        # Concatenar todos los campos del bloque
        block_string = f"{self.block_id}{self.timestamp}{self.data}{self.prev_hash}"
        
        # Calcular hash SHA-256
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte el bloque a un diccionario para serialización.
        
        Returns:
            Diccionario con todos los atributos del bloque
        """
        return {
            'block_id': self.block_id,
            'timestamp': self.timestamp,
            'data': self.data,
            'prev_hash': self.prev_hash,
            'hash': self.hash
        }
    
    @staticmethod
    def from_dict(block_dict: Dict[str, Any]) -> 'Block':
        """
        Crea un bloque a partir de un diccionario.
        
        Args:
            block_dict: Diccionario con los datos del bloque
            
        Returns:
            Instancia de Block
        """
        block = Block(
            block_dict['block_id'],
            block_dict['timestamp'],
            block_dict['data'],
            block_dict['prev_hash']
        )
        # Preservar el hash original (puede estar corrupto para pruebas)
        block.hash = block_dict['hash']
        return block
    
    def __str__(self) -> str:
        """Representación en string del bloque para mostrar en consola."""
        return (
            f"\n{'='*60}\n"
            f"Bloque #{self.block_id}\n"
            f"{'-'*60}\n"
            f"Timestamp:    {self.timestamp}\n"
            f"Datos:        {self.data}\n"
            f"Hash Previo:  {self.prev_hash}\n"
            f"Hash Actual:  {self.hash}\n"
            f"{'='*60}"
        )


class Blockchain:
    """
    Representa la cadena completa de bloques.
    Gestiona la creación, validación y persistencia de la blockchain.
    """
    
    def __init__(self):
        """Inicializa la blockchain con el bloque génesis."""
        self.chain: List[Block] = []
        self.create_genesis_block()
    
    def create_genesis_block(self) -> None:
        """
        Crea el primer bloque de la cadena (bloque génesis).
        Este bloque no tiene predecesor, por lo que su prev_hash es "0".
        """
        genesis_block = Block(
            block_id=0,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            data="Bloque Génesis - Inicio de la cadena",
            prev_hash="0"
        )
        self.chain.append(genesis_block)
    
    def get_latest_block(self) -> Block:
        """
        Obtiene el último bloque de la cadena.
        
        Returns:
            El bloque más reciente
        """
        return self.chain[-1]
    
    def add_block(self, data: str) -> Block:
        """
        Agrega un nuevo bloque al final de la cadena.
        
        Args:
            data: Datos a almacenar en el bloque
            
        Returns:
            El bloque recién creado
        """
        latest_block = self.get_latest_block()
        new_block = Block(
            block_id=latest_block.block_id + 1,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            data=data,
            prev_hash=latest_block.hash
        )
        self.chain.append(new_block)
        return new_block
    
    def verify_chain(self) -> tuple[bool, List[str]]:
        """
        Verifica la integridad de toda la cadena de bloques.
        
        Comprueba:
        1. Que el hash de cada bloque sea correcto (recalculándolo)
        2. Que el prev_hash de cada bloque coincida con el hash del anterior
        
        Returns:
            Tupla (es_válida, lista_de_errores)
        """
        errors = []
        
        # El bloque génesis (índice 0) se verifica solo recalculando su hash
        genesis = self.chain[0]
        if genesis.hash != genesis.calculate_hash():
            errors.append(f"❌ Bloque #{genesis.block_id}: Hash corrupto (no coincide con el calculado)")
        
        # Verificar el resto de bloques
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Verificar que el hash del bloque actual sea correcto
            if current_block.hash != current_block.calculate_hash():
                errors.append(
                    f"❌ Bloque #{current_block.block_id}: Hash corrupto\n"
                    f"   Hash almacenado: {current_block.hash}\n"
                    f"   Hash calculado:  {current_block.calculate_hash()}"
                )
            
            # Verificar que el prev_hash apunte al bloque anterior
            if current_block.prev_hash != previous_block.hash:
                errors.append(
                    f"❌ Bloque #{current_block.block_id}: Enlace roto con bloque anterior\n"
                    f"   prev_hash esperado: {previous_block.hash}\n"
                    f"   prev_hash actual:   {current_block.prev_hash}"
                )
        
        is_valid = len(errors) == 0
        return is_valid, errors
    
    def display_chain(self) -> None:
        """Muestra todos los bloques de la cadena en consola."""
        print(f"\n{'#'*60}")
        print(f"  BLOCKCHAIN - Total de bloques: {len(self.chain)}")
        print(f"{'#'*60}")
        
        for block in self.chain:
            print(block)
    
    def save_to_file(self, filename: str = "blockchain.json") -> None:
        """
        Guarda la blockchain en un archivo JSON.
        
        Args:
            filename: Nombre del archivo donde guardar
        """
        chain_data = [block.to_dict() for block in self.chain]
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(chain_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Blockchain guardada en '{filename}'")
    
    def load_from_file(self, filename: str = "blockchain.json") -> bool:
        """
        Carga la blockchain desde un archivo JSON.
        
        Args:
            filename: Nombre del archivo a cargar
            
        Returns:
            True si se cargó exitosamente, False en caso contrario
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                chain_data = json.load(f)
            
            self.chain = [Block.from_dict(block_dict) for block_dict in chain_data]
            print(f"\n✅ Blockchain cargada desde '{filename}' ({len(self.chain)} bloques)")
            return True
            
        except FileNotFoundError:
            print(f"\n⚠️  Archivo '{filename}' no encontrado. Se creará una nueva blockchain.")
            return False
        except json.JSONDecodeError:
            print(f"\n❌ Error al leer '{filename}'. El archivo está corrupto.")
            return False
        except Exception as e:
            print(f"\n❌ Error inesperado al cargar blockchain: {e}")
            return False
    
    def get_block_by_id(self, block_id: int) -> Optional[Block]:
        """
        Busca un bloque por su ID.
        
        Args:
            block_id: ID del bloque a buscar
            
        Returns:
            El bloque encontrado o None si no existe
        """
        for block in self.chain:
            if block.block_id == block_id:
                return block
        return None
    
    def corrupt_block(self, block_id: int, new_data: str) -> bool:
        """
        Simula un ataque: modifica los datos de un bloque sin recalcular hashes.
        Esta función es para demostrar la detección de alteraciones.
        
        Args:
            block_id: ID del bloque a corromper
            new_data: Nuevos datos a insertar (sin actualizar el hash)
            
        Returns:
            True si se modificó el bloque, False si no se encontró
        """
        block = self.get_block_by_id(block_id)
        if block:
            print(f"\n⚠️  SIMULACIÓN DE ATAQUE:")
            print(f"   Modificando datos del bloque #{block_id}")
            print(f"   Datos originales: {block.data}")
            print(f"   Nuevos datos:     {new_data}")
            print(f"   (El hash NO se recalculará - esto romperá la cadena)")
            
            block.data = new_data
            # Intencionalmente NO recalculamos el hash
            # block.hash = block.calculate_hash()  # <-- Esto NO se hace
            
            return True
        return False
