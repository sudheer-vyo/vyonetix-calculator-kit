import unittest

from vyonetix_calc import cost_per_page, energy_cost, energy_kwh, rated_yield_months


class CalculationTests(unittest.TestCase):
    def test_energy_units_and_cost(self):
        self.assertEqual(energy_kwh(1000, 2), 2.0)
        self.assertAlmostEqual(energy_cost(1000, 2, 0.3), 0.6)
        self.assertEqual(energy_kwh(0, 24), 0.0)

    def test_yield_and_unit_cost(self):
        self.assertEqual(rated_yield_months(3000, 300), 10.0)
        self.assertEqual(cost_per_page(60, 3000), 0.02)

    def test_invalid_values_rejected(self):
        for args in [(-1, 1), (1, float("nan")), (1, float("inf"))]:
            with self.assertRaises(ValueError):
                energy_kwh(*args)
        with self.assertRaises(ValueError):
            rated_yield_months(3000, 0)
        with self.assertRaises(ValueError):
            cost_per_page(50, 0)
        with self.assertRaises(ValueError):
            energy_cost(1, 1, -0.1)


if __name__ == "__main__":
    unittest.main()
