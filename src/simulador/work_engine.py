"""Motor de Trabajo e Ingresos Variables.
Gestiona el banco de preguntas diarias sobre economía/finanzas y el generador
dinámico de horas extras con fórmulas financieras basadas en datos vivos de la partida.
"""

from decimal import Decimal, ROUND_HALF_UP
import random
from typing import Any, Dict, List, Optional

from simulador.economy import INITIAL_WELLBEING


QUESTIONS_BANK: List[Dict[str, Any]] = [
    {
        "id": 1,
        "topic": "Microeconomía",
        "question": "¿Qué representa la 'Restricción Presupuestaria' de un consumidor?",
        "options": [
            "El límite máximo de deuda que un banco comercial autoriza.",
            "Todas las combinaciones de bienes que el consumidor puede adquirir dado su ingreso y los precios vigentes.",
            "La cantidad mínima de ahorro que exige el Banco Central.",
            "El nivel de impuestos indirectos que gravan el consumo."
        ],
        "correct_index": 1,
        "explanation": "La recta de balance o restricción presupuestaria define el conjunto de canastas accesibles gastando todo el ingreso disponible."
    },
    {
        "id": 2,
        "topic": "Finanzas",
        "question": "Si una entidad financiera ofrece un préstamo al 60% de TNA (Tasa Nominal Anual), ¿cuál es la Tasa Efectiva Mensual (TEM) simple?",
        "options": [
            "6% mensual",
            "5% mensual (60% / 12)",
            "10% mensual",
            "4.5% mensual"
        ],
        "correct_index": 1,
        "explanation": "La TEM simple surge de dividir la TNA por los 12 meses del año: 60% / 12 = 5% mensual."
    },
    {
        "id": 3,
        "topic": "Finanzas Personales",
        "question": "¿Qué conviene hacer cuando los gastos planificados superan el ingreso disponible?",
        "options": [
            "Usar crédito sin revisar la capacidad de pago.",
            "Priorizar gastos necesarios y ajustar o postergar los gastos discrecionales.",
            "Ignorar el déficit hasta el siguiente mes.",
            "Aumentar todos los gastos para aprovechar el ingreso."
        ],
        "correct_index": 1,
        "explanation": "Un presupuesto sostenible prioriza necesidades y ajusta los gastos discrecionales para no gastar por encima del ingreso."
    },
    {
        "id": 4,
        "topic": "Teoría del Consumidor",
        "question": "¿Qué establece el 'Efecto Sustitución' cuando se incrementa el precio de un bien?",
        "options": [
            "El consumidor deja de consumir todos los bienes de su canasta.",
            "El consumidor reemplaza el bien encarecido por alternativas relativamente más económicas que satisfacen una necesidad similar.",
            "El ingreso nominal del trabajador aumenta en la misma proporción.",
            "La utilidad marginal del dinero se vuelve negativa."
        ],
        "correct_index": 1,
        "explanation": "Ante el encarecimiento relativo de un bien, el consumidor sustituye su consumo por sustitutos más baratos manteniendo o buscando maximizar su utilidad."
    },
    {
        "id": 5,
        "topic": "Finanzas Personales",
        "question": "¿Qué es el 'Costo de Oportunidad' de una decisión de consumo?",
        "options": [
            "El valor de la mejor alternativa a la que se renuncia al tomar esa decisión.",
            "El recargo por pagar con tarjeta de crédito en cuotas.",
            "El descuento que ofrece un comercio al pagar en efectivo.",
            "La comisión fija de mantenimiento de cuenta bancaria."
        ],
        "correct_index": 0,
        "explanation": "El costo de oportunidad es el beneficio o valor que se resigna al no elegir la mejor opción alternativa disponible."
    },
    {
        "id": 6,
        "topic": "Macroeconomía",
        "question": "¿Por qué la TEA (Tasa Efectiva Anual) es superior a la TNA cuando los intereses se capitalizan mensualmente?",
        "options": [
            "Por el cobro de impuestos a las ganancias bancarias.",
            "Por el efecto del interés compuesto: los intereses devengados cada mes generan nuevos intereses en los meses siguientes.",
            "Porque los bancos cobran comisiones administrativas adicionales.",
            "Por la depreciación cambiaria de la moneda local."
        ],
        "correct_index": 1,
        "explanation": "La capitalización mensual reinvierte los intereses periódicos generados, logrando una tasa efectiva anual acumulada mayor a la nominal."
    },
    {
        "id": 7,
        "topic": "Microeconomía",
        "question": "¿Cuál es la diferencia entre un costo fijo y un costo variable?",
        "options": [
            "El costo fijo depende del volumen de actividad; el variable permanece inalterable.",
            "El costo fijo debe afrontarse independientemente del consumo o nivel de producción; el variable varía según las decisiones de uso o volumen.",
            "Los costos fijos se pagan anualmente y los variables mensualmente.",
            "Los costos fijos están exentos de impuestos y los variables no."
        ],
        "correct_index": 1,
        "explanation": "Los costos fijos (como el alquiler o el abono básico) son independientes del consumo inmediato; los variables dependen de elecciones periódicas."
    },
    {
        "id": 8,
        "topic": "Finanzas",
        "question": "En un descubierto bancario, ¿cuándo comienzan a devengarse los intereses por el saldo deudor?",
        "options": [
            "Únicamente al cierre del año fiscal.",
            "De forma inmediata desde el momento en que la cuenta corriente registra saldo negativo.",
            "A los 90 días de intimación judicial.",
            "Solo si el titular solicita formalmente el crédito por ventanilla."
        ],
        "correct_index": 1,
        "explanation": "El descubierto en cuenta corriente devenga intereses pasivos diarios o mensuales desde el instante en que el balance cae en terreno negativo."
    },
    {
        "id": 9,
        "topic": "Finanzas Personales",
        "question": "¿Qué efecto tiene una ausencia laboral sobre el presupuesto mensual de esta partida?",
        "options": [
            "Reduce el salario liquidado y deja menos dinero disponible para otros gastos.",
            "Aumenta el salario porque se trabajan menos días.",
            "No modifica el ingreso ni el bienestar.",
            "El empleador cubre automáticamente todos los gastos fijos."
        ],
        "correct_index": 0,
        "explanation": "Cada ausencia descuenta salario y reduce el ingreso disponible para cubrir gastos y decisiones de consumo."
    },
    {
        "id": 10,
        "topic": "Economía Conductual",
        "question": "¿Qué concepto describe la tendencia a gastar más dinero cuando se perciben ingresos adicionales en lugar de destinarlos a un fondo de reserva?",
        "options": [
            "Aversión al riesgo.",
            "Preferencia por el consumo inmediato sin reservar una parte para el ahorro.",
            "Paradoja de la frugalidad.",
            "Trampa de liquidez keynesiana."
        ],
        "correct_index": 1,
        "explanation": "Planificar el ahorro antes de decidir gastos discrecionales ayuda a evitar que un ingreso extra se consuma por completo."
    },
    {
        "id": 11,
        "topic": "Microeconomía",
        "question": "¿Qué define a dos bienes como 'bienes sustitutos'?",
        "options": [
            "Deben consumirse de forma conjunta y simultánea (ej. auto y combustible).",
            "El incremento en el precio de uno provoca el aumento en la demanda del otro (ej. Uber y transporte público).",
            "Ambos son provistos exclusivamente por el sector público.",
            "Tienen un precio de equilibrio idéntico en el mercado."
        ],
        "correct_index": 1,
        "explanation": "Los bienes sustitutos satisfacen una misma necesidad funcional; al encarecerse uno, el consumidor se traslada hacia el otro."
    },
    {
        "id": 12,
        "topic": "Finanzas Personales",
        "question": "¿Qué es un 'Fondo de Emergencia' y cuál es su horizonte recomendado?",
        "options": [
            "Un crédito hipotecario a 30 años.",
            "Una reserva de alta liquidez equivalente a entre 3 y 6 meses de gastos fijos para amortiguar imprevistos sin endeudarse.",
            "Un plazo fijo a 10 años sin posibilidad de cancelación anticipada.",
            "La compra especulativa de acciones de alto riesgo bursátil."
        ],
        "correct_index": 1,
        "explanation": "El fondo de emergencia debe ser líquido y seguro para cubrir contingencias (enfermedad, reparaciones) sin tener que recurrir a descubiertos caros."
    },
    {
        "id": 13,
        "topic": "Finanzas Personales",
        "question": "¿Qué caracteriza a un gasto discrecional?",
        "options": [
            "Es un gasto obligatorio que no se puede evitar, como el alquiler.",
            "Es un gasto que puede reducirse o postergarse, como una salida o un delivery.",
            "Es un ingreso que se recibe una sola vez al año.",
            "Es una deuda que no genera intereses."
        ],
        "correct_index": 1,
        "explanation": "Los gastos discrecionales permiten elegir cuánto gastar y pueden ajustarse cuando el presupuesto es limitado."
    },
    {
        "id": 14,
        "topic": "Finanzas",
        "question": "Si el descubierto bancario cobra una TEM del 5%, ¿cuánto se paga de interés mensual por cada $100.000 de saldo deudor?",
        "options": [
            "$500",
            "$5.000",
            "$50.000",
            "$12.000"
        ],
        "correct_index": 1,
        "explanation": "$100.000 * 0.05 = $5.000 de interés mensual directo."
    },
    {
        "id": 15,
        "topic": "Teoría del Consumidor",
        "question": "¿Qué es la 'Utilidad Marginal Decreciente'?",
        "options": [
            "La satisfacción adicional obtenida al consumir una unidad más de un bien tiende a disminuir con cada unidad adicional consumida.",
            "La pérdida de salario por llegar tarde al trabajo.",
            "El aumento del interés bancario a medida que transcurre el tiempo.",
            "La caída del precio de liquidación en tiendas outlet."
        ],
        "correct_index": 0,
        "explanation": "A mayor consumo de un mismo bien, la satisfacción adicional que aporta cada unidad subsiguiente es cada vez menor."
    }
]


def get_daily_question(
    day: int,
    month: int,
    cumulative_utility: Decimal = INITIAL_WELLBEING
) -> Dict[str, Any]:
    """Selecciona preguntas más difíciles cuando el bienestar acumulado es bajo."""
    if cumulative_utility < Decimal("100.0"):
        difficulty = "difícil"
        question_ids = range(11, 16)
    elif cumulative_utility < Decimal("300.0"):
        difficulty = "intermedia"
        question_ids = range(6, 11)
    else:
        difficulty = "fácil"
        question_ids = range(1, 6)

    eligible_questions = [
        question for question in QUESTIONS_BANK
        if question["id"] in question_ids
    ]
    index = ((month - 1) * 30 + (day - 1)) % len(eligible_questions)
    selected_question = dict(eligible_questions[index])
    selected_question["difficulty"] = difficulty
    return selected_question


def generate_live_overtime_challenge(
    tna: Decimal,
    tem: Decimal,
    edesur_cost: Decimal,
    aysa_cost: Decimal,
    gas_cost: Decimal,
    expensas_cost: Decimal,
    unworked_days: int,
    daily_salary: Decimal = Decimal("66666.67")
) -> Dict[str, Any]:
    """Genera dinámicamente un desafío de Horas Extras con fórmulas matemáticas
    utilizando los datos reales y vigentes de la partida del jugador.
    """
    templates = [
        # Tipo 1: TEM desde TNA
        "tem_calculation",
        # Tipo 3: Costo Total de Servicios Básicos
        "total_utilities",
        # Tipo 4: Descuento por ausencias
        "absence_discount",
        # Tipo 5: Costo mensual de expensas
        "expensas_calculation"
    ]

    chosen_type = random.choice(templates)
    reward = Decimal("35000.00")

    if chosen_type == "tem_calculation":
        pct_tna = (tna * Decimal("100")).quantize(Decimal("0.1"))
        correct_pct_tem = (tem * Decimal("100")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        title = "Cálculo de Tasa Efectiva Mensual (TEM)"
        statement = (
            f"Tu cuenta corriente bancaria aplica una TNA del {pct_tna}% anual para descubiertos. "
            f"¿Cuál es la Tasa Efectiva Mensual (TEM) nominal equivalente?"
        )
        hint = "Fórmula: TEM = TNA / 12"

        correct_str = f"{correct_pct_tem}% mensual"
        distractors = [
            f"{(correct_pct_tem * Decimal('1.2')).quantize(Decimal('0.01'))}% mensual",
            f"{(correct_pct_tem * Decimal('0.8')).quantize(Decimal('0.01'))}% mensual",
            f"{(correct_pct_tem + Decimal('2.0')).quantize(Decimal('0.01'))}% mensual"
        ]
        options = [correct_str] + distractors
        random.shuffle(options)
        correct_idx = options.index(correct_str)

        explanation = f"Correcto. TEM = {pct_tna}% / 12 = {correct_pct_tem}% mensual."

    elif chosen_type == "total_utilities":
        total_utilities = (edesur_cost + aysa_cost + gas_cost).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        title = "Gasto Consolidado en Servicios Públicos"
        statement = (
            f"Tus consumos del mes actual registran: Luz (Edesur) ${edesur_cost:,.2f}, "
            f"Agua (AySA) ${aysa_cost:,.2f} y Gas (Metrogas) ${gas_cost:,.2f}. "
            f"¿Cuál es el costo total consolidado de los servicios públicos en tu presupuesto?"
        )
        hint = "Fórmula: Total = Luz + Agua + Gas"
        correct_str = f"${total_utilities:,.2f}"
        distractors = [
            f"${(total_utilities + Decimal('10000.00')):,.2f}",
            f"${(total_utilities - Decimal('8500.00')):,.2f}",
            f"${(total_utilities * Decimal('1.1')).quantize(Decimal('0.01')):,.2f}"
        ]
        options = [correct_str] + distractors
        random.shuffle(options)
        correct_idx = options.index(correct_str)
        explanation = f"Exacto. La suma consolidada de servicios públicos es de ${total_utilities:,.2f}."

    elif chosen_type == "absence_discount":
        sample_absences = max(unworked_days, 3)
        total_deduction = (Decimal(sample_absences) * daily_salary).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        title = "Descuento Salarial por Días No Trabajados"
        statement = (
            f"El valor de tu jornada diaria de trabajo es de ${daily_salary:,.2f}. "
            f"Si un empleado computa {sample_absences} faltas en el mes, ¿cuánto se le descontará en su liquidación?"
        )
        hint = "Fórmula: Descuento = Días_Ausentes * Salario_Diario"
        correct_str = f"${total_deduction:,.2f}"
        distractors = [
            f"${(total_deduction + Decimal('20000.00')):,.2f}",
            f"${(total_deduction * Decimal('0.8')).quantize(Decimal('0.01')):,.2f}",
            f"${(total_deduction * Decimal('1.2')).quantize(Decimal('0.01')):,.2f}"
        ]
        options = [correct_str] + distractors
        random.shuffle(options)
        correct_idx = options.index(correct_str)
        explanation = f"Correcto. {sample_absences} días x ${daily_salary:,.2f} = ${total_deduction:,.2f} de deducción salarial."

    else:
        # expensas_calculation
        title = "Presupuesto mensual de expensas"
        base_expensas = expensas_cost
        statement = (
            f"Las expensas mensuales del edificio en Recoleta son de ${base_expensas:,.2f}. "
            f"¿Cuánto se reserva para cubrir seis meses?"
        )
        hint = "Fórmula: Expensas_Mensuales * 6"
        exact_expensas = (base_expensas * Decimal("6")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        correct_str = f"${exact_expensas:,.2f}"
        distractors = [
            f"${(exact_expensas + Decimal('7500.00')):,.2f}",
            f"${(exact_expensas * Decimal('0.9')).quantize(Decimal('0.01')):,.2f}",
            f"${(exact_expensas * Decimal('1.15')).quantize(Decimal('0.01')):,.2f}"
        ]
        options = [correct_str] + distractors
        random.shuffle(options)
        correct_idx = options.index(correct_str)
        explanation = f"Correcto. ${base_expensas:,.2f} * 6 = ${exact_expensas:,.2f}."

    return {
        "title": title,
        "statement": statement,
        "hint": hint,
        "options": options,
        "correct_index": correct_idx,
        "reward_amount": reward,
        "explanation": explanation
    }
