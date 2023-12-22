# Welcome to ProxPyraDock 🚀💻

ProxPyraDock revolutionizes VM and Docker container deployments, specifically tailored for Proxmox environments. 
This powerful tool enables you to effortlessly clone and deploy multiple VMs from Proxmox templates, either to a 
single node or across an entire cluster. Combining Python, Terraform, and Docker-compose, it streamlines your
infrastructure management, offering a seamless, configurable experience through a simple config.json file. 
Whether you're a developer or a sysadmin, ProxPyraDock simplifies complex deployments, turning them into an efficient 
and enjoyable process. Dive into the future of deployment with ProxPyraDock – where simplicity meets scalability.

## Prerequisites

Before diving into ProxPyraDock, ensure you have the following prerequisites in place to guarantee a smooth and 
efficient deployment experience:

- **Working Python Environment**: ProxPyraDock is built on Python, so a functional Python environment is essential. 
Ensure Python is installed and properly configured on your system.

- **Proxmox Template**: You'll need a Proxmox template to clone VMs from. If you don't have one, check out my other  
[repository](https://github.com/thommue/ProxmoxPackerTemplates) for guidance on creating Proxmox templates using Packer.

- **Terraform Installation**: Terraform is a key component of ProxPyraDock. Make sure Terraform is installed on
your machine where you plan to run ProxPyraDock.

- **Docker Compose on Template**: If you intend to use the Docker Compose functionality of ProxPyraDock, ensure that 
Docker Compose is preinstalled on your Proxmox template.

By meeting these prerequisites, you'll be well-prepared to leverage all the powerful features of ProxPyraDock and 
streamline your VM and Docker deployments.

## Get started

- **config.json**: Generate a ``config.json`` file, like shown below to instruct the python script.
  - Default provider for terraform is bpg/proxmox, check out the [repo](https://github.com/bpg/terraform-provider-proxmox) 
  for more infos

```json
{
  "template_folder": "<folder_with_the_template> Default after clone: templates",
  "compose_folder": "<name_of_folder_for_the_docker_compose_file> Default after clone: docker-compose; Not needed if you do not want to deploy a docker...",
  "proxmox_api_url": "<your_proxmox_url> like: https://10.0.0.0:8006/api/json",
  "proxmox_username": "<your_proxmox_username>",
  "proxmox_password": "<your_password_to_log_into_proxmox>r",
  "terraform_provider": "bpg/proxmox",
  "proxmox_provider_plugin_version": "0.41.0",
  "tls_skip": true,
  "proxmox_nodes": [
    {
      "target_node": "<nem_of_you_proxmox_node>",
      "vm_clone_infos": [
        {
          "vm_name": "<name_of_you_vm>",
          "vm_id": 100,
          "vcpu": "4",
          "memory": "4092",
          "disk_size": "32",
          "storage_pool": "local-lvm",
          "ip": "10.0.0.10",
          "tags": "ubuntu-22-04,docker,nginx"
        }
      ],
      "gw": "10.0.0.1",
      "network_bridge": "vmbr0",
      "interface": "virtio"
    }
  ],
  "ciuser": "<vm_user_name> If not given, defaults to template one",
  "cipassword": "<vm_password> If not given, defaults to template one",
  "sshkeys": "<ssh_rsa> If not given, defaults to template one",
  "ssh_privat_path": "<path_to_privat_key_on_your_machine> Just needed for if you wanna to deploy a docker image, and just used local!",
  "proxmox_clone_template_id": 900
}
```

The configs allow multiple vm infos and / or multiple nodes like:

```json
{
    "proxmox_nodes": [
    {
      "target_node": "<nem_of_you_proxmox_node>",
      "vm_clone_infos": [
        {
          "vm_name": "<name_of_you_vm>",
          "vm_id": 100,
          "vcpu": "4",
          "memory": "4092",
          "disk_size": "32",
          "storage_pool": "local-lvm",
          "ip": "10.0.0.10",
          "tags": "ubuntu-22-04,docker,nginx"
        },
        {
          "vm_name": "<name_of_you_vm>",
          "vm_id": 101,
          "vcpu": "4",
          "memory": "4092",
          "disk_size": "32",
          "storage_pool": "local-lvm",
          "ip": "10.0.0.10",
          "tags": "ubuntu-22-04,docker,nginx"
        }
      ],
      "gw": "10.0.0.1",
      "network_bridge": "vmbr0",
      "interface": "virtio"
    },
    {
      "target_node": "<nem_of_you_proxmox_node>",
      "vm_clone_infos": [
        {
          "vm_name": "<name_of_you_vm>",
          "vm_id": 200,
          "vcpu": "4",
          "memory": "4092",
          "disk_size": "32",
          "storage_pool": "local-lvm",
          "ip": "10.0.0.10",
          "tags": "ubuntu-22-04,docker,nginx"
        }
      ],
      "gw": "10.0.0.1",
      "network_bridge": "vmbr1",
      "interface": "virtio"
    }
    ]
}
```

So just greate the ``config.json`` in the root folder and you are good to go. Have fun, and if there are any issues, 
please reach out.

### Hint
- for **mac** please remove in the ``deployment.py`` the ``Shell=True`` property, then the code works just fine for you.