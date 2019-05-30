import json
import os
import traceback

import boto3
import yaml
from configparser import RawConfigParser
from typing import Dict

from lambda_config.utils import dict_merge

ssm_path = os.getenv('SSM_PARAMETER_PATH', '').strip()
ssm_paths = os.getenv('SSM_PARAMETER_PATHS', '').strip()
ssm_config_type = os.getenv('SSM_CONFIG_TYPE', '').strip()


def load_config() -> Dict:
    """
    Loads config from SSM parameter store and parses it based on the set type.

    :return:
    """
    if ssm_path != '':
        return load_config_for_ssm_path(ssm_path)
    if ssm_paths != '':
        return dict_merge({}, [load_config_for_ssm_path(path.strip()) for path in ssm_paths.split(',')])
    return {}


def load_config_for_ssm_path(path: str) -> Dict:

    try:
        client = boto3.client('ssm')
        config_data = client.get_parameter(os.path.expandvars(path), WithDecryption=True)['Parameter']['Value']
    except:
        print(f'failed to load config from SSM path {path}')
        traceback.print_exc()
        return {}

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
