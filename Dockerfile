FROM python:3.11-bookworm as prod

RUN pip install poetry==1.8.3

RUN poetry config virtualenvs.create false

WORKDIR /src/reworkd/bananalyzer

ADD Prebuild.mk pyproject.toml poetry.lock README.md ./
ADD server/pyproject.toml server/poetry.lock ./server/
RUN make -f Prebuild.mk DEPS_INSTALL
ADD Makefile ./

# Prevent error regarding dubious ownership in repository
RUN git config --global --add safe.directory /src/reworkd/bananalyzer

CMD ["make", "DEV"]
