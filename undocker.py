#!/usr/bin/env python3
import argparse
import json
import subprocess
from pathlib import Path

DEFAULT_CONFIG_PATH = Path("/etc/docker/daemon.json")
parser = argparse.ArgumentParser()
parser.add_argument(
    "-c", "--config-path", "--config", type=Path, default=DEFAULT_CONFIG_PATH
)

if __name__ == "__main__":
    args = parser.parse_args()

    config_path = args.config_path

    if config_path.exists():
        with config_path.open() as fp:
            config = json.load(fp)
    else:
        config = {}

    config.update(
        {
            "registry-mirrors": [
                # "https://dockerhub.timeweb.cloud",
                "https://daocloud.io",
                "https://c.163.com/",
                "https://registry.docker-cn.com",
                "https://mirror.gcr.io",
                "https://huecker.io",
            ]
        }
    )

    config_path.write_text(
        json.dumps(config, ensure_ascii=True, indent=2, sort_keys=True)
    )

    subprocess.check_call(["systemctl", "restart", "docker"])
