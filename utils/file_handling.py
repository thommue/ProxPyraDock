import os
import shutil
from utils.create_obj import ProxmoxNode


def create_temp_folder() -> str:
    folder_name = "tmp"
    folder_path = os.path.join((os.getcwd()), folder_name)
    os.makedirs(folder_path)
    return folder_path


def handle_node_file_structure(folder_path: str, node: ProxmoxNode) -> str:
    tmp_path = os.path.join(folder_path, node.target_node)
    os.makedirs(tmp_path)
    return tmp_path


def remove_temp_folder(folder_path: str) -> None:
    shutil.rmtree(folder_path)
