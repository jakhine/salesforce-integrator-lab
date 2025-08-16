import os, pathlib, yaml
from dotenv import load_dotenv

ROOT = pathlib.Path(__file__).resolve().parents[2]  # корень репо
CONFIG_DIR = ROOT / "config"

# 1) .env (секреты)
load_dotenv(CONFIG_DIR / ".env")

# 2) app.yaml (несекретное)
with open(CONFIG_DIR / "app.yaml", "r") as f:
    APP = yaml.safe_load(f)

def get_env(name, default=None, required=False):
    val = os.getenv(name, default)
    if required and (val is None or val == ""):
        raise RuntimeError(f"Missing required env: {name}")
    return val