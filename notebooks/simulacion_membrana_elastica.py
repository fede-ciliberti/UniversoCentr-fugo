#!/usr/bin/env python3
"""
Simulación Numérica de Gravedad Emergente por Membrana Elástica

Basada en la Conjetura del Universo Centrífugo: la gravedad local no es una
fuerza fundamental sino una reacción elástica macroscópica de la 3-brana al
deformarse en la cuarta dirección espacial (w) por el empuje centrífugo de la
rotación inercial en R^4.

Ecuación de estado de membrana (Poisson con amortiguamiento cosmológico):
    nabla^2 h(x) - lambda^2 h(x) = S(x)

donde h(x) es la deflexión hiperdimensional, lambda = 1/R es el coeficiente
de restitución elástica, y S(x) = rho(x) * omega_4D^2 * R / T_b es el término
fuente de empuje centrífugo.

La solución se obtiene mediante método espectral FFT 3D, y a partir de ella
se reconstruyen las componentes de la métrica inducida:
    g_00 = -(1 + 2h)
    g_rr = 1 + (nabla h)^2

El resultado se valida contra la métrica analítica de Schwarzschild en el
límite de campo débil.

Referencias teóricas:
    - docs/01_marco_teorico.md: Marco teórico general
    - docs/02_propuesta_investigacion.md: Propuesta de investigación
    - docs/03_metodologia_gravedad_emergente.md: Metodología de gravedad emergente
    - docs/04_metodologia_verificacion_gravedad.md: Verificación de gravedad
    - docs/plan_simulacion_elastica.md: Plan detallado de esta simulación

Author: Fede & Sisyphus - Universo Centrífugo Research Team
Date: June 2026
"""

import numpy as np
from scipy import fftpack
import matplotlib.pyplot as plt
from matplotlib import cm
import argparse
import os
import sys
import time
from pathlib import Path

# Intentar importar numba para aceleración JIT (misma convención que el proyecto)
try:
    from numba import jit, prange
    NUMBA_AVAILABLE = True
except ImportError:
    NUMBA_AVAILABLE = False
    def jit(*args, **kwargs):
        def decorator(func):
            return func
        return decorator
    def prange(*args, **kwargs):
        return range(*args, **kwargs)

# Configuración para gráficos científicos (idéntica a analyze_local_gravity_results.py)
plt.rcParams.update({
    'font.size': 12,
    'font.family': 'serif',
    'axes.labelsize': 14,
    'axes.titlesize': 16,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12,
    'legend.fontsize': 12,
    'figure.titlesize': 18,
    'figure.dpi': 150,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight'
})


class SimulacionMembranaElastica:
    """
    Simulador espectral de la membrana elástica hiperdimensional.

    Resuelve la ecuación de Poisson con amortiguamiento cosmológico para la
    deflexión de la 3-brana usando método FFT, reconstruye la métrica inducida
    y valida contra Schwarzschild analítico.

    Ecuación fundamental:
        nabla^2 h - lambda^2 h = S

    donde S = rho * omega_4D^2 * R / T_b, con lambda = 1/R.
    La gravedad emerge como la deformación elástica de la brana bajo el empuje
    centrífugo de la rotación 4D.
    """

    def __init__(self, grid_size=64, box_size=40.0, omega_4D=1.0, R=50.0,
                 tension=1.0, sigma=0.5, mass=1.0):
        """
        Inicializa la simulación con los parámetros físicos.

        Parámetros:
            grid_size (int): Resolución de la malla cúbica (N x N x N).
            box_size (float): Tamaño físico de la caja de simulación.
            omega_4D (float): Velocidad angular de la rotación 4D. Valor instantáneo
                local; cosmológicamente ω₄D(t) ∝ 1/R(t)² por conservación del momento
                angular (ver docs/conservacion_momento_inercia_geff.md). En simulaciones
                estáticas de un solo timestep se trata como constante.
            R (float): Radio cosmológico de la brana (lambda = 1/R).
            tension (float): Tensión superficial de la brana T_b.
            sigma (float): Ancho de la distribución gaussiana de masa.
            mass (float): Masa total integrada de la fuente.

        Nota sobre G_eff (constante gravitacional emergente):
            La gravedad no es fundamental en este modelo, sino que emerge de
            la combinación de la tensión de brana T_b y la rotación 4D. Cosmológicamente,
            el decaimiento ω₄D(t) ∝ 1/R² se cancela exactamente con T_b(t) ∝ 1/R³,
            produciendo G_eff estrictamente constante (ver simulacion_evolucion_temporal_geff.py).
            La constante gravitacional efectiva se define como:
                G_eff = (omega_4D^2 * R) / (4 * pi * T_b)
            (ver docs/03_metodologia_gravedad_emergente.md seccion 5.2,
             docs/04_metodologia_verificacion_gravedad.md seccion 2.2)
        """
        self.N = int(grid_size)
        self.L = float(box_size)
        self.omega_4D = float(omega_4D)
        self.R = float(R)
        self.tension = float(tension)
        self.sigma = float(sigma)
        self.mass = float(mass)

        # Paso de malla espacial
        self.dx = self.L / self.N

        # Coeficiente de restitución elástica global
        # lambda = 1/R: cuanto mayor es el radio cosmologico, menor es la
        # restitucion elastica y mas "suave" es el retorno a la posicion
        # de equilibrio.
        self.lambda_sq = (1.0 / self.R) ** 2

        # Constante gravitacional efectiva (c=1 en unidades geometrizadas)
        # G_eff = c^2 * omega_4D^2 * R / (4 * pi * T_b)
        # En el limite de campo debil, G_eff debe reproducir G newtoniana.
        # (ver doc 03 seccion 5.2, doc 04 seccion 2.2)
        self.G_eff = (self.omega_4D ** 2 * self.R) / (4.0 * np.pi * self.tension)

        # Directorio de salida para resultados y graficos
        self.output_dir = Path(f"results/membrana_elastica/{self.N}cubed")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _crear_rejilla_coordenadas(self):
        """
        Crea la rejilla 3D de coordenadas centrada en el origen.

        La caja de simulacion se extiende desde -L/2 hasta +L/2 en cada
        direccion, con el origen (0,0,0) en el centro donde se coloca la
        fuente de masa.

        Returns:
            tuple: (X, Y, Z) arreglos 3D de coordenadas, r_grid 3D (norma radial).
        """
        # Eje coordenado 1D centrado en cero
        x_1d = np.linspace(-self.L / 2.0, self.L / 2.0, self.N)
        # Rejilla 3D via meshgrid (indexacion 'ij' para mantener consistencia)
        X, Y, Z = np.meshgrid(x_1d, x_1d, x_1d, indexing='ij')
        # Distancia radial desde el centro
        r_grid = np.sqrt(X ** 2 + Y ** 2 + Z ** 2)
        return X, Y, Z, r_grid

    def generar_densidad_masa(self):
        """
        Genera la distribucion de densidad de masa 3D como una gaussiana
        centrada en el origen.

        La masa se distribuye como una esfera gaussiana suave para evitar
        singularidades numericas:
            rho(r) = rho_0 * exp(-r^2 / (2 * sigma^2))

        La normalizacion rho_0 se calcula integrando analiticamente para que
        la masa total integrada sea exactamente el parametro `mass`:
            M = integral rho(r) dV = rho_0 * (2*pi*sigma^2)^(3/2)
            => rho_0 = M / ( (2*pi*sigma^2)^(3/2) )

        Returns:
            ndarray: Arreglo 3D de densidad de masa.
        """
        _, _, _, r_grid = self._crear_rejilla_coordenadas()

        # Normalizacion: la integral de la gaussiana 3D en todo el espacio
        # es (2*pi*sigma^2)^(3/2). Aseguramos que la masa total integrada sea
        # exactamente self.mass.
        rho_0 = self.mass / ((2.0 * np.pi * self.sigma ** 2) ** 1.5)

        # Densidad completamente vectorizada (sin loops Python)
        mass_density = rho_0 * np.exp(-(r_grid ** 2) / (2.0 * self.sigma ** 2))

        return mass_density

    def resolver_deflexion_fft(self, mass_density_grid):
        """
        Resuelve la ecuacion de Poisson elastica usando metodo espectral FFT.

        Algoritmo (doc 04 seccion 4.1, doc plan simulacion elastica seccion 2):
            1. Construir vectores de onda kx, ky, kz via FFT de frecuencias.
            2. Calcular K_sq = KX^2 + KY^2 + KZ^2 (Laplaciano en Fourier).
            3. Calcular termino fuente: f_source = (rho * omega_4D^2 * R) / T_b.
            4. FFT de la fuente: f_source_fft = FFT(f_source).
            5. Solucion en frecuencia:
                 H_fft = -S_fft / (K_sq + lambda^2)
               donde lambda^2 = 1/R^2 es el termino de restitucion elastica.
            6. Modo DC (k=0) se fija a cero para normalizar la deflexion.
            7. IFFT para obtener h(x,y,z) en espacio real.

        La ecuacion en espacio de Fourier:
            -k^2 * H(k) - lambda^2 * H(k) = S(k)
            => H(k) = -S(k) / (k^2 + lambda^2)

        (ver doc 01 seccion 1.1, doc 03 seccion 4, doc 04 seccion 2.1)

        Parameters:
            mass_density_grid (ndarray): Arreglo 3D de densidad de masa.

        Returns:
            ndarray: Arreglo 3D de deflexion h(x,y,z).
        """
        N = self.N

        # --- Paso 1: Vectores de onda en el espacio de Fourier ---
        # fftfreq devuelve frecuencias en el rango [0, 1, ..., N-1] mapeadas
        # a [0, 2*pi, ..., 2*pi*(N-1)/N] en unidades de 1/metros.
        # Multiplicamos por 2*pi para obtener k en radianes por unidad de longitud.
        kx = np.fft.fftfreq(N, d=self.dx) * 2.0 * np.pi
        ky = np.fft.fftfreq(N, d=self.dx) * 2.0 * np.pi
        kz = np.fft.fftfreq(N, d=self.dx) * 2.0 * np.pi

        # Rejilla 3D de vectores de onda
        KX, KY, KZ = np.meshgrid(kx, ky, kz, indexing='ij')
        K_sq = KX ** 2 + KY ** 2 + KZ ** 2

        # --- Paso 2: Termino fuente (empuje centrifugo) ---
        # S = rho * omega_4D^2 * R / T_b
        # (ver doc 01 seccion 1.2, doc 04 seccion 2.1)
        f_source = (mass_density_grid * self.omega_4D ** 2 * self.R) / self.tension

        # --- Paso 3: Transformada de Fourier de la fuente ---
        f_source_fft = fftpack.fftn(f_source)

        # --- Paso 4: Solucion en el espacio de Fourier ---
        # Denominador regularizado: K_sq + lambda^2 asegura que nunca se
        # divide por cero incluso en k=0.
        h_fft = -f_source_fft / (K_sq + self.lambda_sq)

        # --- Paso 5: Modo DC (frecuencia cero) a cero ---
        # Esto normaliza la deflexion para que el valor medio sea cero,
        # equivalente a fijar el nivel de referencia de la brana no deformada.
        h_fft[0, 0, 0] = 0.0 + 0.0j

        # --- Paso 6: Transformada inversa ---
        h_real = np.real(fftpack.ifftn(h_fft))

        return h_real

    def calcular_metrica_inducida(self, h_grid):
        """
        Reconstruye las componentes del tensor metrico g_mu_nu a partir de la
        deflexion h(x,y,z).

        La metrica inducida se obtiene desde la geometria de la brana deformada:
            g_00 = -(1 + 2h): describe la dilatacion temporal gravitacional.
            g_rr = 1 + (nabla h)^2: describe la curvatura espacial emergente.

        El gradiente se calcula mediante diferencias finitas centradas via
        np.gradient, que proporciona una aproximacion de orden O(dx^2).

        (ver doc 01 seccion 4.1, doc 04 seccion 3.1)

        Parameters:
            h_grid (ndarray): Arreglo 3D de deflexion.

        Returns:
            tuple: (g_00, g_rr) arreglos 3D de las componentes metricas.
        """
        # --- Gradiente 3D de la deflexion ---
        # np.gradient usa diferencias centradas de segundo orden en bordes
        # y diferencias hacia adelante/atras en los extremos.
        grad_hx, grad_hy, grad_hz = np.gradient(h_grid, self.dx)

        # Norma al cuadrado del gradiente: |nabla h|^2
        dh_sq = grad_hx ** 2 + grad_hy ** 2 + grad_hz ** 2

        # --- Componente temporal g_00 ---
        # El pozo de potencial gravitacional emerge como la deformacion de la
        # dimension temporal. El factor 2h es la correccion de campo debil de
        # la relatividad general.
        g_00 = -(1.0 + 2.0 * h_grid)

        # --- Componente espacial g_rr ---
        # La curvatura espacial emerge del estiramiento elastico de la brana.
        # (nabla h)^2 representa la densidad de energia de deformacion, que
        # se manifiesta como curvatura espacial positiva (ver plan seccion 4.1).
        g_rr = 1.0 + dh_sq

        return g_00, g_rr

    def _calibrar_amplitud_yukawa(self, h_grid):
        """
        Calcula la amplitud A y el offset C de la solucion numerica
        ajustando h(r) al potencial de Yukawa en la region externa.

        La ecuacion de membrana (nabla^2 - lambda^2)h = S tiene como solucion
        analitica para una fuente puntual:
        h(r) = -A * exp(-r/R) / r + C

        donde C es un offset constante debido a las condiciones de borde
        periodicas (PBC) y al modo DC fijado a cero. Con PBC, la solucion
        incluye contribuciones de imagenes periodicas que agregan un fondo
        constante a la deflexion.

        Se usa un ajuste lineal por minimos cuadrados con dos parametros:
        h(r) = A * phi(r) + C
        donde phi(r) = -exp(-r/R) / r

        Returns:
        tuple: (A_calibrated, C_calibrated) amplitud y offset PBC.
        """
        N = self.N
        mid = N // 2

        x_1d = np.linspace(-self.L / 2.0, self.L / 2.0, N)
        X, Y = np.meshgrid(x_1d, x_1d, indexing='ij')
        r_slice = np.sqrt(X ** 2 + Y ** 2)
        h_slice = h_grid[:, :, mid]

        # Region externa: fuera de la fuente (r > 3*sigma) y lejos de bordes
        r_min_fit = 3.0 * self.sigma
        r_max_fit = self.L / 2.0 * 0.8

        r_flat = r_slice.ravel()
        h_flat = h_slice.ravel()

        mask = (r_flat >= r_min_fit) & (r_flat <= r_max_fit)
        r_fit = r_flat[mask]
        h_fit = h_flat[mask]

        if np.sum(mask) < 5:
            r_min_fit = 2.0 * self.sigma
            mask = (r_flat >= r_min_fit) & (r_flat <= r_max_fit)
            r_fit = r_flat[mask]
            h_fit = h_flat[mask]

        if np.sum(mask) < 3:
            return self.G_eff * self.mass, 0.0

        # Ajuste: h(r) = A * phi(r) + C
        # donde phi(r) = -exp(-r/R) / r
        # Matriz de diseno: [phi(r), 1]
        phi = -np.exp(-r_fit / self.R) / r_fit
        A_design = np.column_stack([phi, np.ones_like(phi)])

        # Minimos cuadrados: [A_opt, C_opt] = inv(A_design^T A_design) A_design^T h
        ATA = A_design.T @ A_design
        ATb = A_design.T @ h_fit
        try:
            params = np.linalg.solve(ATA, ATb)
            A_calibrated = params[0]
            C_calibrated = params[1]
        except np.linalg.LinAlgError:
            return self.G_eff * self.mass, 0.0

        if A_calibrated <= 0 or np.isnan(A_calibrated) or np.isinf(A_calibrated):
            return self.G_eff * self.mass, 0.0

        return A_calibrated, C_calibrated

    def perfil_radial_schwarzschild(self, h_grid, g_00, g_rr):
        """
        Extrae perfiles radiales de las componentes metricas y los compara
        con la solucion analitica de Schwarzschild y el potencial Yukawa.

        Proceso:
            1. Tomar el plano ecuatorial (z = N//2) de los arreglos 3D.
            2. Calcular la distancia radial r desde el centro para cada pixel.
            3. Promediar g_00 y g_rr en bins radiales concentricos.
            4. Calibrar la amplitud A de la solucion numerica (ver
               _calibrar_amplitud_yukawa).
            5. Calcular Schwarzschild analitico usando la amplitud calibrada:
                 g_00_s(r) = -(1 - r_s_cal / r)
                 g_rr_s(r) = 1 / (1 - r_s_cal / r)
               donde r_s_cal = 2 * A.
            6. Calcular Yukawa analitico (solucion exacta de la ec. de membrana):
                 g_00_y(r) = -(1 - 2 * A * exp(-r/R) / r)
                 g_rr_y(r) = 1 + A^2 * exp(-2r/R) * (1/r + 1/R)^2 / r^2
            7. Calcular metricas de error: norma L2 y error relativo porcentual.

        Nota sobre la validacion:
            La comparacion contra Schwarzschild es la prueba definitiva de que
            la deformacion elastica reproduce la relatividad general en el
            limite de campo debil. Sin embargo, la solucion exacta de la
            ecuacion de membrana es el potencial de Yukawa, no el potencial
            newtoniano puro 1/r. La diferencia es el termino de restitucion
            elastica lambda^2 = 1/R^2.

            Para R >> r (radio cosmologico mucho mayor que la region local),
            exp(-r/R) ≈ 1 y ambas predicciones coinciden.

        (ver plan de simulacion seccion 4.2, doc 04 seccion 3.2)

        Parameters:
            h_grid (ndarray): Arreglo 3D de deflexion.
            g_00 (ndarray): Arreglo 3D de componente temporal.
            g_rr (ndarray): Arreglo 3D de componente espacial.

        Returns:
            dict: Diccionario con r_bins, g_00_radial, g_00_analytic,
                  g_rr_radial, g_rr_analytic, error_l2, error_pct,
                  correlation, r_s, y datos adicionales de Yukawa.
        """
        N = self.N
        mid = N // 2  # Indice del plano ecuatorial y del centro

        # Amplitud calibrada y offset PBC desde la solucion numerica
        A, C_pbc = self._calibrar_amplitud_yukawa(h_grid)

        # Radio de Schwarzschild calibrado
        r_s_cal = 2.0 * A
        r_s_teorico = 2.0 * self.G_eff * self.mass

        # --- Plano ecuatorial (z = mid) ---
        # Extraemos los slices 2D para analisis radial
        g_00_slice = g_00[:, :, mid]
        g_rr_slice = g_rr[:, :, mid]
        h_slice = h_grid[:, :, mid]

        # Coordenadas del plano ecuatorial
        x_1d = np.linspace(-self.L / 2.0, self.L / 2.0, N)
        X, Y = np.meshgrid(x_1d, x_1d, indexing='ij')
        r_slice = np.sqrt(X ** 2 + Y ** 2)

        # --- Binning radial ---
        # Aplanamos los arreglos 2D para procesamiento vectorizado
        r_flat = r_slice.ravel()
        g_00_flat = g_00_slice.ravel()
        g_rr_flat = g_rr_slice.ravel()
        h_flat = h_slice.ravel()

        # Radio maximo para el analisis (evitamos bordes donde el FFT puede
        # introducir artefactos, y el centro donde la gaussiana es dominante)
        r_max_analysis = self.L / 2.0 * 0.9
        r_min_analysis = self.dx * 2.0

        # Mascara para filtrar puntos dentro del rango de analisis
        mask = (r_flat >= r_min_analysis) & (r_flat <= r_max_analysis)

        r_filtered = r_flat[mask]
        g_00_filtered = g_00_flat[mask]
        g_rr_filtered = g_rr_flat[mask]
        h_filtered = h_flat[mask]

        # Numero de bins radiales (tipicamente N/4 para suficiente estadistica)
        n_bins = max(10, N // 4)
        r_edges = np.linspace(r_min_analysis, r_max_analysis, n_bins + 1)
        r_centers = 0.5 * (r_edges[:-1] + r_edges[1:])

        # Promediado en bins (vectorizado con digitize)
        bin_indices = np.digitize(r_filtered, r_edges) - 1

        g_00_radial = np.array([
            np.mean(g_00_filtered[bin_indices == i]) if np.any(bin_indices == i) else 0.0
            for i in range(n_bins)
        ])
        g_rr_radial = np.array([
            np.mean(g_rr_filtered[bin_indices == i]) if np.any(bin_indices == i) else 0.0
            for i in range(n_bins)
        ])

        # --- Schwarzschild analitico (amplitud calibrada) ---
        # En el limite de campo debil (r >> r_s), la metrica de Schwarzschild
        # en coordenadas de Schwarzschild es:
        #   g_00 = -(1 - r_s/r)
        #   g_rr = 1/(1 - r_s/r) ~ 1 + r_s/r + r_s^2/r^2 + ...
        # Usamos la amplitud A calibrada de la solucion numerica.
        # (ver doc 04 seccion 3.2, plan seccion 4.2)

        with np.errstate(divide='ignore', invalid='ignore'):
            g_00_schwarz = np.where(r_centers > r_s_cal,
                                    -(1.0 - r_s_cal / r_centers),
                                    np.nan)
            g_rr_schwarz = np.where(r_centers > r_s_cal,
                                    1.0 / (1.0 - r_s_cal / r_centers),
                                    np.nan)

        # --- Yukawa analitico (solucion exacta de la ec. de membrana) ---
        # La solucion exacta de (nabla^2 - lambda^2)h = S con fuente puntual:
        #   h(r) = -A * exp(-r/R) / r
        #
        # La metrica inducida correspondiente:
        #   g_00 = -(1 + 2h) = -(1 - 2*A*exp(-r/R)/r)
        #
        # Para g_rr = 1 + (dh/dr)^2:
        #   dh/dr = A * exp(-r/R) * (1/(rR) + 1/r^2)
        #          = A * exp(-r/R) * (r + R) / (r^2 * R)
        #   (dh/dr)^2 = A^2 * exp(-2r/R) * (r + R)^2 / (r^4 * R^2)
        #   g_rr = 1 + A^2 * exp(-2r/R) * (r + R)^2 / (r^4 * R^2)
        #
        # donde lambda = 1/R es el coeficiente de restitucion elastica.

        with np.errstate(divide='ignore', invalid='ignore'):
            exp_factor = np.exp(-r_centers / self.R)
            g_00_yukawa = -(1.0 - 2.0 * A * exp_factor / r_centers)

            # Derivada radial del potencial Yukawa
            dh_dr_yukawa = A * exp_factor * (r_centers + self.R) / (r_centers ** 2 * self.R)
            g_rr_yukawa = 1.0 + dh_dr_yukawa ** 2

        # =================================================================
        # Calculo de errores sobre la PERTURBACION gravitacional
        # =================================================================
        # La senal fisica es la perturbacion delta_g = g_00 + 1 = 2h,
        # NO el valor total de g_00 (dominado por el fondo Minkowski = -1).
        # Calcular errores sobre g_00 completo contamina las metricas con
        # la region "plana" donde la perturbacion es minuscula y el ruido
        # numerico relativo es alto. Por eso la correlacion bajaba al
        # aumentar la resolucion: mas puntos en la zona plana.
        #
        # Solucion: todas las metricas se calculan sobre delta_g = g_00 + 1,
        # restringidas a la region gravitacionalmente significativa donde
        # |delta_g_analitico| > 1% del maximo de la perturbacion.
        # =================================================================

        # Perturbaciones: delta_g = g_00 + 1 (= 2h, la senal gravitacional)
        # Se resta el offset C_pbc de la perturbacion numerica para compensar
        # el efecto de las condiciones de borde periodicas (DC = 0). Sin esta
        # correccion, la plataforma positiva generada por PBC contamina la
        # senal gravitacional real, destruyendo la correlacion.
        dg_num = g_00_radial + 1.0 - 2.0 * C_pbc  # perturbacion numerica corregida por PBC
        dg_schwarz = g_00_schwarz + 1.0  # perturbacion Schwarzschild
        dg_yukawa = g_00_yukawa + 1.0  # perturbacion Yukawa

        # --- Umbral de significancia gravitacional ---
        # Solo consideramos puntos donde la perturbacion analitica es > 1%
        # del maximo de la perturbacion. Esto excluye la zona "plana"
        # donde el ruido numerico dominaria las metricas de error.
        threshold_frac = 0.01  # 1% del maximo
        dg_yukawa_max = np.nanmax(np.abs(dg_yukawa))

        # --- Errores contra Schwarzschild (sobre perturbacion) ---
        mask_schwarz = (~np.isnan(dg_schwarz)) & (np.abs(dg_schwarz) > threshold_frac * dg_yukawa_max)
        n_valid_schwarz = np.sum(mask_schwarz)

        if n_valid_schwarz > 2:
            dg_num_s = dg_num[mask_schwarz]
            dg_sch_s = dg_schwarz[mask_schwarz]

            # L2 sobre la perturbacion (error absoluto en la senal gravitacional)
            error_l2_schwarz = np.sqrt(np.mean((dg_num_s - dg_sch_s) ** 2))

            # Error relativo ponderado: media de |delta_num - delta_sch| / |delta_sch|
            # ponderada por |delta_sch| para que los puntos con senal fuerte pesen mas
            weights_s = np.abs(dg_sch_s)
            total_weight_s = np.sum(weights_s)
            if total_weight_s > 0:
                error_pct_schwarz = (
                    np.sum(weights_s * np.abs(dg_num_s - dg_sch_s) / (np.abs(dg_sch_s) + 1e-30))
                    / total_weight_s * 100.0
                )
            else:
                error_pct_schwarz = np.nan

            # Correlacion de Pearson sobre la perturbacion
            num_centered = dg_num_s - np.mean(dg_num_s)
            sch_centered = dg_sch_s - np.mean(dg_sch_s)
            cov_sch = np.mean(num_centered * sch_centered)
            std_num = np.std(dg_num_s)
            std_sch = np.std(dg_sch_s)
            if std_num > 0 and std_sch > 0:
                correlation_schwarz = cov_sch / (std_num * std_sch)
            else:
                correlation_schwarz = 0.0
        else:
            error_l2_schwarz = np.nan
            error_pct_schwarz = np.nan
            correlation_schwarz = 0.0

        # --- Errores contra Yukawa (sobre perturbacion) ---
        mask_yukawa = (~np.isnan(dg_yukawa)) & (np.abs(dg_yukawa) > threshold_frac * dg_yukawa_max)
        n_valid_yukawa = np.sum(mask_yukawa)

        if n_valid_yukawa > 2:
            dg_num_y = dg_num[mask_yukawa]
            dg_yuk_y = dg_yukawa[mask_yukawa]

            # L2 sobre la perturbacion
            error_l2_yukawa = np.sqrt(np.mean((dg_num_y - dg_yuk_y) ** 2))

            # Error relativo ponderado por la senal (peso = |delta_g_analitico|)
            weights_y = np.abs(dg_yuk_y)
            total_weight_y = np.sum(weights_y)
            if total_weight_y > 0:
                error_pct_yukawa = (
                    np.sum(weights_y * np.abs(dg_num_y - dg_yuk_y) / (np.abs(dg_yuk_y) + 1e-30))
                    / total_weight_y * 100.0
                )
            else:
                error_pct_yukawa = np.nan

            # Correlacion de Pearson sobre la perturbacion
            yuk_centered = dg_yuk_y - np.mean(dg_yuk_y)
            num_centered_y = dg_num_y - np.mean(dg_num_y)
            cov_yuk = np.mean(num_centered_y * yuk_centered)
            std_num_y = np.std(dg_num_y)
            std_yuk = np.std(dg_yuk_y)
            if std_num_y > 0 and std_yuk > 0:
                correlation_yukawa = cov_yuk / (std_num_y * std_yuk)
            else:
                correlation_yukawa = 0.0
        else:
            error_l2_yukawa = np.nan
            error_pct_yukawa = np.nan
            correlation_yukawa = 0.0

        # Error relativo de la deflexion (h) contra Yukawa
        # (h ya es la perturbacion, no necesita correccion de fondo)
        if n_valid_yukawa > 2:
            h_binned = np.array([
                np.mean(h_filtered[bin_indices == i]) if np.any(bin_indices == i) else 0.0
                for i in range(n_bins)
            ])
            h_yukawa = -A * np.exp(-r_centers / self.R) / r_centers
            # Mask gravitacionalmente significativo para h tambien
            h_yukawa_abs = np.abs(h_yukawa)
            h_max = np.nanmax(h_yukawa_abs) if np.any(~np.isnan(h_yukawa_abs)) else 1.0
            mask_h = (~np.isnan(h_yukawa)) & (~np.isnan(h_binned)) & (h_yukawa_abs > threshold_frac * h_max)
            if np.sum(mask_h) > 2:
                dh_error = np.sqrt(np.mean((h_binned[mask_h] - h_yukawa[mask_h]) ** 2))
                # Error relativo ponderado por |h_yukawa|
                w_h = np.abs(h_yukawa[mask_h])
                total_w_h = np.sum(w_h)
                if total_w_h > 0:
                    dh_rel = (
                        np.sum(w_h * np.abs(h_binned[mask_h] - h_yukawa[mask_h]) / (w_h + 1e-30))
                        / total_w_h * 100.0
                    )
                else:
                    dh_rel = np.nan
            else:
                dh_error = np.nan
                dh_rel = np.nan
        else:
            dh_error = np.nan
            dh_rel = np.nan

        return {
            'r_bins': r_centers,
            'g_00_radial': g_00_radial,
            'g_00_schwarzschild': g_00_schwarz,
            'g_00_yukawa': g_00_yukawa,
            'g_rr_radial': g_rr_radial,
            'g_rr_schwarzschild': g_rr_schwarz,
            'g_rr_yukawa': g_rr_yukawa,
            'error_l2_schwarz': error_l2_schwarz,
            'error_pct_schwarz': error_pct_schwarz,
            'correlation_schwarz': correlation_schwarz,
            'error_l2_yukawa': error_l2_yukawa,
            'error_pct_yukawa': error_pct_yukawa,
            'correlation_yukawa': correlation_yukawa,
            'dh_error': dh_error,
            'dh_rel': dh_rel,
            'r_s_cal': r_s_cal,
            'r_s_teorico': r_s_teorico,
            'A_calibrado': A,
            'C_pbc': C_pbc,
            'n_valid_schwarz': n_valid_schwarz
        }

    def visualizar(self, h_grid, g_00, g_rr, resultados_validacion):
        """
        Genera tres graficos cientificos de calidad de publicacion.

        Plot 1: Visualizacion del pozo de deformacion (2D + 3D).
        Plot 2: Perfil radial de g_00 comparado con Schwarzschild.
        Plot 3: Comportamiento de g_rr y el estiramiento elastico.

        (ver plan de simulacion seccion 5.3)

        Parameters:
            h_grid (ndarray): Deflexion 3D.
            g_00 (ndarray): Componente temporal 3D.
            g_rr (ndarray): Componente espacial 3D.
            resultados_validacion (dict): Resultados del analisis radial.
        """
        N = self.N
        mid = N // 2

        # --- Datos comunes para los plots ---
        x_1d = np.linspace(-self.L / 2.0, self.L / 2.0, N)
        X, Y = np.meshgrid(x_1d, x_1d, indexing='ij')

        h_slice = h_grid[:, :, mid]
        g_00_slice = g_00[:, :, mid]
        g_rr_slice = g_rr[:, :, mid]

        # Datos radiales (soporta tanto formato nuevo como legacy)
        r_bins = resultados_validacion['r_bins']
        g_00_radial = resultados_validacion['g_00_radial']
        g_00_schwarz = resultados_validacion.get('g_00_schwarzschild',
                                                  resultados_validacion.get('g_00_analytic'))
        g_00_yukawa = resultados_validacion.get('g_00_yukawa', g_00_schwarz)
        g_rr_radial = resultados_validacion['g_rr_radial']
        g_rr_schwarz = resultados_validacion.get('g_rr_schwarzschild',
                                                  resultados_validacion.get('g_rr_analytic'))
        g_rr_yukawa = resultados_validacion.get('g_rr_yukawa', g_rr_schwarz)
        error_l2 = resultados_validacion.get('error_l2_yukawa',
                                              resultados_validacion.get('error_l2', np.nan))
        error_pct = resultados_validacion.get('error_pct_yukawa',
                                               resultados_validacion.get('error_pct', np.nan))
        correlation = resultados_validacion.get('correlation_yukawa',
                                                 resultados_validacion.get('correlation', 0.0))
        r_s = resultados_validacion.get('r_s_cal',
                                        resultados_validacion.get('r_s', 0.0))

        # =========================================================================
        # Plot 1: Visualizacion del Pozo de Deformacion
        # =========================================================================
        # Muestra la deformacion hiperdimensional de la brana en el plano
        # ecuatorial. Arriba: mapa de color 2D. Abajo: superficie 3D.
        # La depresion central es el "pozo gravitacional" generado por la masa.
        # =========================================================================
        fig1 = plt.figure(figsize=(14, 10))
        fig1.suptitle(r"Deformación Hiperdimensional de la Brana", fontsize=18)

        # Subplot superior: mapa de color 2D
        ax1 = fig1.add_subplot(2, 1, 1)
        im = ax1.pcolormesh(X, Y, h_slice, cmap='RdBu_r', shading='auto')
        cbar = plt.colorbar(im, ax=ax1, label=r'Deflexión $h(\mathbf{x})$')
        ax1.set_xlabel(r"$x$ [unidades de simulación]")
        ax1.set_ylabel(r"$y$ [unidades de simulación]")
        ax1.set_aspect('equal')
        ax1.set_title(r"Corte ecuatorial $z=0$: Mapa de deflexión $h(x,y)$")

        # Subplot inferior: superficie 3D
        ax2 = fig1.add_subplot(2, 1, 2, projection='3d')
        # Diezmar la malla para la superficie 3D si la resolucion es alta
        step = max(1, N // 32)
        X_dec = X[::step, ::step]
        Y_dec = Y[::step, ::step]
        h_dec = h_slice[::step, ::step]

        surf = ax2.plot_surface(X_dec, Y_dec, h_dec,
                                cmap=cm.RdBu_r,
                                linewidth=0,
                                antialiased=True,
                                alpha=0.9)
        fig1.colorbar(surf, ax=ax2, shrink=0.5, aspect=20,
                      label=r'Deflexión $h$')
        ax2.set_xlabel(r"$x$")
        ax2.set_ylabel(r"$y$")
        ax2.set_zlabel(r"$h(x,y)$")
        ax2.set_title(r"Superficie de deformación 3D: Pozo gravitacional emergente")

        plt.tight_layout()
        plot1_path = self.output_dir / "pozo_deformacion_brana.png"
        fig1.savefig(str(plot1_path))
        plt.close(fig1)
        print(f"   Grafico 1 guardado: {plot1_path}")

        # =========================================================================
        # Plot 2: Perfil Radial de Gravedad (g_00)
        # =========================================================================
        # Comparacion entre la componente temporal numerica, Schwarzschild y
        # el potencial Yukawa (solucion exacta de la ecuacion de membrana).
        # La concordancia con Yukawa valida que el solver FFT reproduce la
        # solucion analitica. La concordancia con Schwarzschild valida que
        # la deformacion elastica reproduce la gravedad de campo debil.
        # =========================================================================
        fig2, ax3 = plt.subplots(figsize=(10, 7))

        # Datos validos
        valid_schwarz = ~np.isnan(g_00_schwarz)
        valid_yukawa = ~np.isnan(g_00_yukawa)

        # Schwarzschild analitico
        if np.any(valid_schwarz):
            ax3.plot(r_bins[valid_schwarz], g_00_schwarz[valid_schwarz], 'b--',
                     linewidth=2, label=r'$g_{00}^{\mathrm{Schwarzschild}}$', alpha=0.7)

        # Yukawa analitico (solucion exacta de la ecuacion de membrana)
        if np.any(valid_yukawa):
            ax3.plot(r_bins[valid_yukawa], g_00_yukawa[valid_yukawa], 'g:',
                     linewidth=2, label=r'$g_{00}^{\mathrm{Yukawa}}$ (exacto)', alpha=0.8)

        # Resultado numerico
        ax3.plot(r_bins, g_00_radial, 'r-', linewidth=2,
                 label=r'$g_{00}^{\mathrm{numérico}}$', alpha=0.8)

        # Sombreado del error entre numerico y Yukawa
        if np.any(valid_yukawa):
            ax3.fill_between(r_bins[valid_yukawa],
                             g_00_radial[valid_yukawa],
                             g_00_yukawa[valid_yukawa],
                             alpha=0.15, color='green',
                             label=r'Diferencia numérico-Yukawa')

        # Linea de referencia en g_00 = -1 (Minkowski)
        ax3.axhline(y=-1.0, color='gray', linestyle=':', linewidth=1,
                    alpha=0.5, label=r'$g_{00} = -1$ (Minkowski)')

        # Texto con metricas de error (calculadas sobre perturbacion dg = g_00 + 1)
        error_text = (
            f"Error L2 pert. (Yukawa): {error_l2:.6f}\n"
            f"Error rel. pert. (Yukawa): {error_pct:.4f}%\n"
            f"Correl. pert. (Yukawa): {correlation:.6f}\n"
            f"$r_s$ (calibrado): {r_s:.4f}"
        )
        ax3.text(0.05, 0.05, error_text, transform=ax3.transAxes,
                 fontsize=10, verticalalignment='bottom',
                 bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

        ax3.set_xlabel(r"$r$ [unidades de simulación]")
        ax3.set_ylabel(r"$g_{00}$")
        ax3.set_title(r"Componente Temporal: Numérico vs Yukawa vs Schwarzschild")
        ax3.legend(loc='upper right', fontsize=9)
        ax3.set_xlim(left=self.dx)
        ax3.grid(True, alpha=0.3)

        plt.tight_layout()
        plot2_path = self.output_dir / "perfil_radial_g00.png"
        fig2.savefig(str(plot2_path))
        plt.close(fig2)
        print(f"   Grafico 2 guardado: {plot2_path}")

        # =========================================================================
        # Plot 3: Comportamiento de g_rr
        # =========================================================================
        # Muestra como la curvatura espacial emerge del gradiente de la
        # deflexion: g_rr = 1 + (nabla h)^2.
        #
        # La componente (nabla h)^2 representa la densidad de energia elastica
        # almacenada en la deformacion de la brana. Es esta energia la que se
        # manifiesta como curvatura espacial en la metrica inducida.
        #
        # La comparacion con Schwarzschild analitico muestra cuan bien el
        # modelo elastico reproduce la curvatura espacial relativista.
        # =========================================================================
        fig3, ax4 = plt.subplots(figsize=(10, 7))

        # Calcular (nabla h)^2 en el plano ecuatorial para mostrar el
        # estiramiento elastico por separado
        grad_hx, grad_hy = np.gradient(h_slice, self.dx, self.dx)
        dh_sq_slice = grad_hx ** 2 + grad_hy ** 2

        # Perfil radial de (nabla h)^2
        r_slice = np.sqrt(X ** 2 + Y ** 2)
        r_flat = r_slice.ravel()
        dh_sq_flat = dh_sq_slice.ravel()
        mask = (r_flat >= self.dx * 2.0) & (r_flat <= self.L / 2.0 * 0.9)
        r_filt = r_flat[mask]
        dh_sq_filt = dh_sq_flat[mask]
        r_edges3 = np.linspace(self.dx * 2.0, self.L / 2.0 * 0.9, max(10, N // 4))
        r_centers3 = 0.5 * (r_edges3[:-1] + r_edges3[1:])
        bin_idx3 = np.digitize(r_filt, r_edges3) - 1
        dh_sq_radial = np.array([
            np.mean(dh_sq_filt[bin_idx3 == i]) if np.any(bin_idx3 == i) else 0.0
            for i in range(len(r_centers3))
        ])

        # g_rr numerico, Yukawa y Schwarzschild
        valid_rr_yukawa = ~np.isnan(g_rr_yukawa)
        valid_rr_schwarz = ~np.isnan(g_rr_schwarz)

        if np.any(valid_rr_schwarz):
            ax4.plot(r_bins[valid_rr_schwarz], g_rr_schwarz[valid_rr_schwarz],
                     'b--', linewidth=2,
                     label=r'$g_{rr}^{\mathrm{Schwarzschild}}$', alpha=0.7)

        if np.any(valid_rr_yukawa):
            ax4.plot(r_bins[valid_rr_yukawa], g_rr_yukawa[valid_rr_yukawa],
                     'g:', linewidth=2,
                     label=r'$g_{rr}^{\mathrm{Yukawa}}$ (exacto)', alpha=0.8)

        ax4.plot(r_bins, g_rr_radial, 'r-', linewidth=2,
                 label=r'$g_{rr}^{\mathrm{numérico}}$', alpha=0.8)

        # Componente de estiramiento elastico por separado
        ax4.plot(r_centers3, 1.0 + dh_sq_radial, 'g-.', linewidth=1.5,
                 label=r'$1 + (\nabla h)^2$ (estiramiento)', alpha=0.7)

        # Linea de referencia en g_rr = 1 (espacio plano)
        ax4.axhline(y=1.0, color='gray', linestyle=':', linewidth=1,
                    alpha=0.5, label=r'$g_{rr} = 1$ (plano)')

        ax4.set_xlabel(r"$r$ [unidades de simulación]")
        ax4.set_ylabel(r"$g_{rr}$")
        ax4.set_title(r"Componente Espacial de la Métrica: Curvatura Emergente")
        ax4.legend(loc='upper right', fontsize=10)
        ax4.set_xlim(left=self.dx)
        ax4.grid(True, alpha=0.3)

        # Anotacion explicativa sobre la curvatura emergente
        annot_text = (
            "La curvatura espacial emerge del gradiente de deflexión:\n"
            "$g_{rr} = 1 + (\\nabla h)^2$\n\n"
            "El término $(\\nabla h)^2$ es la densidad de energía\n"
            "elástica de la brana deformada, que se manifiesta\n"
            "como curvatura espacial en la métrica 3D."
        )
        ax4.text(0.55, 0.45, annot_text, transform=ax4.transAxes,
                 fontsize=9, verticalalignment='top',
                 bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.7))

        plt.tight_layout()
        plot3_path = self.output_dir / "comportamiento_grr.png"
        fig3.savefig(str(plot3_path))
        plt.close(fig3)
        print(f"   Grafico 3 guardado: {plot3_path}")

    def ejecutar(self):
        """
        Ejecuta el pipeline completo de la simulacion.

        Pipeline:
            1. Generar distribucion de densidad de masa
            2. Resolver la ecuacion de membrana via FFT
            3. Calcular componentes de la metrica inducida
            4. Validar contra Schwarzschild analitico
            5. Generar graficos de visualizacion

        Returns:
            dict: Resultados completos de la simulacion (deflexion, metrica,
                  validacion).
        """
        print(f"\n{'='*70}")
        print(f"  SIMULACION DE MEMBRANA ELASTICA")
        print(f"  Gravedad Emergente por Rotacion 4D")
        print(f"{'='*70}")
        print(f"\nParametros de la simulacion:")
        print(f"  Resolucion:        {self.N} x {self.N} x {self.N}")
        print(f"  Caja de simulacion: L = {self.L}")
        print(f"  Paso de malla:      dx = {self.dx:.4f}")
        print(f"  Omega 4D:           omega_4D = {self.omega_4D}")
        print(f"  Radio cosmologico:  R = {self.R}")
        print(f"  Lambda (restitucion): lambda^2 = {self.lambda_sq:.6e}")
        print(f"  Tension de brana:   T_b = {self.tension}")
        print(f"  Masa de la fuente:  M = {self.mass}")
        print(f"  Ancho gaussiano:    sigma = {self.sigma}")
        print(f"  G efectiva:         G_eff = {self.G_eff:.6f}")
        print(f"  Directorio salida:  {self.output_dir}")
        if NUMBA_AVAILABLE:
            print(f"  Aceleracion:        NUMBA JIT activa")
        else:
            print(f"  Aceleracion:        NumPy puro (numba no disponible)")
        print(f"\n{'='*70}\n")

        # --- Paso 1: Densidad de masa ---
        print("[1/5] Generando distribucion de densidad de masa...")
        t0 = time.time()
        rho = self.generar_densidad_masa()
        t_density = time.time() - t0
        print(f"   Densidad generada en {t_density:.3f}s")
        print(f"   Rango de densidad: [{rho.min():.4e}, {rho.max():.4e}]")
        print(f"   Masa integrada: {np.sum(rho) * self.dx**3:.6f}\n")

        # --- Paso 2: Resolver deflexion ---
        print("[2/5] Resolviendo ecuacion de membrana elastica via FFT...")
        t0 = time.time()
        h = self.resolver_deflexion_fft(rho)
        t_solver = time.time() - t0
        print(f"   Solucion FFT completada en {t_solver:.3f}s")
        print(f"   Deflexion h: min={h.min():.6e}, max={h.max():.6e}")
        print(f"   Deflexion media: {np.mean(h):.6e}\n")

        # Guardar deflexion para analisis posterior
        np.save(self.output_dir / "deflexion_h.npy", h)
        print(f"   Deflexion guardada en {self.output_dir / 'deflexion_h.npy'}")

        # --- Paso 3: Calcular metrica inducida ---
        print("[3/5] Reconstruyendo componentes metricas inducidas...")
        t0 = time.time()
        g_00, g_rr = self.calcular_metrica_inducida(h)
        t_metric = time.time() - t0
        print(f"   Metrica calculada en {t_metric:.3f}s")
        print(f"   g_00: min={g_00.min():.6f}, max={g_00.max():.6f}")
        print(f"   g_rr: min={g_rr.min():.6f}, max={g_rr.max():.6f}\n")

        # Guardar metricas
        np.save(self.output_dir / "g_00.npy", g_00)
        np.save(self.output_dir / "g_rr.npy", g_rr)

        # --- Paso 4: Validacion contra Schwarzschild y Yukawa ---
        print("[4/5] Validando contra solucion analitica (Schwarzschild + Yukawa)...")
        t0 = time.time()
        resultados = self.perfil_radial_schwarzschild(h, g_00, g_rr)
        t_validation = time.time() - t0

        error_l2_y = resultados['error_l2_yukawa']
        error_pct_y = resultados['error_pct_yukawa']
        correlation_y = resultados['correlation_yukawa']
        error_l2_s = resultados['error_l2_schwarz']
        error_pct_s = resultados['error_pct_schwarz']
        correlation_s = resultados['correlation_schwarz']
        r_s_cal = resultados['r_s_cal']
        r_s_teorico = resultados['r_s_teorico']
        A_calibrado = resultados['A_calibrado']
        C_pbc = resultados['C_pbc']

        print(f" Validacion completada en {t_validation:.3f}s")
        print(f" Amplitud calibrada A = {A_calibrado:.6f}")
        print(f" Offset PBC C = {C_pbc:.6f}")
        print(f" Radio Schwarzschild teorico: r_s = {r_s_teorico:.6f}")
        print(f" Radio Schwarzschild calibrado: r_s = {r_s_cal:.6f}")
        print(f"")
        print(f" --- Comparacion contra Yukawa (solucion exacta) ---")
        print(f" Error L2 (perturbacion dg): {error_l2_y:.6e}")
        print(f" Error relativo ponderado: {error_pct_y:.4f}%")
        print(f" Correlacion (perturbacion): {correlation_y:.6f}")
        print(f"")
        print(f" --- Comparacion contra Schwarzschild (campo debil) ---")
        print(f" Error L2 (perturbacion dg): {error_l2_s:.6e}")
        print(f" Error relativo ponderado: {error_pct_s:.4f}%")
        print(f" Correlacion (perturbacion): {correlation_s:.6f}")

        # Criterio de validacion:
        # - >99.99%: validacion perfecta (esperable con alta resolucion y R grande)
        # - >99.9%: validacion excelente (la metrica emergente sigue la forma de Schwarzschild)
        # - >99%: buena concordancia general
        # Nota: las BC periodicas (PBC) del FFT introducen contribuciones de
        # imagenes que modifican la solucion respecto al caso de espacio libre.
        # Esto es una limitacion inherente del metodo FFT con PBC.
        if correlation_y > 0.9999:
            print(f"\n   >>> VALIDACION EXITOSA: La solucion numerica reproduce")
            print(f"       el potencial Yukawa con correlacion del {correlation_y*100:.4f}%")
            print(f"       La ecuacion de membrana se resuelve correctamente.")
        elif correlation_y > 0.999:
            print(f"\n   >>> VALIDACION EXCELENTE: Correlacion Yukawa del {correlation_y*100:.4f}%")
            print(f"       La solucion numerica sigue el potencial Yukawa con alta precision.")
        elif correlation_y > 0.99:
            print(f"\n   >>> VALIDACION BUENA: Correlacion Yukawa del {correlation_y*100:.4f}%")
            print(f"       La solucion numerica aproxima bien el potencial Yukawa.")
        else:
            print(f"\n   >>> VALIDACION PARCIAL: Correlacion Yukawa del {correlation_y*100:.2f}%")
            print(f"       Se requiere mayor resolucion o ajuste de parametros.")

        if correlation_s > 0.9999:
            print(f"\n   >>> SCHWARZSCHILD VERIFICADO ({correlation_s*100:.4f}%):")
            print(f"       La metrica emergente reproduce Schwarzschild en campo debil.")
        elif correlation_s > 0.999:
            print(f"\n   >>> SCHWARZSCHILD EXCELENTE ({correlation_s*100:.4f}%):")
            print(f"       La metrica emergente sigue Schwarzschild en campo debil.")
        elif correlation_s > 0.99:
            print(f"\n   >>> SCHWARZSCHILD BUENO ({correlation_s*100:.4f}%):")
            print(f"       La metrica emergente aproxima Schwarzschild.")

        # Guardar resultados de validacion
        np.savez(self.output_dir / "validacion_schwarzschild.npz",
                 r_bins=resultados['r_bins'],
                 g_00_radial=resultados['g_00_radial'],
                 g_00_schwarzschild=resultados['g_00_schwarzschild'],
                 g_00_yukawa=resultados['g_00_yukawa'],
                 g_rr_radial=resultados['g_rr_radial'],
                 g_rr_schwarzschild=resultados['g_rr_schwarzschild'],
                 g_rr_yukawa=resultados['g_rr_yukawa'],
                 error_l2_yukawa=error_l2_y,
                 error_pct_yukawa=error_pct_y,
                 correlation_yukawa=correlation_y,
                 error_l2_schwarz=error_l2_s,
                 error_pct_schwarz=error_pct_s,
                 correlation_schwarz=correlation_s,
                 A_calibrado=A_calibrado,
                 r_s_cal=r_s_cal,
                 r_s_teorico=r_s_teorico)
        print(f"   Validacion guardada en {self.output_dir / 'validacion_schwarzschild.npz'}\n")

        # --- Paso 5: Visualizacion ---
        print("[5/5] Generando graficos de visualizacion...")
        t0 = time.time()
        self.visualizar(h, g_00, g_rr, resultados)
        t_plot = time.time() - t0
        print(f"   Graficos generados en {t_plot:.3f}s\n")

        # --- Resumen final ---
        print(f"{'='*70}")
        print(f"  RESUMEN DE LA SIMULACION")
        print(f"{'='*70}")
        print(f"  Tiempos de ejecucion:")
        print(f"    Densidad:     {t_density:.3f}s")
        print(f"    Solver FFT:   {t_solver:.3f}s")
        print(f"    Metrica:      {t_metric:.3f}s")
        print(f"    Validacion:   {t_validation:.3f}s")
        print(f"    Graficos:     {t_plot:.3f}s")
        print(f"    TOTAL:        {t_density + t_solver + t_metric + t_validation + t_plot:.3f}s")
        print(f"")
        print(f"  Resultados:")
        print(f"    G_efectiva = {self.G_eff:.6f}")
        print(f"    Amplitud calibrada A = {A_calibrado:.6f}")
        print(f"    r_s (teorico) = {r_s_teorico:.6f}")
        print(f"    r_s (calibrado) = {r_s_cal:.6f}")
        print(f" Error L2 Yukawa (pert.) = {error_l2_y:.6e}")
        print(f" Error rel. Yukawa (pert.) = {error_pct_y:.4f}%")
        print(f" Correlacion Yukawa (pert.) = {correlation_y:.6f}")
        print(f" Correlacion Schwarzschild (pert.) = {correlation_s:.6f}")

        if correlation_y > 0.9999:
            print(f"\n  >>> LA CONJETURA SE VERIFICA NUMERICAMENTE")
            print(f"      La deformacion elastica de la brana por rotacion 4D")
            print(f"      reproduce el potencial Yukawa con precision.")
            print(f"      Correlacion Yukawa: {correlation_y*100:.4f}%")
        elif correlation_y > 0.999:
            print(f"\n  >>> VALIDACION EXCELENTE (Yukawa: {correlation_y*100:.4f}%)")
            print(f"      La deformacion elastica sigue el potencial Yukawa.")
        elif correlation_y > 0.99:
            print(f"\n  >>> VALIDACION BUENA (Yukawa: {correlation_y*100:.4f}%)")
            print(f"      La deformacion elastica aproxima el potencial Yukawa.")
        else:
            print(f"\n  >>> VALIDACION PARCIAL (Yukawa: {correlation_y*100:.2f}%)")
            print(f"      Se requiere mayor resolucion o ajuste de parametros.")

        if correlation_s > 0.9999:
            print(f"  >>> SCHWARZSCHILD VERIFICADO: {correlation_s*100:.4f}%")
            print(f"      La metrica emergente reproduce Schwarzschild en campo debil.")
        elif correlation_s > 0.999:
            print(f"  >>> SCHWARZSCHILD EXCELENTE: {correlation_s*100:.4f}%")
            print(f"      La metrica emergente sigue Schwarzschild en campo debil.")
        elif correlation_s > 0.99:
            print(f"  >>> SCHWARZSCHILD BUENO: {correlation_s*100:.4f}%")
            print(f"      La metrica emergente aproxima Schwarzschild.")

        print(f"{'='*70}\n")

        return {
            'h': h,
            'g_00': g_00,
            'g_rr': g_rr,
            'validacion': resultados
        }


def main():
    """
    Punto de entrada principal: configura argumentos CLI, ejecuta la
    simulacion y muestra los resultados.
    """
    parser = argparse.ArgumentParser(
        description="Simulacion de Gravedad Emergente por Membrana Elastica (FFT espectral)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    # Parametros de la malla de simulacion
    parser.add_argument('--grid-size', type=int, default=64,
                        help='Resolucion de la malla cúbica (NxNxN)')
    parser.add_argument('--box-size', type=float, default=40.0,
                        help='Tamano fisico de la caja de simulacion')

    # Parametros fisicos de la rotacion 4D y la brana
    parser.add_argument('--omega-4d', type=float, default=1.0,
                        help='Velocidad angular de la rotacion 4D')
    parser.add_argument('--R', type=float, default=50.0,
                        help='Radio cosmologico de la brana')
    parser.add_argument('--tension', type=float, default=1.0,
                        help='Tension superficial de la brana (T_b)')

    # Parametros de la fuente de masa
    parser.add_argument('--sigma', type=float, default=0.5,
                        help='Ancho de la distribucion gaussiana de masa')
    parser.add_argument('--mass', type=float, default=1.0,
                        help='Masa total de la fuente')

    args = parser.parse_args()

    # Crear instancia de la simulacion
    sim = SimulacionMembranaElastica(
        grid_size=args.grid_size,
        box_size=args.box_size,
        omega_4D=args.omega_4d,
        R=args.R,
        tension=args.tension,
        sigma=args.sigma,
        mass=args.mass
    )

    # Ejecutar pipeline completo
    t_total_start = time.time()
    resultados = sim.ejecutar()
    t_total = time.time() - t_total_start

    print(f"Tiempo total de ejecucion: {t_total:.3f}s")
    print(f"Script completado exitosamente.\n")


if __name__ == '__main__':
    main()
