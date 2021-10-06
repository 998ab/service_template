import yaml

from pathlib import Path


def load_config():
    default_file = Path(__file__).parent.parent / 'config.yaml'
    with open(default_file, 'r') as f:
        config = yaml.safe_load(f)

    return config


__all__ = [
    'load_config',
]
