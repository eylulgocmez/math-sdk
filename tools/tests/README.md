# Unit Tests

Automated tests for slot game development tools.

## Available Tests

| Test File | Description | Tests |
|-----------|-------------|-------|
| test_generator.py | Reel Generator tests | 7 tests |
| test_calculator.py | RTP Calculator tests | 5 tests |

## Running Tests

Run all generator tests:
```bash
python tools/tests/test_generator.py
```

Run all calculator tests:
```bash
python tools/tests/test_calculator.py
```

Run all tests at once:
```bash
python tools/tests/test_generator.py && python tools/tests/test_calculator.py
```

## Test Descriptions

### Generator Tests

| Test | Description |
|------|-------------|
| test_calculate_counts_basic | Verifies symbol counts match weights |
| test_calculate_counts_with_override | Verifies weight override increases symbol count |
| test_check_adjacent_allows | Verifies adjacent rule allows valid placements |
| test_check_adjacent_blocks | Verifies adjacent rule blocks invalid placements |
| test_generate_reel_length | Verifies generated reel has correct length |
| test_generate_reel_contains_all_symbols | Verifies all symbols are present in reel |
| test_generate_all_reels_count | Verifies correct number of reels generated |

### Calculator Tests

| Test | Description |
|------|-------------|
| test_symbol_probabilities | Verifies probability calculations |
| test_symbol_counts | Verifies symbol counting |
| test_volatility_high | Verifies high volatility detection |
| test_volatility_low | Verifies low volatility detection |
| test_hit_probability_calculation | Verifies hit probability math |

## Expected Output
```
==================================================
REEL GENERATOR UNIT TESTS
==================================================

✅ test_calculate_counts_basic PASSED
✅ test_calculate_counts_with_override PASSED
✅ test_check_adjacent_allows PASSED
✅ test_check_adjacent_blocks PASSED
✅ test_generate_reel_length PASSED
✅ test_generate_reel_contains_all_symbols PASSED
✅ test_generate_all_reels_count PASSED

==================================================
RESULTS: 7 passed, 0 failed
==================================================
```

## Adding New Tests

To add a new test:

1. Create a function starting with `test_`
2. Use `assert` statements to verify behavior
3. Print success message at the end
4. Add function to `tests` list in `run_all_tests()`

Example:
```python
def test_my_new_feature():
    """Test description here."""
    result = some_function()
    assert result == expected, f"Expected {expected}, got {result}"
    print("✅ test_my_new_feature PASSED")
```