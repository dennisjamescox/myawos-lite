# Hardware and purchasing list

Product links are examples, not endorsements. Listings and prices change; use
the model and electrical requirements in this guide when comparing sellers.

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

## Purchase links

| Item | Example source |
|---|---|
| Ubuntu computer | [Amazon search: Ubuntu-compatible mini PC](https://www.amazon.com/s?k=mini+pc+ubuntu+compatible) |
| Ubuntu 24.04 LTS | [Official Ubuntu download](https://ubuntu.com/download/desktop) |
| Airspy Mini/R2 | [Airspy official distributors](https://airspy.com/purchase/) |
| LCUS-1 CH340 relay | [Amazon product](https://www.amazon.com/dp/B01CN7E0RQ) or [Amazon search](https://www.amazon.com/s?k=LCUS-1+CH340+USB+relay+5V) |
| USB sound adapter | [Sabrent AU-MMSA](https://www.amazon.com/dp/B00IRVQ0F8) |
| Yaesu FTA-250L | [Aircraft Spruce](https://www.aircraftspruce.com/catalog/avpages/yaesufta250l.php) |
| Yaesu SCU-42 | [Aircraft Spruce](https://www.aircraftspruce.com/catalog/avpages/yaesu_11-18500.php) or [Sporty's](https://www.sportys.com/avionics-and-radios/aviation-radios/yaesu-550-750-headset-adapter.html) |
| PJ-068 microphone plug | [Gibson & Barnes](https://gibson-barnes.com/products/pj-068-cord-plug-for-the-microphone) |
| Airspy receive antenna | [Amazon search: 118–136 MHz SMA antenna](https://www.amazon.com/s?k=VHF+airband+118-136+SMA+antenna) |
| Transmit antenna | [Aircraft Spruce 118–137 MHz example](https://www.aircraftspruce.com/catalog/avpages/antenna11-13828.php) |
| WeatherLink Live | [Davis Instruments](https://davisnet.com/products/weatherlink-live) |
| Ecowitt gateway | [Ecowitt GW1100](https://shop.ecowitt.com/products/gw1100) |

Check whether a headset adapter is included with a new Yaesu radio before
ordering an additional SCU-42. The Ecowitt gateway alone is not an outdoor
weather station; it requires compatible wind and outdoor temperature sensors.

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
