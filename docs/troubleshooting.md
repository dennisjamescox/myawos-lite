# Troubleshooting

## Airspy not found

- Run `airspy_info` and `lsusb`.
- Connect directly rather than through an unpowered hub.
- Check the udev rules and membership in `plugdev`.
- Stop other SDR software that may have claimed the receiver.

## Relay not found

- Confirm it is a 5 V LCUS-1 CH340 serial relay.
- Look for `/dev/serial/by-id/` and `/dev/ttyUSB0`.
- USB error `-71` normally indicates a physical port, plug, cable, or relay fault.
- Move it to a different physical USB port.
- Do not enable transmission until `myawos-lite relay-off` succeeds.

## Relay activates but radio does not key

- COM must connect to radio/PTT ground.
- NO must connect to the PTT conductor.
- NC remains unused.
- Push the SCU-42 completely into the radio and secure both screws.
- Verify continuity between COM and NO only while the relay is active.

## Radio keys but no speech is heard

- Run `myawos-lite play-audio` with PTT disconnected.
- Check the configured ALSA device.
- Check the PJ-068 audio interface and its microphone-audio conductor.
- Increase audio gradually; do not bypass isolation or DC blocking.

## Audio is distorted

- Reduce ALSA playback volume or increase interface attenuation.
- Confirm stereo is summed through resistors rather than shorting channels.
- Keep USB/audio wiring away from the transmitting antenna and coax.

## Five clicks are unreliable

- Reposition or improve the Airspy receive antenna.
- Watch logs for click level versus calibrated noise.
- Adjust `threshold_on_ratio` in small steps.
- Increase the click window only if actual clicks are being recognized separately.
- Investigate local noise before lowering the threshold significantly.

## Weather updates fail

- Run `myawos-lite doctor`.
- Confirm the WeatherLink IP or Ecowitt credentials.
- Verify the computer can reach the station or Internet.
- The service may retain the last successful announcement during a brief failure,
  but it will never transmit it at or beyond `weather.max_age_hours` (12 hours by
  default). It transmits only “No weather available at this time” after that limit.
