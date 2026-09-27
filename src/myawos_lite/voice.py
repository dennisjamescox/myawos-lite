from __future__ import annotations

import json
import os
import tempfile
import wave
from datetime import timezone
from pathlib import Path
from typing import Iterable

from .models import WeatherObservation


def _number_tokens(value: int | str, altimeter: bool = False) -> list[str]:
    text = str(value)
    tokens: list[str] = []
    if text.startswith("-"):
        tokens.append("minus")
        text = text[1:]
    for character in text:
        if character.isdigit():
            tokens.append(character)
        elif character == "." and not altimeter:
            tokens.append("point")
    return tokens


def announcement_tokens(observation: WeatherObservation) -> list[str]:
    zulu = observation.observed_at.astimezone(timezone.utc).strftime("%H%M")
    direction = f"{observation.wind_direction_deg:03d}"
    altimeter = f"{observation.altimeter_inhg:.2f}".replace(".", "")
    tokens = ["intro", *_number_tokens(zulu), "zulu", "wind", *_number_tokens(direction)]
    tokens += ["at", *_number_tokens(observation.wind_speed_kt), "knot"]
    if observation.wind_gust_kt > observation.wind_speed_kt:
        tokens += ["gusts", *_number_tokens(observation.wind_gust_kt), "knot"]
    tokens += ["altimeter", *_number_tokens(altimeter, altimeter=True)]
    tokens += ["temp", *_number_tokens(observation.temperature_c)]
    tokens += ["dewpoint", *_number_tokens(observation.dewpoint_c)]
    return tokens


def _clip_path(media_dir: Path, token: str) -> Path:
    return media_dir / f"WeatherStation_{token}.wav"


def build_announcement(observation: WeatherObservation, media_dir: Path, output: Path) -> list[str]:
    tokens = announcement_tokens(observation)
    clips = [_clip_path(media_dir, token) for token in tokens]
    missing = [str(path) for path in clips if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"Missing voice clips: {', '.join(sorted(set(missing)))}")

    output.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary_name = tempfile.mkstemp(prefix=".current-", suffix=".wav", dir=output.parent)
    os.close(fd)
    temporary = Path(temporary_name)
    try:
        with wave.open(str(clips[0]), "rb") as first:
            parameters = first.getparams()
            audio_format = (first.getnchannels(), first.getsampwidth(), first.getframerate(), first.getcomptype())
        with wave.open(str(temporary), "wb") as destination:
            destination.setnchannels(parameters.nchannels)
            destination.setsampwidth(parameters.sampwidth)
            destination.setframerate(parameters.framerate)
            destination.setcomptype(parameters.comptype, parameters.compname)
            for clip in clips:
                with wave.open(str(clip), "rb") as source:
                    source_format = (
                        source.getnchannels(), source.getsampwidth(), source.getframerate(), source.getcomptype()
                    )
                    if source_format != audio_format:
                        raise ValueError(f"Voice clip format mismatch: {clip}")
                    destination.writeframes(source.readframes(source.getnframes()))
        os.replace(temporary, output)
    finally:
        temporary.unlink(missing_ok=True)
    return tokens


def write_observation(observation: WeatherObservation, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix(output.suffix + ".tmp")
    temporary.write_text(json.dumps(observation.to_dict(), indent=2) + "\n", encoding="utf-8")
    os.replace(temporary, output)
