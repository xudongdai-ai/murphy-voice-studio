# Source Packaging and Privacy

The source distribution excludes personal voice models, retrieval indexes, private audio, training datasets, Python environments, logs, and local backups.

The 32 bundled files under `app/logs/mute*` and `app/logs/reference/` are unchanged upstream Applio fixtures, checked against the original upstream Git blobs. They are not personal recordings or trained voice models.

Preview screenshots are captured from an isolated source environment containing no personal models, indexes, or audio. The author name and WeChat support contact are the public project details.

To build a source ZIP, commit the intended source changes and run `python3 scripts/package_source.py`. The script reads tracked Git blobs, rejects model and audio data except the exact upstream fixtures listed in its manifest, and excludes generated desktop bundles. It includes SHA256 checksums for the exported files.

Personal model and audio directories in the installed studio are separate from this source repository and remain on the local machine.
