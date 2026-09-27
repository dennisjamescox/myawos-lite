from __future__ import annotations

import os
import tomllib
from pathlib import Path
from typing import Any


DEFAULT_CONFIG = Path(os.environ.get("MYAWOS_LITE_CONFIG", "/etc/myawos-lite/config.toml"))


def load_config(path: Path = DEFAULT_CONFIG) -> dict[str, Any]:
    with path.open("rb") as handle:
        config = tomllib.load(handle)
    required = ("station", "radio", "receiver", "transmitter", "weather", "paths")
    missing = [section for section in required if section not in config]
    if missing:
        raise ValueError(f"Missing configuration sections: {', '.join(missing)}")
    return config


def state_path(config: dict[str, Any], name: str) -> Path:
    return Path(config["paths"]["state_directory"]) / name
