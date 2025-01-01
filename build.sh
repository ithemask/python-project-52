#!/usr/bin/env bash
uv run set -o errexit
make install-prod
make collectstatic
make migrate
