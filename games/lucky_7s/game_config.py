"""Lucky 7s game configuration file."""

import os
from src.config.config import Config
from src.config.distributions import Distribution
from src.config.betmode import BetMode


class GameConfig(Config):
    """Lucky 7s configuration class."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        super().__init__()
        self.game_id = "lucky_7s"
        self.provider_number = 0
        self.working_name = "Lucky 7s"
        self.wincap = 7777
        self.win_type = "lines"
        self.rtp = 0.97
        self.construct_paths()

        # Game Dimensions
        self.num_reels = 5
        self.num_rows = [3] * self.num_reels

        # Paytable
        self.paytable = {
            (5, "7"): 77,
            (4, "7"): 37,
            (3, "7"): 7,
            (5, "B"): 50,
            (4, "B"): 15,
            (3, "B"): 5,
            (5, "E"): 40,
            (4, "E"): 12,
            (3, "E"): 4,
            (5, "H"): 30,
            (4, "H"): 10,
            (3, "H"): 3.5,
            (5, "C"): 25,
            (4, "C"): 8,
            (3, "C"): 3,
            (5, "D"): 20,
            (4, "D"): 6,
            (3, "D"): 2,
            (5, "G"): 15,
            (4, "G"): 4,
            (3, "G"): 1.5,
            (5, "L"): 10,
            (4, "L"): 3,
            (3, "L"): 1,
            (5, "O"): 8,
            (4, "O"): 2,
            (3, "O"): 0.5,
            (5, "P"): 6,
            (4, "P"): 1.5,
            (3, "P"): 0.3,
        }

        # Paylines (20 lines)
        self.paylines = {
            1: [0, 0, 0, 0, 0],
            2: [1, 1, 1, 1, 1],
            3: [2, 2, 2, 2, 2],
            4: [0, 1, 2, 1, 0],
            5: [2, 1, 0, 1, 2],
            6: [0, 0, 1, 2, 2],
            7: [2, 2, 1, 0, 0],
            8: [1, 0, 1, 2, 1],
            9: [1, 2, 1, 0, 1],
            10: [0, 1, 1, 1, 2],
            11: [2, 1, 1, 1, 0],
            12: [0, 1, 0, 1, 2],
            13: [2, 1, 2, 1, 0],
            14: [1, 1, 0, 1, 1],
            15: [1, 1, 2, 1, 1],
            16: [0, 2, 1, 0, 2],
            17: [2, 0, 1, 2, 0],
            18: [0, 0, 2, 0, 0],
            19: [2, 2, 0, 2, 2],
            20: [1, 0, 0, 0, 1],
        }

        self.include_padding = True
        self.special_symbols = {"wild": ["7"], "scatter": ["7"], "multiplier": ["7"]}

        # Free spin triggers (scatter count -> free spins)
        self.freespin_triggers = {
            self.basegame_type: {3: 7, 4: 10, 5: 17, 6: 20, 7: 25, 8: 30, 9: 35, 10: 40, 11: 45, 12: 50, 13: 55, 14: 60,
                                 15: 70},
            self.freegame_type: {2: 3, 3: 7, 4: 10, 5: 17, 6: 20, 7: 25, 8: 30, 9: 35, 10: 40, 11: 45, 12: 50, 13: 55,
                                 14: 60, 15: 70},
        }

        self.anticipation_triggers = {
            self.basegame_type: min(self.freespin_triggers[self.basegame_type].keys()) - 1,
            self.freegame_type: min(self.freespin_triggers[self.freegame_type].keys()) - 1,
        }

        # Reels
        reels = {
            "BR0": "BR0.csv",
            "FR0": "FR0.csv",
            "FR1": "FR1.csv",
            "FR2": "FR2.csv",
            "WCAP": "WCAP.csv"
        }
        self.reels = {}
        for r, f in reels.items():
            self.reels[r] = self.read_reels_csv(os.path.join(self.reels_path, f))

        self.padding_reels[self.basegame_type] = self.reels["BR0"]
        self.padding_reels[self.freegame_type] = self.reels["FR0"]

        # Multiplier values for 7 symbol
        self.padding_symbol_values = {
            "7": {"multiplier": {2: 100, 3: 50, 5: 50, 7: 50, 10: 30, 20: 20, 50: 5}}
        }

        # Bonus wheel configurations
        self.bonus_wheels = {
            "bonus": {
                "multiplier_wheel": {2: 100, 3: 80, 5: 60, 7: 40, 10: 25, 15: 10, 20: 5},
                "spin_wheel": {6: 100, 7: 80, 8: 60, 9: 40, 10: 25, 11: 15, 12: 10},
            },
            "super_bonus": {
                "multiplier_wheel": {3: 100, 5: 80, 7: 60, 10: 50, 15: 35, 20: 25, 30: 15, 50: 8, 70: 3},
                "spin_wheel": {8: 100, 9: 80, 10: 60, 11: 50, 12: 40, 13: 30, 14: 20, 15: 12, 16: 8},
            },
            "ultra_bonus": {
                "multiplier_wheel": {5: 100, 7: 80, 10: 60, 15: 50, 20: 40, 30: 30, 40: 20, 50: 12, 70: 6, 100: 2},
                "spin_wheel": {12: 100, 14: 80, 16: 60, 18: 50, 20: 40, 22: 30, 24: 20, 26: 12, 28: 6, 30: 2},
            },
        }

        # Conditions
        basegame_condition = {
            "reel_weights": {self.basegame_type: {"BR0": 1}},
            "mult_values": {self.basegame_type: {1: 1}},
            "force_wincap": False,
            "force_freegame": False,
        }

        zerowin_condition = {
            "reel_weights": {self.basegame_type: {"BR0": 1}},
            "mult_values": {self.basegame_type: {1: 1}},
            "force_wincap": False,
            "force_freegame": False,
        }

        bonus_condition = {
            "reel_weights": {
                self.basegame_type: {"BR0": 1},
                self.freegame_type: {"FR0": 1},
            },
            "scatter_triggers": {3: 50, 4: 10, 5: 2},
            "mult_values": {
                self.basegame_type: {1: 1},
                self.freegame_type: {2: 60, 3: 80, 5: 50, 7: 20, 10: 15, 20: 10, 50: 5},
            },
            "force_wincap": False,
            "force_freegame": True,
        }

        super_bonus_condition = {
            "reel_weights": {
                self.basegame_type: {"BR0": 1},
                self.freegame_type: {"FR1": 1},
            },
            "scatter_triggers": {4: 10, 5: 2},
            "mult_values": {
                self.basegame_type: {1: 1},
                self.freegame_type: {3: 60, 5: 80, 7: 50, 10: 30, 15: 20, 20: 15, 30: 10, 50: 5, 70: 2},
            },
            "force_wincap": False,
            "force_freegame": True,
        }

        ultra_bonus_condition = {
            "reel_weights": {
                self.basegame_type: {"BR0": 1},
                self.freegame_type: {"FR2": 1},
            },
            "scatter_triggers": {5: 2},
            "mult_values": {
                self.basegame_type: {1: 1},
                self.freegame_type: {5: 60, 7: 80, 10: 50, 15: 30, 20: 25, 30: 20, 40: 15, 50: 10, 70: 5, 100: 2},
            },
            "force_wincap": False,
            "force_freegame": True,
        }

        wincap_condition = {
            "reel_weights": {
                self.basegame_type: {"WCAP": 1},
                self.freegame_type: {"WCAP": 1},
            },
            "mult_values": {
                self.basegame_type: {1: 1},
                self.freegame_type: {5: 10, 7: 20, 10: 50, 15: 60, 20: 100, 30: 90, 50: 70, 70: 40, 100: 20},
            },
            "scatter_triggers": {4: 1, 5: 2},
            "force_wincap": True,
            "force_freegame": True,
        }

        mode_maxwins = {
            "base": 7777,
            "bonus": 7777,
            "super_bonus": 7777,
            "ultra_bonus": 7777
        }

        # Bet Modes
        self.bet_modes = [
            # Base game
            BetMode(
                name="base",
                cost=1.0,
                rtp=self.rtp,
                max_win=mode_maxwins["base"],
                auto_close_disabled=False,
                is_feature=True,
                is_buybonus=False,
                distributions=[
                    Distribution(criteria="freegame", quota=0.1, conditions=bonus_condition),
                    Distribution(criteria="0", quota=0.4, win_criteria=0.0, conditions=zerowin_condition),
                    Distribution(criteria="basegame", quota=0.5, conditions=basegame_condition),
                ],
            ),
            # Buy Bonus (100x cost)
            BetMode(
                name="bonus",
                cost=100.0,
                rtp=self.rtp,
                max_win=mode_maxwins["bonus"],
                auto_close_disabled=False,
                is_feature=False,
                is_buybonus=True,
                distributions=[
                    Distribution(criteria="freegame", quota=1.0, conditions=bonus_condition),
                ],
            ),
            # Buy Super Bonus (200x cost)
            BetMode(
                name="super_bonus",
                cost=200.0,
                rtp=self.rtp,
                max_win=mode_maxwins["super_bonus"],
                auto_close_disabled=False,
                is_feature=False,
                is_buybonus=True,
                distributions=[
                    Distribution(criteria="freegame", quota=1.0, conditions=super_bonus_condition),
                ],
            ),
            # Buy Ultra Bonus (300x cost)
            BetMode(
                name="ultra_bonus",
                cost=300.0,
                rtp=self.rtp,
                max_win=mode_maxwins["ultra_bonus"],
                auto_close_disabled=False,
                is_feature=False,
                is_buybonus=True,
                distributions=[
                    Distribution(criteria="freegame", quota=1.0, conditions=ultra_bonus_condition),
                ],
            ),
        ]