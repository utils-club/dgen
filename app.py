"""Bootstrap django template created from yaml file in a django project
"""
import os
import re
import argparse

from subprocess import run
from yaml import safe_load
from contextlib import contextmanager

from jinja2 import Environment, FileSystemLoader

type_reg = re.compile("\-.+\-")
doc_reg = re.compile("\(.+\)")
base_dir = os.path.dirname(__file__)


@contextmanager
def project_env(project_path):
    current_dir = os.getcwd()
    os.chdir(project_path)
    yield
    os.chdir(current_dir)


def get_camelcase(word: str) -> str:
    info = word.capitalize()
    return "".join((a.capitalize() for a in info.split("_")))


def get_model_field(_type: str) -> str:
    return f"{_type}Field" if _type != "FK" else "ForeignKey"


def get_fields(metadata: list):
    answer = []
    for field in metadata["fields"]:
        if "," in field:
            info = [a.strip() for a in field.split(",")]
            _type = (
                "CharField"
                if not ((explicit := [a for a in info if type_reg.match(a)]))
                else get_model_field(explicit[0][1:-1])
            )
            _help = (
                ""
                if not (explicit := [a for a in info if doc_reg.match(a)])
                else explicit[0][1:-1]
            )
            answer.append(
                {
                    "name": info[0],
                    "type": _type,
                    "args": f'help="{_help}"',
                }
            )
        else:
            answer.append(
                {
                    "name": field,
                    "type": "CharField",
                    "args": "max_length=100",
                }
            )
    return answer


def get_methods(metadata: list):
    answer = []
    if "methods" in metadata:
        for method in metadata:
            if "," in method:
                info = [a.strip() for a in method.split(",")]
                _help = (
                    ""
                    if not (explicit := [a for a in info if doc_reg.match(a)])
                    else explicit[0][1:-1]
                )
                answer.append(
                    {
                        "name": info[0],
                        "description": _help,
                    }
                )
            else:
                answer.append({"name": method, "description": f"implements {method}"})
    return answer


def load_metadata(definition_file: str) -> dict:
    apps = []

    with open(definition_file, "r") as fl:
        definition = safe_load(fl)

    for app, meta in definition.items():
        description = description if (description := meta.get("description")) else ""
        if "description" in meta:
            meta.pop("description")
        entities = []
        if not (app == "users" and description == "auth"):
            for entity, metadata in meta.items():
                entities.append(
                    {
                        "name": get_camelcase(entity),
                        "_name": entity.lower(),
                        "fields": get_fields(metadata),
                        "methods": get_methods(metadata),
                        "description": description
                        if (description := metadata.get("description"))
                        else f"implements {entity}",
                    }
                )

        apps.append({"name": app, "description": description, "entities": entities})

    return apps


def build_django_app(app_name):
    order = ["python", "manage.py", "startapp", app_name]
    run(order, check=True)


def build_user_auth_app(project_path):
    build_django_app("users")
    template_dir = os.path.join(base_dir, "templates", "users")
    template_files = [a for a in os.listdir(template_dir) if a and a.endswith(".py")]
    for user_file in template_files:
        with open(os.path.join(template_dir, user_file), "r") as fl:
            code = fl.read()
        with open(os.path.join(project_path, "users", user_file), "w") as fl:
            fl.write(code)


def generate_apps(project_path: str, app_structure: str):
    app = load_metadata(app_structure)
    template_dir = os.path.join(base_dir, "templates")
    environment = Environment(loader=FileSystemLoader(template_dir))
    template_files = [a for a in os.listdir(template_dir) if a and a.endswith(".txt")]
    templates = {a: environment.get_template(a) for a in template_files}
    with project_env(project_path):
        for data in app:
            if data["name"] == "users" and data["description"] == "auth":
                build_user_auth_app(project_path)
            else:
                build_django_app(data["name"])
                contents = (
                    (
                        templates[a].render(app=data),
                        f'{data["name"]}/{a.split(".txt")[0]}.py',
                    )
                    for a in template_files
                )
                for content, target in contents:
                    with open(target, "w") as fl:
                        fl.write(content)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_path", help="absolute path to django project")
    parser.add_argument("app_structure", help="yaml file with app structure")
    args = parser.parse_args()
    generate_apps(args.project_path, args.app_structure)
