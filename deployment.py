import os
import time
import subprocess
from utils.create_obj import Config
from utils.docker_compose import docker_compose_commands
from utils.templating import render_provider_file, render_clone_data
from utils.file_handling import create_temp_folder, handle_node_file_structure, remove_temp_folder

# get the config obj
config_class = Config(path_to_config_json='config.json')
config = config_class.get_config_obj()

# generate a temporary file structure for terraform
root_folder = os.getcwd()
folder_path = create_temp_folder()

# now loop over each node and create the template
for node in config.proxmox_nodes:
    tmp_path = handle_node_file_structure(folder_path=folder_path, node=node)

    render_provider_file(
        template_path=os.path.join(root_folder, config.template_folder),
        tmp_path=tmp_path,
        config_obj=config
    )
    render_clone_data(
        template_path=os.path.join(root_folder, config.template_folder),
        tmp_path=tmp_path,
        config_obj=config
    )

    # now cd to node dir
    os.chdir(tmp_path)

    # terraform commands
    command = ["terraform", "init", "-upgrade"]
    process = subprocess.Popen(command)
    process.wait()
    print(process)

    command = ["terraform", "apply", "-auto-approve"]
    process = subprocess.Popen(command)
    process.wait()
    print(process)

    if config.compose_folder:
        # letting time for the init-config to process in the new cloned vm
        total_wait_time = 120
        while total_wait_time > 0:
            print(f"VM Init set uptime left: {total_wait_time} seconds")
            time.sleep(10)
            total_wait_time -= 10

        # docker-compose commands
        print("Docker Compose Setup Started")
        for vm in node.vm_clone_infos:
            docker_compose_commands(
                root_path=root_folder, compose_folder=config.compose_folder, config=config, hostname=vm.ip
            )

    # change back to root
    os.chdir(root_folder)

remove_temp_folder(folder_path=folder_path)
