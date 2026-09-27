# Release checklist

- Run all unit tests.
- Build and inspect the Debian package.
- Install on a clean Ubuntu 24.04 test computer.
- Confirm a new installation has transmission disabled.
- Run `devices`, `doctor`, `generate`, `play-audio`, and `relay-off`.
- Verify relay disconnection during service stop and computer reboot.
- Test with a dummy load or controlled RF path.
- Confirm five clicks cause exactly one broadcast.
- Confirm PTT releases after normal audio, failed audio, timeout, and service stop.
- Measure audio for intelligibility and overmodulation on a separate receiver.
- Confirm Airspy recalibration after transmission.
- Review the package and Git history for keys, passwords, station coordinates,
  generated logs, and other private deployment information.
- Publish the `.deb`, SHA-256 checksum, source archive, and release notes.
- Update the Google Sites download button to the immutable release URL.
