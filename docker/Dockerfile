# Multistage Docker image for Poetry
# Requires Docker 17.05 or higher
# See https://docs.docker.com/develop/develop-images/multistage-build/
# See https://github.com/python-poetry/poetry/issues/1879

######################### PYTHON-BASE #######################################
# Provides python and libraries for building packages

FROM python:3.10.6-slim as python-base
ENV PYTHON_MAJOR_VERSION="3.10.6" \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_NO_INTERACTION=1 \
    APP_PATH="/app" \
    VENV_PATH="/venv" \
    PACKAGE_ROOT="objectdetection"

# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

WORKDIR $APP_PATH

######################### BUILDER #######################################
# Provides virtual environment with runtime dependencies to build the project
# Uses python venv to create the virtual environment and poetry to mangage project dependencies

FROM python-base as builder
RUN apt-get update  && apt-get install --no-install-recommends -y \
        curl \
        build-essential

# Install last Poetry version, respects $POETRY_HOME
RUN curl -sSL https://install.python-poetry.org | python3 -

# Copy dependencies
COPY ./poetry.lock ./pyproject.toml ./
# Create virtual environment
RUN python -m venv $VENV_PATH
# Install runtime dependencies (--only main), but exclude the project itself (--no-root), which avoids editable mode
RUN . $VENV_PATH/bin/activate && poetry install --only main --no-root

########################## DISTRIBUTION ########################################
# Provides a built-package of our app (a `wheel`), ready for distribution

FROM builder as distribution

# Copy poetry and venv
COPY --from=builder $POETRY_HOME $POETRY_HOME
COPY --from=builder $VENV_PATH $VENV_PATH

# Copy full project and build it (generate distribution files in /app/dist)
COPY . .
RUN . $VENV_PATH/bin/activate && poetry build


########################### PRODUCTION #########################################
# Provides a production ready image

FROM python-base as production

# Copy venv and project distribution files and entrypoint
COPY --from=builder $VENV_PATH $VENV_PATH
COPY --from=distribution $APP_PATH/dist .

# Copy entrypoint & give execution permission
COPY docker/entrypoint.sh /
RUN chmod +x /entrypoint.sh

# Install just the wheels
RUN . $VENV_PATH/bin/activate && pip install *.whl

ENV PYTHONPATH=${PYTHONPATH}:$VENV_PATH/lib/python$PYTHON_MAJOR_VERSION/site-packages/$PACKAGE_ROOT
ENTRYPOINT /entrypoint.sh $0 $@
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "80"]

