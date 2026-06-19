# 🌌 Aberración de Coordenadas por Coriolis 4D: Formalismo Teórico y Remapeo Esférico

## Resumen Ejecutivo

Este documento presenta el formalismo teórico riguroso de la **aberración geométrica de coordenadas** inducida por la rotación hiperdimensional de la brana en el Bulk sobre las geodésicas de los fotones del Fondo Cósmico de Microondas (CMB).

A diferencia del enfoque de-biasing histórico, que corregía la asimetría hemisférica únicamente como una modulación local de la amplitud de temperatura (efecto de segundo orden en $\beta_0$), este formalismo demuestra que el efecto físico primario de la rotación es una **deflexión de geodésicas de primer orden** en $\beta_0$. Esta deflexión angular equivale a una **rotación rígida de la esfera celeste** alrededor del eje de giro del universo, provocando un corrimiento o reacomodo de la posición angular de los parches de temperatura del CMB (aberración esférica de arrastre).

---

## 1. Didáctica de la Aberración para Fede

Para entender cómo se desvían las trayectorias de los fotones en un universo rotante, introducimos un concepto físico fundamental:

* **Aberración Cosmológica (Coriolis 4D)**: Es el cambio aparente en la dirección de llegada de los fotones del CMB debido al giro de nuestra membrana 3D. Es análogo a cuando vas corriendo bajo la lluvia y, aunque el agua cae de forma vertical, tu movimiento te obliga a inclinar el paraguas hacia adelante porque percibís que las gotas caen en diagonal. En el espacio hiperdimensional, la rotación de la brana genera una aceleración de Coriolis lateral que "empuja" las trayectorias de los fotones, haciendo que el satélite Planck los reciba en posiciones angulares desplazadas respecto a su origen real.

---

## 2. Derivación de la Aceleración y la Deflexión Geodésica

Consideremos un fotón del CMB que viaja radialmente hacia el observador (ubicado en el origen de la 3-esfera) con un vector de velocidad:

$$\mathbf{v} = -c \hat{n}$$

Donde $\hat{n} = (\sin\theta \cos\phi, \sin\theta \sin\phi, \cos\theta)$ es el vector unitario de dirección celeste en coordenadas cartesianas.

En el sistema de referencia corotante de la brana, el fotón experimenta una **fuerza de Coriolis hiperdimensional** que introduce una aceleración lateral dada por:

$$\mathbf{a}_{\text{Coriolis}} = -2 (\mathbf{\omega} \times \mathbf{v}) = 2c (\mathbf{\omega} \times \hat{n})$$

Donde $\mathbf{\omega} = \omega_{3D} \hat{V}$ es el vector de velocidad angular 3D proyectado sobre nuestra membrana, alineado al eje del "Eje del Mal" $\hat{V}$ en coordenadas galácticas $(l = 264.0^\circ, b = -29.0^\circ)$.

Dado que la aceleración es siempre perpendicular a la dirección de propagación ($\mathbf{a}_{\text{Coriolis}} \cdot \hat{n} = 0$), actúa puramente como una fuerza deflectora tangencial que no altera la magnitud de la velocidad del fotón ($c$), sino que curva su trayectoria angular.

Integrando la aceleración a lo largo del tiempo de vuelo del fotón desde la Superficie de Última Dispersión (LSS) a distancia de comovimiento $\chi_{\text{LSS}}$, la deflexión angular neta que sufre la dirección del rayo de luz es:

$$\delta\hat{n} = \beta_0 (\hat{V} \times \hat{n})$$

Donde el parámetro de aberración adimensional es:

$$\beta_0 = \frac{\chi_{\text{LSS}} |\mathbf{\omega}_{3D}|}{c}$$

La magnitud del desplazamiento angular del píxel es entonces directamente proporcional al seno de su distancia angular $\alpha$ al eje de rotación:

$$|\delta\hat{n}| = \beta_0 \sin(\alpha)$$

---

## 3. Teorema de Rotación Rígida del Cielo

Un resultado matemático profundo de este formalismo es que el campo de deflexión angular generado por $\delta\hat{n} = \beta_0 (\hat{V} \times \hat{n})$ corresponde **exactamente al generador infinitesimal de una rotación de cuerpo rígido** de toda la esfera celeste alrededor del eje $\hat{V}$.

Esto significa que, para primer orden en $\beta_0$:
* La distancia angular relativa entre todas las manchas acústicas diminutas se conserva perfectamente.
* La esfera del cielo observada por Planck simplemente está **rotada** un ángulo $\beta_0$ respecto al cielo real primordial.

Por lo tanto, la corrección por aberración geométrica no es un filtro local de distorsión elástica pixel a pixel con deformaciones asimétricas, sino un **re-mapeo esférico rígido**.

---

## 4. Ecuación Vectorial de Corrección: Fórmula de Rodrigues

Para corregir la aberración de forma numéricamente estable y libre de las singularidades de los polos de coordenadas esféricas, el algoritmo utiliza la **Fórmula de Rotación de Rodrigues**.

Si la naturaleza rota las coordenadas reales hacia las observadas mediante:

$$\hat{n}_{\text{obs}} = \mathbf{R}(+\beta_0, \hat{V}) \cdot \hat{n}_{\text{real}}$$

La inversión matemática exacta (nuestro algoritmo de-biasing) toma la dirección observada por el satélite $\hat{n}_{\text{obs}}$ y reconstruye su dirección primordial rotándola por un ángulo $-\beta_0$ (o equivalentemente $+\beta_0$ en el sentido inverso de la interpolación):

$$\hat{n}_{\text{shifted}} = \mathbf{R}(+\beta_0, \hat{V}) \cdot \hat{n}_{\text{obs}}$$

La fórmula de Rodrigues calcula esta rotación de forma directa en el espacio tridimensional como:

$$\mathbf{R}(\theta, \hat{k}) \cdot \mathbf{v} = \mathbf{v}\cos\theta + (\hat{k} \times \mathbf{v})\sin\theta + \hat{k}(\hat{k} \cdot \mathbf{v})(1 - \cos\theta)$$

---

## 5. Modulación Acoplada: Temperatura y Amplitud

Además del reacomodo geométrico de píxeles, la velocidad del emisor introduce un efecto Doppler relativista de segundo orden que modula la amplitud de la temperatura según el factor $D(\hat{n})$:

$$D(\hat{n}) = \sqrt{1 - \beta_0^2 \sin^2(\alpha)}$$

Combinando la rotación de coordenadas de Rodrigues (primer orden) con la modulación Doppler y la fuerza centrífuga $A_{4D}\cos^4(\alpha)$ (segundo orden), la ecuación curativa completa que se ejecuta sobre el mapa real es:

$$T_{\text{real}}(\hat{n}_{\text{obs}}) = \frac{T_{\text{obs}}(\hat{n}_{\text{shifted}})}{D(\hat{n}_{\text{obs}}) \cdot (1 + A_{4D}\cos^4\alpha)}$$

---

## 6. Algoritmo de Implementación en HEALPix

Para cada píxel de índice $i$ en la esfera de resolución $N_{side}$:

1. Obtener la dirección cartesiana observada $\hat{n}_i = (x, y, z)$.
2. Calcular la dirección rotada $\hat{n}_{\text{shifted}, i} = \mathbf{R}(+\beta_0, \hat{V}) \cdot \hat{n}_i$ usando Rodrigues.
3. Convertir $\hat{n}_{\text{shifted}, i}$ de vuelta a coordenadas polares de colatitud $\theta_{\text{shifted}, i}$ y longitud $\phi_{\text{shifted}, i}$.
4. Interpolar el valor de temperatura del mapa crudo observado en estas nuevas coordenadas usando interpolación bilineal esférica:
   $$T_{\text{interpolado}, i} = \text{hp.get\_interp\_val}(T_{\text{obs}}, \theta_{\text{shifted}, i}, \phi_{\text{shifted}, i})$$
5. Dividir por los factores de modulación de amplitud para obtener la temperatura purificada $T_{\text{real}, i}$.

Este algoritmo garantiza que las manchas térmicas del CMB **se desplacen físicamente en el mapa celeste** curando las lentes gravitacionales/inerciales de Coriolis 4D de forma exacta.
