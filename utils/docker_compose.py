import os.path
import paramiko
from utils.create_obj import ConfigObj


def docker_compose_commands(root_path: str, compose_folder: str, config: ConfigObj, hostname: str) -> None:
    if not os.path.exists(os.path.join(root_path, compose_folder, 'docker-compose.yaml')):
        print('No Docker Compose File in folder! --> Watch out for the name! [docker-compose.yaml]')
        return
    else:
        # Create an SSH client
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # check if ssh key or just user
        if config.ssh_privat_path and config.sshkeys and config.ciuser:
            private_key = paramiko.RSAKey.from_private_key_file(config.ssh_privat_path)
            client.connect(hostname=hostname, username=config.ciuser,
                           pkey=private_key)
        elif config.ciuser and config.cipassword:
            client.connect(hostname=hostname, username=config.ciuser, password=config.cipassword)
        else:
            print('For the compose deployment you need to add a user to the config file!')
            return

        ftp_client = client.open_sftp()
        ftp_client.put(os.path.join(root_path, compose_folder, 'docker-compose.yaml'), 'docker-compose.yaml')

        # Execute Docker Compose up
        stdin, stdout, stderr = client.exec_command('sudo docker compose up -d')

        # Print output
        print(stdout.read().decode())
        print(stderr.read().decode())

        # Close connections
        ftp_client.close()
        client.close()
        return
