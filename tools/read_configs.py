import json
import os


def get_config(config_file_name: str):
    """
    The get_config function loads the configuration file and returns a dictionary of settings.

    :param config_file_name:str: Specify which config file to use
    :return: A dictionary of the configuration file
    :doc-author: MEGHANI
    """
    abs_path = os.path.abspath(__file__)
    dir_path = os.path.dirname(abs_path)
    os.chdir(dir_path)

    with open(os.path.join(f"{config_file_name}.json")) as json_config:
        config = json.load(json_config)
    return config


def get_config_path(config_file_name: str):
    """
    The get_config_path function returns the absolute path to a config json.

    :param config_file_name:str: Pass the name of the configuration file to be loaded
    :return: The directory path of the config json
    :doc-author: Meghani Mehboob
    """
    abs_path = os.path.abspath(__file__)
    dir_path = os.path.dirname(abs_path)
    return os.path.join(dir_path, config_file_name + ".json")