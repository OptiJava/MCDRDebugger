import json
import logging
import os
import shutil
import sys


class Config:
    def __init__(self,
                 debug=False,
                 core_server_url='https://piston-data.mojang.com/v1/objects/8dd1a28015f51b1803213892b50b7b4fc76e594d'
                                 '/server.jar',
                 auto_eula=False,
                 plugins=None,
                 python_path='',
                 pip_path='',
                 env_path='./env',
                 method='mcdr_command',
                 plugin_code_path=r'./code',
                 mcdr_pack_extra_options='--ignore-patterns __pycache__'
                 ):

        self.debug = debug

        ##########
        # minecraft server configurations
        self.core_server_url = core_server_url
        # will download server core file from this url
        # Default: 1.20.4 vanilla server url from mojang
        self.auto_eula = auto_eula
        # should I agree the eula automatically?
        # Default: False

        ##########
        # mcdreforged configurations
        if plugins is None:
            self.plugins = []
        else:
            self.plugins = plugins
        # did you need other mcdr plugins? add the download url here!
        # Default: empty
        self.python_path = python_path
        # python executable file path
        # Default: blank (will use 'python3 ...' command in default shell later)
        self.pip_path = pip_path
        # pip executable file path
        # Default: blank (will use 'pip3 ...' command in default shell later)
        self.env_path = env_path
        # will init mcdr in this path
        # Default: ./env

        ##########
        # mcdreforged plugin packaging configurations
        self.method = method
        # how can I package your plugin?
        # Options:
        #   mcdr_command: use mcdr pack command
        #   folder: move the whole folder to the 'plugins' folder
        #   single_file: move the single file to the 'plugins' folder
        # Default: mcdr_command
        self.plugin_code_path = plugin_code_path
        # the whole plugin code should in this path
        # you must change it
        # if you choose 'mcdr_command', we will execute pack command in this folder
        # if you choose 'folder', we will move this folder to 'plugins' folder
        # if you choose 'single_file', this path must be a file, maybe '.py' or '.mcdr'
        # Default: ./code
        self.mcdr_pack_extra_options = mcdr_pack_extra_options
        # did you want to add some extra options when packing plugin by mcdr pack command?
        # see mcdr official docs for more details
        # Default: --ignore-patterns __pycache__ (will ignore __pycache__)

    # def keys(self):
    #    return ('debug', 'core_server_url', 'auto_eula', 'plugins', 'python_path',
    #            'pip_path', 'env_path', 'method', 'plugin_code_path', 'mcdr_pack_extra_options')

    # def __getitem__(self, item):
    #    return getattr(self, item)


class MetaData:
    def __init__(self, initialized):
        self.initialized = False
        # will mark as True after init


logger = logging.getLogger('mcdr_debugger')

config = Config()


def main(args: list):
    global config
    if args[1] == 'gen_config':
        logger.info('Generating default config file.')
        with open(r'./env1.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(config.__dict__))
    if args[1] == 'init':
        # read config
        logger.info(f'Reading config file at {args[2]}')
        with open(args[2], 'r', encoding='utf-8') as f:
            def dict2config(d):
                return Config(d['debug'], d['core_server_url'], d['auto_eula'], d['plugins'], d['python_path'],
                              d['pip_path'], d['env_path'], d['method'], d['plugin_code_path'],
                              d['mcdr_pack_extra_options'])

            config = json.loads(f.read(), object_hook=dict2config)

        # mkdir and init mcdr
        if os.path.exists(config.env_path) and os.path.isdir(config.env_path):
            if os.path.exists(os.path.join(config.env_path, 'metadata.json')):
                with open(os.path.join(config.env_path, 'metadata.json'), 'r', encoding='utf-8') as f1:
                    def dict2config2(d):
                        return MetaData(d['initialized'])

                    if json.loads(f1.read(), object_hook=dict2config2).initialized:
                        logger.fatal('###@@@@@@@ Environment has already initialized! @@@@@@@###')
                        raise
            print('We found that the specific env path is existed.')
            print('Shall I clear everything in that folder? [y/N]')
            var1 = input().lower()
            if var1 == 'y' or var1 == 'yes':
                shutil.rmtree(config.env_path)
            else:
                logger.fatal('Cancelled.')
                raise
        elif not os.path.isdir(config.env_path):
            logger.fatal(f'{config.env_path} is a file!')
            raise

        os.mkdir(config.env_path)
        os.chdir(config.env_path)

        if config.python_path == '':
            cu_python_exe_path = 'python3'
        else:
            cu_python_exe_path = config.python_path
        if config.pip_path == '':
            cu_pip_exe_path = 'pip3'
        else:
            cu_pip_exe_path = config.pip_path

        print(f'Shall I install the latest mcdreforged package by using {cu_pip_exe_path}? [y/N]')
        var1 = input().lower()
        if var1 == 'yes' or var1 == 'y':
            os.system(f'{cu_pip_exe_path} install mcdreforged')  # TODO: specific mcdr version
        print(f'Shall I init mcdreforged now in env path? [y/N]')
        var1 = input().lower()
        if var1 == 'yes' or var1 == 'y':
            os.system(f'{cu_python_exe_path} -m mcdreforged init')
        print(f'Shall I download mcdr plugins which you want? (plugin list can be changed in env config file) [y/N]')
        var1 = input().lower()
        if var1 == 'yes' or var1 == 'y':
            # TODO
            pass
        print(f'Shall I download minecraft server core jar now? [y/N]')
        var1 = input().lower()
        if var1 == 'yes' or var1 == 'y':
            # TODO
            pass
        print(f'Shall I agree the eula in eula.txt now? [y/N]')
        var1 = input().lower()
        if var1 == 'y' or var1 == 'yes':
            # TODO
            pass


if __name__ == '__main__':
    main(sys.argv)
