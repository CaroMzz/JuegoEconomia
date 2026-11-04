# Simulador de Supervivencia Economica (Web Life-Sim RPG & CLI)

Simulador interactivo desarrollado en Python y Flask con interfaz grafica estilo videojuego de simulacion de vida / RPG (HTML5, CSS3, JavaScript y Chart.js) y version de terminal (Rich CLI). Modela la toma de decisiones economicas bajo restriccion presupuestaria, el **Efecto Sustitucion** de la Teoria del Consumidor y la dinamica de deuda con costo de oportunidad. Los precios se mantienen fijos durante los seis meses para que el presupuesto sea comparable.

**Diseno Estructurado y HUD Gamificado**: Sin emojis. Toda la visualizacion se apoya en barras de estado (HUD), tarjetas interactivas de decision, estantes de sub-tarjetas desplegables, bordes neon y tipografia de videojuego.

---

## [1] Pilares de Jugabilidad y Diseno del HUD

### HUD Gamificado Superior
- **Barra de Presupuesto Disponible / Liquidez**: Monitorea el capital disponible y salud financiera. Si se entra en descubierto bancario, conmuta a alerta visual de deuda con desglose de tasas (`TNA 60%`, `TEM 5.00%`, `TEA 79.59%`).
- **Barra de Nivel de Bienestar / Utilidad**: Medidor de satisfaccion y energia del jugador acumulada a traves de sus elecciones de consumo y resolucion de formulas.
- **Bienestar inicial**: 300 puntos. Las respuestas incorrectas, ausencias, emergencias y deudas lo reducen; las respuestas correctas, decisiones de consumo y horas extras pueden recuperarlo. Las respuestas correctas dan +2 puntos y las ganancias positivas tienen un tope diario de 5 puntos; el bienestar nunca baja de cero.
- **Dificultad adaptativa**: Las preguntas son faciles con 300 puntos o mas, intermedias entre 100 y 299, y dificiles por debajo de 100.
- **Barra de Progreso Mensual (Dias 1 a 30)**: Cronograma del mes con indicador de avance diario y precios nominales fijos.

---

## [2] Mecanicas del Modelo Economico

### 1. Sistema de Trabajo e Ingresos Variables
- **Calendario Mensual**: Cada mes consta de 30 dias calendarios (horizonte de 6 meses).
- **Salario Neto de Referencia**: \$2.000.000,00 ARS por mes completo (aprox. \$66.666,67 por dia trabajado), con \$1.500.000 de saldo inicial para cubrir los gastos fijos del primer mes. Son supuestos de simulacion, no cotizaciones en tiempo real.
- **Dinamica de Asistencia**:
  - **Fichar y Trabajar (Trivia Financiera)**: El jugador responde una pregunta breve de economia/finanzas $\implies$ Dia trabajado (+salario devengado a liquidacion y bono de bienestar).
  - **No Asistir (Registrar Ausencia)**: Ausencia computada (descuento proporcional de \$66.666,67 a fin de mes, -6 puntos de bienestar e inhabilitacion de horas extras).
- **Horas Extras Condicionales**:
  - **Restriccion Estricta**: UNICAMENTE disponibles si el jugador asistio a trabajar ese dia. Si falto o no ficho, la terminal de horas extras permanece bloqueada (`[ACCESO DENEGADO]`).
  - **Mini-Juego Matematico**: Resolver formulas financieras con los numeros vigentes de la partida (TEM sobre descubierto, costo consolidado de servicios, deduccion por ausencias y calculo de horas extras).
  - Cada respuesta correcta acredita un bono salarial monetario para la liquidacion del mes.

### 2. Arbol de Decisiones de Consumo (Tarjetas Dinamicas de Estilo de Vida)
- **Tarjeta de Alimentacion y Gastronomia**:
  - `[COCINAR EN CASA]`: Opcion economica (\$95.000).
  - `[PEDIR DELIVERY]`: Despliega animadamente un estante de **Sub-Tarjetas de Menu**:
    * *Pizza Portena y Gaseosa* (\$180.000).
    * *Hamburguesa Artesanal y Cerveza* (\$220.000).
    * *Ensalada Gourmet y Vianda Fit* (\$150.000).
- **Tarjeta de Movilidad y Transporte**:
  - `[TRANSPORTE PUBLICO]` (Subte y Colectivo: \$35.000) vs `[VIAJES PRIVADOS]` (se despliega en Sub-Tarjetas de *Uber / Cabify* o *Taxi / Remis*).
- **Tarjeta de Cuidado Personal**:
  - `[PELUQUERIA DE BARRIO]` vs `[LA SAGRADA BARBERIA / SALON VIP RECOLETA]`.
- **Tarjeta de Ocio y Salidas**:
  - `[STREAMING EN CASA]` vs `[SALIDAS Y BOLICHE]`.
- **Tarjeta de Mascotas (Perro y Gato)**:
  - `[ALIMENTO ESTANDAR]` vs `[SUPER PREMIUM Y GUARDERIA]`.

### 3. Gastos Fijos Obligatorios (supuestos nominales)
- Alquiler Departamento (Recoleta): \$850.000,00
- Expensas: \$140.000,00
- Luz (Edesur): \$55.000,00
- Agua (AySA): \$25.000,00
- Gas (Metrogas): \$20.000,00
- Membresia Platino Plus (Megatlon): \$65.000,00
- Canasta Basica de Alimentos Indispensables: \$250.000,00
- Total mensual fijo: \$1.405.000,00. Los montos son referencias aproximadas para el juego y no cotizaciones en tiempo real.

### 4. Tarjetas de Eventos Imprevistos (Pop-ups de Crisis)
- Aparicion aleatoria de emergencias financieras (consulta medica: \$45.000; urgencia veterinaria: \$180.000; auto: \$220.000; plomeria: \$150.000; reparacion de celular: \$180.000; multa: \$65.000; cerrajeria: \$100.000; humedad: \$240.000).
- Decisiones tacticas inmediatas:
  - **Pagar al Contado**: Debita el costo exacto y reduce menos el bienestar.
  - **Financiar con Tarjeta**: Aplica recargo financiero del 15% y mayor penalizacion en utilidad por estres financiero.

### 5. Precios Nominales Estables
- Los precios fijos, consumos, emergencias y sueldo se mantienen constantes durante los seis meses.

### 6. Deuda y Costo de Oportunidad
- Si el saldo al cierre del mes es deficitario, se activa automaticamente un prestamo en descubierto con tasa mensual:
  $$TNA = 60\% \implies TEM = 5\% \implies TEA \approx 79.59\%$$

### 7. Modo Administrador / Demostracion Semestral (Usuario "prueba")
- Selector de modo en cabecera (`Partida Estandar` vs `ADMINISTRADOR (prueba)`).
- Precarga historica completa de los primeros 5 meses para el usuario "prueba" (acumulando liquidaciones, gastos y eventos).
- Posiciona la simulacion en el **Dia 28 de Agosto (Mes 6 de 6)** para experimentar los ultimos 2 dias y la evaluacion final consolidada del semestre sin alterar la partida normal en curso.

---

## [3] Como Ejecutar la Aplicacion Web

Para iniciar el servidor Flask con el HUD Gamificado y las Tarjetas Interactivas:

```bash
python app.py
```

Luego abre tu navegador en **http://localhost:5000** o **http://127.0.0.1:5000**.

*(Tambien puedes ejecutar la version clasica de terminal con `python main.py`).*

---

## [4] Suite de Pruebas Automatizadas (Pytest)

Ejecuta los 51 tests automatizados que verifican los calculos al centavo (`Decimal`, `ROUND_HALF_UP`), la liquidacion salarial, el arbol de consumo, el modo administrador semestral y los endpoints REST de la API:

```bash
pytest -v
```
