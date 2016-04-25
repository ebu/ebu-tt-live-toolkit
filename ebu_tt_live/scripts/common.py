
import logging
from configobj import ConfigObj
import yaml
import re


log = logging.getLogger(__name__)
yaml_file = re.compile('^.*(\.yml|\.yaml)(\w)?$')


def create_loggers():
    logging.basicConfig(level=logging.INFO)


def parse_config(config, module_name=None):
    import ipdb; ipdb.set_trace()
    if yaml_file.match(config):
        log.info('YAML config mode')
    return None
