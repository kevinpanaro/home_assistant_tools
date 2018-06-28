import gnupg
from os import listdir
from os.path import isfile, join


class HassPass:

    def __init__(self):
        self.pass_home_dir = "/Users/kevinpanaro/.password-store"
        self.homeassistant_dir = "homeassistant"
        self.hasspass_path = join(self.pass_home_dir, self.homeassistant_dir)
        self.binary='/usr/local/bin/gpg'
        self.homedir='/Users/kevinpanaro/.gnupg'
        self.gpg_encoding = 'utf-8'
        self.hasspass_dict = {}
        self._setup_gpg()
        self.hasspass_files = self._get_hasspass_files()
        self._form_pass_dict()
        self._make_yaml()

    def _setup_gpg(self):
        '''sets up gpg'''
        self.gpg = gnupg.GPG(binary=self.binary, homedir=self.homedir)
        self.gpg.encoding = self.gpg_encoding

    def _get_hasspass_files(self):
        '''return list of hass files''' 
        files = [file for file in listdir(self.hasspass_path) if isfile(join(self.hasspass_path, file))]
        return files

    def _form_pass_dict(self):
        for file in self.hasspass_files:
            current_file = file.split(".")[0]
            file = join(self.hasspass_path, file)
            with open(file, 'rb') as f:
                data = self.gpg.decrypt_file(filename=f)

            self.hasspass_dict[current_file] = str(data).strip()
        
    def _make_yaml(self):
        alphabetical = sorted(self.hasspass_dict.keys())
        for component in alphabetical:
            print(component + ": " + self.hasspass_dict[component])

if __name__ == '__main__':
    HassPass()
