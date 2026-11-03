"""Pruebas de integración del flujo de juego de 6 meses y Teoría del Consumidor."""

from decimal import Decimal
import pytest

from simulador.game import (
    EconomicSurvivalGame,
    get_catalog_choices,
)
from simulador.models import Category, ConsumptionChoice


class TestGameFlowAndConsumerTheory:
    """Valida la dinámica de los 6 turnos, el efecto sustitución y la solvencia."""

    def test_frugal_strategy_accounts_for_realistic_fixed_costs(self) -> None:
        """Las elecciones económicas permiten sobrevivir con precios fijos."""
        catalog = get_catalog_choices()
        economic_choices = [
            catalog[Category.TRANSPORT][1],      # Subte/Colectivo ($35.000)
            catalog[Category.FOOD][1],           # Cocinar en casa ($95.000)
            catalog[Category.PERSONAL_CARE][1],  # Peluquería barrio ($10.000)
            catalog[Category.PETS][1],           # Alimento estándar ($45.000)
        ]

        game = EconomicSurvivalGame()

        first_result = None
        for month in range(1, 7):
            result = game.execute_turn(economic_choices)
            assert result.month == month
            if month == 1:
                first_result = result

        assert first_result is not None
        assert first_result.total_fixed_cost == Decimal("1405000.00")
        assert first_result.new_debt == Decimal("0.00")
        assert game.history[1].salary_received == Decimal("2000000.00")

        assert game.state.month == 7
        assert game.state.debt == Decimal("0.00")
        assert game.state.cumulative_utility > Decimal("0.0")

    def test_initial_wellbeing_and_static_salary(self) -> None:
        game = EconomicSurvivalGame()
        assert game.state.cumulative_utility == Decimal("300.0")
        assert game.state.cash == Decimal("1500000.00")

        monthly_results = [game.execute_turn([]) for _ in range(6)]
        assert all(result.salary_received == Decimal("2000000.00") for result in monthly_results)
        assert all(result.fixed_costs == monthly_results[0].fixed_costs for result in monthly_results)

    def test_luxury_strategy_leads_to_debt_and_interest(self) -> None:
        """Estrategia suntuaria:
        Elige siempre las alternativas de mayor costo (Uber, Rappi Turbo, Sagrada Barberia, Premium Pets).
        Resultado esperado: El presupuesto mensual se desborda, cae en déficit, se activa el préstamo
        bancario automático y se calculan intereses con la TEM (TNA 60% -> TEM 5%).
        """
        catalog = get_catalog_choices()
        luxury_choices = [
            catalog[Category.TRANSPORT][0],      # Uber ($160.000)
            catalog[Category.FOOD][0],           # Delivery Rappi Turbo ($220.000)
            catalog[Category.PERSONAL_CARE][0],  # La Sagrada Barberia ($30.000)
            catalog[Category.PETS][0],           # Súper Premium + Vet ($90.000)
        ]

        game = EconomicSurvivalGame(
            initial_salary=Decimal("1700000.00"),
            initial_cash=Decimal("0.00"),
        )

        has_incurred_debt = False
        interest_was_charged = False

        for month in range(1, 7):
            result = game.execute_turn(luxury_choices)
            if result.new_debt > Decimal("0.00"):
                has_incurred_debt = True
            if result.interest_applied > Decimal("0.00"):
                interest_was_charged = True

        # Con el gasto suntuario debe incurrir en deuda y cobro de intereses
        assert has_incurred_debt is True
        assert interest_was_charged is True
        assert game.state.debt > Decimal("0.00")

    def test_game_cannot_exceed_six_months(self) -> None:
        """El juego debe rechazar turnos más allá del sexto mes."""
        catalog = get_catalog_choices()
        choices = [options[0] for options in catalog.values()]
        game = EconomicSurvivalGame()

        for _ in range(6):
            game.execute_turn(choices)

        with pytest.raises(RuntimeError, match="La simulación ya ha alcanzado el límite de 6 meses"):
            game.execute_turn(choices)

    def test_fixed_costs_recoleta_megatlon_present(self) -> None:
        """Verifica que los costos fijos obligatorios contengan Recoleta, Edesur/AySA y Megatlon."""
        game = EconomicSurvivalGame()
        fixed_names = [f.name for f in game.fixed_costs]

        assert any("Recoleta" in name for name in fixed_names)
        assert any("Edesur" in name and "AySA" in name for name in fixed_names)
        assert any("Megatlon" in name for name in fixed_names)
