# Hardware and purchasing list

## Required

| Item | Recommended first-release specification |
|---|---|
| Computer | Ubuntu 24.04 mini PC or laptop |
| Receiver | Airspy Mini or Airspy R2 |
| PTT relay | LCUS-1, 5 V USB-powered, one channel, CH340, 9600 baud |
| Relay protocol | ON `A0 01 01 A2`; OFF `A0 01 00 A1` |
| Audio | Dedicated class-compliant USB audio adapter |
| Radio | Yaesu FTA-250L/450L/550 with SCU-42 |
| PTT cable | 3.5 mm plug wired to the SCU-42 PTT connection |
| Audio cable | Isolated, DC-blocked and attenuated 3.5 mm to PJ-068 cable |
| Antennas | Separate receive and transmit antennas appropriate for 118–137 MHz |

The relay contact current rating is not important for PTT. The relay must have
voltage-free COM/NO/NC contacts. Do not connect USB 5 V, relay VCC, or any other
external voltage to the radio PTT contacts.

## Why a dedicated USB audio adapter?

A separate adapter provides a stable ALSA device name, avoids laptop headset
jack detection, and makes replacement installations repeatable. Record its
ALSA identifier with `myawos-lite devices` and use a persistent card name when
possible.

## Audio-interface requirement

The computer produces headphone/line-level audio while the SCU-42 expects a
nominal 150-ohm aviation microphone. Use a purpose-built interface containing:

- stereo-to-mono summing;
- approximately 20–30 dB initial attenuation;
- DC blocking;
- galvanic audio isolation; and
- shielded cable.

Adjust the final level while monitoring on a separate receiver. Excess level
causes distorted or unintelligible AM; insufficient level produces weak audio.

## Receiver protection

Stopping Airspy software during transmission does not protect its RF input.
Provide adequate antenna separation and an RF limiter, disconnect relay, or
other protection appropriate for the transmitter power and site layout.
