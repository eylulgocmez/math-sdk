"""Unit tests for Reel Generator."""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from reel_generator.generator import ReelGenerator


def test_calculate_counts_basic():
    """Test that symbol counts are calculated correctly."""
    generator = ReelGenerator()
    generator.symbols = {
        "A": {"weight": 10},
        "B": {"weight": 20},
        "C": {"weight": 70}
    }
    generator.reel_length = 100

    counts = generator.calculate_counts()

    assert counts["A"] == 10, f"A should be 10, got {counts['A']}"
    assert counts["B"] == 20, f"B should be 20, got {counts['B']}"
    assert counts["C"] == 70, f"C should be 70, got {counts['C']}"
    assert sum(counts.values()) == 100, f"Total should be 100, got {sum(counts.values())}"

    print("✅ test_calculate_counts_basic PASSED")


def test_calculate_counts_with_override():
    """Test that weight override works correctly."""
    generator = ReelGenerator()
    generator.symbols = {
        "A": {"weight": 10},
        "B": {"weight": 90}
    }
    generator.reel_length = 100

    # Without override: A=10%, B=90%
    counts_normal = generator.calculate_counts()

    # Override A from 10 to 50
    # New ratio: A=50, B=90 → A=36%, B=64%
    counts_override = generator.calculate_counts(weight_override={"A": 50})

    # A should be MORE than before
    assert counts_override["A"] > counts_normal["A"], \
        f"A with override ({counts_override['A']}) should be more than without ({counts_normal['A']})"

    # Total should still be 100
    assert sum(counts_override.values()) == 100, \
        f"Total should be 100, got {sum(counts_override.values())}"

    print("✅ test_calculate_counts_with_override PASSED")

def test_check_adjacent_allows():
    """Test that adjacent check allows valid placements."""
    generator = ReelGenerator()
    generator.symbols = {
        "A": {"weight": 10, "max_adjacent": 3}
    }

    # Reel with 2 A's at the end
    reel = ["B", "B", "A", "A"]

    # Should allow 3rd A (max_adjacent is 3)
    result = generator.check_adjacent(reel, "A", len(reel))
    assert result == True, "Should allow 3rd A when max_adjacent is 3"

    print("✅ test_check_adjacent_allows PASSED")


def test_check_adjacent_blocks():
    """Test that adjacent check blocks invalid placements."""
    generator = ReelGenerator()
    generator.symbols = {
        "A": {"weight": 10, "max_adjacent": 2}
    }

    # Reel with 2 A's at the end
    reel = ["B", "B", "A", "A"]

    # Should NOT allow 3rd A (max_adjacent is 2)
    result = generator.check_adjacent(reel, "A", len(reel))
    assert result == False, "Should block 3rd A when max_adjacent is 2"

    print("✅ test_check_adjacent_blocks PASSED")


def test_generate_reel_length():
    """Test that generated reel has correct length."""
    generator = ReelGenerator()
    generator.symbols = {
        "A": {"weight": 30},
        "B": {"weight": 70}
    }
    generator.reel_length = 100

    counts = generator.calculate_counts()
    reel = generator.generate_reel(counts)

    assert len(reel) == 100, f"Reel length should be 100, got {len(reel)}"

    print("✅ test_generate_reel_length PASSED")


def test_generate_reel_contains_all_symbols():
    """Test that generated reel contains all symbols."""
    generator = ReelGenerator()
    generator.symbols = {
        "A": {"weight": 10},
        "B": {"weight": 20},
        "C": {"weight": 70}
    }
    generator.reel_length = 100

    counts = generator.calculate_counts()
    reel = generator.generate_reel(counts)

    unique_symbols = set(reel)
    assert "A" in unique_symbols, "Reel should contain A"
    assert "B" in unique_symbols, "Reel should contain B"
    assert "C" in unique_symbols, "Reel should contain C"

    print("✅ test_generate_reel_contains_all_symbols PASSED")


def test_generate_all_reels_count():
    """Test that correct number of reels are generated."""
    generator = ReelGenerator()
    generator.symbols = {
        "A": {"weight": 50},
        "B": {"weight": 50}
    }
    generator.reel_length = 50
    generator.num_reels = 5

    reels = generator.generate_all_reels()

    assert len(reels) == 5, f"Should generate 5 reels, got {len(reels)}"

    print("✅ test_generate_all_reels_count PASSED")


def run_all_tests():
    """Run all unit tests."""
    print("=" * 50)
    print("REEL GENERATOR UNIT TESTS")
    print("=" * 50)
    print()

    tests = [
        test_calculate_counts_basic,
        test_calculate_counts_with_override,
        test_check_adjacent_allows,
        test_check_adjacent_blocks,
        test_generate_reel_length,
        test_generate_reel_contains_all_symbols,
        test_generate_all_reels_count,
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