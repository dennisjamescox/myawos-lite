# Google Sites page: MyAWOS Lite

This file is the copy-and-paste content plan for a new page under **myawos.com**.
In Google Sites, create a page named **MyAWOS Lite**, use the section order
below, upload `docs/wiring.svg` as the connection diagram, and replace the
placeholder download links after the GitHub repository is published.

---

## Hero section

### MyAWOS Lite

**Request-driven weather radio without a Raspberry Pi or custom transmitter.**

MyAWOS Lite uses an Airspy receiver to detect five microphone clicks, retrieves
current conditions from a supported weather station, and keys a conventional
aviation radio through a USB relay to speak the report in a consistent
prerecorded voice.

Buttons:

- **Download for Ubuntu** → GitHub Releases `.deb`
- **View source code** → GitHub repository
- **Installation guide** → page anchor or published documentation

## What it does

- Continuously receives the selected aviation frequency with Airspy Mini/R2.
- Detects five valid clicks inside a configurable time window.
- Retrieves WeatherLink Live or Ecowitt weather observations.
- Builds the spoken report locally from recorded voice clips.
- Keys a Yaesu radio using an isolated USB-relay contact.
- Plays audio through a dedicated USB sound adapter.
- Releases PTT, restarts the receiver, and recalibrates automatically.

## What you need

- Ubuntu 24.04 computer
- Airspy Mini or Airspy R2
- 5 V LCUS-1 CH340 USB relay
- USB audio adapter
- Yaesu FTA-250L, FTA-450L or FTA-550 with SCU-42
- Isolated and attenuated 3.5 mm-to-PJ-068 audio interface
- Suitable receive and transmit antennas
- WeatherLink Live or Ecowitt weather station

Add a link labeled **Full hardware list** to `docs/hardware.md` after the
documentation is hosted.

## How it connects

Upload and insert `docs/wiring.svg` at full width.

Caption:

> The Airspy is receive-only. The USB relay provides a dry PTT contact, while a
> separate USB audio adapter supplies isolated and attenuated microphone audio
> to the radio through the SCU-42.

## Three-step installation

### 1. Install

```text
sudo apt install ./myawos-lite_0.1.0_all.deb
sudo myawos-lite setup
```

### 2. Verify

```text
sudo myawos-lite doctor
sudo myawos-lite generate
sudo myawos-lite play-audio
sudo myawos-lite relay-off
```

These checks do not key the radio.

### 3. Commission

After verifying wiring, antenna protection, audio quality, station authority
and fail-safe PTT release, run `sudo myawos-lite enable-transmit --confirm`
and start the service.

## Designed to fail safely

- Automatic transmission is disabled in every new installation.
- The relay OFF command is sent at service startup and shutdown.
- Weather and audio files are replaced atomically.
- A failed weather update retains the last valid announcement.
- Maximum transmission time and request cooldown are configurable.
- The receiver is recalibrated after each transmission.

## Supported weather stations

The first release supports local WeatherLink Live observations and Ecowitt
cloud observations. The adapter design allows more weather stations to be
added without changing the receiver or transmitter code.

## Important notice

MyAWOS Lite controls a radio transmitter. Installation does not grant authority
to transmit. The station operator is responsible for licensing, frequency use,
station identification, RF exposure, antenna installation, interference
prevention and verifying every broadcast before operational use.

## Download and support

Buttons:

- **Latest release** → `https://github.com/OWNER/myawos-lite/releases/latest`
- **Documentation** → `https://github.com/OWNER/myawos-lite/tree/main/docs`
- **Report a problem** → `https://github.com/OWNER/myawos-lite/issues`

Replace `OWNER` after the GitHub repository is created.
