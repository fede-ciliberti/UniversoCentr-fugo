#!/usr/bin/env python3
"""
Script de Instalación para Windows con Soporte GPU
Instala todas las dependencias necesarias para ejecutar simulaciones BSSN
con aceleración GPU en Windows

Fecha: 14 de diciembre de 2025
Autor: Universo Centrífugo Research Team
"""

import os
import sys
import platform
import subprocess
import urllib.request
import zipfile
import shutil
from pathlib import Path
import json

class WindowsGPUInstaller:
    """Instalador de dependencias para Windows con soporte GPU"""
    
    def __init__(self):
        self.system = platform.system()
        self.machine = platform.machine()
        self.python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
        
        # Directorios de instalación
        self.install_dir = Path.cwd()
        self.deps_dir = self.install_dir / "dependencies"
        self.deps_dir.mkdir(exist_ok=True)
        
        # Archivo de requisitos
        self.requirements_file = self.install_dir / "requirements_windows_gpu.txt"
        
        print("🔧 Instalador Windows GPU para Einstein Simulator")
        print("=" * 60)
        print(f"Sistema: {self.system}")
        print(f"Arquitectura: {self.machine}")
        print(f"Python: {self.python_version}")
        print(f"Directorio: {self.install_dir}")
        print("=" * 60)
    
    def check_system_requirements(self):
        """Verifica los requisitos del sistema"""
        print("\n🔍 Verificando requisitos del sistema...")
        
        # Verificar Windows
        if self.system != "Windows":
            print("❌ Este script está diseñado para Windows")
            return False
        
        # Verificar versión de Python
        if sys.version_info < (3, 8):
            print("❌ Se requiere Python 3.8 o superior")
            return False
        
        # Verificar pip
        try:
            import pip
            print("✅ pip disponible")
        except ImportError:
            print("❌ pip no está disponible")
            return False
        
        # Verificar arquitectura de 64 bits
        if "64" not in self.machine:
            print("⚠️  Se recomienda arquitectura de 64 bits para mejor rendimiento")
        
        print("✅ Requisitos básicos verificados")
        return True
    
    def create_requirements_file(self):
        """Crea el archivo de requisitos para Windows con GPU"""
        print("\n📝 Creando archivo de requisitos...")
        
        requirements = [
            "# Requisitos básicos",
            "numpy>=1.21.0",
            "scipy>=1.7.0",
            "matplotlib>=3.5.0",
            "pathlib2>=2.3.6",
            "tqdm>=4.62.0",
            "",
            "# Aceleración GPU - CuPy (NVIDIA CUDA)",
            "# Nota: CuPy requiere CUDA Toolkit 11.x o 12.x",
            "# cupy-cuda11x>=10.0.0  # Descomentar para CUDA 11.x",
            "# cupy-cuda12x>=10.0.0  # Descomentar para CUDA 12.x",
            "",
            "# Alternativa GPU - PyOpenCL (AMD/Intel/NVIDIA)",
            "# pyopencl>=2021.1.1",
            "",
            "# Optimización numérica",
            "numba>=0.56.0",
            "",
            "# Herramientas de desarrollo",
            "wheel>=0.37.0",
            "setuptools>=60.0.0",
            "",
            "# Visualización y análisis",
            "h5py>=3.5.0",
            "pillow>=8.3.0",
            "",
            "# Utilidades",
            "psutil>=5.8.0",
            "packaging>=21.0"
        ]
        
        with open(self.requirements_file, 'w') as f:
            f.write('\n'.join(requirements))
        
        print(f"✅ Archivo de requisitos creado: {self.requirements_file}")
    
    def install_basic_requirements(self):
        """Instala requisitos básicos sin dependencias GPU"""
        print("\n📦 Instalando requisitos básicos...")
        
        try:
            # Actualizar pip
            subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                         check=True, capture_output=True)
            print("✅ pip actualizado")
            
            # Instalar requisitos básicos
            basic_requirements = [
                "numpy>=1.21.0",
                "scipy>=1.7.0", 
                "matplotlib>=3.5.0",
                "numba>=0.56.0",
                "tqdm>=4.62.0",
                "wheel>=0.37.0",
                "setuptools>=60.0.0",
                "h5py>=3.5.0",
                "psutil>=5.8.0"
            ]
            
            for req in basic_requirements:
                print(f"   Instalando {req}...")
                subprocess.run([sys.executable, "-m", "pip", "install", req], 
                             check=True, capture_output=True)
            
            print("✅ Requisitos básicos instalados")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Error instalando requisitos: {e}")
            return False
    
    def detect_gpu_and_install_gpu_support(self):
        """Detecta GPU e instala soporte apropiado"""
        print("\n🎮 Detectando GPU e instalando soporte...")
        
        # Intentar detectar NVIDIA GPU
        nvidia_detected = self._detect_nvidia_gpu()
        
        if nvidia_detected:
            print("✅ GPU NVIDIA detectada")
            return self._install_cupy()
        else:
            print("⚠️  No se detectó GPU NVIDIA")
            print("   Intentando instalar PyOpenCL para soporte genérico...")
            return self._install_pyopencl()
    
    def _detect_nvidia_gpu(self):
        """Detecta si hay una GPU NVIDIA disponible"""
        try:
            # Intentar ejecutar nvidia-smi
            result = subprocess.run(["nvidia-smi"], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print("✅ nvidia-smi disponible")
                return True
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        
        # Intentar detectar a través de WMI (Windows Management Instrumentation)
        try:
            import wmi
            c = wmi.WMI()
            for gpu in c.Win32_VideoController():
                if "NVIDIA" in gpu.Name:
                    print(f"✅ GPU NVIDIA detectada: {gpu.Name}")
                    return True
        except ImportError:
            # Intentar instalar wmi y reintentar
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", "wmi"], 
                             check=True, capture_output=True)
                import wmi
                c = wmi.WMI()
                for gpu in c.Win32_VideoController():
                    if "NVIDIA" in gpu.Name:
                        print(f"✅ GPU NVIDIA detectada: {gpu.Name}")
                        return True
            except:
                pass
        
        return False
    
    def _install_cupy(self):
        """Instala CuPy para aceleración NVIDIA CUDA"""
        print("\n🚀 Instalando CuPy para aceleración CUDA...")
        
        try:
            # Intentar determinar versión de CUDA
            cuda_version = self._detect_cuda_version()
            
            if cuda_version:
                print(f"✅ CUDA {cuda_version} detectado")
                if cuda_version.startswith("11"):
                    cupy_package = "cupy-cuda11x"
                elif cuda_version.startswith("12"):
                    cupy_package = "cupy-cuda12x"
                else:
                    cupy_package = "cupy-cuda11x"  # Por defecto
                    print("⚠️  Versión CUDA no reconocida, usando cupy-cuda11x")
            else:
                print("⚠️  No se detectó CUDA, intentando instalación genérica...")
                cupy_package = "cupy-cuda11x"  # Intentar con CUDA 11.x
            
            print(f"   Instalando {cupy_package}...")
            subprocess.run([sys.executable, "-m", "pip", "install", cupy_package], 
                         check=True, capture_output=True)
            
            # Verificar instalación
            try:
                import cupy as cp
                print(f"✅ CuPy instalado correctamente (versión {cp.__version__})")
                
                # Probar GPU
                if cp.cuda.is_available():
                    device_count = cp.cuda.get_device_count()
                    print(f"✅ {device_count} dispositivos CUDA disponibles")
                    return True
                else:
                    print("⚠️  CuPy instalado pero no se detectaron dispositivos CUDA")
                    return False
            except ImportError:
                print("❌ Error importando CuPy")
                return False
                
        except subprocess.CalledProcessError as e:
            print(f"❌ Error instalando CuPy: {e}")
            return False
    
    def _detect_cuda_version(self):
        """Detecta la versión de CUDA instalada"""
        try:
            # Intentar ejecutar nvcc
            result = subprocess.run(["nvcc", "--version"], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                output = result.stdout
                for line in output.split('\n'):
                    if "release" in line.lower():
                        # Extraer versión (ej: "release 11.8, V11.8.89")
                        import re
                        match = re.search(r'release (\d+\.\d+)', line)
                        if match:
                            return match.group(1)
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        
        return None
    
    def _install_pyopencl(self):
        """Instala PyOpenCL para soporte genérico de GPU"""
        print("\n⚡ Instalando PyOpenCL para soporte genérico de GPU...")
        
        try:
            # Instalar PyOpenCL
            subprocess.run([sys.executable, "-m", "pip", "install", "pyopencl"], 
                         check=True, capture_output=True)
            
            # Verificar instalación
            try:
                import pyopencl as cl
                print(f"✅ PyOpenCL instalado correctamente (versión {cl.VERSION})")
                
                # Listar plataformas disponibles
                platforms = cl.get_platforms()
                if platforms:
                    print(f"✅ {len(platforms)} plataformas OpenCL disponibles:")
                    for i, platform in enumerate(platforms):
                        print(f"   {i}: {platform.name}")
                        devices = platform.get_devices()
                        for j, device in enumerate(devices):
                            print(f"     - {device.name}")
                    return True
                else:
                    print("⚠️  PyOpenCL instalado pero no se detectaron plataformas")
                    return False
            except ImportError:
                print("❌ Error importando PyOpenCL")
                return False
                
        except subprocess.CalledProcessError as e:
            print(f"❌ Error instalando PyOpenCL: {e}")
            return False
    
    def create_executable_with_pyinstaller(self):
        """Crea un ejecutable con PyInstaller"""
        print("\n📦 Creando ejecutable con PyInstaller...")
        
        try:
            # Instalar PyInstaller
            subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], 
                         check=True, capture_output=True)
            
            # Crear script de especificación
            spec_content = f'''
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['run_simulation_windows_gpu.py'],
    pathex=['{self.install_dir}'],
    binaries=[],
    datas=[],
    hiddenimports=[
        'numpy',
        'scipy',
        'matplotlib',
        'numba',
        'cupy',
        'pyopencl',
        'checkpoint_manager'
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='EinsteinSimulatorGPU',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None
)
'''
            
            spec_file = self.install_dir / "einstein_simulator.spec"
            with open(spec_file, 'w') as f:
                f.write(spec_content)
            
            # Ejecutar PyInstaller
            subprocess.run([
                sys.executable, "-m", "PyInstaller", 
                "--onefile", 
                "--console",
                "--name", "EinsteinSimulatorGPU",
                "run_simulation_windows_gpu.py"
            ], check=True, capture_output=True, cwd=self.install_dir)
            
            print("✅ Ejecutable creado: EinsteinSimulatorGPU.exe")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Error creando ejecutable: {e}")
            return False
    
    def create_configuration_files(self):
        """Crea archivos de configuración para Windows"""
        print("\n⚙️  Creando archivos de configuración...")
        
        # Configuración de checkpoints
        checkpoint_config = {
            "checkpoint_dir": "checkpoints",
            "frequent_interval": 100,
            "periodic_interval": 1000,
            "max_checkpoints": 10,
            "compression_level": 6
        }
        
        config_file = self.install_dir / "checkpoint_config.json"
        with open(config_file, 'w') as f:
            json.dump(checkpoint_config, f, indent=2)
        
        print(f"✅ Configuración de checkpoints creada: {config_file}")
        
        # Script de inicio por lotes
        batch_script = f'''@echo off
echo Einstein Simulator GPU - Iniciando simulacion...
echo.

REM Verificar datos iniciales
if not exist "simulation_initial_data.npz" (
    echo Error: No se encontraron datos iniciales
    echo Ejecute primero: python setup_numerical_simulation.py
    pause
    exit /b 1
)

REM Iniciar simulacion con GPU
python run_simulation_windows_gpu.py

echo.
echo Simulacion completada
pause
'''
        
        batch_file = self.install_dir / "run_simulation.bat"
        with open(batch_file, 'w') as f:
            f.write(batch_script)
        
        print(f"✅ Script de inicio creado: {batch_file}")
    
    def create_documentation(self):
        """Crea documentación específica para Windows"""
        print("\n📚 Creando documentación...")
        
        doc_content = '''# Einstein Simulator GPU - Guía de Instalación Windows

## Requisitos del Sistema

- Windows 10/11 (64 bits recomendado)
- Python 3.8 o superior
- GPU NVIDIA con CUDA Toolkit 11.x/12.x (opcional)
- 8 GB RAM mínimo (16 GB recomendado)
- 2 GB espacio en disco

## Instalación

### 1. Instalar Python
Descargue e instale Python desde https://python.org
Asegúrese de marcar "Add Python to PATH" durante la instalación.

### 2. Ejecutar instalador
```bash
python install_windows_gpu.py
```

### 3. Generar datos iniciales
```bash
python setup_numerical_simulation.py
```

### 4. Ejecutar simulación
```bash
# Usando el script por lotes
run_simulation.bat

# O directamente
python run_simulation_windows_gpu.py
```

## Configuración GPU

### Para GPU NVIDIA (recomendado)
1. Instale CUDA Toolkit desde https://developer.nvidia.com/cuda-downloads
2. El instalador automáticamente detectará e instalará CuPy

### Para otras GPUs (AMD/Intel)
El instalador intentará usar PyOpenCL para soporte genérico

## Uso de Checkpoints

Los checkpoints se guardan automáticamente en el directorio `checkpoints/`:
- Checkpoints frecuentes: cada 100 pasos
- Checkpoints periódicos: cada 1000 pasos

Para reanudar una simulación interrumpida:
```bash
python run_simulation_windows_gpu.py --resume auto
```

## Rendimiento

### GPU vs CPU
- GPU NVIDIA (CUDA): 10-50x aceleración
- GPU genérica (OpenCL): 2-10x aceleración
- CPU multi-core: rendimiento base

### Optimización
- Use resoluciones más altas para mejor aprovechamiento de GPU
- Monitoree el uso de memoria GPU
- Ajuste los intervalos de checkpoint según sus necesidades

## Solución de Problemas

### Errores comunes
1. "CUDA not found": Instale CUDA Toolkit
2. "Out of memory": Reduzca la resolución de la malla
3. "Import error": Verifique la instalación de dependencias

### Soporte
Para problemas técnicos, consulte los logs en la consola o revise el archivo `checkpoint_metadata.json`.

## Ejecutable Portable

El instalador puede crear un ejecutable portable (`EinsteinSimulatorGPU.exe`) que no requiere instalación de Python.
'''
        
        doc_file = self.install_dir / "WINDOWS_GPU_GUIDE.md"
        with open(doc_file, 'w', encoding='utf-8') as f:
            f.write(doc_content)
        
        print(f"✅ Documentación creada: {doc_file}")
    
    def run_installation(self):
        """Ejecuta el proceso completo de instalación"""
        print("\n🚀 Iniciando instalación completa...")
        
        steps = [
            ("Verificando requisitos", self.check_system_requirements),
            ("Creando archivo de requisitos", self.create_requirements_file),
            ("Instalando requisitos básicos", self.install_basic_requirements),
            ("Detectando GPU e instalando soporte", self.detect_gpu_and_install_gpu_support),
            ("Creando archivos de configuración", self.create_configuration_files),
            ("Creando documentación", self.create_documentation),
        ]
        
        for step_name, step_func in steps:
            print(f"\n📋 {step_name}...")
            if not step_func():
                print(f"❌ Falló: {step_name}")
                return False
        
        # Preguntar si crear ejecutable
        try:
            response = input("\n¿Desea crear un ejecutable portable? (s/n): ").lower()
            if response in ['s', 'si', 'y', 'yes']:
                print("\n📦 Creando ejecutable portable...")
                if self.create_executable_with_pyinstaller():
                    print("✅ Ejecutable creado exitosamente")
                else:
                    print("⚠️  No se pudo crear el ejecutable")
        except KeyboardInterrupt:
            print("\n⏹️  Instalación cancelada por el usuario")
            return False
        
        print("\n✅ Instalación completada exitosamente!")
        print("\n📋 Próximos pasos:")
        print("1. Genere datos iniciales: python setup_numerical_simulation.py")
        print("2. Ejecute la simulación: python run_simulation_windows_gpu.py")
        print("3. O use el script por lotes: run_simulation.bat")
        print("\n📚 Consulte WINDOWS_GPU_GUIDE.md para más información")
        
        return True

def main():
    """Función principal del instalador"""
    installer = WindowsGPUInstaller()
    
    try:
        success = installer.run_installation()
        if success:
            print("\n🎉 Instalación completada con éxito!")
            sys.exit(0)
        else:
            print("\n❌ La instalación falló")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⏹️  Instalación cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()