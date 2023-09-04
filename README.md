# proc-watch

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

## Prometheus exporting
The current method writes to a text file, the default path is `/tmp/proc_watch.prom`:

```sh
less /tmp/proc_watch.prom
```
