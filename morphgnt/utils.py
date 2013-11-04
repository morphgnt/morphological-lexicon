import yaml


def default_wrapper(key, metadata):
    return metadata


def load_yaml(filename, wrapper=default_wrapper):
    with open(filename) as f:
        return {
            key: wrapper(key, metadata)
            for key, metadata in yaml.load(f).items()
        }
