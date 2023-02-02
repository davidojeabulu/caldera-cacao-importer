"""
Main module for importing a Cacao playbook
"""
import sys

from typing import List

# # Add the root directory to the search path
current_dir: str = sys.path[0]
current_dir_path: List[str] = current_dir.split("/")[:-2]
root_dir: str = "/".join(current_dir_path)
sys.path.append(root_dir)

from ability_converter.cacao_importer import (
    construct_abilities, construct_profile, construct_sources
 )


def main(args: List[str]) -> None:
    # Construct the playbook and convert the workflow steps for each playbook
    # path given
    for cacao_playbooks_path in args[1:]:
        playbook = construct_abilities.CacaoPlaybook(cacao_playbooks_path)
        playbook.convert_workflow_steps()
        construct_sources.construct_sources(playbook.playbook)
        construct_profile.write_profile(playbook.playbook)

if __name__ == '__main__':
    main(sys.argv)
