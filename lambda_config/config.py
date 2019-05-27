import json
import os

import boto3
import yaml
from configparser import RawConfigParser
from typing import Dict

ssm_path = os.getenv('SSM_PARAMETER_PATH')
ssm_config_type = os.getenv('SSM_CONFIG_TYPE')


def load_config() -> Dict:
    """
    Loads config from SSM parameter store and parses it based on the set type.

    :return:
    """
    client = boto3.client('ssm')
    config_data = client.get_parameter(ssm_path, WithDecryption=True)['Parameter']['Value']
    if ssm_config_type == 'yaml':
        return load_config_from_yaml(config_data)
    if ssm_config_type == 'json':
        return load_config_from_json(config_data)
    if ssm_config_type == 'ini':
        return load_config_from_ini(config_data)
    return {
        'data': config_data
    }


def load_config_from_yaml(config_data: str) -> Dict:
    """
    Parses a yaml config string into a dict.

    :param config_data:
    :return:
    """
    return yaml.load(config_data)


def load_config_from_json(config_data: str) -> Dict:
    """
    Parses a json config string into a dict.

    :param config_data:
    :return:
    """
    return json.loads(config_data)


def load_config_from_ini(config_data: str) -> Dict:
    """
    Parses an init config string into a dict.

    :param config_data:
    :return:
    """
    config_dict = {}
    config = RawConfigParser(allow_no_value=True)
    config.read_string(config_data)

    for section in config.sections():
        config_dict[section] = {}
        for options in config.options(section):
            config_dict[section][options] = config.get(section, options)

    return config_dict
