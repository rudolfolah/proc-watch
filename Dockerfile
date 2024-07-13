FROM python:3.12-bookworm
COPY . /src/proc_watch
WORKDIR /src/proc_watch
RUN pip install --no-cache-dir -r requirements.txt
ENTRYPOINT ["python", "main.py"]
