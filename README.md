# MyAWOS Lite

Website: <https://dennisjamescox.github.io/myawos-lite/>

MyAWOS has grown to include FAA weather cameras, runway-light operations, AWC
weather integration and other advanced features. MyAWOS Lite keeps the first
installation focused: five microphone clicks are detected by an Airspy, a USB
relay keys a conventional aviation radio, and the computer plays a
prerecorded-voice report built from the latest local weather observation.

No source-code editing is required. Users install one Ubuntu package and answer
a guided setup wizard.

This repository is intentionally a small subset of MyAWOS. It does not include
HackRF transmission, cloud modeling, forecasts, camera images, email reports,
GPIO, OLED displays, or SMS integrations.

## Supported first-release hardware

- Ubuntu 24.04 on an x86-64 mini PC or laptop
- Airspy Mini or Airspy R2 for receive-only click detection
- LCUS-1-style 5 V CH340 one-channel USB serial relay
- Dedicated USB audio adapter with an ALSA playback device
- Yaesu FTA-250L, FTA-450L, or FTA-550 using an SCU-42 adapter
- An isolated, DC-blocked, attenuated computer-audio-to-PJ-068 cable
- WeatherLink Live local data or Ecowitt cloud data

See [hardware.md](docs/hardware.md) before purchasing or connecting equipment.

## Install the package

The public installer is intended to be published at:

`https://github.com/dennisjamescox/myawos-lite/releases/latest/download/myawos-lite_0.1.1_all.deb`

Visitors can download a public GitHub Release asset without a GitHub account.
Ubuntu 24.04 must already be installed, and internet access is required while
`apt` downloads the package dependencies.

```bash
sudo apt install ./myawos-lite_0.1.1_all.deb
sudo myawos-lite setup
sudo myawos-lite doctor
```

The package installs with `transmitter.enabled = false`. It never keys the
radio merely because installation completed.

After the wiring and station authorization have been checked:

```bash
sudo myawos-lite enable-transmit --confirm
sudo systemctl enable --now myawos-lite
```

## Useful commands

```bash
sudo myawos-lite devices       # list Airspy, relay and ALSA devices
sudo myawos-lite doctor        # verify the installation
sudo myawos-lite generate      # fetch weather and build current.wav
sudo myawos-lite play-audio    # audio output only; never keys PTT
sudo myawos-lite relay-off     # send only the relay OFF command
sudo myawos-lite disable-transmit
sudo myawos-lite status
sudo systemctl status myawos-lite
sudo journalctl -u myawos-lite -f
```

## Build a Debian package

On Ubuntu with `dpkg-deb` installed:

```bash
./scripts/build-deb.sh
```

The package is written to `dist/`. Source installation is available through
`sudo ./scripts/install-source.sh`.

## Documentation

- [Installation and commissioning](docs/installation.md)
- [Hardware and purchasing list](docs/hardware.md)
- [Wiring and connections](docs/wiring.md)
- [Operation](docs/operation.md)
- [Troubleshooting](docs/troubleshooting.md)
- [Google Sites page content](site/google-sites-page.md)

## Safety and authorization

MyAWOS Lite controls a radio transmitter. The operator is responsible for
frequency authorization, station identification, RF exposure, antenna
installation, audio quality, and preventing harmful interference. Keep
transmission disabled until the relay, PTT release, audio level, antenna, and
receiver protection have been verified. Never test on an operational aviation
frequency without authorization.
