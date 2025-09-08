FROM python:3.12-bookworm

RUN apt-get update && apt-get install -y procps && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

ENV RUN_IN_SHELL=false
ENV PROM_EXPORT_PATH=/app/metrics/proc_watch.prom

RUN mkdir -p /app/metrics

CMD ["sh", "-c", "while true; do python main.py; sleep 60; done"]

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD test -f /app/metrics/proc_watch.prom && test "$(find /app/metrics/proc_watch.prom -mmin -2)" || exit 1
