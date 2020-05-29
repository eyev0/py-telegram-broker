import configparser
import os
from pathlib import Path


class Section(dict):
    def __init__(self, parser, sect_name):
        self._parser = parser
        self.contents = parser[sect_name]
        self._parser_func_map = {
            'i': self._parser.getint,
            'f': self._parser.getfloat,
            'b': self._parser.getboolean,
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
    def __init__(self, debug):
        if debug:
            work_dir = str(Path(os.path.dirname(__file__)).parent)
        else:
            work_dir = os.getcwd()
        conf_path = work_dir + '/init/config.ini'
        config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
        config.read(conf_path)
        self.configparser = config
        self.sections = config.sections()

        for section_name in self.sections:
            section = Section(config, section_name)
            setattr(self, section_name, section)

    def __repr__(self):
        repr_str = ''
        for section_name in self.sections:
            repr_str += f'\n[{section_name}]\n'
            for key in getattr(self, section_name):
                repr_str += f'    {key}={getattr(self, section_name)[key]}\n'
        return repr_str
