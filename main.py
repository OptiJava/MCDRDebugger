import json
import logging
import sys


class Config:
    debug = False

    ##########
    # minecraft server configurations
    core_server_url = 'https://piston-data.mojang.com/v1/objects/8dd1a28015f51b1803213892b50b7b4fc76e594d/server.jar'
    # will download server core file from this url
    # Default: 1.20.4 vanilla server url from mojang
    auto_eula = False
    # should I agree the eula automatically?
    # Default: False

    ##########
    # mcdreforged configurations
    plugins = []
    # did you need other mcdr plugins? add the download url here!
    # Default: empty
    python_path = ''
    # python executable file path
    # Default: blank (will use 'python3 ...' command in default shell later)
    pip_path = ''
    # pip executable file path
    # Default: blank (will use 'pip3 ...' command in default shell later)
    env_path = './env'
    # will init mcdr in this path
    # Default: ./env

    ##########
    # mcdreforged plugin packaging configurations
    method = 'mcdr_command'
    # how can I package your plugin?
    # Options:
    #   mcdr_command: use mcdr pack command
    #   folder: move the whole folder to the 'plugins' folder
    #   single_file: move the single file to the 'plugins' folder
    # Default: mcdr_command
    plugin_code_path = './code'
    # the whole plugin code should in this path
    # you must change it
    # if you choose 'mcdr_command', we will execute pack command in this folder
    # if you choose 'folder', we will move this folder to 'plugins' folder
    # if you choose 'single_file', this path must be a file, maybe '.py' or '.mcdr'
    # Default: ./code
    mcdr_pack_extra_options = '--ignore-patterns __pycache__'
    # did you want to add some extra options when packing plugin by mcdr pack command?
    # see mcdr official docs for more details
    # Default: --ignore-patterns __pycache__ (will ignore __pycache__)

    def keys(self):
        return ('debug', 'core_server_url', 'auto_eula', 'plugins', 'python_path',
                'pip_path', 'env_path', 'method', 'plugin_code_path', 'mcdr_pack_extra_options')

    def __getitem__(self, item):
        return getattr(self, item)


logger = logging.getLogger('mcdr_debugger')

config = Config()


def main(args: list):
    if args[0] == 'gen_config':
        with open(r'./env1.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(dict(config)))
    if args[0] == 'init':
        pass


if __name__ == '__main__':
    main(sys.argv)
