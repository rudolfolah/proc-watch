# proc-watch

![License Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue)
![Python](https://img.shields.io/badge/Python-green)
![Prometheus](https://img.shields.io/badge/Prometheus-orange)

`proc-watch` is a tool for monitoring processes and logging their CPU and memory usage.

Copyright (C) 2023 Rudolf Olah

Licensed under Apache 2.0 license

## Local Dev

```bash
pyenv local
python -m venv .venv --prompt .
source .venv/bin/activate
pip install -r requirements.txt
```

## [Prometheus exporting](https://github.com/prometheus/client_python)
The current method writes to a text file, the default path is `/tmp/proc_watch.prom`:

```sh
less /tmp/proc_watch.prom
```

## Docker

Build the image:

```sh
docker build -t proc-watch:latest .
```

Run it:

```sh
docker run -it --rm proc-watch:latest --pid=host
```
