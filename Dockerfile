ARG ENV

FROM python:3.9-slim as base

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PATH="$PATH:$HOME/.local/bin"


FROM base AS python-deps

# Install pipenv and compilation dependencies
RUN pip install pipenv

# Install python dependencies
COPY Pipfile ./
COPY Pipfile.lock ./
RUN if test "x$ENV" = "xproduction"; then \
        PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy --ignore-pipfile; \
    else \
        PIPENV_VENV_IN_PROJECT=1 pipenv install --dev; \
    fi


FROM base AS runtime

# Copy virtual env from python-deps stage
COPY --from=python-deps /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

# Switch to code directory
WORKDIR /app

# Install application into container
COPY . .

# Configuration files
COPY conf/application.conf.py ./
COPY conf/gunicorn.conf.py ./
COPY entrypoint.sh ./

ENTRYPOINT ["./entrypoint.sh"]
