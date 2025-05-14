import pytest
from helper import compute_p_total

@pytest.mark.parametrize("p_step, n, expected", [
    (80, 2, 64.0),                          # 0.8^2 * 100 = 64.0
    (85, 3, 61.412),                        # 0.85^3 * 100 ≈ 61.412
    (99.9, 56, pytest.approx(94.551, rel=1e-3)),  # from actual calculation
    ("invalid", 56, "Invalid"),
    (99, "oops", "Invalid"),
    (0, 5, 0.0),
])
def test_compute_p_total(p_step, n, expected):
    result = compute_p_total(p_step, n)
    assert result == expected