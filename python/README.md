# Vyonetix Calc Kit (Python)

Small dependency-free CLI for transparent energy-cost and consumable-yield scenarios.

## Install

```console
python -m pip install vyonetix-calc-kit
```

## Example

```console
vyonetix-calc energy --watts 100 --hours 8 --tariff-per-kwh 0.30
vyonetix-calc yield --rated-pages 3000 --pages-per-month 300
vyonetix-calc cost-per-page --cartridge-cost 60 --rated-pages 3000
```

The command prints machine-readable JSON to standard output. Inputs are provided by the caller. The calculations do not read device telemetry, certify product compatibility, or report live prices or inventory.

## Related interactive tools

- [Vyonetix electricity cost tool](https://deals.vyonetixsolutions.com.au/tools/electricity-cost/)
- [Vyonetix printer supplies finder](https://deals.vyonetixsolutions.com.au/tools/printer-supply-toolbox/)
- [Public tools RSS feed](https://deals.vyonetixsolutions.com.au/tools/tools-rss.xml)

Some website pages contain clearly disclosed affiliate links. The package itself has no retailer tracking, network calls, analytics, or automatic affiliate redirects.

## License

MIT. See the repository license. Third-party brand names are descriptive only; no manufacturer endorsement is implied.
