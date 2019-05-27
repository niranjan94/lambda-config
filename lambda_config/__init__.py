import os

from lambda_config.config import load_config
from aws_xray_sdk.core import patch_all

if os.getenv('SKIP_XRAY') != 'true':
    patch_all()

config = load_config()
