# MCDRDebugger

> A small tool which can debug your mcdr plugin faster :)

## CLI Usage

- `python3 main.py gen_config`: Generate a default config file(env1.json) in current path.
- `python3 main.py init <config_file_path>`: Init a testing environment. You will debug your plugin by this environment.
- `python3 main.py test <config_file_path>`: Test your plugin.

## Config

```
        ##########
        # Log
        
        debug
        # Default: false


        ##########
        # minecraft server configurations
        
        core_server_url
        # if this is empty, we will not download server core file
        # will download server core file from this url
        # Default: 1.20.4 vanilla server url from mojang
        
        auto_eula
        # should I agree the eula automatically?
        # Default: False


        ##########
        # mcdreforged configurations
        
        plugins
        # did you need other mcdr plugins? add the download url here!
        # Default: empty list
        
        python_path
        # python executable file path
        # Default: blank (will use 'python3 ...' command in default shell later)
        
        pip_path
        # pip executable file path
        # Default: blank (will use 'pip3 ...' command in default shell later)
        
        env_path
        # will init mcdr in this path
        # Default: ./env


        ##########
        # mcdreforged plugin packaging configurations
        
        method
        # how can I package your plugin?
        # Options:
        #   mcdr_command: use mcdr pack command
        #   folder: move the whole folder to the 'plugins' folder
        #   single_file: move the single file to the 'plugins' folder
        # Default: mcdr_command
        
        plugin_code_path
        # the whole plugin code should in this path
        # you must change it
        # if you choose 'mcdr_command', we will execute pack command in this folder
        # if you choose 'folder', we will move this folder to 'plugins' folder
        # if you choose 'single_file', this path must be a file, maybe '.py' or '.mcdr'
        # Default: ./code
        
        mcdr_pack_extra_options
        # did you want to add some extra options when packing plugin by mcdr pack command?
        # see mcdr official docs for more details
        # -i & -o options will be filled automatically by this script. You mustn't add -i or -o option.
        # Default: --ignore-file .gitignore
```