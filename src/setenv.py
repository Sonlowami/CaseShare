# This file serves to load the environment variables from the .env file
# It expects them to be .env file to be in the same repository as this file
# You can change the env_file_path to be the path to your .env file or other file you specify

import os

env_file_path = '.env'

def setenv():
    with open(env_file_path) as f:
        for line in f:
            key, value = line.strip().split('=')
            os.environ[key] = value


if __name__ == '__main__':
    setenv()
