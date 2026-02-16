# RTP Calculator

Estimates RTP (Return to Player) by analyzing game config and reel strips.

## Features

- Reads game_config.py automatically
- Analyzes reel strip CSV files
- Calculates symbol probabilities
- Estimates volatility (High/Medium/Low)
- Base game RTP calculation
- Total RTP estimate (including free spins)
- Generates detailed reports

## Usage

Basic usage (uses default game):
```bash
python tools/rtp_calculator/calculator.py
```

With specific game folder:
```bash
python tools/rtp_calculator/calculator.py --game games/lucky_7s
```

Show help:
```bash
python tools/rtp_calculator/calculator.py --help
```

## Command Line Arguments

| Argument | Short | Description | Default |
|----------|-------|-------------|---------|
| --game | -g | Path to game folder | games/lucky_7s |
| --help | -h | Show help message | - |

## How It Works

1. Loads `game_config.py` from game folder
2. Reads reel strip CSV files
3. Calculates symbol probabilities per reel
4. Uses paytable to estimate RTP contribution
5. Estimates free spin trigger probability
6. Generates comprehensive report

## Output

Report includes:
- Target RTP (from config)
- Win Cap (from config)
- Volatility estimate per reel type
- Symbol probabilities with visual bars
- Base game RTP estimate
- Free spin contribution
- Total RTP estimate

## Example Output
```
============================================================
RTP CALCULATOR REPORT
============================================================
Game: lucky_7s
Target RTP: 97.0%
Win Cap: 7777x

------------------------------------------------------------
REEL: BR0
------------------------------------------------------------
Estimated Volatility: High

Symbol Probabilities (Reel 1):
   P       15.0%  ===============
   L       13.0%  =============
   7        2.0%  ==

Base Game RTP Estimate: 63.29%

TOTAL RTP ESTIMATE:
   Base Game RTP:       63.29%
   FS Trigger Prob:      0.01%
   FS Avg Spins:         10.0
   FS Avg Multiplier:     3.5x
   Free Spin RTP:        0.17%
   --------------------------
   TOTAL RTP:           63.46%
============================================================
```

## Important Notes

> **This is an ESTIMATE only.**
> Run full simulation (`make sim`) for accurate RTP calculation.

The calculator provides quick feedback during development, but final RTP verification requires running the complete simulation.

## Report Location

Reports are saved to: `games/{game_name}/rtp_report.txt`