"""Module for creating a Caldera profile from a Cacao playbook"""
from typing import Dict, List, TypedDict

import yaml

# pylint: disable=import-error, no-name-in-module
from ability_converter.cacao_importer.cacao_types import (
    CacaoPlaybookAttributes, WorkflowStep
)
class CalderaProfile(TypedDict):
    """Class defining the attributes of a Caldera adversary profile"""
    adversary_id: str
    name: str
    description: str
    atomic_ordering: List[str]
    objective: str
    tags: List[str]


def collate_caldera_ids(workflow_steps: Dict[str, WorkflowStep]) -> List[str]:
    """Collate all of the ids of the abilities used within the playbook"""
    ids: List[str] = []
    for step in workflow_steps.values():
        ids.extend(step['caldera_ability_ids'])
    return ids


def write_profile(playbook: CacaoPlaybookAttributes) -> None:
    """Construct profile representing Cacao playbook and write .yml file"""
    profile: CalderaProfile = {
        'adversary_id': playbook['caldera_id'],
        'name': playbook['name'],
        'description': playbook['description'],
        'atomic_ordering': collate_caldera_ids(playbook['workflow']),
        'objective': playbook['objective_id'],
        'tags': []
    }

    # Write the profile into the adversaries directory
    file_name: str = f"data/adversaries/{profile['adversary_id']}.yml"
    with open(file_name, 'w') as file:
        yaml.dump(profile, file)
