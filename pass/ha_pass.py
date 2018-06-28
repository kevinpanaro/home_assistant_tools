import gnupg
from os import listdir, access, remove
from os.path import isfile, join, dirname, realpath


class HassPass:

    def __init__(self, 
                 pass_home_dir = "/Users/kevinpanaro/.password-store",
                 hass_dir = "homeassistant", binary = "/usr/local/bin/gpg",
                 home_dir = "/Users/kevinpanaro/.gnupg", gpg_encoding = "utf-8",
                 save_file = "secrets.yaml"):
        self.pass_home_dir = pass_home_dir
        self.hass_dir = hass_dir
        self.hasspass_path = join(self.pass_home_dir, self.hass_dir)
        self.binary = binary
        self.homedir = home_dir
        self.gpg_encoding = gpg_encoding
        self.hasspass_dict = {}
        self.save_file = join(dirname(realpath(__file__)), save_file)

        self._setup_gpg()
        self.make_yaml()

    def _setup_gpg(self):
        '''sets up gpg'''
        self.gpg = gnupg.GPG(binary=self.binary, homedir=self.homedir)
        self.gpg.encoding = self.gpg_encoding

    def _get_hasspass_files(self):
        '''return list of hass files''' 
        files = [file for file in listdir(self.hasspass_path) if isfile(join(self.hasspass_path, file))]
        self.hasspass_files = files

    def _form_pass_dict(self):
        '''makes pass dict'''
        self._get_hasspass_files()
        for file in self.hasspass_files:
            current_file = file.split(".")[0]
            file = join(self.hasspass_path, file)
            with open(file, 'rb') as f:
                data = self.gpg.decrypt_file(filename=f)

            self.hasspass_dict[current_file] = str(data).strip()

    def _reset_yaml(self):
        if not access(self.save_file, 0): # if true, file doesn't exist
            with open(self.save_file, 'w') as f:
                pass
        else:
            remove(self.save_file)
            self._reset_yaml()

        
    def make_yaml(self):
        '''creates a yaml, unfinished'''
        self._reset_yaml()
        self._form_pass_dict()
        alphabetical = sorted(self.hasspass_dict.keys())
        for component in alphabetical:
            with open(self.save_file, 'a') as f:
                f.write(component + ": " + self.hasspass_dict[component] + '\n')

if __name__ == '__main__':
    HassPass()
    