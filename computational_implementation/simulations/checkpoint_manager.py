#!/usr/bin/env python3
"""
Sistema de Checkpoints Robusto para Simulaciones BSSN
Implementa guardado automático, recuperación inteligente y validación de integridad

Fecha: 14 de diciembre de 2025
Autor: Universo Centrífugo Research Team
"""

import os
import time
import json
import hashlib
import numpy as np
import pickle
import gzip
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CheckpointManager:
    """
    Gestor de checkpoints robusto con múltiples niveles de guardado
    y recuperación inteligente de simulaciones interrumpidas.
    """
    
    def __init__(self, checkpoint_dir: str = "checkpoints", 
                 frequent_interval: int = 100,
                 periodic_interval: int = 1000,
                 max_checkpoints: int = 10,
                 compression_level: int = 6):
        """
        Inicializa el gestor de checkpoints.
        
        Args:
            checkpoint_dir: Directorio para almacenar checkpoints
            frequent_interval: Intervalo de pasos para checkpoints frecuentes
            periodic_interval: Intervalo de pasos para checkpoints periódicos
            max_checkpoints: Número máximo de checkpoints a mantener
            compression_level: Nivel de compresión (1-9)
        """
        self.checkpoint_dir = Path(checkpoint_dir)
        self.checkpoint_dir.mkdir(exist_ok=True)
        
        self.frequent_interval = frequent_interval
        self.periodic_interval = periodic_interval
        self.max_checkpoints = max_checkpoints
        self.compression_level = compression_level
        
        # Metadatos de checkpoints
        self.metadata_file = self.checkpoint_dir / "checkpoint_metadata.json"
        self.metadata = self._load_metadata()
        
        logger.info(f"CheckpointManager inicializado:")
        logger.info(f"  Directorio: {self.checkpoint_dir}")
        logger.info(f"  Intervalo frecuente: {frequent_interval} pasos")
        logger.info(f"  Intervalo periódico: {periodic_interval} pasos")
        logger.info(f"  Máximo checkpoints: {max_checkpoints}")
    
    def _load_metadata(self) -> Dict:
        """Carga metadatos de checkpoints desde archivo"""
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Error cargando metadatos: {e}")
        
        return {
            'checkpoints': {},
            'last_checkpoint': None,
            'simulation_params': {}
        }
    
    def _save_metadata(self):
        """Guarda metadatos de checkpoints a archivo"""
        try:
            with open(self.metadata_file, 'w') as f:
                json.dump(self.metadata, f, indent=2)
        except Exception as e:
            logger.error(f"Error guardando metadatos: {e}")
    
    def _compute_checksum(self, data: Dict) -> str:
        """Calcula checksum SHA-256 para verificar integridad"""
        data_bytes = pickle.dumps(data)
        return hashlib.sha256(data_bytes).hexdigest()
    
    def _compress_data(self, data: Dict) -> bytes:
        """Comprime datos usando gzip"""
        data_bytes = pickle.dumps(data)
        return gzip.compress(data_bytes, compresslevel=self.compression_level)
    
    def _decompress_data(self, compressed_data: bytes) -> Dict:
        """Descomprime datos gzip"""
        data_bytes = gzip.decompress(compressed_data)
        return pickle.loads(data_bytes)
    
    def _create_checkpoint_filename(self, step: int, checkpoint_type: str) -> str:
        """Crea nombre de archivo para checkpoint"""
        timestamp = int(time.time())
        return f"checkpoint_{checkpoint_type}_step_{step:06d}_{timestamp}.chk"
    
    def _cleanup_old_checkpoints(self, checkpoint_type: str):
        """Elimina checkpoints antiguos manteniendo solo los más recientes"""
        checkpoints = self.metadata['checkpoints'].get(checkpoint_type, [])
        
        if len(checkpoints) > self.max_checkpoints:
            # Ordenar por paso y eliminar los más antiguos
            checkpoints.sort(key=lambda x: x['step'])
            
            for checkpoint in checkpoints[:-self.max_checkpoints]:
                try:
                    os.remove(checkpoint['filepath'])
                    logger.info(f"Eliminado checkpoint antiguo: {checkpoint['filepath']}")
                except Exception as e:
                    logger.warning(f"Error eliminando checkpoint {checkpoint['filepath']}: {e}")
            
            # Actualizar metadatos
            self.metadata['checkpoints'][checkpoint_type] = checkpoints[-self.max_checkpoints:]
    
    def save_checkpoint(self, step: int, t: float, simulation_state: Dict, 
                       simulation_params: Dict = None) -> Optional[str]:
        """
        Guarda un checkpoint de la simulación.
        
        Args:
            step: Paso actual de la simulación
            t: Tiempo actual de la simulación
            simulation_state: Estado completo de la simulación
            simulation_params: Parámetros de la simulación
            
        Returns:
            Ruta del archivo guardado o None si no se guardó
        """
        # Determinar tipo de checkpoint
        checkpoint_type = None
        if step % self.periodic_interval == 0:
            checkpoint_type = 'periodic'
        elif step % self.frequent_interval == 0:
            checkpoint_type = 'frequent'
        
        if checkpoint_type is None:
            return None
        
        try:
            # Preparar datos del checkpoint
            checkpoint_data = {
                'step': step,
                'time': t,
                'timestamp': time.time(),
                'simulation_state': simulation_state,
                'simulation_params': simulation_params or {},
                'checkpoint_type': checkpoint_type
            }
            
            # Calcular checksum
            checksum = self._compute_checksum(checkpoint_data)
            checkpoint_data['checksum'] = checksum
            
            # Comprimir datos
            compressed_data = self._compress_data(checkpoint_data)
            
            # Crear archivo
            filename = self._create_checkpoint_filename(step, checkpoint_type)
            filepath = self.checkpoint_dir / filename
            
            with open(filepath, 'wb') as f:
                f.write(compressed_data)
            
            # Actualizar metadatos
            checkpoint_info = {
                'step': step,
                'time': t,
                'timestamp': time.time(),
                'filepath': str(filepath),
                'checksum': checksum,
                'size_bytes': len(compressed_data),
                'type': checkpoint_type
            }
            
            if checkpoint_type not in self.metadata['checkpoints']:
                self.metadata['checkpoints'][checkpoint_type] = []
            
            self.metadata['checkpoints'][checkpoint_type].append(checkpoint_info)
            self.metadata['last_checkpoint'] = checkpoint_info
            
            if simulation_params:
                self.metadata['simulation_params'] = simulation_params
            
            # Limpiar checkpoints antiguos
            self._cleanup_old_checkpoints(checkpoint_type)
            
            # Guardar metadatos
            self._save_metadata()
            
            logger.info(f"Checkpoint guardado: {filename} ({len(compressed_data)/1024/1024:.2f} MB)")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"Error guardando checkpoint: {e}")
            return None
    
    def load_checkpoint(self, checkpoint_file: str = None, 
                       step: int = None, 
                       checkpoint_type: str = None) -> Tuple[Optional[Dict], Optional[Dict]]:
        """
        Carga un checkpoint de la simulación.
        
        Args:
            checkpoint_file: Ruta específica del archivo a cargar
            step: Paso específico a cargar
            checkpoint_type: Tipo de checkpoint ('frequent' o 'periodic')
            
        Returns:
            Tupla (estado_simulación, parámetros_simulación) o (None, None) si hay error
        """
        try:
            # Determinar qué checkpoint cargar
            if checkpoint_file:
                filepath = Path(checkpoint_file)
                if not filepath.exists():
                    logger.error(f"No existe el archivo: {checkpoint_file}")
                    return None, None
            else:
                # Buscar checkpoint más reciente
                checkpoint_info = self._find_best_checkpoint(step, checkpoint_type)
                if not checkpoint_info:
                    logger.info("No se encontró checkpoint adecuado")
                    return None, None
                
                filepath = Path(checkpoint_info['filepath'])
            
            # Cargar y descomprimir datos
            with open(filepath, 'rb') as f:
                compressed_data = f.read()
            
            checkpoint_data = self._decompress_data(compressed_data)
            
            # Verificar integridad
            stored_checksum = checkpoint_data.get('checksum')
            if stored_checksum:
                # Recalcular checksum sin el campo checksum
                temp_checksum = checkpoint_data.pop('checksum', None)
                computed_checksum = self._compute_checksum(checkpoint_data)
                checkpoint_data['checksum'] = temp_checksum
                
                if stored_checksum != computed_checksum:
                    logger.error(f"Checksum inválido para {filepath}")
                    return None, None
            
            logger.info(f"Checkpoint cargado: {filepath.name}")
            logger.info(f"  Paso: {checkpoint_data['step']}, Tiempo: {checkpoint_data['time']:.4f}")
            
            return checkpoint_data['simulation_state'], checkpoint_data['simulation_params']
            
        except Exception as e:
            logger.error(f"Error cargando checkpoint: {e}")
            return None, None
    
    def _find_best_checkpoint(self, step: int = None, 
                             checkpoint_type: str = None) -> Optional[Dict]:
        """Encuentra el mejor checkpoint disponible según criterios"""
        if step is not None:
            # Buscar checkpoint con paso específico o el más cercano anterior
            best_checkpoint = None
            best_diff = float('inf')
            
            for cptype, checkpoints in self.metadata['checkpoints'].items():
                if checkpoint_type and cptype != checkpoint_type:
                    continue
                
                for checkpoint in checkpoints:
                    diff = abs(checkpoint['step'] - step)
                    if checkpoint['step'] <= step and diff < best_diff:
                        best_diff = diff
                        best_checkpoint = checkpoint
            
            return best_checkpoint
        
        elif checkpoint_type:
            # Devolver el más reciente del tipo especificado
            checkpoints = self.metadata['checkpoints'].get(checkpoint_type, [])
            if checkpoints:
                return max(checkpoints, key=lambda x: x['step'])
        
        else:
            # Devolver el último checkpoint guardado
            return self.metadata.get('last_checkpoint')
        
        return None
    
    def list_checkpoints(self) -> Dict[str, List[Dict]]:
        """Lista todos los checkpoints disponibles"""
        return self.metadata['checkpoints']
    
    def get_latest_checkpoint(self) -> Optional[Dict]:
        """Devuelve información del checkpoint más reciente"""
        return self.metadata.get('last_checkpoint')
    
    def validate_checkpoint(self, checkpoint_file: str) -> bool:
        """
        Valida la integridad de un checkpoint.
        
        Args:
            checkpoint_file: Ruta del archivo a validar
            
        Returns:
            True si el checkpoint es válido, False en caso contrario
        """
        try:
            filepath = Path(checkpoint_file)
            if not filepath.exists():
                return False
            
            # Cargar y verificar checksum
            with open(filepath, 'rb') as f:
                compressed_data = f.read()
            
            checkpoint_data = self._decompress_data(compressed_data)
            
            stored_checksum = checkpoint_data.get('checksum')
            if not stored_checksum:
                return False
            
            temp_checksum = checkpoint_data.pop('checksum', None)
            computed_checksum = self._compute_checksum(checkpoint_data)
            checkpoint_data['checksum'] = temp_checksum
            
            return stored_checksum == computed_checksum
            
        except Exception as e:
            logger.error(f"Error validando checkpoint: {e}")
            return False
    
    def cleanup_all_checkpoints(self):
        """Elimina todos los checkpoints y metadatos"""
        try:
            for checkpoint_type, checkpoints in self.metadata['checkpoints'].items():
                for checkpoint in checkpoints:
                    try:
                        os.remove(checkpoint['filepath'])
                    except Exception as e:
                        logger.warning(f"Error eliminando {checkpoint['filepath']}: {e}")
            
            if self.metadata_file.exists():
                os.remove(self.metadata_file)
            
            self.metadata = {'checkpoints': {}, 'last_checkpoint': None, 'simulation_params': {}}
            logger.info("Todos los checkpoints eliminados")
            
        except Exception as e:
            logger.error(f"Error en limpieza: {e}")
    
    def get_checkpoint_stats(self) -> Dict:
        """Devuelve estadísticas de los checkpoints"""
        stats = {
            'total_checkpoints': 0,
            'total_size_mb': 0,
            'by_type': {},
            'latest_step': 0,
            'oldest_step': float('inf')
        }
        
        for checkpoint_type, checkpoints in self.metadata['checkpoints'].items():
            type_stats = {
                'count': len(checkpoints),
                'size_mb': sum(c['size_bytes'] for c in checkpoints) / 1024 / 1024,
                'latest_step': max(c['step'] for c in checkpoints) if checkpoints else 0,
                'oldest_step': min(c['step'] for c in checkpoints) if checkpoints else 0
            }
            
            stats['by_type'][checkpoint_type] = type_stats
            stats['total_checkpoints'] += type_stats['count']
            stats['total_size_mb'] += type_stats['size_mb']
            
            if type_stats['latest_step'] > stats['latest_step']:
                stats['latest_step'] = type_stats['latest_step']
            
            if type_stats['oldest_step'] < stats['oldest_step']:
                stats['oldest_step'] = type_stats['oldest_step']
        
        return stats