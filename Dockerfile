FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /usr/src/app

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PATH="/usr/src/app/.venv/bin:$PATH"

# Install dependencies first, in their own layer, so source-only changes don't bust the cache
COPY interview-tuition-api/pyproject.toml interview-tuition-api/uv.lock ./
RUN uv sync --locked --no-install-project --no-dev

# Now add the source and sync the project itself
COPY interview-tuition-api/app.py ./
COPY interview-tuition-api/src ./src
RUN uv sync --locked --no-dev

EXPOSE 5000

CMD ["uv", "run", "python", "app.py"]
