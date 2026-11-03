"""Pruebas de precios constantes y costos fijos nominales de la version web."""

from decimal import Decimal

from simulador.web_game import WebEconomicGame


def test_base_fixed_costs_are_realistic_nominal_estimates() -> None:
    game = WebEconomicGame()

    costs = game.get_fixed_costs_breakdown()

    assert costs == {
        "Alquiler (Recoleta)": Decimal("850000.00"),
        "Expensas": Decimal("140000.00"),
        "Luz (Edesur)": Decimal("55000.00"),
        "Agua (AySA)": Decimal("25000.00"),
        "Gas (Metrogas)": Decimal("20000.00"),
        "Gimnasio (Megatlon Platino Plus)": Decimal("65000.00"),
        "Comida basica indispensable": Decimal("250000.00")
    }
    assert game.get_total_fixed_costs() == Decimal("1405000.00")


def test_costs_remain_constant_after_closing_months() -> None:
    game = WebEconomicGame()
    initial_costs = game.get_fixed_costs_breakdown()

    for _ in range(3):
        game.close_month()
        assert game.get_fixed_costs_breakdown() == initial_costs
        assert game.base_salary == Decimal("2000000.00")
