# ---- builder ----
FROM docker.m.daocloud.io/python:3.14-alpine AS builder

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_PYTHON_DOWNLOADS=never
ENV UV_NO_DEV=1
ENV UV_NO_INSTALL_PROJECT=1

# Install uv tool
COPY --from=ghcr.m.daocloud.io/astral-sh/uv:0.12.13 /uv /usr/local/bin/uv

# Download dependencies by use cache layer(exclude dev dependencies)
COPY pyproject.toml uv.lock ./

# ---- uv / pip cache ----
#RUN --mount=type=cache,target=/root/.cache/uv \
#    --mount=type=cache,target=/root/.cache/pip \
#    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
#    --mount=type=bind,source=uv.lock,target=uv.lock \
RUN uv sync --locked

# Copy source code(exclude dev dependencies)
COPY ./ ./
#RUN --mount=type=cache,target=/root/.cache/uv \
#    --mount=type=cache,target=/root/.cache/pip \
RUN uv sync --locked

# ---- build app ----
FROM docker.m.daocloud.io/python:3.14-alpine

WORKDIR /app

# Add virtualenv to PATH so uvicorn can find the packages
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
# No need to download python packages in production
ENV UV_PYTHON_DOWNLOADS=never

COPY --from=builder /app /app

EXPOSE 8000

RUN apk add --no-cache tini

# Use tini as init process
ENTRYPOINT ["/sbin/tini", "--"]

# Use uvicorn run asgi server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
