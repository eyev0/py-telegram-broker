import ast
import configparser
import os
from pathlib import Path
from typing import Tuple


def literal_eval(func):
    def wrapper(*args, **kwargs):
        orig_result = func(*args, **kwargs)
        return ast.literal_eval(orig_result)
    return wrapper


class Section:
    def __init__(self, config_parser: configparser.ConfigParser, section_name):
        self._name = section_name
        self._parser = config_parser
        self._raw_contents = config_parser[section_name]
        self._options = []
        self._parser_func_map = {
            'i': self._parser.getint,
            'f': self._parser.getfloat,
            'b': self._parser.getboolean,
            'e': literal_eval(self._parser.get),
            's': self._parser.get,
        }

        for key in self._raw_contents:
            parsed_key, parsed_value = self.parse_raw_option(self._name, key)
            self.set_option(parsed_key, parsed_value, append_key=True)

    def get_raw_contents(self):
        return self._raw_contents

    def get_options_list(self):
        return self._options

    def get_name(self):
        return self._name

    def set_option(self, key, value, append_key=False):
        setattr(self, key, value)
        if append_key:
            self._options.append(key)

    def get_option(self, key):
        return getattr(self, key, None)

    def parse_raw_option(self, sect_name: str, opt_key: str, mode='s') -> Tuple:
        if opt_key[1] == ',':
            mode = opt_key[0]
            parsed_key = opt_key[2:]
        else:
            parsed_key = opt_key
        get_func = self._parser_func_map[mode]
        parsed_value = get_func(sect_name, opt_key)
        return parsed_key, parsed_value

    def override_with(self, section):
        for key in section.get_options_list():
            value = section.get_option(key)
            self.set_option(key, value, append_key=key not in self.get_options_list())


class Config:
    def __init__(self, path, debug):
        self.sections = []
        self.section_names = []
        self.configparser = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
        self.configparser.read(path)
        self.dynamic_load_sections()

    def __repr__(self):
        repr_str = ''
        for section in self.sections:
            repr_str += f'\n[{section.get_name()}]\n'
            for key in section.get_options_list():
                repr_str += f'    {key}={section.get_option(key)}\n'
        return repr_str

    def get_sect(self, section_name) -> Section:
        return getattr(self, section_name, None)

    def dynamic_load_sections(self):
        for section_name in self.configparser.sections():
            section = Section(self.configparser, section_name)
            self.sections.append(section)
            self.section_names.append(section_name)
            setattr(self, section_name, section)

    def override_with(self, conf):
        for section_name in conf.section_names:
            if section_name not in self.section_names:
                self.sections.append(conf.get_sect(section_name))
                self.section_names.append(section_name)
            else:
                self.get_sect(section_name).override_with(conf.get_sect(section_name))


class ConfigNotImplementedError(BaseException):
    """./config/config.ini not implemented error"""


class DefaultConfigNotExistsError(BaseException):
    """./config/config.ini not implemented error"""


class ConfigManager:
    def __init__(self, debug):
        if debug:
            app_dir = str(Path(os.path.dirname(__file__)).parent)
        else:
            app_dir = os.getcwd()

        self.path_default = app_dir + '/defaults/config.ini'
        self.path_env = app_dir + '/config/config.ini'

        if not os.path.exists(self.path_default):
            raise DefaultConfigNotExistsError()
        if not os.path.exists(self.path_env):
            raise ConfigNotImplementedError()
        # default conf
        self.config = Config(self.path_default, debug)
        # env-based conf
        env_config = Config(self.path_env, debug)

        self.config.override_with(env_config)
