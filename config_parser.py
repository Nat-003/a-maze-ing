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
                tmp = clean_line.split('=', 1)
                if len(tmp) == 1:
                    continue
                key, value = tmp
                config.update({key: value})
            upper_config = key_capitalize(config)
        for key in MANDATORY_KEYS:
            if key not in upper_config:
                raise ValueError(f"Missing mandatory key: {key}")
        return upper_config
    except FileNotFoundError as e:
        print(f"Error file {e} does not exist")


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
                try:
                    new_value = int(value)
                    config[key] = new_value
                except ValueError:
                    raise ValueError(f"Error invalid height or width: {value}")
            elif key in ("ENTRY", "EXIT"):
                try:
                    new_value = []
                    tmp = value.split(',')
                    for v in tmp:
                        new_value.append(int(v))
                    config[key] = new_value
                except ValueError:
                    raise ValueError(f"Error invalid entry or exit: {value}")
            elif key == "PERFECT":
                if value == "True" or value == "False":
                    config[key] = (value == "True")
                else:
                    raise ValueError(f"incorrect boolean value {value}")
            elif key == "SEED":
                try:
                    config[key] = int(value)
                except ValueError:
                    config[key] = None
                    print("Warning invalid SEED entered, using random seed")
        entry = config["ENTRY"]
        exit_point = config["EXIT"]
        width = config["WIDTH"]
        height = config["HEIGHT"]
        entry_x, entry_y = entry
        exit_x, exit_y = exit_point
        if entry_x < 0 or entry_x >= width or entry_y < 0 or entry_y >= height:
            print(f"Warning: Entry coordinates({entry_x},{entry_y}) out of bounds for maze ({width},{height}) defaulting to (0,0)")
            config["ENTRY"] = (0, 0)
        elif exit_x < 0 or exit_x >= width or exit_y < 0 or exit_y >= height:
            print(f"Warning: Exit coordinates({exit_x},{exit_y}) out of bounds for maze ({width},{height}) defaulting to ({width-1},{height-1})")
            config["EXIT"] = (width-1, height-1)
        return config      
    except ValueError as e:
        print(f"{e}")
  
