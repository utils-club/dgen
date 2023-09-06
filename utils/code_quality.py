import os
from subprocess import run


def prepare_code(path: str, run_prefix="poetry "):
    orders = [
        f"{run_prefix}python black {path}",
        f"{run_prefix}python isort {path}",
        f"{run_prefix}python flake8 {path}",
        f"git add {path}",
    ]
    for order in orders:
        run(order.split(" "), check=True)


def export_to_requirements():
    run(
        ["poetry", "export", "-f", "requirements.txt", "--output", "requirements.txt"],
        check=True,
    )
