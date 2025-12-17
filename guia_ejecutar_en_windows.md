# 💾 **Guía Completa: Ejecutar Código en Windows con GPU**

## 🎯 **Resumen: Qué Necesitas Hacer**

Para llevar el código a tu máquina Windows con GPU y ejecutar las simulaciones, necesitas seguir estos pasos:

---

## 📦 **Paso 1: Preparar el Paquete Portable**

### **Opción A: Copiar Todo el Proyecto (Recomendado)**
```bash
# En tu máquina Linux actual:
cd /home/fciliberti/Trabajos/Lab/
tar -czf UniversoCentrifugo_Windows_GPU.tar.gz UniversoCentrífugo/
```

### **Opción B: Solo Archivos Esenciales**
Copia estos archivos clave a tu pendrive:
```
📁 UniversoCentrífugo/
├── 📄 requirements.txt
├── 📄 install_windows_gpu.py
├── 📄 run_simulation_windows_gpu.py
├── 📄 checkpoint_manager.py
├── 📄 verify_hubble_law_final.py
├── 📁 computational_implementation/simulations/
└── 📁 experimental_validation/hubble_verification/
```

---

## 🖥️ **Paso 2: Configurar tu Máquina Windows**

### **2.1 Instalar Python (si no lo tienes)**
- Descarga **Python 3.9+** desde [python.org](https://python.org)
- Durante instalación: ✅ **"Add Python to PATH"**
- Reinicia tu PC

### **2.2 Instalar Drivers NVIDIA**
- Descarga **CUDA Toolkit 11.x o 12.x** desde [NVIDIA](https://developer.nvidia.com/cuda-toolkit)
- Descarga **drivers GPU** más recientes
- Reinicia tu PC

### **2.3 Verificar Instalación**
Abre **CMD** o **PowerShell** y ejecuta:
```cmd
python --version
nvidia-smi
```

---

## 🚀 **Paso 3: Instalación Automática en Windows**

### **3.1 Extraer y Navegar**
```cmd
# Extraer el proyecto y navegar a la carpeta
cd C:\UniversoCentrifugo\
```

### **3.2 Ejecutar Instalador**
```cmd
python install_windows_gpu.py
```

Este script automáticamente:
- ✅ Detecta tu GPU NVIDIA
- ✅ Instala CuPy para aceleración CUDA
- ✅ Instala todas las dependencias necesarias
- ✅ Configura el entorno para Windows

### **3.3 Verificar Instalación**
```cmd
python -c "import cupy; print('✅ GPU OK')"  # Debe mostrar "GPU OK"
python benchmark_gpu_cpu.py  # Debe mostrar speedup GPU
```

---

## 🎮 **Paso 4: Ejecutar Simulaciones con GPU**

### **4.1 Simulación Rápida (Prueba)**
```cmd
python run_simulation_windows_gpu.py --resolution 32 --final_time 1.0
```

### **4.2 Simulación de Mayor Resolución**
```cmd
python run_simulation_windows_gpu.py --resolution 64 --final_time 2.0
```

### **4.3 Verificar Resultados**
```cmd
python verify_hubble_law_final.py
```

---

## 🔧 **Configuración Avanzada para GPU**

### **Parámetros de Rendimiento**
Crea `config_gpu.json`:
```json
{
  "resolution": 64,
  "final_time": 2.0,
  "checkpoint_interval": 500,
  "use_gpu": true,
  "gpu_memory_fraction": 0.8,
  "num_cpu_cores": 8
}
```

### **Ejecución con Configuración**
```cmd
python run_simulation_windows_gpu.py --config config_gpu.json
```

---

## 📊 **Paso 5: Monitorear Rendimiento**

### **5.1 Durante Ejecución**
El script mostrará:
- **GPU Usage**: % de utilización de la GPU
- **VRAM**: Memoria GPU utilizada
- **Throughput**: Puntos procesados/segundo
- **Speedup**: Comparación CPU vs GPU

### **5.2 Benchmarks Específicos**
```cmd
python benchmark_gpu_cpu.py --detailed
```

Esto te dará:
- **Speedup exacto** para tu GPU
- **Memoria óptima** por resolución
- **Configuración recomendada**

---

## 🎯 **Rendimiento Esperado en Windows con GPU**

| GPU NVIDIA | Resolución 32³ | Resolución 64³ | Resolución 128³ |
|-----------|----------------|----------------|-----------------|
| **RTX 3060** | ~1-2 min | ~5-10 min | ~30-60 min |
| **RTX 4070** | ~30-60 seg | ~2-5 min | ~15-30 min |
| **RTX 4090** | ~15-30 seg | ~1-3 min | ~8-15 min |

---

## 🔍 **Solución de Problemas Comunes**

### **Problema: "CUDA not found"**
```cmd
# Reinstalar CuPy específico para tu CUDA
pip uninstall cupy
pip install cupy-cuda11x  # o cupy-cuda12x
```

### **Problema: "Out of memory"**
Reduce resolución o memoria GPU:
```json
{
  "gpu_memory_fraction": 0.5,
  "resolution": 32
}
```

### **Problema: "DLL not found"**
Reinstala **CUDA Toolkit** y reinicia Windows.

---

## 📁 **Archivos Generados en Windows**

Las simulaciones crearán estos archivos:
```
📁 checkpoints/              # Checkpoints automáticos
📄 simulation_results.npz     # Resultados finales
📄 hubble_analysis_*.png     # Gráficos de análisis
📄 benchmark_results.json     # Rendimiento medido
```

---

## 🎉 **Verificación Final**

Si todo funciona correctamente, deberías ver:
1. **"GPU detected and initialized"** al inicio
2. **Speedup de 10-40x** respecto a CPU
3. **Checkpoints guardados** automáticamente
4. **Resultados de Hubble** con expansión detectada
5. **Gráficos generados** automáticamente

---

## 🚀 **Resumen del Flujo Completo**

```cmd
# 1. Extraer y navegar
cd C:\UniversoCentrifugo\

# 2. Instalar automáticamente
python install_windows_gpu.py

# 3. Ejecutar simulación con GPU
python run_simulation_windows_gpu.py --resolution 64

# 4. Verificar resultados
python verify_hubble_law_final.py
```

**Con esto tendrás el sistema completo funcionando en tu Windows con GPU, listo para ejecutar simulaciones de alta resolución y validar la Conjetura del Universo Centrífugo con máxima potencia computacional.**