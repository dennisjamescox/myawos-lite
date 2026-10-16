# Google Sites page: MyAWOS Lite

This is the copy-and-paste plan for a page named **MyAWOS Lite** on
`myawos.com`. Google Sites does not import this file as a finished page. Create
the sections below in Google Sites, upload `docs/wiring.svg`, and use the button
links shown here.

---

## Hero

# MyAWOS Lite

MyAWOS has expanded to FAA weather cameras, runway-light operations, AWC
weather integration, daily reports, and much more. That power can be
overwhelming for someone building a first station, so I created **MyAWOS Lite**.

MyAWOS Lite does one job: a pilot clicks the microphone five times, and the
station speaks the current local weather over a conventional aviation radio.
There is **no source code to edit**. Download one Ubuntu installer and answer a
short setup wizard.

Buttons:

- **Download MyAWOS Lite 0.1.1** → `https://github.com/dennisjamescox/myawos-lite/releases/latest/download/myawos-lite_0.1.1_all.deb`
- **See what to buy** → page anchor: What you need
- **Installation instructions** → page anchor: Install MyAWOS Lite

Small text below the download button:

> The download is public. A GitHub account is not required.

## How it works

### 1. A pilot makes five clicks

An Airspy receive-only radio listens on the airport frequency. MyAWOS Lite
distinguishes five microphone clicks from background noise and normal radio
traffic.

### 2. MyAWOS Lite gets the weather

The computer reads wind, gust, temperature, dew point and pressure directly
from a WeatherLink Live unit on the local network, or from an Ecowitt weather
station. It assembles a fresh report from the included prerecorded voice clips.

### 3. A separate radio transmits the report

A USB relay closes the radio's PTT contact. A dedicated USB audio adapter sends
the report through an isolated, attenuated interface to the radio microphone
input. When playback ends, MyAWOS Lite releases PTT and restarts the Airspy.

### 4. It waits for the next request

The receiver recalibrates automatically. A configurable cooldown prevents
back-to-back accidental transmissions.

## What MyAWOS Lite includes

- Airspy click detection
- WeatherLink Live and Ecowitt weather support
- Prerecorded weather voice clips
- USB-relay PTT control
- Automatic Ubuntu service
- Hardware detection and a guided setup wizard
- Safe audio-only and relay-OFF tests
- Documentation and a connection diagram

MyAWOS Lite intentionally leaves out cameras, email reports, AWC products,
forecasts, runway-light control, displays, GPIO and SDR transmission. Those
remain available in the full MyAWOS project.

## Fresh-weather protection in version 0.1.1

- MyAWOS Lite uses the observation timestamp supplied by WeatherLink Live—not
  the time an old file or response happened to be processed.
- Brief connection failures may use the last valid report.
- At 12 hours old, the previous weather values are no longer transmitted.
- Missing, invalid or old weather produces only: **“No weather available at
  this time.”**
- WeatherLink Live uses its local HTTP interface and Python's standard library,
  so no separate Davis/WeatherLink Python package is required.

## What you need

Only buy the items you do not already own. Product availability and prices can
change; model numbers and electrical requirements matter more than the seller.

| Component | Recommended example and purchase link | Important detail |
|---|---|---|
| Computer | Existing x86-64 PC, or [Amazon search: Ubuntu mini PC](https://www.amazon.com/s?k=mini+pc+ubuntu+compatible) | Must run Ubuntu 24.04 and have at least four USB ports, or use a powered hub. |
| Operating system | [Download Ubuntu 24.04 LTS](https://ubuntu.com/download/desktop) | Install Ubuntu before installing MyAWOS Lite. |
| Receive-only radio | [Airspy official distributors](https://airspy.com/purchase/) | Buy an Airspy Mini or Airspy R2. Do not substitute an Airspy HF+ for this release. |
| USB PTT relay | [Amazon: LCUS-1 CH340 one-channel USB relay](https://www.amazon.com/dp/B01CN7E0RQ) or [Amazon search](https://www.amazon.com/s?k=LCUS-1+CH340+USB+relay+5V) | Must be the 5 V USB/CH340 model with dry COM/NO/NC contacts and protocol `A0 01 01 A2`. |
| USB audio adapter | [Sabrent AU-MMSA on Amazon](https://www.amazon.com/dp/B00IRVQ0F8) | Use a separate class-compliant adapter so the setup is repeatable. |
| Aviation radio | [Yaesu FTA-250L at Aircraft Spruce](https://www.aircraftspruce.com/catalog/avpages/yaesufta250l.php) | An existing compatible FTA-250L, FTA-450L or FTA-550 may be used. |
| Radio adapter | [Yaesu SCU-42 at Aircraft Spruce](https://www.aircraftspruce.com/catalog/avpages/yaesu_11-18500.php) or [Sporty's](https://www.sportys.com/avionics-and-radios/aviation-radios/yaesu-550-750-headset-adapter.html) | Check the radio box first; some radio packages include a headset adapter. |
| Audio plug/interface | [PJ-068 microphone plug](https://gibson-barnes.com/products/pj-068-cord-plug-for-the-microphone) plus the interface described in the wiring guide | This is a custom isolated, DC-blocked, attenuated lead—not a plain adapter cable. |
| Receive antenna | [Amazon search: VHF airband SMA receive antenna](https://www.amazon.com/s?k=VHF+airband+118-136+SMA+antenna) | It must cover 118–137 MHz and fit the Airspy SMA connector. |
| Transmit antenna | [118–137 MHz airband antenna at Aircraft Spruce](https://www.aircraftspruce.com/catalog/avpages/antenna11-13828.php) | Use an antenna/feed line rated for transmit and appropriate to the installation. |
| Weather source: Davis | [WeatherLink Live 6100](https://davisnet.com/products/weatherlink-live) | For an existing compatible Davis sensor suite; MyAWOS Lite reads it over the local network. |
| Weather source: Ecowitt | [Ecowitt GW1100](https://shop.ecowitt.com/products/gw1100) | Requires compatible outdoor wind and temperature sensors; choose the correct regional RF frequency. |

Add a button below the table:

- **Full hardware and wiring guide** → `https://github.com/dennisjamescox/myawos-lite/tree/main/docs`

### About the custom audio lead

The computer produces headphone-level audio; the SCU-42/PJ-068 input expects
aviation-microphone audio. The lead must provide stereo-to-mono summing,
approximately 20–30 dB initial attenuation, DC blocking, galvanic isolation and
shielding. A generic 3.5 mm-to-PJ-068 cable is not a substitute. Have the lead
built and checked by someone qualified to work with radio audio if you are not
comfortable assembling it.

## How everything connects

Upload `docs/wiring.svg` at full width here.

Caption:

> Airspy only listens. The separate Yaesu radio transmits. The USB relay acts
> only as a dry PTT switch, and the USB audio path is isolated and attenuated
> before it reaches the SCU-42 microphone input.

## Before downloading

You need:

1. A computer already running Ubuntu 24.04 with internet access.
2. The Airspy, USB relay and USB audio adapter connected.
3. The weather station and Ubuntu computer on the same network for WeatherLink
   Live, or Ecowitt API credentials for Ecowitt cloud.
4. The radio wiring completed, but leave the radio off and PTT disconnected
   during initial setup.
5. The authorized airport frequency and station identifier.

You do **not** need Python, Git, a GitHub account, or any source-code editing.

## Install MyAWOS Lite

### Step 1 — Download

Click **Download MyAWOS Lite** above. Ubuntu normally saves the file in the
`Downloads` folder.

### Step 2 — Install the app and its dependencies

Open Terminal and run:

```text
cd ~/Downloads
sudo apt install ./myawos-lite_0.1.1_all.deb
```

This installs MyAWOS Lite, the Airspy utilities, Python runtime libraries,
audio tools, the included voice clips, USB permissions and the background
service. Internet access is needed while Ubuntu downloads dependencies.

### Step 3 — Run the guided setup

```text
sudo myawos-lite setup
```

The wizard asks for the station identifier, radio frequency, audio device and
weather source. For WeatherLink Live, it asks for the unit's local IP address.
For Ecowitt, it asks for the application key, API key and station MAC address.
The wizard writes the configuration; users do not edit a program file.

### Step 4 — Run the checks

```text
sudo myawos-lite devices
sudo myawos-lite doctor
sudo myawos-lite generate
sudo myawos-lite play-audio
sudo myawos-lite relay-off
```

`play-audio` never keys PTT. Run these checks with the radio off or PTT
disconnected. Do not continue until `doctor` passes, audio comes from the
correct USB adapter, and COM–NO is open after `relay-off`.

### Step 5 — Commission the transmitter

After checking the wiring, authorized frequency, antenna system, receiver
protection, audio level and fail-safe PTT release with a separate monitor:

```text
sudo myawos-lite enable-transmit --confirm
sudo systemctl enable --now myawos-lite
```

MyAWOS Lite now starts automatically after a reboot.

## Does the download install everything?

**It installs all MyAWOS Lite software and asks Ubuntu to install the required
software dependencies.** It also installs the voice clips, hardware rules and
background service.

It cannot install Ubuntu itself, connect physical wiring, discover a weather
station password/API key, choose an authorized frequency, set the final radio
audio level, or validate an antenna installation. Those are the short setup and
commissioning steps above. Automatic RF transmission remains disabled until
the operator explicitly enables it.

## Designed to fail safely

- A new installation cannot transmit automatically.
- The relay OFF command is sent at service startup and shutdown.
- Audio and weather files are replaced atomically.
- A brief failed weather update may retain the last valid announcement.
- Weather at or beyond the configurable 12-hour age limit is never reported;
  the station says only that weather is unavailable.
- Maximum transmit time and request cooldown are configurable.
- The Airspy restarts and recalibrates after each transmission.

## Download, documentation and help

- **Download installer** → `https://github.com/dennisjamescox/myawos-lite/releases/latest/download/myawos-lite_0.1.1_all.deb`
- **View the latest release** → `https://github.com/dennisjamescox/myawos-lite/releases/latest`
- **Documentation** → `https://github.com/dennisjamescox/myawos-lite/tree/main/docs`
- **Report a problem** → `https://github.com/dennisjamescox/myawos-lite/issues`
- **SHA-256 checksum** → `https://github.com/dennisjamescox/myawos-lite/releases/latest/download/SHA256SUMS`

The repository must remain **public** so visitors can download the installer
without creating or signing into a GitHub account.

## Important notice

MyAWOS Lite controls a radio transmitter. Installing the software does not
grant authority to transmit. The station operator is responsible for licensing,
frequency coordination, station identification, RF exposure, antenna and feed
line safety, interference prevention, receiver protection, audio quality and
verifying every broadcast before operational use.
