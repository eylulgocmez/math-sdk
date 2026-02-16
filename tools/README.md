# Slot Game Development Tools

A collection of professional tools for slot game development.

## Available Tools

| Tool | Description | Usage |
|------|-------------|-------|
| [Reel Generator](./reel_generator/) | Generate reel strips with symbol weights and adjacent rules | `python tools/reel_generator/generator.py` |
| [RTP Calculator](./rtp_calculator/) | Estimate RTP from game config and reel strips | `python tools/rtp_calculator/calculator.py` |

## Quick Start

### 1. Generate Reel Strips
```bash
# Create reel strips for your game
python tools/reel_generator/generator.py --config tools/reel_generator/configs/lucky_7s.json
```

### 2. Calculate RTP Estimate
```bash
# Analyze RTP for your game
python tools/rtp_calculator/calculator.py --game games/lucky_7s
```

## Tool Details

### Reel Generator

Creates CSV reel strip files based on JSON configuration.

**Features:**
- Symbol weight configuration
- Adjacent symbol rules (prevent unwanted patterns)
- Multiple reel types (BR0, FR0, WCAP)
- Visual statistics output
- Automatic log generation

**Output:** CSV files in `games/{game_name}/reels/`

[Full Documentation →](./reel_generator/README.md)

---

### RTP Calculator

Estimates RTP by analyzing game configuration and reel strips.

**Features:**
- Reads game_config.py automatically
- Symbol probability analysis
- Volatility estimation
- Base game RTP calculation
- Free spin RTP contribution
- Detailed reports

**Output:** Report saved to `games/{game_name}/rtp_report.txt`

[Full Documentation →](./rtp_calculator/README.md)

---

## Workflow
```
1. Create game config (game_config.py)
           ↓
2. Create reel generator config (JSON)
           ↓
3. Run Reel Generator → CSV files
           ↓
4. Run RTP Calculator → RTP estimate
           ↓
5. Run Simulation (make sim) → Verify RTP
           ↓
6. Adjust and repeat if needed
```

## Requirements

No external packages required. All tools use Python built-in libraries.

See [requirements.txt](./requirements.txt) for details.

## Version

v1.0.0