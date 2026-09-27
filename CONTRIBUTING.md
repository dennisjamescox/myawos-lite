# Contributing

Keep MyAWOS Lite focused on its small supported hardware matrix. New weather
sources should implement a separate adapter returning `WeatherObservation`.
New relay or receiver types should not weaken startup/shutdown PTT safety.

Run before submitting a change:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -e .
python -m unittest discover -s tests -v
./scripts/build-deb.sh
```

Do not commit API keys, station credentials, generated weather files, audio
captures, exact private station locations, or live configuration files.
