"""
Module adds an ability to Caldera framework

Below are the inputs required to create an ability are found at:
https://caldera.readthedocs.io/en/latest/Basic-Usage.html
"""
import os
import string

import yaml

# pylint: disable=import-error, no-name-in-module
from ability_converter.ability_types import Ability

# Constant defining the set of alphanumeric characters
ALPHANUMERIC_CHARS = list(string.digits + string.ascii_lowercase)

def write_ability(ability: Ability) -> None:
    """
    Function creates yaml file consisting of the data of the input ability with
    the file name as ability[id].yml
    """
    # Construct the file_contents in the appropriate format using the contents
    # the ability
    file_contents: Ability = {
        "id": ability['id'],
        "name": ability['name'],
        "description": ability['description'],
        "tactic": ability['tactic'] or "Miscallaneous",
        "technique_id": ability['technique_id'] or "x|x",
        "technique_name": ability['technique_name'] or "Miscallaneous",
        "singleton": ability['singleton'],
        "repeatable": ability['repeatable'],
        "delete_payload": ability['delete_payload'],
        "requirements": ability['requirements'],
        "executors": ability['executors']
    }

    # Ensure directory containing abilities of the same tactic is created
    tactic_folder_path = f"data/abilities/{file_contents['tactic']}"
    file_name = (
        f"data/abilities/{file_contents['tactic']}/{file_contents['id']}.yml"
    )
    os.makedirs(tactic_folder_path, exist_ok=True)

    # Write the contents of the ability to the .yaml file
    with open(file_name, 'w') as file:
        yaml.dump([file_contents], file)
