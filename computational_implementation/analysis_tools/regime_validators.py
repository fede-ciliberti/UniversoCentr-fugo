#!/usr/bin/env python3
"""
Validadores especializados para regímenes físicos específicos.
Módulo de la Tarea 2.1.2 - Validación de Regímenes Físicos

Este módulo contiene las clases especializadas para validar:
- Régimen Local (Schwarzschild)
- Régimen Global (Cosmológico) 
- Análisis de Zona de Transición

Fecha: 29 de junio de 2025
Autor: Universo Centrífugo Research Team
"""

import numpy as np
from scipy.optimize import curve_fit
from scipy import ndimage

class LocalRegimeValidator:
    """
    Validador especializado para el régimen gravitacional local (Schwarzschild).
    
    Verifica que la métrica cerca de la masa local reproduce aproximadamente
    la solución de Schwarzschild en el límite de campo débil.
    """
    
    def __init__(self, tolerance=0.01):
        """
        Args:
            tolerance: Tolerancia para desviación de la masa teórica (default: 1%)
        """
        self.tolerance = tolerance
    
    def validate(self, common_data):
        """
        Ejecuta la validación completa del régimen local.
        
        Args:
            common_data: Datos comunes preparados por el validador principal
            
        Returns:
            dict: Resultados de la validación local
        """
        print("\n🌌 VALIDACIÓN DEL RÉGIMEN LOCAL (SCHWARZSCHILD)")
        print("=" * 60)
        
        # Extraer datos de la región local
        local_mask = common_data['regions']['local']
        
        if np.sum(local_mask) == 0:
            return {'success': False, 'error': 'No data in local region'}
        
        # Extraer componentes métricos en la región local
        metric_components = common_data['metric_components']
        r_field = common_data['r_field']
        
        r_local = r_field[local_mask]
        g_xx_local = metric_components['gamma_xx'][local_mask]
        g_yy_local = metric_components['gamma_yy'][local_mask]
        g_zz_local = metric_components['gamma_zz'][local_mask]
        
        print(f"📊 Datos de región local:")
        print(f"   • Puntos analizados: {len(r_local)}")
        print(f"   • Rango radial: {np.min(r_local):.3f} - {np.max(r_local):.3f}")
        
        # Promediar en bins radiales para reducir ruido
        r_centers, metric_profiles = self._compute_radial_profiles(
            r_local, g_xx_local, g_yy_local, g_zz_local
        )
        
        if len(r_centers) < 3:
            return {'success': False, 'error': 'Insufficient radial points'}
        
        # Ajustar a formas de Schwarzschild
        schwarzschild_fits = self._fit_schwarzschild_profiles(
            r_centers, metric_profiles, common_data['mass_params']['mass']
        )
        
        # Evaluar éxito de la validación
        success = self._evaluate_local_success(schwarzschild_fits)
        
        return {
            'success': success,
            'r_centers': r_centers,
            'metric_profiles': metric_profiles,
            'schwarzschild_fits': schwarzschild_fits,
            'mass_measurements': {comp: fit['M_eff'] for comp, fit in schwarzschild_fits.items()},
            'validation_summary': self._create_local_summary(schwarzschild_fits)
        }
    
    def _compute_radial_profiles(self, r_local, g_xx, g_yy, g_zz, n_bins=10):
        """Calcula perfiles radiales promediados."""
        r_bins = np.linspace(np.min(r_local), np.max(r_local), n_bins + 1)
        r_centers = []
        profiles = {'g_xx': [], 'g_yy': [], 'g_zz': []}
        
        for i in range(n_bins):
            bin_mask = (r_local >= r_bins[i]) & (r_local < r_bins[i+1])
            if np.sum(bin_mask) > 0:
                r_centers.append(np.mean(r_local[bin_mask]))
                profiles['g_xx'].append(np.mean(g_xx[bin_mask]))
                profiles['g_yy'].append(np.mean(g_yy[bin_mask]))
                profiles['g_zz'].append(np.mean(g_zz[bin_mask]))
        
        return np.array(r_centers), {k: np.array(v) for k, v in profiles.items()}
    
    def _fit_schwarzschild_profiles(self, r_centers, profiles, expected_mass):
        """Ajusta perfiles métricos a formas de Schwarzschild."""
        fits = {}
        
        def schwarzschild_weak_field(r, M_eff):
            """Schwarzschild en aproximación de campo débil: g ≈ 1 + 2M/r"""
            return 1.0 + 2*M_eff/r
        
        for component, profile_data in profiles.items():
            try:
                # Ajuste con masa esperada como valor inicial
                popt, pcov = curve_fit(
                    schwarzschild_weak_field, 
                    r_centers, 
                    profile_data,
                    p0=[expected_mass],
                    maxfev=1000
                )
                
                M_eff = popt[0]
                profile_theory = schwarzschild_weak_field(r_centers, M_eff)
                error_rms = np.sqrt(np.mean((profile_data - profile_theory)**2))
                mass_deviation = abs(M_eff - expected_mass) / expected_mass
                
                fits[component] = {
                    'M_eff': M_eff,
                    'error_rms': error_rms,
                    'mass_deviation': mass_deviation,
                    'profile_theory': profile_theory,
                    'fit_success': True
                }
                
                print(f"   {component}: M_eff = {M_eff:.4f}, error = {error_rms:.6f}, dev = {mass_deviation*100:.2f}%")
                
            except Exception as e:
                fits[component] = {
                    'fit_success': False,
                    'error': str(e)
                }
                print(f"   {component}: Ajuste fallido - {e}")
        
        return fits
    
    def _evaluate_local_success(self, fits):
        """Evalúa si la validación local es exitosa."""
        successful_fits = [fit for fit in fits.values() if fit.get('fit_success', False)]
        
        if len(successful_fits) == 0:
            return False
        
        # Criterio: al menos 2 componentes con desviación de masa < tolerancia
        valid_components = [
            fit for fit in successful_fits 
            if fit.get('mass_deviation', float('inf')) < self.tolerance
        ]
        
        return len(valid_components) >= 2
    
    def _create_local_summary(self, fits):
        """Crea resumen de la validación local."""
        successful_fits = [fit for fit in fits.values() if fit.get('fit_success', False)]
        
        if len(successful_fits) == 0:
            return "❌ Ningún ajuste exitoso"
        
        avg_deviation = np.mean([fit['mass_deviation'] for fit in successful_fits])
        avg_error = np.mean([fit['error_rms'] for fit in successful_fits])
        
        status = "✅ VÁLIDO" if avg_deviation < self.tolerance else "⚠️  PARCIAL"
        
        return f"{status} - Desv. masa: {avg_deviation*100:.1f}%, RMS: {avg_error:.4f}"

class GlobalRegimeValidator:
    """
    Validador especializado para el régimen cosmológico global.
    
    Verifica que la métrica en regiones lejanas preserve las propiedades
    cosmológicas esperadas (isotropía, expansión de Hubble).
    """
    
    def __init__(self, tolerance=0.05):
        """
        Args:
            tolerance: Tolerancia para desviaciones del régimen cosmológico (default: 5%)
        """
        self.tolerance = tolerance
    
    def validate(self, common_data):
        """
        Ejecuta la validación completa del régimen global.
        
        Args:
            common_data: Datos comunes preparados por el validador principal
            
        Returns:
            dict: Resultados de la validación global
        """
        print("\n🌌 VALIDACIÓN DEL RÉGIMEN GLOBAL (COSMOLÓGICO)")
        print("=" * 60)
        
        global_mask = common_data['regions']['global']
        
        if np.sum(global_mask) == 0:
            return {'success': False, 'error': 'No data in global region'}
        
        # Analizar isotropía
        isotropy_results = self._analyze_isotropy(common_data, global_mask)
        
        # Analizar perturbaciones
        perturbation_results = self._analyze_perturbations(common_data, global_mask)
        
        # Analizar evolución temporal si disponible
        temporal_results = self._analyze_temporal_evolution(common_data)
        
        # Evaluar éxito global
        success = self._evaluate_global_success(isotropy_results, perturbation_results)
        
        return {
            'success': success,
            'isotropy': isotropy_results,
            'perturbations': perturbation_results,
            'temporal_evolution': temporal_results,
            'max_perturbation': perturbation_results.get('max_perturbation', 0),
            'validation_summary': self._create_global_summary(isotropy_results, perturbation_results)
        }
    
    def _analyze_isotropy(self, common_data, global_mask):
        """Analiza la isotropía en la región global."""
        metric_components = common_data['metric_components']
        
        gamma_xx_global = metric_components['gamma_xx'][global_mask]
        gamma_yy_global = metric_components['gamma_yy'][global_mask]
        gamma_zz_global = metric_components['gamma_zz'][global_mask]
        
        # Calcular desviaciones de isotropía
        isotropy_xx_yy = np.mean(np.abs(gamma_xx_global - gamma_yy_global))
        isotropy_yy_zz = np.mean(np.abs(gamma_yy_global - gamma_zz_global))
        isotropy_xx_zz = np.mean(np.abs(gamma_xx_global - gamma_zz_global))
        
        max_anisotropy = max(isotropy_xx_yy, isotropy_yy_zz, isotropy_xx_zz)
        
        print(f"📏 Análisis de isotropía:")
        print(f"   • |γ_xx - γ_yy|: {isotropy_xx_yy:.6f}")
        print(f"   • |γ_yy - γ_zz|: {isotropy_yy_zz:.6f}")
        print(f"   • |γ_xx - γ_zz|: {isotropy_xx_zz:.6f}")
        print(f"   • Máxima anisotropía: {max_anisotropy:.6f}")
        
        is_isotropic = max_anisotropy < self.tolerance
        
        return {
            'max_anisotropy': max_anisotropy,
            'isotropy_components': {
                'xx_yy': isotropy_xx_yy,
                'yy_zz': isotropy_yy_zz,
                'xx_zz': isotropy_xx_zz
            },
            'is_isotropic': is_isotropic
        }
    
    def _analyze_perturbations(self, common_data, global_mask):
        """Analiza perturbaciones de la métrica plana."""
        metric_components = common_data['metric_components']
        
        # Calcular desviaciones de métrica plana
        gamma_xx_global = metric_components['gamma_xx'][global_mask]
        gamma_yy_global = metric_components['gamma_yy'][global_mask]
        gamma_zz_global = metric_components['gamma_zz'][global_mask]
        
        # Términos cruzados (deberían ser ~0 para métrica diagonal)
        gamma_xy_global = metric_components['gamma_xy'][global_mask]
        gamma_xz_global = metric_components['gamma_xz'][global_mask]
        gamma_yz_global = metric_components['gamma_yz'][global_mask]
        
        diagonal_deviations = [
            np.mean(np.abs(gamma_xx_global - 1.0)),
            np.mean(np.abs(gamma_yy_global - 1.0)),
            np.mean(np.abs(gamma_zz_global - 1.0))
        ]
        
        off_diagonal_magnitudes = [
            np.mean(np.abs(gamma_xy_global)),
            np.mean(np.abs(gamma_xz_global)),
            np.mean(np.abs(gamma_yz_global))
        ]
        
        max_diagonal_perturbation = max(diagonal_deviations)
        max_off_diagonal = max(off_diagonal_magnitudes)
        max_perturbation = max(max_diagonal_perturbation, max_off_diagonal)
        
        print(f"📊 Análisis de perturbaciones:")
        print(f"   • Max desviación diagonal: {max_diagonal_perturbation:.6f}")
        print(f"   • Max término cruzado: {max_off_diagonal:.6f}")
        print(f"   • Perturbación máxima: {max_perturbation:.6f}")
        
        return {
            'max_perturbation': max_perturbation,
            'diagonal_deviations': diagonal_deviations,
            'off_diagonal_magnitudes': off_diagonal_magnitudes,
            'is_unperturbed': max_perturbation < self.tolerance
        }
    
    def _analyze_temporal_evolution(self, common_data):
        """Analiza evolución temporal si hay datos disponibles."""
        raw_data = common_data['raw_data']
        
        if 'time_evolution' not in raw_data['base_results']:
            return {'available': False}
        
        time_evolution = raw_data['base_results']['time_evolution']
        metric_evolution = raw_data['base_results']['metric_evolution']
        
        if len(time_evolution) < 2:
            return {'available': False}
        
        # Analizar evolución del determinante (factor de escala)
        det_evolution = [m['det_gamma'] for m in metric_evolution]
        times = time_evolution
        
        det_initial = det_evolution[0]
        det_final = det_evolution[-1]
        time_span = times[-1] - times[0]
        
        if time_span > 0:
            expansion_rate = (det_final - det_initial) / (det_initial * time_span)
        else:
            expansion_rate = 0
        
        print(f"⏱️  Análisis temporal:")
        print(f"   • Span temporal: {time_span:.4f}")
        print(f"   • Tasa de expansión: {expansion_rate:.6f}")
        
        return {
            'available': True,
            'times': times,
            'det_evolution': det_evolution,
            'expansion_rate': expansion_rate,
            'time_span': time_span,
            'expansion_detected': abs(expansion_rate) > 1e-6
        }
    
    def _evaluate_global_success(self, isotropy_results, perturbation_results):
        """Evalúa el éxito de la validación global."""
        is_isotropic = isotropy_results.get('is_isotropic', False)
        is_unperturbed = perturbation_results.get('is_unperturbed', False)
        
        # Criterio: tanto isotropía como ausencia de perturbaciones
        return is_isotropic and is_unperturbed
    
    def _create_global_summary(self, isotropy_results, perturbation_results):
        """Crea resumen de la validación global."""
        iso_status = "✅" if isotropy_results.get('is_isotropic', False) else "❌"
        pert_status = "✅" if perturbation_results.get('is_unperturbed', False) else "❌"
        
        max_aniso = isotropy_results.get('max_anisotropy', 0)
        max_pert = perturbation_results.get('max_perturbation', 0)
        
        return f"{iso_status} Isotropía (max: {max_aniso:.4f}), {pert_status} Perturbaciones (max: {max_pert:.4f})"

class TransitionAnalyzer:
    """
    Analizador especializado para la zona de transición entre regímenes.
    
    Verifica que la transición entre los regímenes local y global sea suave
    sin discontinuidades o saltos abruptos.
    """
    
    def analyze(self, common_data):
        """
        Analiza la suavidad de la transición entre regímenes.
        
        Args:
            common_data: Datos comunes preparados por el validador principal
            
        Returns:
            dict: Resultados del análisis de transición
        """
        print("\n🌉 ANÁLISIS DE LA ZONA DE TRANSICIÓN")
        print("=" * 50)
        
        # Analizar perfil radial completo
        profile_results = self._compute_full_radial_profile(common_data)
        
        if not profile_results.get('success', False):
            return profile_results
        
        # Analizar suavidad
        smoothness_results = self._analyze_smoothness(profile_results)
        
        return {
            'success': True,
            'radial_profile': profile_results,
            'smoothness': smoothness_results,
            'is_smooth': smoothness_results.get('is_smooth', False),
            'validation_summary': self._create_transition_summary(smoothness_results)
        }
    
    def _compute_full_radial_profile(self, common_data):
        """Calcula el perfil radial completo."""
        r_field = common_data['r_field']
        gamma_xx = common_data['metric_components']['gamma_xx']
        
        r_flat = r_field.flatten()
        gamma_flat = gamma_xx.flatten()
        
        # Filtrar puntos válidos
        valid_mask = (r_flat > 0) & np.isfinite(gamma_flat)
        r_valid = r_flat[valid_mask]
        gamma_valid = gamma_flat[valid_mask]
        
        if len(r_valid) < 10:
            return {'success': False, 'error': 'Insufficient valid points'}
        
        # Crear bins logarítmicos para mejor cobertura
        r_min = np.min(r_valid)
        r_max = np.max(r_valid)
        n_bins = 30
        
        r_bins = np.logspace(np.log10(r_min), np.log10(r_max), n_bins + 1)
        r_centers = []
        gamma_profile = []
        gamma_stds = []
        
        for i in range(n_bins):
            bin_mask = (r_valid >= r_bins[i]) & (r_valid < r_bins[i+1])
            if np.sum(bin_mask) >= 3:  # Mínimo 3 puntos por bin
                r_centers.append(np.mean(r_valid[bin_mask]))
                gamma_profile.append(np.mean(gamma_valid[bin_mask]))
                gamma_stds.append(np.std(gamma_valid[bin_mask]))
        
        if len(r_centers) < 5:
            return {'success': False, 'error': 'Insufficient radial bins'}
        
        print(f"📊 Perfil radial completo:")
        print(f"   • Bins válidos: {len(r_centers)}")
        print(f"   • Rango: {r_centers[0]:.3f} - {r_centers[-1]:.3f}")
        
        return {
            'success': True,
            'r_centers': np.array(r_centers),
            'gamma_profile': np.array(gamma_profile),
            'gamma_stds': np.array(gamma_stds)
        }
    
    def _analyze_smoothness(self, profile_results):
        """Analiza la suavidad del perfil radial."""
        r_centers = profile_results['r_centers']
        gamma_profile = profile_results['gamma_profile']
        
        # Calcular derivadas numéricas
        dr = np.diff(r_centers)
        dgamma_dr = np.diff(gamma_profile) / dr
        
        # Segunda derivada (curvatura)
        if len(dgamma_dr) > 1:
            d2gamma_dr2 = np.diff(dgamma_dr) / dr[:-1]
            max_curvature = np.max(np.abs(d2gamma_dr2))
            mean_curvature = np.mean(np.abs(d2gamma_dr2))
        else:
            max_curvature = float('inf')
            mean_curvature = float('inf')
        
        # Criterio de suavidad
        smoothness_threshold = 0.1
        is_smooth = max_curvature < smoothness_threshold
        
        print(f"📈 Análisis de suavidad:")
        print(f"   • Curvatura máxima: {max_curvature:.6f}")
        print(f"   • Curvatura promedio: {mean_curvature:.6f}")
        print(f"   • {'✅ Suave' if is_smooth else '⚠️  Discontinuidades posibles'}")
        
        return {
            'max_curvature': max_curvature,
            'mean_curvature': mean_curvature,
            'is_smooth': is_smooth,
            'smoothness_threshold': smoothness_threshold
        }
    
    def _create_transition_summary(self, smoothness_results):
        """Crea resumen del análisis de transición."""
        status = "✅ SUAVE" if smoothness_results.get('is_smooth', False) else "⚠️  RUGOSA"
        max_curv = smoothness_results.get('max_curvature', float('inf'))
        
        return f"{status} - Curvatura máx: {max_curv:.4f}"