FROM python:3.11-bookworm as prod

RUN pip install poetry==1.8.3

RUN poetry config virtualenvs.create false

WORKDIR /src/reworkd/bananalyzer

ADD Makefile pyproject.toml poetry.lock README.md ./
ADD server/pyproject.toml server/poetry.lock ./server/
RUN make DEPS_INSTALL

# Prevent error regarding dubious ownership in repository
RUN git config --global --add safe.directory /src/reworkd/bananalyzer

CMD ["make", "DEV"]
