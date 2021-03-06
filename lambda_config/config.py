import json
import os
import tempfile
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

    :return: the config as dictionary
    """
    if ssm_path != '':
        return load_config_for_ssm_path(ssm_path)
    if ssm_paths != '':
        return dict_merge({}, [load_config_for_ssm_path(path.strip()) for path in ssm_paths.split(',')])
    return {}


def get_config_from_ssm_path(path: str, store: bool = False) -> str:
    """
    Get config from the given SSM Parameter store path.

    :param str path: path to the config
    :param bool store: should the config be stored to a file
    :return: config as string or path to config as string.
    """
    config_file_path = tempfile.mktemp()
    client = boto3.client('ssm')
    config_data = client.get_parameter(Name=path, WithDecryption=True)['Parameter']['Value']
    if not store:
        return config_data
    with open(config_file_path, 'w') as fd:
        fd.write(config_data)
    return config_file_path


def load_config_for_ssm_path(path: str) -> Dict:
    """
    Load config from an SSM Parameter store path.

    :param str path: path to the config
    :return: the config as dictionary
    """
    resolved_path = os.path.expandvars(path)
    try:
        config_data = get_config_from_ssm_path(resolved_path)
    except Exception:
        print(f'failed to load config from SSM path {resolved_path}')
        traceback.print_exc()
        return {}

    try:
        if ssm_config_type == 'yaml':
            return load_config_from_yaml(config_data)
        if ssm_config_type == 'json':
            return load_config_from_json(config_data)
        if ssm_config_type == 'ini':
            return load_config_from_ini(config_data)
    except Exception:
        print(f'failed to parse config from SSM path {resolved_path}')
        traceback.print_exc()
        pass
    return {
        'data': config_data
    }


def load_config_from_yaml(config_data: str) -> Dict:
    """
    Parses a yaml config string into a dict.

    :param str config_data: the config data to parse
    :return: the parsed config as dictionary
    """
    return yaml.load(config_data, Loader=yaml.FullLoader)


def load_config_from_json(config_data: str) -> Dict:
    """
    Parses a json config string into a dict.

    :param str config_data: the config data to parse
    :return: the parsed config as dictionary
    """
    return json.loads(config_data)


def load_config_from_ini(config_data: str) -> Dict:
    """
    Parses an init config string into a dict.

    :param str config_data: the config data to parse
    :return: the parsed config as dictionary
    """
    config_dict = {}
    config = RawConfigParser(allow_no_value=True)
    config.read_string(config_data)

    for section in config.sections():
        config_dict[section] = {}
        for options in config.options(section):
            config_dict[section][options] = config.get(section, options)

    return config_dict
