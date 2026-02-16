"""Unit tests for RTP Calculator."""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from rtp_calculator.calculator import RTPCalculator


def test_symbol_probabilities():
    """Test that symbol probabilities are calculated correctly."""
    # Create a simple test case
    calculator = RTPCalculator.__new__(RTPCalculator)
    calculator.reels = {
        "TEST": [
            ["A", "A", "B", "B", "B", "B", "B", "B", "B", "B"],  # Reel 1: A=20%, B=80%
        ]
    }
    calculator.symbol_counts = {}
    calculator.symbol_probabilities = {}

    calculator._calculate_symbol_counts("TEST")

    probs = calculator.symbol_probabilities["TEST"][0]

    assert abs(probs["A"] - 0.2) < 0.01, f"A probability should be 0.2, got {probs['A']}"
    assert abs(probs["B"] - 0.8) < 0.01, f"B probability should be 0.8, got {probs['B']}"

    print("✅ test_symbol_probabilities PASSED")


def test_symbol_counts():
    """Test that symbol counts are calculated correctly."""
    calculator = RTPCalculator.__new__(RTPCalculator)
    calculator.reels = {
        "TEST": [
            ["A", "A", "A", "B", "B", "C"],  # A=3, B=2, C=1
        ]
    }
    calculator.symbol_counts = {}
    calculator.symbol_probabilities = {}

    calculator._calculate_symbol_counts("TEST")

    counts = calculator.symbol_counts["TEST"][0]

    assert counts["A"] == 3, f"A count should be 3, got {counts['A']}"
    assert counts["B"] == 2, f"B count should be 2, got {counts['B']}"
    assert counts["C"] == 1, f"C count should be 1, got {counts['C']}"

    print("✅ test_symbol_counts PASSED")


def test_volatility_high():
    """Test that high volatility is detected correctly."""
    calculator = RTPCalculator.__new__(RTPCalculator)
    calculator.symbol_probabilities = {
        "TEST": {
            0: {"WILD": 0.02, "LOW": 0.98}  # WILD is rare = High volatility
        }
    }

    # Mock config
    class MockConfig:
        paytable = {(5, "WILD"): 1000, (5, "LOW"): 10}

    calculator.config = MockConfig()

    volatility = calculator.get_volatility_estimate("TEST")

    assert volatility == "High", f"Volatility should be High, got {volatility}"

    print("✅ test_volatility_high PASSED")


def test_volatility_low():
    """Test that low volatility is detected correctly."""
    calculator = RTPCalculator.__new__(RTPCalculator)
    calculator.symbol_probabilities = {
        "TEST": {
            0: {"WILD": 0.15, "LOW": 0.85}  # WILD is common = Low volatility
        }
    }

    # Mock config
    class MockConfig:
        paytable = {(5, "WILD"): 1000, (5, "LOW"): 10}

    calculator.config = MockConfig()

    volatility = calculator.get_volatility_estimate("TEST")

    assert volatility == "Low", f"Volatility should be Low, got {volatility}"

    print("✅ test_volatility_low PASSED")


def test_hit_probability_calculation():
    """Test that hit probability is calculated correctly."""
    calculator = RTPCalculator.__new__(RTPCalculator)
    calculator.symbol_probabilities = {
        "TEST": {
            0: {"A": 0.1},
            1: {"A": 0.1},
            2: {"A": 0.1},
            3: {"A": 0.1},
            4: {"A": 0.1},
        }
    }
    calculator.config = type('Config', (), {'num_reels': 5})()

    # Probability of 3 A's in a row = 0.1 * 0.1 * 0.1 * 0.9 = 0.0009
    prob = calculator.calculate_symbol_hit_probability("TEST", "A", 3)

    expected = 0.1 * 0.1 * 0.1 * 0.9  # Three A's then not-A
    assert abs(prob - expected) < 0.0001, f"Probability should be {expected}, got {prob}"

    print("✅ test_hit_probability_calculation PASSED")


def run_all_tests():
    """Run all unit tests."""
    print("=" * 50)
    print("RTP CALCULATOR UNIT TESTS")
    print("=" * 50)
    print()

    tests = [
        test_symbol_probabilities,
        test_symbol_counts,
        test_volatility_high,
        test_volatility_low,
        test_hit_probability_calculation,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"❌ {test.__name__} FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"❌ {test.__name__} ERROR: {e}")
            failed += 1

    print()
    print("=" * 50)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("=" * 50)


if __name__ == "__main__":
    run_all_tests()