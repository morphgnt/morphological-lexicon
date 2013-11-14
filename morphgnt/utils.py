import yaml


def load_yaml(filename, wrapper=lambda key, metadata: metadata):
    with open(filename) as f:
        return {
            key: wrapper(key, metadata)
            for key, metadata in (yaml.load(f) or {}).items()
        }
