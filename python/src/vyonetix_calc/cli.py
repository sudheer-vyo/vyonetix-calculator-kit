"""Command-line interface that emits a single JSON result."""
import argparse
import json
import sys

from . import cost_per_page, energy_cost, energy_kwh, rated_yield_months


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="vyonetix-calc", description="Generic user-input hardware planning estimates")
    commands = root.add_subparsers(dest="command", required=True)
    energy = commands.add_parser("energy", help="estimate energy and cost from watts, hours and tariff")
    energy.add_argument("--watts", type=float, required=True)
    energy.add_argument("--hours", type=float, required=True)
    energy.add_argument("--tariff-per-kwh", type=float, required=True)
    yield_cmd = commands.add_parser("yield", help="estimate rated yield duration from user inputs")
    yield_cmd.add_argument("--rated-pages", type=float, required=True)
    yield_cmd.add_argument("--pages-per-month", type=float, required=True)
    cpp = commands.add_parser("cost-per-page", help="divide supplied cartridge cost by rated pages")
    cpp.add_argument("--cartridge-cost", type=float, required=True)
    cpp.add_argument("--rated-pages", type=float, required=True)
    return root


def main() -> int:
    args = parser().parse_args()
    try:
        if args.command == "energy":
            result = {"calculation": args.command, "energy_kwh": energy_kwh(args.watts, args.hours),
                      "estimated_cost": energy_cost(args.watts, args.hours, args.tariff_per_kwh),
                      "currency": "currency units from supplied tariff"}
        elif args.command == "yield":
            result = {"calculation": args.command,
                      "estimated_months": rated_yield_months(args.rated_pages, args.pages_per_month),
                      "limitation": "Rated yield scenario only; not measured remaining toner."}
        else:
            result = {"calculation": args.command,
                      "cost_per_page": cost_per_page(args.cartridge_cost, args.rated_pages),
                      "currency": "currency units from supplied cartridge cost"}
        print(json.dumps(result, separators=(",", ":")))
        return 0
    except ValueError as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
