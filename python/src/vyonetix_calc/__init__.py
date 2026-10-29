"""Transparent, user-input engineering planning calculations."""

__version__ = "0.1.0"


def _nonnegative(value: float, label: str) -> float:
    import math
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value < 0:
        raise ValueError(f"{label} must be a finite number greater than or equal to zero")
    return float(value)


def _positive(value: float, label: str) -> float:
    value = _nonnegative(value, label)
    if value == 0:
        raise ValueError(f"{label} must be greater than zero")
    return value


def energy_kwh(watts: float, hours: float) -> float:
    return _nonnegative(watts, "watts") * _nonnegative(hours, "hours") / 1000.0


def energy_cost(watts: float, hours: float, tariff_per_kwh: float) -> float:
    return energy_kwh(watts, hours) * _nonnegative(tariff_per_kwh, "tariff_per_kwh")


def rated_yield_months(rated_pages: float, pages_per_month: float) -> float:
    return _positive(rated_pages, "rated_pages") / _positive(pages_per_month, "pages_per_month")


def cost_per_page(cartridge_cost: float, rated_pages: float) -> float:
    return _nonnegative(cartridge_cost, "cartridge_cost") / _positive(rated_pages, "rated_pages")
