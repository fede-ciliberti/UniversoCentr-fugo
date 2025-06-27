#!/usr/bin/env python3
"""
Configurador específico para simulación 64³ con parámetros optimizados
"""

import numpy as np
import json
import os

def create_64cubed_configuration():
    """Crea configuración optimizada para resolución 64³"""
    
    print("🔧 CONFIGURANDO SIMULACIÓN 64³")
    print("=" * 40)
    
    # Configuración base para 64³
    config = {
        # Parámetros de malla
        'grid_size': 64,
        'domain_size': 20.0,  # Dominio espacial [-10, +10] en cada dirección
        
        # Parámetros temporales (ajustados para estabilidad en alta resolución)
        'dt': 0.008,  # Paso temporal más pequeño para estabilidad
        't_final': 1.5,  # Tiempo final un poco mayor
        
        # Parámetros físicos (valores actuales - conservadores)
        'R_param': 1.0,
        'omega_4d_param': 0.1,
        
        # Configuración de salida
        'output_every': 10,  # Salida cada 10 pasos
        'checkpoint_every': 25,  # Checkpoint cada 25 pasos
        
        # Estimaciones
        'estimated_time_hours': 1.3,
        'estimated_memory_gb': 0.1,
        
        # Metadatos
        'description': "Simulación 64³ - Verificación de escalamiento con parámetros conservadores",
        'purpose': "Confirmar que efectos de 32³ escalan correctamente"
    }
    
    # Calcular parámetros derivados
    n_steps = int(config['t_final'] / config['dt'])
    config['n_steps'] = n_steps
    
    print(f"📊 Configuración generada:")
    print(f"   Resolución: {config['grid_size']}³ = {config['grid_size']**3:,} puntos")
    print(f"   Dominio: [{-config['domain_size']/2:.1f}, +{config['domain_size']/2:.1f}]³")
    print(f"   Paso temporal: dt = {config['dt']}")
    print(f"   Tiempo final: t = {config['t_final']}")
    print(f"   Número de pasos: {n_steps:,}")
    print(f"   Tiempo estimado: {config['estimated_time_hours']:.1f} horas")
    
    print(f"\n🧪 Parámetros físicos:")
    print(f"   R_param = {config['R_param']} (radio 3-esfera)")
    print(f"   omega_4d_param = {config['omega_4d_param']} (velocidad angular 4D)")
    
    # Calcular cantidades físicas derivadas
    v_tangential = config['omega_4d_param'] * config['R_param']
    period_4d = 2 * np.pi / config['omega_4d_param']
    H0_effective = config['omega_4d_param'] / (2 * np.pi)
    
    print(f"\n📐 Cantidades derivadas:")
    print(f"   Velocidad tangencial 4D: {v_tangential:.3f}")
    print(f"   Período rotación 4D: {period_4d:.1f} unidades")
    print(f"   H₀ efectiva: {H0_effective:.6f}")
    
    return config

def save_configuration(config, filename="config_64cubed.json"):
    """Guarda la configuración en archivo JSON"""
    with open(filename, 'w') as f:
        json.dump(config, f, indent=2)
    print(f"\n💾 Configuración guardada: {filename}")
    return filename

def create_custom_simulation_script(config):
    """Crea script de simulación personalizado para 64³"""
    
    script_content = f'''#!/usr/bin/env python3
"""
Script de simulación personalizado para resolución 64³
Generado automáticamente con configuración optimizada
"""

import numpy as np
import time
import json
from pathlib import Path

# Importar funciones del sistema de simulación
import sys
sys.path.append('notebooks')

from setup_numerical_simulation import setup_simulation_data
from run_numerical_simulation import run_einstein_simulation

def main():
    """Ejecuta simulación 64³ con configuración personalizada"""
    
    print("🚀 SIMULACIÓN EINSTEIN 64³ - CONFIGURACIÓN PERSONALIZADA")
    print("=" * 70)
    
    # Cargar configuración
    with open('config_64cubed.json', 'r') as f:
        config = json.load(f)
    
    print(f"📊 Configuración cargada:")
    print(f"   Resolución: {{config['grid_size']}}³")
    print(f"   Tiempo estimado: {{config['estimated_time_hours']}} horas")
    print(f"   Parámetros físicos: R={{config['R_param']}}, ω₄D={{config['omega_4d_param']}}")
    
    # Generar datos iniciales
    print(f"\\n🔧 Generando datos iniciales...")
    setup_simulation_data(
        grid_size=config['grid_size'],
        domain_size=config['domain_size'],
        R_param=config['R_param'],
        omega_4d_param=config['omega_4d_param']
    )
    
    # Ejecutar simulación
    print(f"\\n🚀 Iniciando simulación...")
    start_time = time.time()
    
    results = run_einstein_simulation(
        dt=config['dt'],
        t_final=config['t_final'],
        output_every=config['output_every'],
        checkpoint_every=config['checkpoint_every']
    )
    
    end_time = time.time()
    elapsed_hours = (end_time - start_time) / 3600
    
    print(f"\\n✅ Simulación completada!")
    print(f"⏱️  Tiempo real: {{elapsed_hours:.2f}} horas")
    print(f"📈 Estimación era: {{config['estimated_time_hours']:.1f}} horas")
    print(f"🎯 Precisión estimación: {{(elapsed_hours/config['estimated_time_hours'])*100:.1f}}%")
    
    # Guardar metadatos de la ejecución
    execution_metadata = {{
        'actual_time_hours': elapsed_hours,
        'estimated_time_hours': config['estimated_time_hours'],
        'execution_date': time.strftime('%Y-%m-%d %H:%M:%S'),
        'configuration_used': config
    }}
    
    with open('execution_metadata_64cubed.json', 'w') as f:
        json.dump(execution_metadata, f, indent=2)
    
    print(f"💾 Metadatos guardados: execution_metadata_64cubed.json")
    print(f"📊 Para analizar resultados, ejecuta: python quick_analysis.py")

if __name__ == "__main__":
    main()
'''
    
    with open('run_simulation_64cubed.py', 'w') as f:
        f.write(script_content)
    
    # Hacer ejecutable
    os.chmod('run_simulation_64cubed.py', 0o755)
    
    print(f"📝 Script personalizado creado: run_simulation_64cubed.py")
    return 'run_simulation_64cubed.py'

def offer_parameter_alternatives():
    """Ofrece configuraciones alternativas con diferentes parámetros"""
    
    print(f"\n🎮 CONFIGURACIONES ALTERNATIVAS DISPONIBLES")
    print("=" * 50)
    
    alternatives = [
        {
            'name': 'Conservadora',
            'R_param': 1.0,
            'omega_4d_param': 0.1,
            'description': 'Configuración actual - efectos moderados'
        },
        {
            'name': 'Efectos Pronunciados',
            'R_param': 1.0,
            'omega_4d_param': 0.2,
            'description': 'Doble velocidad angular - efectos más fuertes'
        },
        {
            'name': 'Estructura Grande',
            'R_param': 2.0,
            'omega_4d_param': 0.1,
            'description': 'Radio mayor - efectos a gran escala'
        },
        {
            'name': 'Efectos Máximos',
            'R_param': 2.0,
            'omega_4d_param': 0.2,
            'description': 'Ambos parámetros aumentados - máximos efectos'
        },
        {
            'name': 'Efectos Sutiles',
            'R_param': 1.0,
            'omega_4d_param': 0.05,
            'description': 'Velocidad reducida - efectos más sutiles'
        }
    ]
    
    for i, alt in enumerate(alternatives, 1):
        v_tang = alt['omega_4d_param'] * alt['R_param']
        H0_eff = alt['omega_4d_param'] / (2 * np.pi)
        
        print(f"\\n{i}. {alt['name']}:")
        print(f"   R = {alt['R_param']}, ω₄D = {alt['omega_4d_param']}")
        print(f"   v₄D = {v_tang:.3f}, H₀eff = {H0_eff:.6f}")
        print(f"   {alt['description']}")
    
    return alternatives

def main():
    """Función principal"""
    
    # Crear configuración base
    config = create_64cubed_configuration()
    
    # Guardar configuración
    config_file = save_configuration(config)
    
    # Crear script personalizado
    script_file = create_custom_simulation_script(config)
    
    # Mostrar alternativas
    alternatives = offer_parameter_alternatives()
    
    print(f"\\n🎯 PRÓXIMOS PASOS:")
    print("=" * 20)
    print(f"1. ✅ Configuración 64³ lista")
    print(f"2. 🚀 Para ejecutar con parámetros actuales:")
    print(f"   python {script_file}")
    print(f"\\n3. 🎮 Para modificar parámetros:")
    print(f"   Edita {config_file} y luego ejecuta el script")
    print(f"\\n4. 📊 Para analizar resultados después:")
    print(f"   python quick_analysis.py")
    
    print(f"\\n❓ ¿Quieres ejecutar ahora con la configuración conservadora?")
    print(f"   Los parámetros (R=1.0, ω=0.1) deberían dar resultados similares")
    print(f"   pero más detallados que tu simulación 32³ exitosa.")

if __name__ == "__main__":
    main()