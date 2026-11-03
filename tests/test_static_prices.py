"""Pruebas de precios nominales constantes durante la simulacion."""

from decimal import Decimal

from simulador.game import EconomicSurvivalGame, get_catalog_choices
from simulador.models import Category, FixedCostItem


def test_fixed_cost_item_rounds_to_the_cent() -> None:
    item = FixedCostItem("Test", Decimal("10.005"))
    assert item.calculate_cost() == Decimal("10.01")


def test_fixed_prices_and_salary_remain_unchanged_for_six_months() -> None:
    game = EconomicSurvivalGame()
    choices = [options[1] for options in get_catalog_choices().values()]
    fixed_costs = game.get_effective_fixed_costs()

    for _ in range(game.TOTAL_MONTHS):
        result = game.execute_turn(choices)
        assert result.salary_received == Decimal("2000000.00")
        assert result.fixed_costs == fixed_costs


def test_costly_and_economical_choices_have_fixed_nominal_prices() -> None:
    catalog = get_catalog_choices()
    assert catalog[Category.TRANSPORT][0].calculate_cost() == Decimal("160000.00")
    assert catalog[Category.TRANSPORT][1].calculate_cost() == Decimal("35000.00")
    assert catalog[Category.FOOD][0].calculate_cost() == Decimal("220000.00")
    assert catalog[Category.FOOD][1].calculate_cost() == Decimal("95000.00")
