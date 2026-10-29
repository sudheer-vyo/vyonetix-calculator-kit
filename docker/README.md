# Container image build

This repository includes a Dockerfile for the generic, offline Python planning CLI. Build locally from the repository root:

```console
docker build -f docker/Dockerfile -t vyonetix-calc:0.1.0 .
docker run --rm vyonetix-calc:0.1.0 energy --watts 100 --hours 8 --tariff-per-kwh 0.30
```

The image is not published to Docker Hub yet. A public Docker Hub namespace and authorized publisher login/token are required before push. The CLI contains no credentials, analytics, retailer lookup, or automatic network traffic.
