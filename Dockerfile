# Build with: docker compose build   (the private framework is supplied as the "framework" build context, ../Project)
FROM python:3.12-slim-bookworm
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 PIP_DEFAULT_TIMEOUT=120

RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates gnupg \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && npm install -g @anthropic-ai/claude-code \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Framework: copy only what it needs (the full folder holds a multi-GB .venv and .git history)
COPY --from=framework pyproject.toml README.md requirements.txt /opt/omnicode/Project/
COPY --from=framework omnicode_core/ /opt/omnicode/Project/omnicode_core/
COPY --from=framework omnicode_host/ /opt/omnicode/Project/omnicode_host/
COPY --from=framework layer1-omnicode-mcp/ /opt/omnicode/Project/layer1-omnicode-mcp/
COPY --from=framework layer2-omnicode-spec/ /opt/omnicode/Project/layer2-omnicode-spec/
COPY --from=framework layer3-omnicode-gateway/ /opt/omnicode/Project/layer3-omnicode-gateway/
COPY --from=framework migrations/ /opt/omnicode/Project/migrations/
# Claude Code safety hooks: the host installs them into every run folder
COPY --from=framework plugins/omnicode-sdd-plugin/ /opt/omnicode/Project/plugins/omnicode-sdd-plugin/

WORKDIR /opt/omnicode/app
COPY requirements.txt .
# CPU-only PyTorch first: the default wheel bundles several GB of CUDA libraries a container cannot use.
RUN pip install --no-cache-dir --upgrade pip setuptools wheel \
    && pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu \
    && pip install --no-cache-dir -r requirements.txt
COPY . .

RUN useradd --create-home --uid 10001 omnicode \
    && mkdir -p /home/omnicode/.omnicode \
    && chown -R omnicode:omnicode /opt/omnicode /home/omnicode
USER omnicode
# `main.py ui` builds the symbol index on first start (the leak scanner fails closed without one)
CMD ["python", "main.py", "ui", "--host", "0.0.0.0", "--port", "8080"]
