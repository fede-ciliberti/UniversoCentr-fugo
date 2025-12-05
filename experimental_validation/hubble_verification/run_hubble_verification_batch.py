#!/usr/bin/env python3
"""
Script orquestador para la verificación por lotes de la Ley de Hubble.
Tarea 4 del Plan de Verificación.

Este script busca todos los resultados de simulaciones BSSN y ejecuta
el script de análisis 'verify_hubble_law.py' para cada uno.
"""
import subprocess
import os
import glob

def run_command(command):
    """Ejecuta un comando y captura su salida."""
    print(f'\n---> Ejecutando: {" ".join(command)}')
    try:
        result = subprocess.run(command, check=True, text=True, capture_output=True)
        print(result.stdout)
        if result.stderr:
            print(f'Salida de error: {result.stderr}')
        print(f'---> ¡Comando completado exitosamente!')
        return True
    except subprocess.CalledProcessError as e:
        print(f'¡ERROR! El comando falló con el código de salida {e.returncode}')
        print(f'Salida: {e.stdout}')
        print(f'Error: {e.stderr}')
        return False

def main():
    """Función principal que orquesta el análisis por lotes."""
    print('=' * 80)
    print('INICIO DE LA VERIFICACIÓN POR LOTES DE LA LEY DE HUBBLE')
    print('=' * 80)
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    results_archive_dir = os.path.join(base_dir, '..', 'results_archive', 'simulation_outputs')
    
    print(f'Buscando resultados de simulación en: {results_archive_dir}')
    
    simulation_files = glob.glob(os.path.join(results_archive_dir, '**', 'simulation_results.npz'), recursive=True)
    
    if not simulation_files:
        print('\n⚠️ No se encontraron archivos \'simulation_results.npz\'.')
        print('Asegúrese de que las simulaciones de la Tarea 3 se hayan completado.')
        return

    print(f'\nEncontrados {len(simulation_files)} archivos de resultados para analizar.')
    
    successful_analyses = 0
    for filepath in simulation_files:
        print(f'\n{"="*30} ANALIZANDO: {os.path.relpath(filepath, base_dir)} {"="*30}')
        
        analysis_command = [
            'python3',
            os.path.join(base_dir, 'verify_hubble_law.py'),
            '--filepath', filepath
        ]
        
        # Cambiar al directorio del script de análisis para que los reportes se guarden allí
        original_cwd = os.getcwd()
        os.chdir(base_dir)
        
        if run_command(analysis_command):
            successful_analyses += 1
        
        os.chdir(original_cwd)

    print(f'\n{"="*80}')
    print('VERIFICACIÓN POR LOTES COMPLETADA')
    print(f'Se analizaron exitosamente {successful_analyses} de {len(simulation_files)} simulaciones.')
    print('=' * 80)

if __name__ == '__main__':
    main()