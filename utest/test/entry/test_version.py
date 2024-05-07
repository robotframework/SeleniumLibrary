import subprocess
import sys


def test_version():
    cmd = [
        sys.executable,
        "src/SeleniumLibrary/entry",
        "--version"
    ]
    process = subprocess.run(cmd, capture_output=True, check=True)
    lines = process.stdout.decode("utf-8").splitlines()
    python_version = (
        f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    )
    assert len(lines) == 5
    assert "Used Python is: " in lines[0], lines[0]
    assert python_version in lines[1], lines[1]
    assert 'Robot Framework version: "' in lines[2], lines[2]
    assert 'Installed SeleniumLibrary version is: ' in lines[3], lines[3]
    assert 'Installed selenium version is: ' in lines[4], lines[4]
