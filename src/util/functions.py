import os
from pathlib import Path


def check_empty_fields(*fields, button):
    for field in fields:
        if not field.get().strip():
            button.config(state="disabled")
            return
    button.config(state="normal")


def get_db_location(app_name="StudentScheduler", db_name="data.db"):
    if os.name == "nt":
        base_dir = Path(os.getenv("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
    else:
        base_dir = Path(os.getenv("XDG_DATA_HOME", Path.home() / ".local" / "share"))

    app_dir = base_dir / app_name
    app_dir.mkdir(parents=True, exist_ok=True)

    return app_dir / db_name
