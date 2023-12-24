import os
import shutil


def create_temp_folder() -> str:
    folder_name = "tmp"
    folder_path = os.path.join((os.getcwd()), folder_name)
    os.makedirs(folder_path)
    return folder_path


def remove_temp_folder(folder_path: str) -> None:
    shutil.rmtree(folder_path)
