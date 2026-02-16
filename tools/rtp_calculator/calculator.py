"""RTP Calculator - Calculates estimated RTP from game config and reel strips."""

import sys
import argparse
import os
import csv
from typing import Dict, List, Tuple

# Add project root to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))


class RTPCalculator:
    """Calculate RTP using game config and reel strip data."""

    def __init__(self, game_path: str):
        self.game_path = game_path
        self.config = None
        self.reels = {}
        self.symbol_counts = {}
        self.symbol_probabilities = {}

        self._load_game_config()
        self._load_reels()

    def _load_game_config(self):
        """Load game configuration from game_config.py."""
        # Import game config dynamically
        config_path = os.path.join(self.game_path, 'game_config.py')

        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Game config not found: {config_path}")

        # Import the module
        import importlib.util
        spec = importlib.util.spec_from_file_location("game_config", config_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        self.config = module.GameConfig()

    def _load_reels(self):
        """Load reel strips from CSV files."""
        reels_path = os.path.join(self.game_path, 'reels')

        if not os.path.exists(reels_path):
            raise FileNotFoundError(f"Reels folder not found: {reels_path}")

        for filename in os.listdir(reels_path):
            if filename.endswith('.csv'):
                reel_name = filename.replace('.csv', '')
                filepath = os.path.join(reels_path, filename)
                self.reels[reel_name] = self._read_csv(filepath)
                self._calculate_symbol_counts(reel_name)

    def _read_csv(self, filepath: str) -> List[List[str]]:
        """Read CSV file and return as list of columns (reels)."""
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)

        # Transpose: rows to columns
        num_reels = len(rows[0]) if rows else 0
        reels = [[] for _ in range(num_reels)]

        for row in rows:
            for i, symbol in enumerate(row):
                reels[i].append(symbol)

        return reels

    def _calculate_symbol_counts(self, reel_name: str):
        """Calculate symbol counts and probabilities for a reel set."""
        reels = self.reels[reel_name]
        counts = {}

        for reel_idx, reel in enumerate(reels):
            counts[reel_idx] = {}
            for symbol in reel:
                counts[reel_idx][symbol] = counts[reel_idx].get(symbol, 0) + 1

        self.symbol_counts[reel_name] = counts

        # Calculate probabilities
        probs = {}
        for reel_idx, reel in enumerate(reels):
            reel_length = len(reel)
            probs[reel_idx] = {}
            for symbol, count in counts[reel_idx].items():
                probs[reel_idx][symbol] = count / reel_length

        self.symbol_probabilities[reel_name] = probs

    def calculate_symbol_hit_probability(self, reel_name: str, symbol: str, count: int) -> float:
        """Calculate probability of getting exactly 'count' of a symbol on payline."""
        probs = self.symbol_probabilities.get(reel_name, {})

        if not probs:
            return 0.0

        # Probability of symbol appearing on first 'count' reels
        probability = 1.0
        for reel_idx in range(count):
            if reel_idx in probs and symbol in probs[reel_idx]:
                probability *= probs[reel_idx][symbol]
            else:
                probability *= 0

        # Probability of NOT appearing on next reel (if exists)
        if count < len(probs):
            next_reel = count
            if next_reel in probs:
                symbol_prob = probs[next_reel].get(symbol, 0)
                probability *= (1 - symbol_prob)

        return probability

    def calculate_line_rtp(self, reel_name: str = "BR0") -> Dict:
        """Calculate RTP contribution for each symbol."""
        if not hasattr(self.config, 'paytable'):
            return {"error": "No paytable found in config"}

        paytable = self.config.paytable
        results = {}
        total_rtp = 0.0

        # Get unique symbols from paytable
        symbols = set()
        for (count, symbol), payout in paytable.items():
            symbols.add(symbol)

        for symbol in symbols:
            symbol_rtp = 0.0
            symbol_details = []

            # Calculate for each winning combination (3, 4, 5 of a kind)
            for match_count in [3, 4, 5]:
                key = (match_count, symbol)
                if key in paytable:
                    payout = paytable[key]
                    prob = self.calculate_symbol_hit_probability(reel_name, symbol, match_count)

                    # Multiply by number of paylines
                    num_paylines = len(self.config.paylines) if hasattr(self.config, 'paylines') else 1
                    contribution = prob * payout * num_paylines

                    symbol_rtp += contribution
                    symbol_details.append({
                        "match": match_count,
                        "payout": payout,
                        "probability": prob,
                        "contribution": contribution
                    })

            results[symbol] = {
                "rtp_contribution": symbol_rtp,
                "details": symbol_details
            }
            total_rtp += symbol_rtp

        return {
            "reel_type": reel_name,
            "symbols": results,
            "base_rtp": total_rtp,
            "base_rtp_percent": total_rtp * 100
        }

    def get_volatility_estimate(self, reel_name: str = "BR0") -> str:
        """Estimate volatility based on symbol distribution."""
        probs = self.symbol_probabilities.get(reel_name, {})

        if not probs or not hasattr(self.config, 'paytable'):
            return "Unknown"

        # Get high-value symbol probability (first reel)
        paytable = self.config.paytable

        # Find highest paying symbol
        max_payout = 0
        high_symbol = None
        for (count, symbol), payout in paytable.items():
            if payout > max_payout:
                max_payout = payout
                high_symbol = symbol

        if high_symbol and 0 in probs:
            high_prob = probs[0].get(high_symbol, 0)

            if high_prob < 0.03:
                return "High"
            elif high_prob < 0.06:
                return "Medium-High"
            elif high_prob < 0.10:
                return "Medium"
            else:
                return "Low"

        return "Unknown"

    def calculate_total_rtp_estimate(self, reel_name: str = "BR0") -> Dict:
        """
        Estimate total RTP including free spins and bonuses.

        NOTE: This is an ESTIMATE only. Run full simulation (make sim) for accurate RTP.
        """

        # Base game RTP
        base_rtp_data = self.calculate_line_rtp(reel_name)
        base_rtp = base_rtp_data.get('base_rtp', 0)

        # Free spin trigger probability (3+ scatters)
        scatter_symbol = None
        if hasattr(self.config, 'special_symbols'):
            scatters = self.config.special_symbols.get('scatter', [])
            if scatters:
                scatter_symbol = scatters[0]

        fs_trigger_prob = 0
        fs_avg_multiplier = 1
        fs_avg_spins = 0

        if scatter_symbol:
            probs = self.symbol_probabilities.get(reel_name, {})

            # Probability of scatter on each reel
            scatter_probs = []
            for reel_idx in range(self.config.num_reels if hasattr(self.config, 'num_reels') else 5):
                if reel_idx in probs:
                    scatter_probs.append(probs[reel_idx].get(scatter_symbol, 0))
                else:
                    scatter_probs.append(0)

            # Probability of 3+ scatters (simplified)
            if len(scatter_probs) >= 3:
                avg_prob = sum(scatter_probs) / len(scatter_probs)
                from math import comb
                fs_trigger_prob = comb(5, 3) * (avg_prob ** 3) * ((1 - avg_prob) ** 2)
                fs_trigger_prob += comb(5, 4) * (avg_prob ** 4) * ((1 - avg_prob) ** 1)
                fs_trigger_prob += comb(5, 5) * (avg_prob ** 5)

            # Average free spins (from config)
            if hasattr(self.config, 'freespin_triggers'):
                triggers = self.config.freespin_triggers.get(self.config.basegame_type, {})
                if triggers:
                    fs_avg_spins = sum(triggers.values()) / len(triggers)

            # Average multiplier (from config)
            if hasattr(self.config, 'padding_symbol_values'):
                mult_data = self.config.padding_symbol_values.get(scatter_symbol, {})
                mult_values = mult_data.get('multiplier', {})
                if mult_values:
                    total_weight = sum(mult_values.values())
                    fs_avg_multiplier = sum(m * w for m, w in mult_values.items()) / total_weight

        # Free spin RTP contribution
        fs_rtp = fs_trigger_prob * fs_avg_spins * base_rtp * fs_avg_multiplier

        # Total RTP estimate
        total_rtp = base_rtp + fs_rtp

        return {
            "base_rtp": base_rtp,
            "base_rtp_percent": base_rtp * 100,
            "fs_trigger_prob": fs_trigger_prob,
            "fs_trigger_percent": fs_trigger_prob * 100,
            "fs_avg_spins": fs_avg_spins,
            "fs_avg_multiplier": fs_avg_multiplier,
            "fs_rtp": fs_rtp,
            "fs_rtp_percent": fs_rtp * 100,
            "total_rtp": total_rtp,
            "total_rtp_percent": total_rtp * 100
        }

    def generate_report(self) -> str:
        """Generate full RTP analysis report."""
        lines = []

        lines.append("=" * 60)
        lines.append("RTP CALCULATOR REPORT")
        lines.append("=" * 60)
        lines.append(f"Game: {self.config.game_id if hasattr(self.config, 'game_id') else 'Unknown'}")
        lines.append(f"Target RTP: {self.config.rtp * 100 if hasattr(self.config, 'rtp') else 'N/A'}%")
        lines.append(f"Win Cap: {self.config.wincap if hasattr(self.config, 'wincap') else 'N/A'}x")
        lines.append("")

        # Analyze each reel type
        for reel_name in self.reels.keys():
            lines.append("-" * 60)
            lines.append(f"REEL: {reel_name}")
            lines.append("-" * 60)

            # Volatility estimate
            volatility = self.get_volatility_estimate(reel_name)
            lines.append(f"Estimated Volatility: {volatility}")
            lines.append("")

            # Symbol probabilities
            lines.append("Symbol Probabilities (Reel 1):")
            probs = self.symbol_probabilities.get(reel_name, {})
            if 0 in probs:
                sorted_probs = sorted(probs[0].items(), key=lambda x: -x[1])
                for symbol, prob in sorted_probs:
                    bar = "=" * int(prob * 100)
                    lines.append(f"   {symbol:<6} {prob * 100:>5.1f}%  {bar}")
            lines.append("")

            # RTP calculation
            rtp_data = self.calculate_line_rtp(reel_name)
            if "error" not in rtp_data:
                lines.append(f"Base Game RTP Estimate: {rtp_data['base_rtp_percent']:.2f}%")
                # Total RTP estimate
                total_rtp_data = self.calculate_total_rtp_estimate(reel_name)
                lines.append("")
                lines.append("TOTAL RTP ESTIMATE:")
                lines.append(f"   Base Game RTP:      {total_rtp_data['base_rtp_percent']:>6.2f}%")
                lines.append(f"   FS Trigger Prob:    {total_rtp_data['fs_trigger_percent']:>6.2f}%")
                lines.append(f"   FS Avg Spins:       {total_rtp_data['fs_avg_spins']:>6.1f}")
                lines.append(f"   FS Avg Multiplier:  {total_rtp_data['fs_avg_multiplier']:>6.1f}x")
                lines.append(f"   Free Spin RTP:      {total_rtp_data['fs_rtp_percent']:>6.2f}%")
                lines.append(f"   --------------------------")
                lines.append(f"   TOTAL RTP:          {total_rtp_data['total_rtp_percent']:>6.2f}%")
                lines.append("")
                lines.append("RTP by Symbol:")

                sorted_symbols = sorted(
                    rtp_data['symbols'].items(),
                    key=lambda x: -x[1]['rtp_contribution']
                )

                for symbol, data in sorted_symbols:
                    contrib = data['rtp_contribution'] * 100
                    lines.append(f"   {symbol:<6} {contrib:>6.2f}%")

            lines.append("")

        lines.append("=" * 60)
        lines.append("Note: This is an ESTIMATE. Actual RTP may vary.")
        lines.append("Run full simulation for accurate RTP calculation.")
        lines.append("=" * 60)

        return "\n".join(lines)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Calculate RTP estimates for slot games')
    parser.add_argument('--game', '-g', type=str, default='games/lucky_7s',
                        help='Path to game folder')
    args = parser.parse_args()

    game_path = args.game

    if not os.path.exists(game_path):
        print(f"Error: Game folder not found: {game_path}")
        print(f"Please provide a valid game path. Example: games/lucky_7s")
        return

    try:
        calculator = RTPCalculator(game_path)
        report = calculator.generate_report()
        print(report)

        # Save report
        report_path = os.path.join(game_path, "rtp_report.txt")
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\nReport saved: {report_path}")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()