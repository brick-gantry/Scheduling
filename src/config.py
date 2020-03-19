config_path = '/project/etc/config.yml'
redis = {}


def load():
    import sys
    import yaml
    with open(config_path) as stream:
        for k, v in yaml.load(stream).items():
            setattr(sys.modules[__name__], k, v)
