"""Handles the state and output for Lucky 7s game."""

from game_override import GameStateOverride


class GameState(GameStateOverride):
    """Handles game logic and events for Lucky 7s."""

    def run_spin(self, sim, simulation_seed=None):
        """Run a single base game spin."""
        self.reset_seed(sim)
        self.repeat = True
        while self.repeat:
            self.reset_book()
            self.draw_board()

            # Evaluate wins
            self.evaluate_lines_board()

            self.win_manager.update_gametype_wins(self.gametype)

            # Check for free spin trigger
            if self.check_fs_condition():
                self.run_freespin_from_base()

            self.evaluate_finalwin()
            self.check_repeat()
        self.imprint_wins()

    def run_freespin(self):
        """Run free spin rounds with wheel multiplier."""
        self.reset_fs_spin()

        # Determine bonus type and spin wheels
        scatter_count = self.count_special_symbols("scatter")
        self.bonus_type = self.determine_bonus_type(scatter_count)

        if self.bonus_type:
            multiplier, spins = self.spin_bonus_wheels(self.bonus_type)
            self.global_multiplier = multiplier
            self.tot_fs = spins

        while self.fs < self.tot_fs:
            self.update_freespin()
            self.draw_board()

            # Evaluate wins with global multiplier
            self.evaluate_lines_board()

            # Check for retrigger
            if self.check_fs_condition():
                self.update_fs_retrigger_amt()

            self.win_manager.update_gametype_wins(self.gametype)

        self.end_freespin()