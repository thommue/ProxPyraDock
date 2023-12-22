import os
from jinja2 import Environment, FileSystemLoader
from utils.create_obj import ConfigObj


def render_provider_file(template_path: str, tmp_path: str, config_obj: ConfigObj) -> None:
    # render
    template = Environment(loader=FileSystemLoader(template_path)).get_template('provider.tf.j2')
    rendered_content = template.render(config=config_obj)

    # save
    with open((os.path.join(tmp_path, "provider.tf")), "w") as terra_file:
        terra_file.write(rendered_content)


def render_clone_data(template_path: str, tmp_path: str, config_obj: ConfigObj) -> None:
    # render
    template = Environment(loader=FileSystemLoader(template_path)).get_template('clone.tf.j2')
    rendered_content = template.render(config=config_obj)

    # save
    with open((os.path.join(tmp_path, "clone.tf")), "w") as clone_file:
        clone_file.write(rendered_content)
