# macOS Launcher

Source files for the Murphy Voice Studio desktop launcher.

## Build

On macOS, run `./desktop/build.command` from the repository root, or double-click `build.command`. The script creates and locally signs `build/Murphy Voice Studio.app`. Generated application bundles are excluded from Git.

The launcher opens the local studio at `http://127.0.0.1:6969`. It requires an existing installation at `~/pinokio/api/applio.git/app` with its Python environment in `app/env`. Logs are written to `~/Library/Logs/Murphy-Voice-Studio.log`.

`launcher.sh` starts the service, `Info.plist` contains bundle metadata, and `resources/` contains the application icon. No voice models, private audio, or training data are packaged by the launcher build.
