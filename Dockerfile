FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /usr/src/app

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PATH="/usr/src/app/.venv/bin:$PATH"

# Install dependencies first, in their own layer, so source-only changes don't bust the cache
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-install-project --no-dev

# Now add the source and sync the project itself
COPY app.py ./
COPY src ./src
RUN uv sync --locked --no-dev

EXPOSE 5000

CMD ["uv", "run", "python", "app.py"]
