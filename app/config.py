import configparser
import os
from pathlib import Path
import ast


def literal_eval(func):
    def wrapper(*args, **kwargs):
        orig_result = func(*args, **kwargs)
        return ast.literal_eval(orig_result)
    return wrapper


class Section(dict):
    def __init__(self, parser, sect_name):
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


class Config:
    def parse_conf(self, path):
        self.configparser.read(path)
        self.sections = self.configparser.sections()

        for section_name in self.sections:
            section = Section(self.configparser, section_name)
            setattr(self, section_name, section)

    def __init__(self, debug):
        self.configparser = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
        self.sections = []

        if debug:
            work_dir = str(Path(os.path.dirname(__file__)).parent)
        else:
            work_dir = os.getcwd()
        def_conf_path = work_dir + '/init/default.ini'
        conf_path = work_dir + '/init/config.ini'
        self.parse_conf(def_conf_path)
        self.parse_conf(conf_path)

    def __repr__(self):
        repr_str = ''
        for section_name in self.sections:
            repr_str += f'\n[{section_name}]\n'
            for key in getattr(self, section_name):
                repr_str += f'    {key}={getattr(self, section_name)[key]}\n'
        return repr_str
