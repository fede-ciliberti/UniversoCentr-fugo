#!/usr/bin/env python3
"""
Script de Benchmarking para Comparar Rendimiento CPU vs GPU
Mide y compara el rendimiento de las simulaciones BSSN en diferentes configuraciones

Fecha: 14 de diciembre de 2025
Autor: Universo Centrífugo Research Team
"""

import os
import sys
import time
import platform
import numpy as np
import multiprocessing as mp
from pathlib import Path
import json
import matplotlib.pyplot as plt
import psutil
from typing import Dict, List, Tuple, Any
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Importar módulos del simulador
try:
    from checkpoint_manager import CheckpointManager
    from run_simulation_windows_gpu import EinsteinSimulatorGPU, GPUAccelerator
except ImportError as e:
    logger.error(f"No se pudieron importar los módulos necesarios: {e}")
    sys.exit(1)

class BenchmarkSuite:
    """Suite de benchmarks para comparar rendimiento CPU vs GPU"""
    
    def __init__(self, output_dir: str = "benchmark_results"):
        """
        Inicializa el suite de benchmarks.
        
        Args:
            output_dir: Directorio para guardar resultados
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Información del sistema
        self.system_info = self._get_system_info()
        
        # Resultados
        self.results = {
            'system_info': self.system_info,
            'benchmarks': []
        }
        
        logger.info("BenchmarkSuite inicializado")
        logger.info(f"Directorio de salida: {self.output_dir}")
    
    def _get_system_info(self) -> Dict:
        """Obtiene información detallada del sistema"""
        info = {
            'platform': platform.platform(),
            'processor': platform.processor(),
            'architecture': platform.architecture(),
            'python_version': platform.python_version(),
            'cpu_count': mp.cpu_count(),
            'memory_total_gb': psutil.virtual_memory().total / (1024**3),
            'memory_available_gb': psutil.virtual_memory().available / (1024**3)
        }
        
        # Información GPU
        gpu_info = self._get_gpu_info()
        info.update(gpu_info)
        
        return info
    
    def _get_gpu_info(self) -> Dict:
        """Obtiene información de GPUs disponibles"""
        gpu_info = {
            'gpu_available': False,
            'gpu_type': None,
            'gpu_memory_gb': None,
            'gpu_count': 0
        }
        
        try:
            accelerator = GPUAccelerator()
            if accelerator.gpu_available:
                gpu_info.update({
                    'gpu_available': True,
                    'gpu_type': accelerator.gpu_type,
                    'gpu_memory_gb': accelerator.gpu_memory,
                    'gpu_count': accelerator.cupy_available and hasattr(accelerator, 'device_count') or 1
                })
        except Exception as e:
            logger.warning(f"No se pudo obtener información GPU: {e}")
        
        return gpu_info
    
    def _create_test_data(self, grid_size: Tuple[int, int, int]) -> Dict:
        """Crea datos de prueba para benchmarks"""
        nx, ny, nz = grid_size
        
        # Crear malla
        x = np.linspace(-1, 1, nx)
        y = np.linspace(-1, 1, ny)
        z = np.linspace(-1, 1, nz)
        X, Y, Z = np.meshgrid(x, y, z, indexing='ij')
        
        # Crear tensor de energía-momento sintético
        T_mu_nu = np.zeros((nx, ny, nz, 4, 4))
        
        # Componente T_tt (densidad de energía)
        r = np.sqrt(X**2 + Y**2 + Z**2)
        T_mu_nu[:, :, :, 0, 0] = np.exp(-r**2 / 0.1)
        
        # Componentes espaciales (presión)
        T_mu_nu[:, :, :, 1, 1] = 0.3 * T_mu_nu[:, :, :, 0, 0]
        T_mu_nu[:, :, :, 2, 2] = 0.3 * T_mu_nu[:, :, :, 0, 0]
        T_mu_nu[:, :, :, 3, 3] = 0.3 * T_mu_nu[:, :, :, 0, 0]
        
        return {
            'X': X,
            'Y': Y,
            'Z': Z,
            'T_mu_nu_evaluated': T_mu_nu
        }
    
    def _save_test_data(self, test_data: Dict, filename: str):
        """Guarda datos de prueba en archivo NPZ"""
        filepath = self.output_dir / filename
        np.savez_compressed(filepath, **test_data)
        return str(filepath)
    
    def benchmark_configuration(self, grid_size: Tuple[int, int, int], 
                              use_gpu: bool, max_cores: int = None,
                              duration_seconds: float = 30.0) -> Dict:
        """
        Ejecuta benchmark para una configuración específica.
        
        Args:
            grid_size: Tamaño de la malla (nx, ny, nz)
            use_gpu: Usar GPU si está disponible
            max_cores: Número máximo de cores a usar
            duration_seconds: Duración del benchmark en segundos
            
        Returns:
            Diccionario con resultados del benchmark
        """
        nx, ny, nz = grid_size
        total_points = nx * ny * nz
        
        config_name = f"GPU_{accelerator.gpu_type}" if use_gpu else f"CPU_{max_cores or 'all'}"
        
        logger.info(f"Iniciando benchmark: {config_name} - Malla {grid_size}")
        
        # Crear datos de prueba
        test_data = self._create_test_data(grid_size)
        test_file = self._save_test_data(test_data, f"benchmark_data_{nx}x{ny}x{nz}.npz")
        
        try:
            # Configurar simulador
            checkpoint_config = {
                'checkpoint_dir': self.output_dir / f"checkpoints_{config_name}",
                'frequent_interval': 10000,  # Desactivar checkpoints para benchmark
                'periodic_interval': 100000,
                'max_checkpoints': 1
            }
            
            simulator = EinsteinSimulatorGPU(
                data_file=test_file,
                max_cores=max_cores,
                use_gpu=use_gpu,
                checkpoint_config=checkpoint_config
            )
            
            # Reducir tiempo de simulación para benchmark
            original_t_final = simulator.t_final
            simulator.t_final = duration_seconds * simulator.dt * 100  # Aproximadamente duration_seconds
            simulator.n_steps = int(simulator.t_final / simulator.dt)
            
            # Medir uso de recursos antes de iniciar
            process = psutil.Process()
            initial_memory = process.memory_info().rss / (1024**2)  # MB
            
            # Ejecutar benchmark
            start_time = time.time()
            start_step = 0
            
            # Ejecutar simulación por tiempo limitado
            for step in range(simulator.n_steps):
                t = simulator.run_single_timestep(step * simulator.dt)
                
                # Verificar si alcanzamos el tiempo límite
                elapsed = time.time() - start_time
                if elapsed >= duration_seconds:
                    break
            
            end_time = time.time()
            
            # Medir uso de recursos después
            final_memory = process.memory_info().rss / (1024**2)  # MB
            peak_memory = max(initial_memory, final_memory)
            
            # Calcular métricas
            total_time = end_time - start_time
            steps_completed = step + 1
            points_processed = steps_completed * total_points
            throughput = points_processed / total_time
            
            result = {
                'configuration': config_name,
                'grid_size': grid_size,
                'total_points': total_points,
                'use_gpu': use_gpu,
                'max_cores': max_cores,
                'duration_seconds': total_time,
                'steps_completed': steps_completed,
                'points_processed': points_processed,
                'throughput_points_per_second': throughput,
                'throughput_kpoints_per_second': throughput / 1000,
                'memory_usage_mb': peak_memory,
                'memory_per_point_bytes': (peak_memory * 1024**2) / points_processed if points_processed > 0 else 0,
                'gpu_type': simulator.gpu_accelerator.gpu_type if use_gpu else None,
                'gpu_memory_gb': simulator.gpu_accelerator.gpu_memory if use_gpu else None
            }
            
            logger.info(f"✅ Benchmark {config_name} completado:")
            logger.info(f"   Tiempo: {total_time:.2f}s")
            logger.info(f"   Throughput: {throughput/1000:.1f}k puntos/segundo")
            logger.info(f"   Memoria: {peak_memory:.1f} MB")
            
            return result
            
        except Exception as e:
            logger.error(f"Error en benchmark {config_name}: {e}")
            return {
                'configuration': config_name,
                'grid_size': grid_size,
                'error': str(e),
                'use_gpu': use_gpu,
                'max_cores': max_cores
            }
    
    def run_comprehensive_benchmark(self) -> Dict:
        """Ejecuta un benchmark completo con múltiples configuraciones"""
        logger.info("🚀 Iniciando benchmark comprehensivo...")
        
        # Configuraciones a probar
        grid_sizes = [
            (16, 16, 16),    # Pequeña
            (32, 32, 32),    # Mediana
            (64, 64, 64),    # Grande
        ]
        
        configurations = []
        
        # Configuraciones CPU
        cpu_cores = [1, 2, 4, mp.cpu_count()]
        for cores in cpu_cores:
            configurations.append({
                'use_gpu': False,
                'max_cores': cores,
                'name': f'CPU_{cores}_cores'
            })
        
        # Configuraciones GPU (si está disponible)
        if self.system_info['gpu_available']:
            configurations.append({
                'use_gpu': True,
                'max_cores': None,
                'name': f'GPU_{self.system_info["gpu_type"]}'
            })
        
        # Ejecutar benchmarks
        for grid_size in grid_sizes:
            logger.info(f"\n📊 Probando malla: {grid_size}")
            
            for config in configurations:
                result = self.benchmark_configuration(
                    grid_size=grid_size,
                    use_gpu=config['use_gpu'],
                    max_cores=config['max_cores'],
                    duration_seconds=20.0  # 20 segundos por benchmark
                )
                
                self.results['benchmarks'].append(result)
        
        return self.results
    
    def analyze_results(self) -> Dict:
        """Analiza y genera estadísticas de los resultados"""
        logger.info("📈 Analizando resultados...")
        
        # Filtrar benchmarks exitosos
        successful_benchmarks = [b for b in self.results['benchmarks'] if 'error' not in b]
        
        if not successful_benchmarks:
            logger.warning("No hay benchmarks exitosos para analizar")
            return {}
        
        analysis = {
            'summary': {},
            'by_grid_size': {},
            'by_configuration': {},
            'performance_comparison': {}
        }
        
        # Análisis por tamaño de malla
        for benchmark in successful_benchmarks:
            grid_key = f"{benchmark['grid_size'][0]}x{benchmark['grid_size'][1]}x{benchmark['grid_size'][2]}"
            
            if grid_key not in analysis['by_grid_size']:
                analysis['by_grid_size'][grid_key] = []
            
            analysis['by_grid_size'][grid_key].append(benchmark)
        
        # Análisis por configuración
        for benchmark in successful_benchmarks:
            config_key = benchmark['configuration']
            
            if config_key not in analysis['by_configuration']:
                analysis['by_configuration'][config_key] = []
            
            analysis['by_configuration'][config_key].append(benchmark)
        
        # Calcular mejor rendimiento
        best_throughput = max(successful_benchmarks, key=lambda x: x['throughput_points_per_second'])
        analysis['performance_comparison']['best_throughput'] = best_throughput
        
        # Comparación GPU vs CPU
        gpu_benchmarks = [b for b in successful_benchmarks if b['use_gpu']]
        cpu_benchmarks = [b for b in successful_benchmarks if not b['use_gpu']]
        
        if gpu_benchmarks and cpu_benchmarks:
            avg_gpu_throughput = np.mean([b['throughput_points_per_second'] for b in gpu_benchmarks])
            avg_cpu_throughput = np.mean([b['throughput_points_per_second'] for b in cpu_benchmarks])
            
            analysis['performance_comparison']['gpu_speedup'] = avg_gpu_throughput / avg_cpu_throughput
            analysis['performance_comparison']['avg_gpu_throughput'] = avg_gpu_throughput
            analysis['performance_comparison']['avg_cpu_throughput'] = avg_cpu_throughput
        
        # Guardar análisis
        analysis_file = self.output_dir / "benchmark_analysis.json"
        with open(analysis_file, 'w') as f:
            json.dump(analysis, f, indent=2)
        
        logger.info(f"✅ Análisis guardado en: {analysis_file}")
        return analysis
    
    def generate_plots(self):
        """Genera gráficos de los resultados del benchmark"""
        logger.info("📊 Generando gráficos...")
        
        # Filtrar benchmarks exitosos
        successful_benchmarks = [b for b in self.results['benchmarks'] if 'error' not in b]
        
        if not successful_benchmarks:
            logger.warning("No hay benchmarks exitosos para graficar")
            return
        
        # Crear figura con múltiples subplots
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Benchmark Results: CPU vs GPU Performance', fontsize=16)
        
        # 1. Throughput por configuración
        ax1 = axes[0, 0]
        configs = list(set(b['configuration'] for b in successful_benchmarks))
        throughputs = []
        
        for config in configs:
            config_benchmarks = [b for b in successful_benchmarks if b['configuration'] == config]
            avg_throughput = np.mean([b['throughput_kpoints_per_second'] for b in config_benchmarks])
            throughputs.append(avg_throughput)
        
        bars = ax1.bar(configs, throughputs)
        ax1.set_title('Average Throughput by Configuration')
        ax1.set_ylabel('Throughput (k points/second)')
        ax1.tick_params(axis='x', rotation=45)
        
        # Colorear barras según tipo
        for i, bar in enumerate(bars):
            if 'GPU' in configs[i]:
                bar.set_color('green')
            else:
                bar.set_color('blue')
        
        # 2. Uso de memoria
        ax2 = axes[0, 1]
        memory_usage = [b['memory_usage_mb'] for b in successful_benchmarks]
        grid_sizes = [f"{b['grid_size'][0]}³" for b in successful_benchmarks]
        
        scatter = ax2.scatter(range(len(memory_usage)), memory_usage, 
                            c=['green' if b['use_gpu'] else 'blue' for b in successful_benchmarks],
                            s=100, alpha=0.7)
        ax2.set_title('Memory Usage by Grid Size')
        ax2.set_ylabel('Memory Usage (MB)')
        ax2.set_xticks(range(len(grid_sizes)))
        ax2.set_xticklabels(grid_sizes, rotation=45)
        
        # 3. Escalabilidad con número de cores
        ax3 = axes[1, 0]
        cpu_benchmarks = [b for b in successful_benchmarks if not b['use_gpu']]
        
        if cpu_benchmarks:
            cores = [b['max_cores'] for b in cpu_benchmarks]
            throughputs_cpu = [b['throughput_kpoints_per_second'] for b in cpu_benchmarks]
            
            ax3.plot(cores, throughputs_cpu, 'bo-', label='CPU', markersize=8)
            ax3.set_title('CPU Scalability')
            ax3.set_xlabel('Number of Cores')
            ax3.set_ylabel('Throughput (k points/second)')
            ax3.legend()
            ax3.grid(True, alpha=0.3)
        
        # 4. Comparación directa GPU vs CPU
        ax4 = axes[1, 1]
        
        # Agrupar por tamaño de malla
        grid_sizes_unique = list(set(b['grid_size'] for b in successful_benchmarks))
        
        for grid_size in grid_sizes_unique:
            size_benchmarks = [b for b in successful_benchmarks if b['grid_size'] == grid_size]
            
            cpu_data = [b for b in size_benchmarks if not b['use_gpu']]
            gpu_data = [b for b in size_benchmarks if b['use_gpu']]
            
            if cpu_data and gpu_data:
                cpu_throughput = np.mean([b['throughput_kpoints_per_second'] for b in cpu_data])
                gpu_throughput = np.mean([b['throughput_kpoints_per_second'] for b in gpu_data])
                
                x_pos = len(grid_sizes_unique) - grid_sizes_unique.index(grid_size) - 1
                width = 0.35
                
                ax4.bar(x_pos - width/2, cpu_throughput, width, label='CPU' if grid_size == grid_sizes_unique[0] else '', color='blue', alpha=0.7)
                ax4.bar(x_pos + width/2, gpu_throughput, width, label='GPU' if grid_size == grid_sizes_unique[0] else '', color='green', alpha=0.7)
        
        ax4.set_title('GPU vs CPU Comparison by Grid Size')
        ax4.set_ylabel('Throughput (k points/second)')
        ax4.set_xticks(range(len(grid_sizes_unique)))
        ax4.set_xticklabels([f"{s[0]}³" for s in grid_sizes_unique])
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Guardar gráfico
        plot_file = self.output_dir / "benchmark_plots.png"
        plt.savefig(plot_file, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"✅ Gráficos guardados en: {plot_file}")
    
    def save_results(self):
        """Guarda todos los resultados del benchmark"""
        logger.info("💾 Guardando resultados...")
        
        # Guardar resultados completos
        results_file = self.output_dir / "benchmark_results.json"
        with open(results_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        logger.info(f"✅ Resultados guardados en: {results_file}")
        
        # Generar reporte resumido
        self._generate_summary_report()
    
    def _generate_summary_report(self):
        """Genera un reporte resumido en formato Markdown"""
        successful_benchmarks = [b for b in self.results['benchmarks'] if 'error' not in b]
        
        if not successful_benchmarks:
            return
        
        # Calcular estadísticas
        best_throughput = max(successful_benchmarks, key=lambda x: x['throughput_points_per_second'])
        gpu_benchmarks = [b for b in successful_benchmarks if b['use_gpu']]
        cpu_benchmarks = [b for b in successful_benchmarks if not b['use_gpu']]
        
        report = f"""# Benchmark Report: CPU vs GPU Performance

## System Information
- **Platform**: {self.system_info['platform']}
- **CPU**: {self.system_info['processor']}
- **Cores**: {self.system_info['cpu_count']}
- **Memory**: {self.system_info['memory_total_gb']:.1f} GB
- **GPU Available**: {'Yes' if self.system_info['gpu_available'] else 'No'}
"""
        
        if self.system_info['gpu_available']:
            report += f"""- **GPU Type**: {self.system_info['gpu_type']}
- **GPU Memory**: {self.system_info['gpu_memory_gb']:.1f} GB
"""
        
        report += f"""
## Performance Summary

### Best Performance
- **Configuration**: {best_throughput['configuration']}
- **Grid Size**: {best_throughput['grid_size']}
- **Throughput**: {best_throughput['throughput_kpoints_per_second']:.1f}k points/second
- **Memory Usage**: {best_throughput['memory_usage_mb']:.1f} MB

### GPU vs CPU Comparison
"""
        
        if gpu_benchmarks and cpu_benchmarks:
            avg_gpu_throughput = np.mean([b['throughput_kpoints_per_second'] for b in gpu_benchmarks])
            avg_cpu_throughput = np.mean([b['throughput_kpoints_per_second'] for b in cpu_benchmarks])
            speedup = avg_gpu_throughput / avg_cpu_throughput
            
            report += f"""- **Average GPU Throughput**: {avg_gpu_throughput:.1f}k points/second
- **Average CPU Throughput**: {avg_cpu_throughput:.1f}k points/second
- **GPU Speedup**: {speedup:.1f}x
"""
        
        report += """
## Detailed Results

| Configuration | Grid Size | Throughput (k pts/s) | Memory (MB) | Time (s) |
|---------------|------------|----------------------|-------------|-----------|
"""
        
        for benchmark in successful_benchmarks:
            report += f"| {benchmark['configuration']} | {benchmark['grid_size'][0]}³ | {benchmark['throughput_kpoints_per_second']:.1f} | {benchmark['memory_usage_mb']:.1f} | {benchmark['duration_seconds']:.1f} |\n"
        
        report += """
## Recommendations

Based on the benchmark results:

1. **For optimal performance**: Use the configuration with highest throughput
2. **Memory considerations**: Monitor memory usage for larger grid sizes
3. **GPU acceleration**: Provides significant speedup when available
4. **CPU scaling**: Performance scales with number of cores up to a point

## Files Generated
- `benchmark_results.json`: Complete results data
- `benchmark_analysis.json`: Statistical analysis
- `benchmark_plots.png`: Performance visualizations
"""
        
        # Guardar reporte
        report_file = self.output_dir / "benchmark_report.md"
        with open(report_file, 'w') as f:
            f.write(report)
        
        logger.info(f"✅ Reporte guardado en: {report_file}")

def main():
    """Función principal del benchmark"""
    print("🚀 Einstein Simulator GPU - Benchmark Suite")
    print("Comparando rendimiento CPU vs GPU")
    print("=" * 60)
    
    # Crear suite de benchmarks
    benchmark = BenchmarkSuite()
    
    try:
        # Ejecutar benchmarks
        results = benchmark.run_comprehensive_benchmark()
        
        # Analizar resultados
        analysis = benchmark.analyze_results()
        
        # Generar gráficos
        benchmark.generate_plots()
        
        # Guardar resultados
        benchmark.save_results()
        
        print("\n✅ Benchmark completado exitosamente!")
        print(f"📁 Resultados guardados en: {benchmark.output_dir}")
        print("\n📊 Archivos generados:")
        print("  - benchmark_results.json")
        print("  - benchmark_analysis.json")
        print("  - benchmark_plots.png")
        print("  - benchmark_report.md")
        
    except Exception as e:
        logger.error(f"Error durante el benchmark: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()