import json
import logging
import os
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse

import requests
from tqdm import tqdm


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


def execute_command(cmd: str, default_decision_code: int = 1):
    def exe():
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while True:
            line = process.stdout.readline()
            if not line:
                process.wait()
                logger.info(f'Operation finished. Exit code: {process.returncode}')
                break
            print(line)
        return process.returncode
    while True:
        if exe() != 0:  # TODO: specific mcdr version
            logger.debug('Failed!')
            if err_note(f'Failed to execute {cmd}', default_decision_code) == 0:
                break
            else:
                continue
        else:
            break


def err_note(msg: str, default: int) -> int:
    # Return code: 1: exit now!  0: ignore this error  -1: repeat this operation
    logger.debug(f'We run into an error. Message: {msg}. Default decision code: {default}')
    logger.error(msg)
    if default == 0:
        def_s = 'ignore this error'
    elif default == 1:
        def_s = 'exit now!'
    elif default == -1:
        def_s = 'repeat this operation'
    else:
        def_s = 'exit now!'
    print('Unfortunately, the last operation was failed, what shall I do?')
    print(f'Press e for exit now, i for ignore this error, r for repeat this operation. Default option: {def_s}')
    var1 = input().lower()
    if var1 == 'e':
        logger.debug('Decision code is 1.')
        raise
    elif var1 == 'i':
        logger.debug('Decision code is 0')
        return 0
    elif var1 == 'r':
        logger.debug('Decision code is -1')
        return -1
    else:
        logger.debug(f'Decision code is {default}')
        if default == 1:
            raise
        return default


def install_mcdr(cu_pip_exe_path):
    execute_command(f'{cu_pip_exe_path} install mcdreforged', default_decision_code=-1)


def init_env_mcdr(cu_python_exe_path):
    cu_p = os.getcwd()
    os.chdir(config.env_path)
    execute_command(f'{cu_python_exe_path} -m mcdreforged init', default_decision_code=1)
    os.chdir(cu_p)


def download_plugins():
    logger.info('Downloading plugins')
    plugin_folder_path = os.path.join(os.path.abspath(config.env_path), 'plugins')
    logger.debug(f'Plugin path: {plugin_folder_path}')

    for url in config.plugins:
        logger.info(f'Downloading {url}')

        logger.debug('Sending HEAD request...')
        response = requests.head(url)
        logger.debug('HEAD request was sent.')
        content_length = response.headers.get('content-length')
        logger.debug(f'Content length: {content_length}')

        pbar = tqdm(total=int(content_length), unit='B', unit_scale=True)

        response = requests.get(url, stream=True)
        logger.debug('GET request was sent.')

        plg_file_path = os.path.join(plugin_folder_path, urlparse(url).path.split("/")[-1])
        #Path(plg_file_path).touch()

        with open(plg_file_path, 'wb') as f:
            for chunk in response.iter_content(1024):  # chunk size: 1KB
                if chunk:
                    f.write(chunk)
                    pbar.update(len(chunk))
        pbar.close()
        logger.info(f'Download complete!')
    logger.info('Plugins download completed!')


def download_minecraft_core_jar():
    # TODO
    raise NotImplementedError


def agree_eula():
    # TODO
    raise NotImplementedError


def main(args: list):
    global config

    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('[%(asctime)s] %(name)s %(levelname)s: %(message)s',
                                           datefmt='%Y-%m-%d %H:%M:%S'))
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

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

        if config.debug is True:
            logger.info('Logging level is set to debug.')
            logger.setLevel(logging.DEBUG)

        # mkdir and init mcdr
        logger.info('Checking environment...')
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
        elif os.path.isfile(config.env_path):
            logger.fatal(f'{config.env_path} is a file!')
            raise
        else:
            logger.info('Fine. We will create a new environment.')

        logger.debug('Creating env folders.')
        os.mkdir(config.env_path)

        if config.python_path == '':
            cu_python_exe_path = 'python3'
        else:
            cu_python_exe_path = config.python_path
        if config.pip_path == '':
            cu_pip_exe_path = 'pip3'
        else:
            cu_pip_exe_path = config.pip_path

        logger.info(f'Python path: {cu_python_exe_path}')
        logger.info(f'pip path: {cu_pip_exe_path}')

        print(f'Shall I install the latest mcdreforged package by using {cu_pip_exe_path}? [y/N]')
        var1 = input().lower()
        if var1 == 'yes' or var1 == 'y':
            logger.info('Installing latest mcdreforged')
            install_mcdr(cu_pip_exe_path)
        print(f'Shall I init mcdreforged now in env path? [y/N]')
        var1 = input().lower()
        if var1 == 'yes' or var1 == 'y':
            init_env_mcdr(cu_python_exe_path)
        print(f'Shall I download mcdr plugins which you want? (plugin list can be changed in env config file) [y/N]')
        var1 = input().lower()
        if var1 == 'yes' or var1 == 'y':
            download_plugins()
        print(f'Shall I download minecraft server core jar now? [y/N]')
        var1 = input().lower()
        if var1 == 'yes' or var1 == 'y':
            download_minecraft_core_jar()
        print(f'Shall I agree the eula in eula.txt now? [y/N]')
        var1 = input().lower()
        if var1 == 'y' or var1 == 'yes':
            agree_eula()
    if args[1] == 'test':
        logger.info('Plugin test started.')
        # TODO
        raise NotImplementedError


if __name__ == '__main__':
    main(sys.argv)
