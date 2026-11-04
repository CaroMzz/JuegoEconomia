"""Cálculos económicos y financieros deterministas para el Simulador.
Utiliza Decimal con redondeo ROUND_HALF_UP para asegurar precisión financiera al centavo.
"""

from decimal import Decimal, ROUND_HALF_UP
from typing import Tuple

CENT = Decimal("0.01")
RATE_PRECISION = Decimal("0.000001")
WELLBEING_PRECISION = Decimal("0.1")
INITIAL_WELLBEING = Decimal("300.0")
ABSENCE_WELLBEING_PENALTY = Decimal("6.0")
DAILY_WELLBEING_GAIN_LIMIT = Decimal("5.0")
DEBT_WELLBEING_PENALTY_PER_100K = Decimal("20.0")
MAX_DEBT_WELLBEING_PENALTY = Decimal("120.0")
BASE_RENT_RECOLETA = Decimal("850000.00")
BASE_EXPENSES = Decimal("140000.00")
BASE_EDESUR = Decimal("55000.00")
BASE_AYSA = Decimal("25000.00")
BASE_GAS = Decimal("20000.00")
BASE_GYM = Decimal("65000.00")
BASE_GROCERIES = Decimal("250000.00")


def round_currency(value: Decimal) -> Decimal:
    """Redondea un monto monetario al centavo más cercano usando ROUND_HALF_UP."""
    return value.quantize(CENT, rounding=ROUND_HALF_UP)


def calculate_tem(tna: Decimal) -> Decimal:
    """Convierte la TNA (Tasa Nominal Anual) a TEM (Tasa Efectiva Mensual).
    
    Fórmula estándar bancaria:
        TEM = TNA / 12
    """
    if tna < Decimal("0.0"):
        raise ValueError("La TNA no puede ser negativa.")
    return (tna / Decimal("12")).quantize(RATE_PRECISION, rounding=ROUND_HALF_UP)


def calculate_tea(tem: Decimal) -> Decimal:
    """Calcula la TEA (Tasa Efectiva Anual) correspondiente a una TEM.
    
    Fórmula de capitalización compuesta:
        TEA = (1 + TEM)^12 - 1
    """
    if tem < Decimal("0.0"):
        raise ValueError("La TEM no puede ser negativa.")
    one_plus_tem = Decimal("1.0") + tem
    tea = (one_plus_tem ** 12) - Decimal("1.0")
    return tea.quantize(RATE_PRECISION, rounding=ROUND_HALF_UP)


def apply_debt_interest(debt: Decimal, tem: Decimal) -> Tuple[Decimal, Decimal]:
    """Aplica la tasa mensual de interés (TEM) al saldo deudor.
    
    Retorna:
        (interes_generado, deuda_total_con_intereses)
    Ambos redondeados exactamente al centavo.
    """
    if debt <= Decimal("0.00"):
        return Decimal("0.00"), Decimal("0.00")
    
    interest = round_currency(debt * tem)
    total_debt = round_currency(debt + interest)
    return interest, total_debt


def apply_wellbeing_change(
    current_wellbeing: Decimal,
    change: Decimal
) -> Tuple[Decimal, Decimal]:
    """Aplica un cambio de bienestar y devuelve el nuevo nivel y el cambio efectivo."""
    updated = max(Decimal("0.0"), current_wellbeing + change)
    updated = updated.quantize(WELLBEING_PRECISION, rounding=ROUND_HALF_UP)
    return updated, updated - current_wellbeing


def limit_daily_wellbeing_gain(
    requested_gain: Decimal,
    gain_already_earned: Decimal
) -> Decimal:
    """Limita los puntos positivos que se pueden acumular en una jornada."""
    if requested_gain <= Decimal("0.0"):
        return requested_gain
    remaining = max(Decimal("0.0"), DAILY_WELLBEING_GAIN_LIMIT - gain_already_earned)
    return min(requested_gain, remaining)


def calculate_debt_wellbeing_penalty(debt: Decimal) -> Decimal:
    """Penaliza el estrés financiero: 20 puntos por cada $100.000, hasta 120."""
    if debt <= Decimal("0.00"):
        return Decimal("0.0")
    penalty = min(
        debt / Decimal("100000.00") * DEBT_WELLBEING_PENALTY_PER_100K,
        MAX_DEBT_WELLBEING_PENALTY
    )
    return -penalty.quantize(WELLBEING_PRECISION, rounding=ROUND_HALF_UP)
