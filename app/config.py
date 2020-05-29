import ast
import configparser
import os
from pathlib import Path


def literal_eval(func):
    def wrapper(*args, **kwargs):
        orig_result = func(*args, **kwargs)
        return ast.literal_eval(orig_result)
    return wrapper


class Section(dict):
    def __init__(self, parser, sect_name):
        self.name = sect_name
        self._parser = parser
        self.contents = parser[sect_name]
        self._parser_func_map = {
            'i': self._parser.getint,
            'f': self._parser.getfloat,
            'b': self._parser.getboolean,
            'e': literal_eval(self._parser.get),
            's': self._parser.get,
        }

        for key in self.contents:
            setattr(self, self.parsekey(key), self.parseopt(sect_name, key))

        super().__init__(self.contents)

    def set(self, key, value):
        self[key] = value
        self.contents[key] = value

    @staticmethod
    def parsekey(opt_key: str):
        if opt_key[1] == ',':
            return opt_key[2:]
        return opt_key

    def parseopt(self, sect_name: str, opt_key: str, mode='s'):
        if opt_key[1] == ',':
            mode = opt_key[0]
        get_func = self._parser_func_map[mode]
        return get_func(sect_name, opt_key)


class ConfigProxy:
    def parse_conf(self, path):
        self.configparser.read(path)
        for section_name in self.configparser.sections():
            section = Section(self.configparser, section_name)
            self.sections.append(section)
            setattr(self, section_name, section)

    def __init__(self, path, debug):
        self.configparser = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
        self.sections = []
        self.parse_conf(path)

    def get_sect(self, section_name) -> Section:
        return getattr(self, section_name, None)

    def __repr__(self):
        repr_str = ''
        for section in self.sections:
            repr_str += f'\n[{section.name}]\n'
            for key in section:
                repr_str += f'    {key}={section[key]}\n'
        return repr_str


class ConfigNotImplementedError(BaseException):
    """./config/config.ini not implemented error"""


class Config(ConfigProxy):
    def __init__(self, debug):
        if debug:
            app_dir = str(Path(os.path.dirname(__file__)).parent)
        else:
            app_dir = os.getcwd()
        # default conf
        super().__init__(app_dir + '/defaults/config.ini', debug)

        # env-based conf
        conf_path = app_dir + '/config/config.ini'
        if not os.path.exists(conf_path):
            raise ConfigNotImplementedError()
        conf = ConfigProxy(conf_path, debug)
        self.merge(conf)

    def merge(self, another_conf: ConfigProxy):
        # add new sections
        for section in another_conf.sections:
            if section not in self.sections:
                self.sections.append(section)
        # add/replace parameters in all sections
        for section in another_conf.sections:
            for key in section:
                self.get_sect(section.name).set(key, section[key])
