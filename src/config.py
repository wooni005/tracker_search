import os
import configparser

CONFIG_INI_FILE = '/home/arjan/.config/trackersearchgui/config.ini'


class Config:
    def __init__(self, tkRoot):
        self.configIniFile = CONFIG_INI_FILE
        self.config = configparser.ConfigParser()
        self.tkRoot = tkRoot
        if not os.path.exists(self.configIniFile):
            self.config['geometry'] = {'size': "400x400"}
            # TODO: Default config search area
            # TODO: Default config document types
            self.config['searchArea'] = '~/Documents'
            self.config.write(open(self.configIniFile, 'w'))
        else:
            # Read File
            self.config.read(self.configIniFile)

            # Check if file has geometry section
            try:
                self.config.get('geometry', 'size')
                # self.config.get('searchArea', '')
            except configparser.NoOptionError:
                print("NO OPTION CALLED SIZE")
                self.saveConfigfile()

    def saveConfigfile(self):
        self.config['geometry'] = {'size': self.tkRoot.geometry()}
        self.config.write(open(self.configIniFile, 'w'))

    def get(self, section, option):
        return self.config.get(section, option)

    def items(self, section):
        return self.config.items(section)
