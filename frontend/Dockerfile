FROM python:3.12-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:0.7 /uv /usr/local/bin/uv

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --no-dev --no-install-project --frozen

COPY main.py .

RUN uv sync --no-dev --frozen


FROM python:3.12-slim

RUN addgroup --system --gid 1001 appgroup && \
    adduser --system --uid 1001 --ingroup appgroup appuser

WORKDIR /app

COPY --from=builder --chown=appuser:appgroup /app/.venv /app/.venv
COPY --chown=appuser:appgroup main.py .
COPY --chown=appuser:appgroup templates/ templates/

ENV PATH="/app/.venv/bin:$PATH"

USER appuser

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:3000/')" || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"]
