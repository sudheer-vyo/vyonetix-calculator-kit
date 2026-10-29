# Developer distribution status

Updated 2026-10-29. This repository contains useful source packages and a machine-readable formula catalog. Package-index listing is a separate action from publishing this Git repository.

| Channel | Package | State |
|---|---|---|
| GitHub | `sudheer-vyo/vyonetix-calculator-kit` | Public repository; source update to be published in this commit |
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
