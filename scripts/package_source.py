"""Export committed source files while rejecting private model and audio data."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
DATA_SUFFIXES = {".pth", ".pt", ".onnx", ".index", ".safetensors", ".ckpt", ".npy", ".npz", ".wav", ".mp3", ".flac", ".m4a", ".ogg", ".aiff", ".aac", ".opus", ".pkl", ".pickle"}


def export_source(output):
    if subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT):
        raise SystemExit("Commit source changes before packaging.")
    fixtures = json.loads(subprocess.check_output(["git", "show", "HEAD:scripts/upstream-fixtures.json"], cwd=ROOT))
    files = []
    for entry in subprocess.check_output(["git", "ls-tree", "-rz", "HEAD"], cwd=ROOT).split(b"\0"):
        if not entry:
            continue
        metadata, raw_path = entry.split(b"\t", 1)
        mode, kind, sha = metadata.decode().split()
        path = raw_path.decode()
        if kind != "blob" or mode not in {"100644", "100755"}:
            raise SystemExit("Unsupported source entry: " + path)
        parts = Path(path).parts
        if not path.isascii() or any(part in {".git", "env", "venv", ".venv", "backups", "build"} or part.startswith(".env") or part.endswith(".app") for part in parts):
            raise SystemExit("Local or generated artifact in source: " + path)
        data = subprocess.check_output(["git", "cat-file", "blob", sha], cwd=ROOT)
        digest = hashlib.sha256(data).hexdigest()
        if path.startswith(("app/assets/audios/", "app/assets/datasets/")) and Path(path).name != ".gitkeep":
            raise SystemExit("Runtime audio or dataset in source: " + path)
        if path.startswith("app/logs/") or Path(path).suffix.lower() in DATA_SUFFIXES:
            if fixtures.get(path) != digest:
                raise SystemExit("Model, recording or training data in source: " + path)
        if Path(path).suffix.lower() in {".zip", ".log"}:
            raise SystemExit("Runtime log or nested archive in source: " + path)
        files.append((path, mode, data, digest))
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
        for path, mode, data, _ in files:
            info = zipfile.ZipInfo("Murphy-Voice-Studio-Source/" + path)
            info.external_attr = int(mode, 8) << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, data)
        checksums = "".join(digest + "  " + path + "\n" for path, _, _, digest in files)
        archive.writestr("Murphy-Voice-Studio-Source/SHA256SUMS.txt", checksums)
    print("Exported", len(files), "verified source files to", output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "build/Murphy-Voice-Studio-Source.zip")
    export_source(parser.parse_args().output.resolve())
