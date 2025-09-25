import numpy as np
import sys

def inspect_npz(file_path):
    try:
        data = np.load(file_path, allow_pickle=True)
        print(f"Contenido de {file_path}:")
        for key in data.keys():
            print(f"  - {key}")
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {file_path}", file=sys.stderr)
    except Exception as e:
        print(f"Error al leer {file_path}: {e}", file=sys.stderr)

if __name__ == "__main__":
    files_to_inspect = [
        "experimental_validation/results_archive/simulation_outputs/sim_control.npz",
        "local_gravity_simulation_results.npz",
        "experimental_validation/results_archive/simulation_outputs/sim_cluster.npz"
    ]
    
    for f in files_to_inspect:
        inspect_npz(f)
        print("-" * 20)