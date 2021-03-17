FROM python:3.8-slim as base

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

ENV PATH="$PATH:$HOME/.local/bin"

# Switch to code directory
WORKDIR /app


FROM base AS python-deps

# Install pipenv and compilation dependencies
RUN pip install pipenv

# Install python dependencies
COPY Pipfile ./
COPY Pipfile.lock ./
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy --ignore-pipfile


FROM base AS runtime

# Copy virtual env from python-deps stage
COPY --from=python-deps /app/.venv /.venv
ENV PATH="/.venv/bin:$PATH"

# Install application into container
COPY . .

# Configuration files
COPY conf/application.conf.py ./
COPY conf/gunicorn.conf.py ./
COPY entrypoint.sh ./

RUN ls -la
ENTRYPOINT ["./entrypoint.sh"]
