import subprocess
import os
import argparse
import time
import sys

# --- Configuración de Rutas y Comandos ---

# Mapeo de fases a los scripts correspondientes en la carpeta 'notebooks'
PIPELINE_STAGES = {
    "1_setup": "notebooks/setup_local_gravity_sources.py",
    "2_simulation": "notebooks/run_local_gravity_simulation.py",
    "3_analysis": "notebooks/analyze_local_gravity_results.py"
}

# --- Funciones Auxiliares ---

def print_header(title):
    """Imprime un encabezado estandarizado para las secciones del pipeline."""
    print("\n" + "=" * 80)
    print(f"🚀 INICIANDO: {title}")
    print("=" * 80)

def print_subheader(message):
    """Imprime un sub-encabezado."""
    print("\n" + "-" * 60)
    print(f"  {message}")
    print("-" * 60)

def check_prerequisites():
    """Verifica que todos los scripts necesarios para el pipeline existan."""
    print_subheader("Verificando prerequisitos del pipeline...")
    all_found = True
    for stage, script_path in PIPELINE_STAGES.items():
        if not os.path.exists(script_path):
            print(f"❌ ERROR: No se encontró el script para la fase '{stage}': {script_path}")
            all_found = False
        else:
            print(f"✅ Encontrado: {script_path}")
    
    if not all_found:
        print("\nPipeline abortado. Faltan archivos críticos.")
        sys.exit(1)
    print("Todos los scripts del pipeline están presentes.")

def run_command(command, stage_name):
    """Ejecuta un comando del sistema y maneja errores."""
    print(f"\n▶️  Ejecutando comando para la fase '{stage_name}':")
    print(f"   $ {' '.join(command)}")
    
    start_time = time.time()
    try:
        # Usamos Popen para capturar la salida en tiempo real
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8')
        
        # Imprimir la salida línea por línea si stdout está disponible
        if process.stdout:
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    print(f"   | {output.strip()}")

        # Esperar a que el proceso termine y obtener el código de retorno
        return_code = process.wait()

        end_time = time.time()
        duration = end_time - start_time
        
        if return_code != 0:
            print(f"\n❌ ERROR: La fase '{stage_name}' falló con código de error {return_code}.")
            print(f"   Duración: {duration:.2f} segundos.")
            return False
        
        print(f"\n✅ ÉXITO: La fase '{stage_name}' se completó en {duration:.2f} segundos.")
        return True

    except FileNotFoundError:
        print(f"❌ ERROR: El comando 'python' no se encontró. Asegúrese de que Python esté en el PATH.")
        return False
    except Exception as e:
        print(f"❌ ERROR: Ocurrió una excepción inesperada durante la fase '{stage_name}': {e}")
        return False

# --- Lógica Principal del Pipeline ---

def main(args):
    """Función principal que orquesta la ejecución del pipeline."""
    
    start_pipeline_time = time.time()
    print_header(f"PIPELINE COMPLETO DE GRAVEDAD LOCAL (Resolución: {args.resolution}³)")
    
    check_prerequisites()

    # --- FASE 1: Configuración de Datos Iniciales ---
    print_header("FASE 1: Configuración de Datos Iniciales")
    cmd_setup = [
        "python", PIPELINE_STAGES["1_setup"],
        "--resolution", str(args.resolution),
        "--mass", str(args.mass)
    ]
    if not run_command(cmd_setup, "1_setup"):
        sys.exit(1)

    # --- FASE 2: Ejecución de la Simulación ---
    print_header("FASE 2: Ejecución de la Simulación Numérica")
    cmd_simulation = [
        "python", PIPELINE_STAGES["2_simulation"],
        "--resolution", str(args.resolution),
        "--t_final", str(args.t_final),
        "--dt_checkpoints", str(args.dt_checkpoints)
    ]
    if args.cores:
        cmd_simulation.extend(["--cores", str(args.cores)])
    if not run_command(cmd_simulation, "2_simulation"):
        sys.exit(1)

    # --- FASE 3: Análisis de Resultados ---
    print_header("FASE 3: Análisis Científico de Resultados")
    cmd_analysis = [
        "python", PIPELINE_STAGES["3_analysis"],
        "--resolution", str(args.resolution),
        "--mass", str(args.mass)
    ]
    if not run_command(cmd_analysis, "3_analysis"):
        sys.exit(1)

    # --- Finalización del Pipeline ---
    end_pipeline_time = time.time()
    total_duration = end_pipeline_time - start_pipeline_time
    
    print_header("PIPELINE COMPLETADO EXITOSAMENTE")
    print(f"Resolución analizada: {args.resolution}³")
    print(f"Tiempo total de ejecución: {total_duration / 60:.2f} minutos.")
    
    # Generar reporte final simple
    report_path = f"results/local_gravity_{args.resolution}cubed/pipeline_report_{args.resolution}cubed.txt"
    print_subheader(f"Generando reporte final en: {report_path}")
    try:
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        with open(report_path, "w") as f:
            f.write("="*50 + "\n")
            f.write(f"REPORTE DE EJECUCIÓN DEL PIPELINE - {time.ctime()}\n")
            f.write("="*50 + "\n\n")
            f.write(f"Resolución: {args.resolution}³\n")
            f.write(f"Masa de la partícula: {args.mass}\n")
            f.write(f"Tiempo final de simulación: {args.t_final}\n")
            f.write(f"Tiempo total del pipeline: {total_duration:.2f} segundos\n\n")
            f.write("Fases completadas:\n")
            f.write("  - [X] Fase 1: Configuración de datos iniciales\n")
            f.write("  - [X] Fase 2: Ejecución de la simulación\n")
            f.write("  - [X] Fase 3: Análisis científico\n\n")
            f.write("Resultados principales generados en:\n")
            f.write(f"  - Directorio de checkpoints: output/local_gravity_{args.resolution}cubed/\n")
            f.write(f"  - Directorio de análisis: results/local_gravity_{args.resolution}cubed/\n")
        print("✅ Reporte generado.")
    except IOError as e:
        print(f"❌ ERROR: No se pudo escribir el archivo de reporte: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Pipeline automatizado para la simulación y análisis de gravedad local.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # Argumentos principales
    parser.add_argument('--resolution', type=int, default=32, choices=[32, 64, 128],
                        help='Resolución de la malla de simulación (N en N³).')
    
    # Argumentos de la simulación
    parser.add_argument('--t_final', type=float, default=1.0,
                        help='Tiempo final para la evolución de la simulación.')
    parser.add_argument('--dt_checkpoints', type=float, default=0.1,
                        help='Intervalo de tiempo para guardar checkpoints.')
    parser.add_argument('--mass', type=float, default=0.5,
                        help='Masa de la partícula para las fases 1 y 3.')
    parser.add_argument('--cores', type=int,
                        help='Número de cores a utilizar en la simulación (opcional, por defecto usa la configuración del script).')

    parsed_args = parser.parse_args()
    main(parsed_args)