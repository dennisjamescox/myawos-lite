# Installation and commissioning

## 1. Install

Download the `.deb`, then run:

```bash
sudo apt install ./myawos-lite_0.1.0_all.deb
sudo myawos-lite setup
```

The setup wizard writes `/etc/myawos-lite/config.toml` as `root:myawos` with
mode 640 and leaves automatic transmission disabled.

## 2. Inspect devices

```bash
sudo myawos-lite devices
```

Select the Airspy, `/dev/serial/by-id/...` relay path, and ALSA output in the
configuration. Reconnect USB devices and rerun the command if anything is
missing.

## 3. Verify the weather source

For WeatherLink Live, set `weather.type = "weatherlink_live"` and enter its
local IP address. For Ecowitt cloud, set `weather.type = "ecowitt_cloud"` and
enter the application key, API key, and station MAC. Keep the configuration
restricted to `root:myawos` because it may contain credentials.

```bash
sudo myawos-lite doctor
sudo myawos-lite generate
```

## 4. Test audio without transmitting

Leave the radio off or disconnected from PTT:

```bash
sudo myawos-lite play-audio
```

Select a different `transmitter.audio_device` if sound reaches the wrong jack.

## 5. Test the fail-safe state

```bash
sudo myawos-lite relay-off
```

Verify that the relay LED is off and COM–NO is open. If this fails, do not
connect or power the radio.

## 6. Commission transmission

After checking wiring, antenna/RF protection, frequency authorization and a
separate monitoring receiver, explicitly enable transmission and the service:

```bash
sudo myawos-lite enable-transmit --confirm
sudo systemctl enable --now myawos-lite
sudo journalctl -u myawos-lite -f
```

Begin with a dummy load or otherwise controlled test path. Confirm that five
clicks produce one transmission, audio is intelligible, and PTT always releases.
