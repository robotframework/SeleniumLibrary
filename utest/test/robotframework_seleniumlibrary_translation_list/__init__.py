from pathlib import Path


def get_language() -> list:
    curr_dir = Path(__file__).parent.absolute()
    return [
        {
            "language": "eng",
            "path": curr_dir / "translate1.json"
        },
        {
            "language": "swe",
            "path": curr_dir / "translate2.json"
        }
    ]