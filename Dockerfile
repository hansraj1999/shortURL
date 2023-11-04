ARG PYTHON_VERSION=3.11.1-alpine3.16
FROM python:$PYTHON_VERSION as builder
WORKDIR /

RUN apk add --no-cache g++
RUN mkdir -p /root/.ssh
RUN python -m venv .venv \
	&& .venv/bin/pip install --no-cache-dir -U pip==22.3.1
ADD requirements.txt .
RUN .venv/bin/pip install --no-cache-dir -r ./requirements.txt
COPY . /bithash/short_url

FROM python:$PYTHON_VERSION
WORKDIR /bithash/short_url


COPY --from=builder /bithash/short_url /bithash/short_url
COPY --from=builder /.venv /.venv
EXPOSE 80


ENV PATH="/.venv/bin:$PATH"
ENV PYTHONPATH /srv/avis/

ENTRYPOINT ["python3", "entrypoint.py"]
