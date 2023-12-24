import json
from typing import List, Optional
from pydantic import BaseModel


class VmClone(BaseModel):
    vm_name: str
    vm_id: int
    vcpu: str
    memory: str
    disk_size: str
    storage_pool: str
    ip: str
    tags: str


class ProxmoxNode(BaseModel):
    target_node: str
    vm_clone_infos: List[VmClone]
    gw: str
    network_bridge: str
    interface: str
    proxmox_clone_template_id: int


class ConfigObj(BaseModel):
    template_folder: str
    compose_folder: Optional[str]
    proxmox_api_url: str
    proxmox_username: str
    proxmox_password: str
    terraform_provider: str
    proxmox_provider_plugin_version: str
    tls_skip: bool
    proxmox_nodes: List[ProxmoxNode]
    ciuser: Optional[str]
    cipassword: Optional[str]
    sshkeys: Optional[str]
    ssh_privat_path: Optional[str]


class Config:
    def __init__(self, path_to_config_json: str):
        self.config = self._read_config(path_to_config_json=path_to_config_json)

    def get_config_obj(self) -> ConfigObj:
        proxmox_nodes = []
        for node in self.config['proxmox_nodes']:
            vm_clones = []
            for vm_info in node['vm_clone_infos']:
                vm_clones.append(
                    VmClone(
                        vm_name=vm_info["vm_name"],
                        vm_id=vm_info["vm_id"],
                        vcpu=vm_info["vcpu"],
                        memory=vm_info["memory"],
                        disk_size=vm_info["disk_size"],
                        storage_pool=vm_info["storage_pool"],
                        ip=vm_info["ip"],
                        tags=vm_info["tags"],
                    )
                )

            proxmox_nodes.append(
                ProxmoxNode(
                    target_node=node["target_node"],
                    vm_clone_infos=vm_clones,
                    gw=node["gw"],
                    network_bridge=node["network_bridge"],
                    interface=node["interface"],
                    proxmox_clone_template_id=node["proxmox_clone_template_id"]
                )
            )
        return ConfigObj(
            template_folder=self.config["template_folder"],
            compose_folder=self.config.get('compose_folder', None),
            proxmox_api_url=self.config["proxmox_api_url"],
            proxmox_username=self.config["proxmox_username"],
            proxmox_password=self.config["proxmox_password"],
            terraform_provider=self.config["terraform_provider"],
            proxmox_provider_plugin_version=self.config["proxmox_provider_plugin_version"],
            tls_skip=self.config["tls_skip"],
            proxmox_nodes=proxmox_nodes,
            ciuser=self.config.get('ciuser', None),
            cipassword=self.config.get('cipassword', None),
            sshkeys=self.config.get('sshkeys', None),
            ssh_privat_path=self.config.get('ssh_privat_path', None),
        )

    @staticmethod
    def _read_config(path_to_config_json: str) -> dict:
        # read in the config file
        with open(path_to_config_json, "r") as config_file:
            return json.load(config_file)
