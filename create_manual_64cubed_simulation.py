#!/usr/bin/env python3
"""
Configuración manual para simulación 64³ sin usar el optimizador automático
"""

import numpy as np
import json
import sys
import os

# Agregar path a notebooks
sys.path.append('notebooks')

# Importar funciones necesarias
try:
    from setup_numerical_simulation import main as setup_main
    from run_numerical_simulation import run_einstein_simulation
except ImportError:
    print("❌ Error importando funciones. Ejecutando directamente...")

def create_64cubed_config():
    """Crea configuración específica para 64³"""
    config = {
        "system_type": "custom_64cubed",
        "resolution": 64,
        "grid_size": 64,
        "domain_size": 20.0,
        "dt": 0.008,
        "t_final": 1.5,
        "n_steps": 187,
        "output_every": 10,
        "checkpoint_every": 25,
        "estimated_time_minutes": 80,
        "estimated_memory_gb": 0.1,
        "R_param": 1.0,
        "omega_4d_param": 0.1
    }
    
    with open('manual_64cubed_config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print("✅ Configuración 64³ creada: manual_64cubed_config.json")
    return config

def generate_64cubed_script():
    """Genera script específico para 64³"""
    script_content = '''#!/usr/bin/env python3
"""
Simulación manual 64³ con parámetros específicos
"""

import numpy as np
import subprocess
import time
import sys
import os

def run_simulation_64cubed():
    """Ejecuta simulación 64³ paso a paso"""
    
    print("🚀 SIMULACIÓN MANUAL 64³")
    print("=" * 40)
    print("Parámetros: R=1.0, ω₄D=0.1")
    print("Resolución: 64³ = 262,144 puntos")
    print("Tiempo estimado: 1.3 horas")
    
    start_time = time.time()
    
    # Paso 1: Generar datos iniciales 64³
    print("\\n🔧 Generando datos iniciales 64³...")
    
    # Crear script temporal de setup
    setup_script = """
import numpy as np
import sys
sys.path.append('notebooks')

# Parametros específicos para 64³
grid_size = 64
domain_size = 20.0
R_param = 1.0
omega_4d_param = 0.1

# Generar malla
x = np.linspace(-domain_size/2, domain_size/2, grid_size)
y = np.linspace(-domain_size/2, domain_size/2, grid_size)
z = np.linspace(-domain_size/2, domain_size/2, grid_size)

dx = x[1] - x[0]
dy = y[1] - y[0] 
dz = z[1] - z[0]

print(f"Malla 64³ generada:")
print(f"  Dominio: [{x[0]:.1f}, {x[-1]:.1f}]³")
print(f"  Espaciado: dx={dx:.3f}, dy={dy:.3f}, dz={dz:.3f}")
print(f"  Puntos totales: {grid_size**3:,}")

# Crear coordenadas 3D
X, Y, Z = np.meshgrid(x, y, z, indexing='ij')

# Calcular tensor energía-momento para rotación 4D
print("\\nCalculando tensor energía-momento...")

# Componentes de velocidad 4D en rotación isoclínica
# u = (u_t, u_x, u_y, u_z) con rotación en plano (x,w)
omega_4d = omega_4d_param
R = R_param

# Para simplificar, usamos aproximación de campo débil
# T_00 (densidad de energía)
rho_energy = 0.5 * omega_4d**2 * R**2 * np.ones_like(X)

# T_ij (presión/tensión espacial)
T_xx = 0.1 * rho_energy * (1 + 0.01 * X/R)
T_yy = 0.1 * rho_energy * (1 + 0.01 * Y/R)  
T_zz = 0.1 * rho_energy * (1 + 0.01 * Z/R)

# Términos cruzados pequeños
T_xy = 0.01 * rho_energy * X * Y / R**2
T_xz = 0.01 * rho_energy * X * Z / R**2
T_yz = 0.01 * rho_energy * Y * Z / R**2

print(f"  Densidad energía máx: {np.max(rho_energy):.6f}")
print(f"  Componente T_xx rango: [{np.min(T_xx):.6f}, {np.max(T_xx):.6f}]")

# Inicializar métrica espacial (aproximadamente plana)
gamma_xx = np.ones_like(X)
gamma_yy = np.ones_like(X)
gamma_zz = np.ones_like(X)
gamma_xy = np.zeros_like(X)
gamma_xz = np.zeros_like(X)
gamma_yz = np.zeros_like(X)

# Añadir pequeña perturbación inicial
center_x, center_y, center_z = grid_size//2, grid_size//2, grid_size//2
r_squared = (X - x[center_x])**2 + (Y - y[center_y])**2 + (Z - z[center_z])**2
r = np.sqrt(r_squared + 1e-10)  # Evitar división por cero

# Perturbación tipo masa puntual muy pequeña
mass_param = 0.001
perturbation = mass_param / (1 + r)

gamma_xx += 0.001 * perturbation
gamma_yy += 0.001 * perturbation
gamma_zz += 0.001 * perturbation

print(f"  Perturbación inicial máx: {np.max(perturbation):.6f}")

# Inicializar curvatura extrínseca (pequeña)
K_xx = np.zeros_like(X)
K_yy = np.zeros_like(X)
K_zz = np.zeros_like(X)
K_xy = np.zeros_like(X)
K_xz = np.zeros_like(X)
K_yz = np.zeros_like(X)

# Guardar datos
print("\\nGuardando datos iniciales...")
np.savez('simulation_initial_data_64cubed.npz',
         # Malla
         x=x, y=y, z=z,
         dx=dx, dy=dy, dz=dz,
         
         # Métrica espacial inicial
         gamma_xx=gamma_xx,
         gamma_yy=gamma_yy,
         gamma_zz=gamma_zz,
         gamma_xy=gamma_xy,
         gamma_xz=gamma_xz,
         gamma_yz=gamma_yz,
         
         # Curvatura extrínseca inicial
         K_xx=K_xx,
         K_yy=K_yy,
         K_zz=K_zz,
         K_xy=K_xy,
         K_xz=K_xz,
         K_yz=K_yz,
         
         # Tensor energía-momento
         T_00=rho_energy,
         T_xx=T_xx,
         T_yy=T_yy,
         T_zz=T_zz,
         T_xy=T_xy,
         T_xz=T_xz,
         T_yz=T_yz,
         
         # Parámetros
         R_param=R_param,
         omega_4d_param=omega_4d_param,
         grid_size=grid_size,
         domain_size=domain_size
)

print("✅ Datos iniciales 64³ guardados: simulation_initial_data_64cubed.npz")
size_mb = os.path.getsize('simulation_initial_data_64cubed.npz') / (1024*1024)
print(f"   Tamaño archivo: {size_mb:.1f} MB")
"""
    
    with open('temp_setup_64cubed.py', 'w') as f:
        f.write(setup_script)
    
    try:
        result = subprocess.run('python temp_setup_64cubed.py', shell=True, check=True)
        print("✅ Datos iniciales generados")
    except subprocess.CalledProcessError:
        print("❌ Error generando datos iniciales")
        return False
    finally:
        if os.path.exists('temp_setup_64cubed.py'):
            os.remove('temp_setup_64cubed.py')
    
    # Paso 2: Ejecutar simulación adaptada
    print("\\n🚀 Ejecutando simulación 64³...")
    
    simulation_script = """
import numpy as np
import time
from numba import jit, prange
import multiprocessing as mp

# Cargar datos iniciales
print("📁 Cargando datos 64³...")
data = np.load('simulation_initial_data_64cubed.npz')

# Extraer arrays
gamma_xx = data['gamma_xx'].copy()
gamma_yy = data['gamma_yy'].copy()
gamma_zz = data['gamma_zz'].copy()
gamma_xy = data['gamma_xy'].copy()
gamma_xz = data['gamma_xz'].copy()
gamma_yz = data['gamma_yz'].copy()

K_xx = data['K_xx'].copy()
K_yy = data['K_yy'].copy()
K_zz = data['K_zz'].copy()
K_xy = data['K_xy'].copy()
K_xz = data['K_xz'].copy()
K_yz = data['K_yz'].copy()

T_00 = data['T_00']
T_xx = data['T_xx']
T_yy = data['T_yy']
T_zz = data['T_zz']

dx = float(data['dx'])
dy = float(data['dy'])
dz = float(data['dz'])

grid_size = int(data['grid_size'])
print(f"✅ Datos cargados: {grid_size}³ puntos")

# Parámetros de simulación
dt = 0.008
t_final = 1.5
n_steps = int(t_final / dt)
output_every = 10

print(f"📊 Configuración temporal:")
print(f"   dt = {dt}")
print(f"   t_final = {t_final}")
print(f"   n_steps = {n_steps}")

@jit(nopython=True, parallel=True)
def compute_derivatives(field, dx, dy, dz):
    \"\"\"Calcula derivadas espaciales con diferencias finitas\"\"\"
    nx, ny, nz = field.shape
    d_dx = np.zeros_like(field)
    d_dy = np.zeros_like(field)
    d_dz = np.zeros_like(field)
    
    for i in prange(1, nx-1):
        for j in range(1, ny-1):
            for k in range(1, nz-1):
                d_dx[i,j,k] = (field[i+1,j,k] - field[i-1,j,k]) / (2*dx)
                d_dy[i,j,k] = (field[i,j+1,k] - field[i,j-1,k]) / (2*dy)
                d_dz[i,j,k] = (field[i,j,k+1] - field[i,j,k-1]) / (2*dz)
    
    return d_dx, d_dy, d_dz

@jit(nopython=True, parallel=True)
def evolve_metric_simple(gamma_xx, gamma_yy, gamma_zz, 
                        K_xx, K_yy, K_zz, T_xx, T_yy, T_zz, dt):
    \"\"\"Evolución simplificada de la métrica\"\"\"
    
    # Evolución de la métrica: ∂γ_ij/∂t = -2αK_ij
    # (α = 1 para simplificar)
    gamma_xx_new = gamma_xx - 2.0 * dt * K_xx
    gamma_yy_new = gamma_yy - 2.0 * dt * K_yy
    gamma_zz_new = gamma_zz - 2.0 * dt * K_zz
    
    # Evolución de K: ∂K_ij/∂t ≈ fuente gravitacional
    # Simplificado: K evoluciona debido al tensor energía-momento
    source_strength = 0.01  # Factor pequeño para estabilidad
    
    K_xx_new = K_xx + dt * source_strength * T_xx
    K_yy_new = K_yy + dt * source_strength * T_yy
    K_zz_new = K_zz + dt * source_strength * T_zz
    
    return gamma_xx_new, gamma_yy_new, gamma_zz_new, K_xx_new, K_yy_new, K_zz_new

# Listas para almacenar evolución
times = []
metric_evolution = []

print("\\n🚀 Iniciando evolución temporal...")
start_time = time.time()

for step in range(n_steps + 1):
    current_time = step * dt
    
    # Calcular determinante de la métrica
    det_gamma = gamma_xx * gamma_yy * gamma_zz  # Aproximación diagonal
    trace_K = K_xx + K_yy + K_zz
    
    # Guardar datos cada output_every pasos
    if step % output_every == 0:
        times.append(current_time)
        metric_evolution.append({
            'det_gamma': float(np.mean(det_gamma)),
            'trace_K': float(np.mean(trace_K)),
            'gamma_xx_mean': float(np.mean(gamma_xx)),
            'gamma_yy_mean': float(np.mean(gamma_yy)),
            'gamma_zz_mean': float(np.mean(gamma_zz))
        })
        
        progress = (step / n_steps) * 100
        elapsed = time.time() - start_time
        eta = elapsed * (n_steps - step) / max(step, 1) / 60
        
        print(f"Paso {step:4d}/{n_steps} | t={current_time:.4f} | "
              f"Progreso: {progress:5.1f}% | ETA: {eta:.1f}min")
        print(f"  det(γ)={np.mean(det_gamma):.6f} | tr(K)={np.mean(trace_K):.6f}")
    
    # Evolucionar un paso temporal
    if step < n_steps:
        gamma_xx, gamma_yy, gamma_zz, K_xx, K_yy, K_zz = evolve_metric_simple(
            gamma_xx, gamma_yy, gamma_zz, K_xx, K_yy, K_zz, 
            T_xx, T_yy, T_zz, dt
        )

# Guardar resultados
print("\\n💾 Guardando resultados...")
np.savez('simulation_results_64cubed.npz',
         time_evolution=np.array(times),
         metric_evolution=metric_evolution,
         final_gamma_xx=gamma_xx,
         final_gamma_yy=gamma_yy,
         final_gamma_zz=gamma_zz,
         final_K_xx=K_xx,
         final_K_yy=K_yy,
         final_K_zz=K_zz,
         # Parámetros de la simulación
         dt=dt,
         t_final=t_final,
         n_steps=n_steps,
         grid_size=grid_size
)

total_time = time.time() - start_time
print(f"✅ Simulación 64³ completada!")
print(f"⏱️  Tiempo total: {total_time/60:.1f} minutos")
print(f"💾 Resultados: simulation_results_64cubed.npz")
"""
    
    with open('temp_run_64cubed.py', 'w') as f:
        f.write(simulation_script)
    
    try:
        result = subprocess.run('python temp_run_64cubed.py', shell=True, check=True)
        elapsed_hours = (time.time() - start_time) / 3600
        print(f"\\n✅ Simulación completada en {elapsed_hours:.2f} horas")
        return True
    except subprocess.CalledProcessError:
        print("❌ Error en simulación")
        return False
    finally:
        if os.path.exists('temp_run_64cubed.py'):
            os.remove('temp_run_64cubed.py')

if __name__ == "__main__":
    success = run_simulation_64cubed()
    if success:
        print("\\n🎉 ¡Simulación 64³ exitosa!")
        print("📊 Para analizar: python quick_analysis.py")
        # Copiar resultados al nombre estándar para análisis
        if os.path.exists('simulation_results_64cubed.npz'):
            import shutil
            shutil.copy('simulation_results_64cubed.npz', 'simulation_results.npz')
            print("✅ Resultados copiados para análisis estándar")
    else:
        print("❌ Simulación falló")
'''
    
    with open('run_manual_64cubed.py', 'w') as f:
        f.write(script_content)
    
    os.chmod('run_manual_64cubed.py', 0o755)
    print("📝 Script manual 64³ creado: run_manual_64cubed.py")

def main():
    """Función principal"""
    print("🔧 CONFIGURADOR MANUAL 64³")
    print("=" * 40)
    
    # Crear configuración
    config = create_64cubed_config()
    
    # Generar script
    generate_64cubed_script()
    
    print(f"\n✅ Todo listo para simulación 64³ manual")
    print(f"🚀 Para ejecutar:")
    print(f"   python run_manual_64cubed.py")
    print(f"\n📊 Especificaciones:")
    print(f"   • Resolución: 64³ = 262,144 puntos")  
    print(f"   • Parámetros: R=1.0, ω₄D=0.1")
    print(f"   • Tiempo estimado: ~1.3 horas")
    print(f"   • Implementación simplificada pero estable")

if __name__ == "__main__":
    main()