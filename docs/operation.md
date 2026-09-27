# Operation

At startup MyAWOS Lite sends the relay OFF command, starts a weather-refresh
worker, calibrates the Airspy noise floor, and listens for the configured click
sequence. Weather and audio files are atomically replaced in
`/var/lib/myawos-lite`, so a transmission never reads a partially generated file.

After a valid request, the service stops Airspy sampling, closes PTT, waits for
the radio to key, plays the current announcement, opens PTT, restarts Airspy,
and recalibrates. Accepted requests are recorded in `requests.jsonl`.

## Routine checks

```bash
sudo systemctl status myawos-lite
sudo myawos-lite doctor
sudo journalctl -u myawos-lite --since today
```

## Disable transmission immediately

```bash
sudo systemctl stop myawos-lite
sudo myawos-lite relay-off
sudo myawos-lite disable-transmit
```

## Updating

```bash
sudo apt install ./myawos-lite_NEW_VERSION_all.deb
sudo myawos-lite doctor
sudo systemctl restart myawos-lite
```

Package upgrades preserve the operator configuration and state directory.
