def parse_config(filepath: str) -> dict:
    config = {}
    MANDATORY_KEYS = ['WIDTH', 'HEIGHT', 'ENTRY', 'EXIT', 'OUTPUT_FILE', 'PERFECT']
    try:
        with open(filepath, 'r') as f:
            for line in f:
                clean_line = line.strip()
                if not clean_line or clean_line.startswith('#'):
                    continue
                key, value= clean_line.split('=', 1)
                config.update({key: value})
                print(value)
            upper_config = key_capitalize(config)
        for key in MANDATORY_KEYS:
            if key not in upper_config:
                raise ValueError(f"Missing mandatory key: {key}")
    except FileNotFoundError as e:
        print(f"Error file {e} does not exist")
    except ValueError as e:
        print(f"{e}")
    return upper_config


def  key_capitalize(config: dict) -> dict:
    new_config = {}
    for key, value in config.items():
       new = str(key).upper()
       new_config.update({new :value})
    return new_config


parse_config("test.txt")


