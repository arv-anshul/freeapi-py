# https://dev.to/kummerer94/multi-stage-docker-builds-for-pyton-projects-using-uv-223g

FROM python:3.11-slim as build

WORKDIR /app

ENV VIRTUAL_ENV=/home/packages/.venv

RUN pip install -U pip uv
COPY requirements.lock .
RUN uv venv /home/packages/.venv && uv pip install --no-cache -r requirements.lock

# Activate the virtualenv in the container
# https://pythonspeed.com/articles/multi-stage-docker-python/
ENV PATH="/home/packages/.venv/bin:$PATH"

COPY . .

CMD ["uvicorn", "freeapi.app:app", "--host", "0.0.0.0", "--port", "8000"]
