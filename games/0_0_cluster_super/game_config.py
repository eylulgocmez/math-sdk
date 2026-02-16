"""Cluster game configuration file/setup"""

import os
from src.config.config import Config
from src.config.distributions import Distribution
from src.config.betmode import BetMode


class GameConfig(Config):
    """Singleton cluster game configuration class."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        super().__init__()
        self.game_id = "0_0_cluster_super"
        self.provider_number = 0
        self.working_name = "Sample Cluster Game"
        self.wincap = 5000.0
        self.win_type = "cluster"
        self.rtp = 0.9700
        self.construct_paths()

        # Game Dimensions
        self.num_reels = 7
        # Optionally include variable number of rows per reel
        self.num_rows = [7] * self.num_reels
        # Board and Symbol Properties
        t1, t2, t3, t4 = (5, 5), (6, 8), (9, 12), (13, 36)
        pay_group = {
            (t1, "H1"): 7.0,
            (t2, "H1"): 18.0,
            (t3, "H1"): 35.0,
            (t4, "H1"): 85.0,
            (t1, "H2"): 3.0,
            (t2, "H2"): 7.0,
            (t3, "H2"): 15.0,
            (t4, "H2"): 55.0,
            (t1, "H3"): 2.0,
            (t2, "H3"): 5.0,
            (t3, "H3"): 10.0,
            (t4, "H3"): 40.0,
            (t1, "H4"): 1.5,
            (t2, "H4"): 4.0,
            (t3, "H4"): 8.0,
            (t4, "H4"): 28.0,
            (t1, "L1"): 0.4,
            (t2, "L1"): 1.0,
            (t3, "L1"): 2.5,
            (t4, "L1"): 6.0,
            (t1, "L2"): 0.3,
            (t2, "L2"): 0.8,
            (t3, "L2"): 2.0,
            (t4, "L2"): 5.0,
            (t1, "L3"): 0.1,
            (t2, "L3"): 0.5,
            (t3, "L3"): 1.5,
            (t4, "L3"): 3.0,
            (t1, "L4"): 0.1,
            (t2, "L4"): 0.3,
            (t3, "L4"): 1.0,
            (t4, "L4"): 2.5,
        }
        self.paytable = self.convert_range_table(pay_group)

        self.include_padding = True
        self.special_symbols = {"wild": ["W"], "scatter": ["S"]}

        self.freespin_triggers = {
            self.basegame_type: {4: 10, 5: 12, 6: 15, 7: 18, 8: 20},
            self.freegame_type: {3: 5, 4: 8, 5: 10, 6: 12, 7: 15, 8: 18},
        }
        self.anticipation_triggers = {
            self.basegame_type: min(self.freespin_triggers[self.basegame_type].keys()) - 1,
            self.freegame_type: min(self.freespin_triggers[self.freegame_type].keys()) - 1,
        }

        self.maximum_board_mult = 512

        reels = {"BR0": "BR0.csv", "FR0": "FR0.csv", "FR0_SUPER": "FR0_SUPER.csv", "WCAP": "WCAP.csv"}
        self.reels = {}
        for r, f in reels.items():
            self.reels[r] = self.read_reels_csv(os.path.join(self.reels_path, f))
        mode_maxwins = {"base": 5000, "bonus": 5000, "super_bonus": 5000}

        self.bet_modes = [
            BetMode(
                name="base",
                cost=1.0,
                rtp=self.rtp,
                max_win=mode_maxwins["base"],
                auto_close_disabled=False,
                is_feature=True,
                is_buybonus=False,
                distributions=[
                    Distribution(
                        criteria="wincap",
                        quota=0.001,
                        win_criteria=mode_maxwins["base"],
                        conditions={
                            "reel_weights": {
                                self.basegame_type: {"BR0": 1},
                                self.freegame_type: {"FR0": 1, "WCAP": 5},
                            },
                            "scatter_triggers": {4: 1, 5: 2},
                            "force_wincap": True,
                            "force_freegame": True,
                        },
                    ),
                    Distribution(
                        criteria="freegame",
                        quota=0.1,
                        conditions={
                            "reel_weights": {
                                self.basegame_type: {"BR0": 1},
                                self.freegame_type: {"FR0": 1},
                            },
                            "scatter_triggers": {4: 5, 5: 1},
                            "force_wincap": False,
                            "force_freegame": True,
                        },
                    ),
                    Distribution(
                        criteria="0",
                        quota=0.4,
                        win_criteria=0.0,
                        conditions={
                            "reel_weights": {self.basegame_type: {"BR0": 1}},
                            "force_wincap": False,
                            "force_freegame": False,
                        },
                    ),
                    Distribution(
                        criteria="basegame",
                        quota=0.5,
                        conditions={
                            "reel_weights": {self.basegame_type: {"BR0": 1}},
                            "force_wincap": False,
                            "force_freegame": False,
                        },
                    ),
                ],
            ),
            BetMode(
                name="bonus",
                cost=200,
                rtp=self.rtp,
                max_win=mode_maxwins["bonus"],
                auto_close_disabled=False,
                is_feature=True,
                is_buybonus=False,
                distributions=[
                    Distribution(
                        criteria="wincap",
                        quota=0.001,
                        win_criteria=mode_maxwins["bonus"],
                        conditions={
                            "reel_weights": {
                                self.basegame_type: {"BR0": 1},
                                self.freegame_type: {"FR0": 1, "WCAP": 5},
                            },
                            "mult_values": {
                                self.basegame_type: {
                                    2: 10,
                                    3: 20,
                                    4: 30,
                                    5: 20,
                                    10: 20,
                                    20: 20,
                                    50: 10,
                                },
                                self.freegame_type: {
                                    2: 10,
                                    3: 20,
                                    4: 30,
                                    5: 20,
                                    10: 20,
                                    20: 20,
                                    50: 10,
                                },
                            },
                            "scatter_triggers": {4: 1, 5: 2},
                            "force_wincap": True,
                            "force_freegame": True,
                        },
                    ),
                    Distribution(
                        criteria="freegame",
                        quota=0.1,
                        conditions={
                            "reel_weights": {
                                self.basegame_type: {"BR0": 1},
                                self.freegame_type: {"FR0": 1},
                            },
                            "scatter_triggers": {4: 5, 5: 1},
                            "force_wincap": False,
                            "force_freegame": True,
                        },
                    ),
                ],
            ),
            BetMode(
                name="super_bonus",
                cost=500,
                rtp=self.rtp,
                max_win=mode_maxwins["super_bonus"],
                auto_close_disabled=False,
                is_feature=True,
                is_buybonus=False,
                distributions=[
                    Distribution(
                        criteria="wincap",
                        quota=0.002,
                        win_criteria=mode_maxwins["super_bonus"],
                        conditions={
                            "reel_weights": {
                                self.basegame_type: {"BR0": 1},
                                self.freegame_type: {"FR0_SUPER": 1, "WCAP": 5},
                            },
                            "mult_values": {
                                self.basegame_type: {
                                    3: 35,
                                    5: 28,
                                    10: 20,
                                    20: 12,
                                    50: 5,
                                },
                                self.freegame_type: {
                                    3: 35,
                                    5: 28,
                                    10: 20,
                                    20: 12,
                                    50: 5,
                                },
                            },
                            "scatter_triggers": {4: 1, 5: 2},
                            "force_wincap": True,
                            "force_freegame": True,
                        },
                    ),
                    Distribution(
                        criteria="freegame",
                        quota=0.05,
                        conditions={
                            "reel_weights": {
                                self.basegame_type: {"BR0": 1},
                                self.freegame_type: {"FR0_SUPER": 1},
                            },
                            "scatter_triggers": {4: 5, 5: 1},
                            "force_wincap": False,
                            "force_freegame": True,
                        },
                    ),
                ],
            ),
        ]
