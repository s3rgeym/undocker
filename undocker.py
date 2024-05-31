#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from functools import partial
from pathlib import Path

DEFAULT_CONFIG_PATH = Path("/etc/docker/daemon.json")

CSI = "\x1b["
RESET = CSI + "0m"
RED = CSI + "31m"
GREEN = CSI + "32m"
YELLOW = CSI + "33m"
BLUE = CSI + "34m"
PURPLE = CSI + "35m"

DOCKER_REGISTRY_MIRRORS = [
    # "https://dockerhub.timeweb.cloud",
    # "http://hub-mirror.c.163.com",
    # "https://docker.mirrors.ustc.edu.cn",
    "https://daocloud.io",
    "https://c.163.com/",
    "https://registry.docker-cn.com",
    "https://mirror.gcr.io",
    "https://huecker.io",
]

print = partial(print, file=sys.stderr, flush=True)


parser = argparse.ArgumentParser()
parser.add_argument(
    "-c", "--config-path", "--config", type=Path, default=DEFAULT_CONFIG_PATH
)


def main(argv=None):
    args = parser.parse_args(argv)

    config_path = args.config_path

    try:
        if config_path.exists():
            with config_path.open() as fp:
                config = json.load(fp)
        else:
            config = {}

        config.update(
            {
                "registry-mirrors": sorted(DOCKER_REGISTRY_MIRRORS)
            }
        )

        config_path.write_text(
            json.dumps(config, ensure_ascii=True, indent=2, sort_keys=True)
        )

        print(GREEN + "Config succcessfully updated" + RESET)

        subprocess.check_call(["systemctl", "restart", "docker"])

        print(GREEN + "Docker restarted" + RESET)
    except Exception as ex:
        print(RED + "Error:", str(ex) + RESET)
        return 1


if __name__ == "__main__":
    sys.exit(main())
