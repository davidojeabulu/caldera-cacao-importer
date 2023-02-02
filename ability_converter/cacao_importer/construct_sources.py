"""
Module for creating the fact sources and relationships of a
Cacao playbook to be used within Caldera
"""
from typing import List, TypedDict

import yaml

# pylint: disable=import-error, no-name-in-module
from ability_converter.cacao_importer.cacao_types import (
    CacaoPlaybookAttributes, Fact, Relationship
)

class Sources(TypedDict):
    """Class defining attributes of Sources"""
    id: str
    name: str
    facts: List[Fact]
    relationships: List[Relationship]

def construct_sources(playbook: CacaoPlaybookAttributes) -> None:
    """
    Write the yml file containing the sources and relationships of the
    playbook
    """
    sources: Sources = {
        'id': playbook['sources_id'],
        'name': f"{playbook['name']} sources",
        'facts': playbook['facts'],
        'relationships': playbook['relationships']
    }

    # Write the sources into the sources directory
    file_name: str = f"data/sources/{playbook['sources_id']}.yml"
    with open(file_name, 'w') as file:
        yaml.dump(sources, file)
