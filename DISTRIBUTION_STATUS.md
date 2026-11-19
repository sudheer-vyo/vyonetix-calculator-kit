# Developer distribution status

Updated 2026-11-19. This repository contains useful source packages and a machine-readable formula catalog. Package-index listing is a separate action from publishing this Git repository.

| Channel | Package | State |
|---|---|---|
| GitHub | `sudheer-vyo/vyonetix-calculator-kit` | Public repository; source update published in commit [`5fe7f2a`](https://github.com/sudheer-vyo/vyonetix-calculator-kit/commit/5fe7f2a580c7543b7e004d02e2f9ef36773c0d6d) on 2026-10-29 |
| npm | `vyonetix-calculator-kit@0.2.0` | Package built and name endpoint returned HTTP 404 (not found) on 2026-10-29, consistent with an available name; not uploaded because npm CLI is not authenticated |
| PyPI | `vyonetix-calc-kit==0.1.0` | Wheel built and name endpoint returned HTTP 404 (not found) on 2026-10-29, consistent with an available name; not uploaded because no PyPI publisher credential/trusted publisher is configured |
| Docker Hub | proposed `vyonetix-calc-kit` | Dockerfile prepared; Docker CLI/daemon and Docker Hub credential are not configured, so image was not built or uploaded |

## Commands after registry accounts are configured

From the repository root:

```console
npm publish --access public
python -m pip install build twine
python -m build --wheel ./python
python -m twine check python/dist/*
python -m twine upload python/dist/*
docker build -f docker/Dockerfile -t <your-dockerhub-namespace>/vyonetix-calc-kit:0.1.0 .
docker push <your-dockerhub-namespace>/vyonetix-calc-kit:0.1.0
```

Do not place tokens in this repository. Use each registry's secure login or trusted-publisher mechanism. Check package name ownership immediately before first publication; a prior 404 is a dated observation, not a permanent reservation. Docker namespace must be the account owner controls.

These platforms provide package discovery and reuse, not guaranteed impressions, installs, website traffic, subscribers, or affiliate revenue. The package calculations are generic and offline; user values are not submitted to Vyonetix.

## 2026-11-19 Vyonetix browser-tool directory

The public repository now includes a generated directory of 44 live Vyonetix browser-tool links, a JSON catalogue, and three original engineering walkthroughs for SFP optical margin, constant-power PoE cable drop, and uncompressed video bandwidth. The catalogue is a web-page directory, not an OpenAPI service. It contains no retailer links, prices, inventory or deal feed. The walkthroughs use hypothetical examples and cite manufacturer/standards sources. The three existing package tests passed locally before publication. No GitHub view, site visit, affiliate click or sale is attributed to this update; measure those from the respective platform reports.
