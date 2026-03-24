MANDATORY_KEYS = ['WIDTH', 'HEIGHT', 'ENTRY', 'EXIT', 'OUTPUT_FILE',
                  'PERFECT']


def get_key(filepath: str) -> dict:
    config = {}
    upper_config = {}
    try:
        with open(filepath, 'r') as f:
            for line in f:
                clean_line = line.strip()
                if not clean_line or clean_line.startswith('#'):
                    continue
                key, value = clean_line.split('=', 1)
                config.update({key: value})
                # print(value)
            upper_config = key_capitalize(config)
        for key in MANDATORY_KEYS:
            if key not in upper_config:
                raise ValueError(f"Missing mandatory key: {key}")
    except FileNotFoundError as e:
        print(f"Error file {e} does not exist")
    return upper_config


def key_capitalize(config: dict) -> dict:
    new_config = {}
    for key, value in config.items():
        new = str(key).upper()
        new_config.update({new: value})
    return new_config


def parse_config(filepath: str) -> dict:
    config = {}
    try:
        config = get_key(filepath)
        for key, value in config.items():
            if key in ("WIDTH", "HEIGHT"):
                new_value = int(value)
                config[key] = new_value
            elif key in ("ENTRY", "EXIT"):
                new_value = []
                tmp = value.split(',')
                for v in tmp:
                    new_value.append(int(v))
                config[key] = new_value
            elif key == "PERFECT":
                config[key] = (value == "True")
    except ValueError as e:
        print(f"{e}")
    return config


