import configparser

class ConfigHandler:
    def __init__(self, file_name='config.ini'):
        self.file_name = file_name
        self.config = configparser.ConfigParser()
        self.system_ids = []

    def get_system_ids(self):
        self.read_config()
        self.system_ids = [x[1] for x in self.config.items('systems')] # Only get ID from each (name, ID) tuple
        return self.system_ids

    def read_config(self):
        self.config.read(self.file_name)

    def update_config_value(self, section, key, value):
        self.config.set(section, key, value)
        with open(self.file_name, 'w') as configfile:
            self.config.write(configfile)

    def add_new_section(self, section, tuple_list = None):
        self.config.add_section(section)

        if tuple_list is not None:
            for item in tuple_list:
                self.config.set(section, item[0], item[1])

        with open(self.file_name, 'w') as configfile:
            self.config.write(configfile)