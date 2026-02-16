"""Game override functions for Lucky 7s."""

from game_executables import GameExecutables
from src.calculations.statistics import get_random_outcome


class GameStateOverride(GameExecutables):
    """
    Lucky 7s specific overrides.
    7 symbol = Wild + Scatter + Multiplier
    Dual wheel system for bonus modes.
    """

    def reset_book(self):
        """Reset game specific properties."""
        super().reset_book()
        self.wheel_multiplier = 1
        self.wheel_spins = 0
        self.bonus_type = None

    def assign_special_sym_function(self):
        """Assign special functions to the 7 symbol."""
        self.special_symbol_functions = {
            "7": [self.assign_mult_property],
        }

    def assign_mult_property(self, symbol) -> dict:
        """Assign multiplier value to 7 symbol in freegame."""
        multiplier_value = 1
        if self.gametype == self.config.freegame_type:
            multiplier_value = get_random_outcome(
                self.get_current_distribution_conditions()["mult_values"][self.gametype]
            )
        symbol.assign_attribute({"multiplier": multiplier_value})

    def check_repeat(self):
        """Check if game should repeat."""
        super().check_repeat()
        if self.repeat is False:
            win_criteria = self.get_current_betmode_distributions().get_win_criteria()
            if win_criteria is not None and self.final_win != win_criteria:
                self.repeat = True
                return
            if win_criteria is None and self.final_win == 0:
                self.repeat = True
                return

    def determine_bonus_type(self, scatter_count):
        """Determine bonus type based on scatter count."""
        if scatter_count >= 5:
            return "ultra_bonus"
        elif scatter_count >= 4:
            return "super_bonus"
        elif scatter_count >= 3:
            return "bonus"
        return None

    def spin_bonus_wheels(self, bonus_type):
        """
        Spin the dual wheels for bonus mode.
        Inner wheel = Multiplier
        Outer wheel = Free spins
        Returns (multiplier, spins)
        """
        if bonus_type is None:
            return 1, 0

        wheels = self.config.bonus_wheels.get(bonus_type, None)
        if wheels is None:
            return 1, 0

        # Spin inner wheel (multiplier)
        multiplier_wheel = wheels.get("multiplier_wheel", {1: 1})
        self.wheel_multiplier = get_random_outcome(multiplier_wheel)

        # Spin outer wheel (spins)
        spin_wheel = wheels.get("spin_wheel", {7: 1})
        self.wheel_spins = get_random_outcome(spin_wheel)

        return self.wheel_multiplier, self.wheel_spins

    def get_bonus_reel_type(self, bonus_type):
        """Get the reel type for bonus mode."""
        reel_map = {
            "bonus": "FR0",
            "super_bonus": "FR1",
            "ultra_bonus": "FR2",
        }
        return reel_map.get(bonus_type, "FR0")