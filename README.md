# Vyonetix calculator kit

Small dependency-free JavaScript planning functions and an embeddable electricity-use widget. The widget computes locally, displays an estimate immediately and lets a visitor deliberately open the fuller Vyonetix tool.

## JavaScript library

Install from npm when the package release is available:

```console
npm install vyonetix-calculator-kit
```

```js
import { energyKWh, energyCost, ratedYieldMonths, costPerPage } from 'vyonetix-calculator-kit';
```

The package exposes the user-input calculations at its root and the optional web component at `vyonetix-calculator-kit/widget`.

## Use the functions

```js
import { energyKWh, energyCost, ratedYieldMonths, costPerPage } from './calculations.mjs';
energyKWh(1000, 2);                 // 2 kWh
energyCost(1000, 2, 0.30);          // 0.60 in your tariff's currency
ratedYieldMonths(3000, 300);        // 10 months, based only on entered rated yield
costPerPage(60, 3000);              // 0.02 per page in your entered currency
```

Inputs must be finite numbers. Negative inputs and zero denominators raise `RangeError`. Toner calculations are simple workload scenarios: rated yield is not measured remaining toner, and actual output varies with the printing conditions. No device compatibility, live stock or electrical safety is inferred.

## Embed

Place the two module files on your own reviewed HTTPS host, then use:

```html
<script type="module" src="./energy-widget.mjs"></script>
<vyonetix-energy></vyonetix-energy>
```

For a local demonstration, serve this folder with `python -m http.server 8783 --bind 127.0.0.1`, then open `http://127.0.0.1:8783/demo.html`. JavaScript modules require HTTP/HTTPS rather than opening a local file directly.

## Formulas

- Energy (kWh) = power (W) × operating time (hours) / 1000.
- Cost = energy (kWh) × entered cost per kWh.
- Yield scenario (months) = entered rated page yield / entered monthly page count.
- Cost per page = entered cartridge cost / entered page yield.

Use measured power and your own tariff. Defaults are example inputs. This is a planning aid and does not read appliance or printer telemetry.

## Python CLI and JSON definitions

The [`python/`](python/) folder contains an installable Python CLI that returns JSON, and [`datasets/calculations-v1.json`](datasets/calculations-v1.json) documents the formulas and units in a machine-readable format. Install the Python package from PyPI when its release is published:

```console
python -m pip install vyonetix-calc-kit
vyonetix-calc energy --watts 100 --hours 8 --tariff-per-kwh 0.30
```

The [`docker/`](docker/) folder contains a Dockerfile and build instructions. The image is not published yet; it requires the owner's Docker Hub namespace and login before push.

## Validation

Run `npm test` with a maintained Node.js release supporting `node:test`. No dependency install is required. The tests cover unit calculations, zero load, invalid values and denominators. Browser/mobile/accessibility review has not yet been completed; report reproducible issues without serial numbers or personal information.

## Vyonetix tools and updates

- [Electricity tool](https://deals.vyonetixsolutions.com.au/tools/electricity-cost/)
- [Printer supplies finder](https://deals.vyonetixsolutions.com.au/tools/printer-supply-toolbox/)
- [Tools RSS feed](https://deals.vyonetixsolutions.com.au/tools/feed.xml)

The widget's optional link opens Vyonetix. Some website pages include disclosed affiliate links; a purchase is optional. This package contains no retailer content, images, API keys, analytics, push requests or automatic redirects.

## License

Original code in this repository is available under the MIT license. Third-party trademarks and materials are not licensed by this repository. No manufacturer endorsement is implied.
