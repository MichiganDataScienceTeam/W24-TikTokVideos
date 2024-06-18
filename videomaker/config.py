import toml
import os

config_path = os.path.join(os.path.dirname(__file__), "./config.toml")
with open(config_path, "r") as f:
    config = toml.load(f)

with open("client_secrets.toml") as f:
    creds = toml.load(f)
