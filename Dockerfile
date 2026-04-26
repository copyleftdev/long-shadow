# farmwatch — single-image deployment of the three watcher tools
#
# Build:    docker build -t farmwatch:latest .
# Run:      see docker-compose.yml in the same directory
#
# The image runs supercronic (cron alternative that logs to stdout, suitable for
# containers) on a fixed schedule. State is persisted to a volume mounted at /state.
# All three watchers exit 1 when they have NEW findings; the entrypoint posts the
# state file's `alerts` array to $WEBHOOK_URL when that happens.

FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DEBIAN_FRONTEND=noninteractive

# git for repo cloning, curl for webhook posts, ca-certificates for HTTPS, tini as init.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        git ca-certificates curl tini jq && \
    rm -rf /var/lib/apt/lists/*

# supercronic — cron without the systemd nonsense, logs go to stdout.
ARG SUPERCRONIC_VERSION=v0.2.30
ARG SUPERCRONIC_SHA1SUM=9aeb41e00cc7b71d30d33c57a2333f2c2581a201
RUN curl -fsSLO "https://github.com/aptible/supercronic/releases/download/${SUPERCRONIC_VERSION}/supercronic-linux-amd64" && \
    echo "${SUPERCRONIC_SHA1SUM}  supercronic-linux-amd64" | sha1sum -c - && \
    chmod +x supercronic-linux-amd64 && \
    mv supercronic-linux-amd64 /usr/local/bin/supercronic

# Single Python dep
RUN pip install --no-cache-dir requests==2.32.3

WORKDIR /opt/farmwatch
# Copy the tool surface area only — leave /state empty for volume mount
COPY tools/ ./tools/
COPY catalog/ ./catalog/
COPY evidence/wallet_addresses/baseline.txt ./evidence/wallet_addresses/baseline.txt
COPY scripts/ ./scripts/
COPY docker/crontab ./crontab
COPY docker/entrypoint.sh ./entrypoint.sh
COPY docker/run-and-alert.sh ./run-and-alert.sh
RUN chmod +x ./entrypoint.sh ./run-and-alert.sh ./tools/*.py

# Non-root user for everything except git clones into /state (which it owns)
RUN useradd -m -u 10001 -s /usr/sbin/nologin farmwatch && \
    mkdir -p /state && chown -R farmwatch:farmwatch /state /opt/farmwatch
USER farmwatch

VOLUME ["/state"]

ENTRYPOINT ["/usr/bin/tini", "--", "/opt/farmwatch/entrypoint.sh"]
