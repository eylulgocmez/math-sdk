"""Reel Strip Generator for slot games."""

import json
import argparse
import random
import csv
import os
from datetime import datetime
from typing import Dict, List


class ReelGenerator:
    """Professional reel strip generator with advanced features."""

    def __init__(self, config_path: str = None):
        self.config = None
        self.symbols = {}
        self.reel_length = 100
        self.num_reels = 5

        if config_path:
            self.load_config(config_path)

    def load_config(self, config_path: str):
        """Load configuration from JSON file."""
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)

        self.symbols = self.config.get('symbols', {})
        self.reel_length = self.config.get('reel_length', 100)
        self.num_reels = self.config.get('num_reels', 5)

    def calculate_counts(self, weight_override: Dict[str, int] = None) -> Dict[str, int]:
        """Calculate symbol counts based on weights."""
        weights = {}
        for symbol, data in self.symbols.items():
            if weight_override and symbol in weight_override:
                weights[symbol] = weight_override[symbol]
            else:
                weights[symbol] = data.get('weight', 10)

        total_weight = sum(weights.values())
        counts = {}

        for symbol, weight in weights.items():
            count = round((weight / total_weight) * self.reel_length)
            counts[symbol] = max(1, count)

        # Adjust to match reel_length
        diff = self.reel_length - sum(counts.values())
        if diff != 0:
            max_symbol = max(weights, key=weights.get)
            counts[max_symbol] += diff

        return counts

    def check_adjacent(self, reel: List[str], symbol: str, position: int) -> bool:
        """Check if symbol placement violates adjacent rules."""
        max_adj = self.symbols.get(symbol, {}).get('max_adjacent', 99)

        count = 0
        for i in range(position - 1, -1, -1):
            if reel[i] == symbol:
                count += 1
            else:
                break

        return count < max_adj

    def generate_reel(self, counts: Dict[str, int]) -> List[str]:
        """Generate a single reel strip."""
        pool = []
        for symbol, count in counts.items():
            pool.extend([symbol] * count)

        random.shuffle(pool)

        reel = []
        max_attempts = len(pool) * 10
        attempts = 0

        while pool and attempts < max_attempts:
            idx = random.randint(0, len(pool) - 1)
            symbol = pool[idx]

            if self.check_adjacent(reel, symbol, len(reel)):
                reel.append(symbol)
                pool.pop(idx)
                attempts = 0
            else:
                attempts += 1
                if attempts > 50:
                    random.shuffle(pool)

        if pool:
            reel.extend(pool)

        return reel

    def generate_all_reels(self, weight_override: Dict[str, int] = None) -> List[List[str]]:
        """Generate all reel strips."""
        counts = self.calculate_counts(weight_override)

        reels = []
        for i in range(self.num_reels):
            reel = self.generate_reel(counts.copy())
            reels.append(reel)

        return reels

    def export_csv(self, reels: List[List[str]], output_path: str):
        """Export reels to CSV file."""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for row_idx in range(self.reel_length):
                row = [reels[col_idx][row_idx] for col_idx in range(len(reels))]
                writer.writerow(row)

    def generate_game_reels(self, output_dir: str):
        """Generate all reel types for the game."""
        if not self.config:
            return

        reel_types = self.config.get('reel_types', {})

        for reel_name, reel_config in reel_types.items():
            weight_override = reel_config.get('weight_override', {})
            reels = self.generate_all_reels(weight_override)

            output_path = os.path.join(output_dir, f"{reel_name}.csv")
            self.export_csv(reels, output_path)

    def get_statistics_text(self, reels: List[List[str]]) -> str:
        """Return reel statistics as formatted text."""
        total_counts = {}

        for reel in reels:
            for symbol in reel:
                total_counts[symbol] = total_counts.get(symbol, 0) + 1

        total = sum(total_counts.values())
        sorted_symbols = sorted(total_counts.items(), key=lambda x: -x[1])

        lines = []
        lines.append(f"\n   {'Symbol':<8} {'Count':<8} {'Percent':<10} {'Distribution'}")
        lines.append(f"   {'-' * 50}")

        for symbol, count in sorted_symbols:
            pct = (count / total) * 100
            bar_length = int(pct * 2)
            bar = "=" * bar_length
            lines.append(f"   {symbol:<8} {count:<8} {pct:>5.1f}%     {bar}")

        lines.append(f"   {'-' * 50}")
        lines.append(f"   {'TOTAL':<8} {total:<8} {100.0:>5.1f}%")

        return '\n'.join(lines)

    def print_statistics(self, reels: List[List[str]]):
        """Print reel statistics with visual bar chart."""
        print(self.get_statistics_text(reels))


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Generate reel strips for slot games')
    parser.add_argument('--config', '-c', type=str, default='tools/reel_generator/configs/lucky_7s.json',
                        help='Path to config JSON file')
    parser.add_argument('--output', '-o', type=str, default=None,
                        help='Output directory for CSV files')
    args = parser.parse_args()

    config_path = args.config

    if not os.path.exists(config_path):
        print(f"Error: Config file not found: {config_path}")
        print(f"Please create a config file. See README.md for examples.")
        return

    generator = ReelGenerator(config_path)

    # Determine output directory
    if args.output:
        output_dir = args.output
    else:
        game_name = generator.config.get('game_name', 'unknown')
        output_dir = f"games/{game_name}/reels"

    # Create log file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"generation_log_{timestamp}.txt"
    log_path = os.path.join("tools/reel_generator/logs", log_filename)
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    # Write to both terminal and file
    log_lines = []

    log_lines.append(f"{'=' * 50}")
    log_lines.append(f"REEL GENERATOR")
    log_lines.append(f"{'=' * 50}")
    log_lines.append(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log_lines.append(f"Config: {config_path}")
    log_lines.append(f"Game: {generator.config.get('game_name', 'Unknown')}")
    log_lines.append(f"Reel Length: {generator.reel_length}")
    log_lines.append(f"Num Reels: {generator.num_reels}")
    log_lines.append(f"Symbols: {len(generator.symbols)}")
    log_lines.append(f"{'=' * 50}\n")

    reel_types = generator.config.get('reel_types', {})

    for reel_name, reel_config in reel_types.items():
        # Check for custom reel_length
        custom_length = reel_config.get('reel_length', None)
        if custom_length:
            generator.reel_length = custom_length
        else:
            generator.reel_length = generator.config.get('reel_length', 100)

        log_lines.append(f"Generating {reel_name} (length: {generator.reel_length})...")
        weight_override = reel_config.get('weight_override', {})
        reels = generator.generate_all_reels(weight_override)

        output_path = os.path.join(output_dir, f"{reel_name}.csv")
        generator.export_csv(reels, output_path)

        log_lines.append(f"   Saved: {output_path}")

        # Get statistics
        stats = generator.get_statistics_text(reels)
        log_lines.append(stats)
        log_lines.append("")

    log_lines.append(f"{'=' * 50}")
    log_lines.append(f"All reels generated successfully!")
    log_lines.append(f"Output: {output_dir}")
    log_lines.append(f"Log: {log_path}")
    log_lines.append(f"{'=' * 50}\n")

    # Print to terminal
    for line in log_lines:
        print(line)

    # Save to file
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(log_lines))


if __name__ == "__main__":
    main()