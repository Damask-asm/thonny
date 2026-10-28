"""Verified official runtime plus the two reviewed source changes; no pip resolution."""
import hashlib
import json
import shutil
import subprocess
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "5eb79646973128838818c960d6dcefa85086c603"
INPUTS = {
    "thonny-5.0.0-windows-portable-x64.zip": (
        "https://github.com/thonny/thonny/releases/download/v5.0.0/",
        "5b744151065bdbd6a0d823dfa791a72cbbc3372a549a5e4cb175434a9787eaee",
    ),
    "innosetup-6.4.3.exe": (
        "https://github.com/jrsoftware/issrc/releases/download/is-6_4_3/",
        "f3c42116542c4cc57263c5ba6c4feabfc49fe771f2f98a79d2f7628b8762723b",
    ),
}


def main():
    subprocess.run(["git", "merge-base", "--is-ancestor", BASE, "HEAD"], cwd=ROOT, check=True)
    changed = subprocess.check_output(
        ["git", "diff", "--name-only", BASE, "--", "thonny"], cwd=ROOT, text=True
    ).splitlines()
    assert sorted(changed) == ["thonny/__init__.py", "thonny/workbench.py"], changed
    cache = ROOT / "build" / "downloads"
    cache.mkdir(parents=True, exist_ok=True)
    for name, (url, digest) in INPUTS.items():
        dest = cache / name
        if not dest.exists():
            urllib.request.urlretrieve(url + name, dest)
        assert hashlib.sha256(dest.read_bytes()).hexdigest() == digest, name

    bundle = ROOT / "build" / "bundle"
    assert not bundle.exists(), "Use a fresh build directory"
    with zipfile.ZipFile(cache / next(iter(INPUTS))) as z:
        z.extractall(bundle)
    assert (bundle / "python.exe").exists()
    package = bundle / "Lib" / "site-packages" / "thonny"
    assert (package / "VERSION").read_text().strip() == "5.0.0"
    for name in ["workbench.py", "__init__.py"]:
        original = subprocess.check_output(["git", "show", f"{BASE}:thonny/{name}"], cwd=ROOT)
        assert (package / name).read_bytes().replace(b"\r\n", b"\n") == original.replace(b"\r\n", b"\n"), name
        shutil.copy2(ROOT / "thonny" / name, package / name)
    # Installed application uses a separate roaming profile, never a writable portable profile.
    (bundle / "portable_thonny.ini").unlink(missing_ok=True)
    (bundle / "shared_thonny.ini").touch()
    for pyc in package.rglob("*.pyc"):
        pyc.unlink()
    for name in ["LICENSE.txt", "CREDITS.rst", "README.rst"]:
        shutil.copy2(ROOT / name, bundle / name)
    shutil.copytree(ROOT / "licenses", bundle / "licenses", dirs_exist_ok=True)
    shutil.copy2(ROOT / "classroom" / "MANUAL_TESTS.md", bundle / "CLASSROOM_MANUAL_TESTS.md")
    (ROOT / "dist").mkdir(exist_ok=True)
    manifest = {"upstream_commit": BASE, "source_commit": subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "inputs_sha256": {name: entry[1] for name, entry in INPUTS.items()}}
    (ROOT / "dist" / "build-inputs.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
