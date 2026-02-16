# Reel Generator

Professional reel strip generator for slot games.

## Features

- Symbol weight configuration
- Adjacent symbol rules (max_adjacent)
- Multiple reel types (BR0, FR0, WCAP)
- CSV export (SDK compatible)
- Visual statistics with bar charts
- Automatic log file generation

## Usage

Basic usage (uses default config):
```bash
python tools/reel_generator/generator.py
```

With specific config file:
```bash
python tools/reel_generator/generator.py --config tools/reel_generator/configs/lucky_7s.json
```

With custom output directory:
```bash
python tools/reel_generator/generator.py --output games/my_game/reels
```

Show help:
```bash
python tools/reel_generator/generator.py --help
```

## Command Line Arguments

| Argument | Short | Description | Default |
|----------|-------|-------------|---------|
| --config | -c | Path to config JSON file | configs/lucky_7s.json |
| --output | -o | Output directory for CSV files | games/{game_name}/reels |
| --help | -h | Show help message | - |

## Configuration

Create a JSON config file in `configs/` folder:
```json
{
    "game_name": "my_game",
    "reel_length": 100,
    "num_reels": 5,
    "symbols": {
        "W": {"weight": 3, "max_adjacent": 1},
        "H1": {"weight": 8, "max_adjacent": 3},
        "L1": {"weight": 15, "max_adjacent": 5}
    },
    "reel_types": {
        "BR0": {
            "description": "Base game reel",
            "weight_override": {}
        },
        "FR0": {
            "description": "Free spin reel",
            "weight_override": {"W": 6}
        }
    }
}
```

## Config Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| game_name | Name of the game | "lucky_7s" |
| reel_length | Positions per reel | 100 |
| num_reels | Number of reels | 5 |
| symbols | Symbol definitions | See below |
| reel_types | Different reel configurations | See below |

### Symbol Properties

| Property | Description | Example |
|----------|-------------|---------|
| weight | Relative frequency (higher = more common) | 3 |
| max_adjacent | Maximum consecutive same symbols | 1 |

### weight_override

Override default weights for specific reel types:
- Empty `{}` = use default weights
- `{"W": 6}` = increase W weight to 6 for this reel

## Output

- CSV files saved to `games/{game_name}/reels/`
- Log files saved to `tools/reel_generator/logs/`

## Example Output
```
==================================================
REEL GENERATOR
==================================================
Timestamp: 2026-02-14 12:49:16
Game: lucky_7s
Reel Length: 100
Num Reels: 5
Symbols: 10
==================================================

Generating BR0...
   Saved: games/lucky_7s/reels/BR0.csv

   Symbol   Count    Percent    Distribution
   --------------------------------------------------
   P        75        15.0%     ==============================
   L        65        13.0%     ==========================
   7        10         2.0%     ====
   --------------------------------------------------
   TOTAL    500      100.0%
```