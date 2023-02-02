"""
Module which reads a CACAO playbook v1.0 and constructs the necessary abilities
to create a Caldera profile

For details on the Cacao playbook, see:
https://docs.oasis-open.org/cacao/security-playbooks/v1.0/security-playbooks-v1.0.html
"""
import json
import os
import random
import string

from typing import List

import ability_converter.cacao_importer.cacao_types as cacao_types

# pylint: disable=import-error, no-name-in-module
from ability_converter.cacao_importer.cacao_types import (
    CacaoPlaybookAttributes, WorkflowStep
)
from ability_converter.ability_types import (
    Ability, Executor, Fact, Parser
)
from ability_converter.write_ability import (
    write_ability
)

# Constant defining the set of alphanumeric characters
ALPHANUMERIC_CHARS = list(string.digits + string.ascii_lowercase)

def generate_ability_id() -> str:
    """
    Function generates a random ID of the form
    xxxxxxxx-xxxx-4xxx-xxxx-xxxxxxxxxxxx
    """
    generated_id: List[str] = list("xxxxxxxx-xxxx-4xxx-xxxx-xxxxxxxxxxxx")
    for index in enumerate(generated_id):
        # Replace each character 'x' with a random alphanumeric character
        generated_id[index[0]] = (
            random.sample(ALPHANUMERIC_CHARS, 1)[0]
            if (index[1] == 'x') else index[1]
        )
    return "".join(generated_id)


def handle_http_api_command(
    command_string: str,
    ability: Ability,
    step: WorkflowStep,
    parsers: List[Parser]
    ) -> None:
    """
    Handle a command with the command type set to 'http-api'
    """
    executor_base: Executor = {
        'payloads': [],
        'uploads': [],
        'command': command_string,
        'timeout': step['timeout'],
        'cleanup': [],
        'parsers': [parsers] if parsers else []
    }
    # Construct the executors
    linux_executor: Executor = {
        'platform': 'linux',
        'name': 'sh',
        **executor_base
    }
    darwin_executor: Executor = {
        'platform': 'darwin',
        'name': 'sh',
        **executor_base
    }
    windows_executor: Executor = {
        'platform': 'windows',
        'name': 'pwsh',
        **executor_base
    }

    # Add the executors to the ability
    ability['executors'] = [
        linux_executor, darwin_executor, windows_executor
        ]


def handle_ssh_command(
    command_string: str,
    ability: Ability,
    step: WorkflowStep,
    parsers: List[Parser]
    ) -> None:
    """
    Handle a command with the command type set to 'ssh'
    """
    executor_base: Executor = {
        'payloads': [],
        'uploads': [],
        'command': command_string,
        'timeout': step['timeout'],
        'cleanup': [],
        'parsers': [parsers] if parsers else []
    }
    # Construct the executors
    linux_executor: Executor = {
        'platform': 'linux',
        'name': 'sh',
        **executor_base
    }
    darwin_executor: Executor = {
        'platform': 'darwin',
        'name': 'sh',
        **executor_base
    }
    windows_executor: Executor = {
        'platform': 'windows',
        'name': 'pwsh',
        **executor_base
    }

    # Add the executors to the ability
    ability['executors'] = [
        linux_executor, darwin_executor, windows_executor
        ]


def handle_bash_command(
    command_string: str,
    ability: Ability,
    step: WorkflowStep,
    parsers: List[Parser]
    ) -> None:
    """
    Handle a command with the command type set to 'bash'
    """
    executor_base: Executor = {
        'name': 'bash',
        'payloads': [],
        'uploads': [],
        'command': command_string,
        'timeout': step['timeout'],
        'cleanup': [],
        'parsers': [parsers] if parsers else []
    }
    # Construct the executors
    linux_executor: Executor = {
        'platform': 'linux',
        **executor_base
    }
    darwin_executor: Executor = {
        'platform': 'darwin',
        **executor_base
    }
    windows_executor: Executor = {
        'platform': 'windows',
        **executor_base
    }

    # Add the executors to the ability
    ability['executors'] = [
        linux_executor, darwin_executor, windows_executor
        ]


def handle_openc2_json_command(
    command_string: str,
    ability: Ability,
    step: WorkflowStep,
    parsers: List[Parser]
    ) -> None:
    """
    Handle a command with the command type set to 'openc2-json'
    """
    executor_base: Executor = {
        'name': 'native',
        'payloads': [],
        'uploads': [],
        'command': command_string,
        'timeout': step['timeout'],
        'cleanup': [],
        'parsers': [ parsers ] if parsers else []
    }
    # Construct the executors
    linux_executor: Executor = {
        'platform': 'linux',
        **executor_base
    }
    darwin_executor: Executor = {
        'platform': 'darwin',
        **executor_base
    }
    windows_executor: Executor = {
        'platform': 'windows',
        **executor_base
    }

    # Add the executors to the ability
    ability['executors'] = [
        linux_executor, darwin_executor, windows_executor
        ]


class CacaoPlaybook:
    """Class object for a Cacao playbook"""

    def __init__(self, path_to_file: str) -> None:
        """Initialise CacaoPlaybook class"""
        # Load the Cacao playbook
        with open(path_to_file) as file:
            self.playbook: CacaoPlaybookAttributes = json.loads(file.read())

        # Give the playbook a Caldera ID, Sources ID and Operations ID
        self.playbook['caldera_id'] = generate_ability_id()
        self.playbook['sources_id'] = generate_ability_id()
        self.playbook['objective_id'] = generate_ability_id()

        # Initialise the playbook relationships
        self.playbook['relationships'] = []

    def construct_requirements(
        self,
        step: WorkflowStep
        ) -> List[Fact]:
        """
        Construct the requirement based on the command and workflow step
        """
        requirements: List[Fact] = []
        # Construct requirements only if 'in_args' attribute is present
        try:
            for in_arg in step['in_args']:
                fact: Fact = {}
                # If a variable is given, so has form $$VAR_NAME$$, obtain
                # VAR_NAME
                if in_arg[0] == "$" and in_arg[-1] == "$":
                    var_name: str = in_arg.split("$$")[1]
                    fact = {'source': f"{self.playbook['name']}.{var_name}"}
                    requirements.append(fact)
                else:
                    fact = {'source': f"{self.playbook['name']}.{in_arg}"}
                    requirements.append(fact)
        except KeyError:
            pass
        return requirements

    def construct_parsers(
        self,
        step: WorkflowStep
        ) -> List[Fact]:
        """
        Construct the parser based on the command and workflow step
        """
        parsers: List[Fact] = []
        # Construct requirments only if 'out_args' attribute is present
        try:
            for out_arg in step['out_args']:
                fact: Fact = {}
                # If a variable is given, so has form $$VAR_NAME$$, obtain
                # VAR_NAME
                if out_arg[0] == "$" and out_arg[-1] == "$":
                    var_name: str = out_arg.split("$$")[1]
                    fact = {'source': f"{self.playbook['name']}.{var_name}"}
                    parsers.append(fact)
                else:
                    fact = {'source': f"{self.playbook['name']}.{out_arg}"}
                    parsers.append(fact)
        except KeyError:
            pass
        return parsers

    def construct_playbook_facts(self) -> List[cacao_types.Fact]:
        """Construct the list of facts from the playbook variables"""
        facts: List[cacao_types.Fact] = []
        for var in self.playbook['playbook_variables']:
            # Obtain the var_name from $$var_name$$
            var_name: str = var.split("$$")[1]
            facts.append({'trait': var_name, 'value': "", 'score': 1})
        return facts

    def handle_single_step(
        self,
        step: WorkflowStep
        ) -> None:
        """
        Handle a workflow step with Workflow Step Type set to single
        """
        # Initialise the list of ability ids
        step['caldera_ability_ids'] = []

        # Use the corresponding handler depending on the command type
        # Note that commands of type 'manual' isn't handled
        for command in step['commands']:
            command_string: str = ""
            if command.get('command') is not None:
                command_string = command['command']
            elif command.get('command_b64') is not None:
                command_string = command['command_b64']

            if command['type'] == "attack-cmd":
                # Case in which the command is a Caldera ability
                step['caldera_ability_ids'].append(command_string['id'])
            else:
                ability: Ability = {
                    'id': generate_ability_id(),
                    'name': (
                        f"{step['name']}: {len(step['caldera_ability_ids'])+ 1}"
                    ),
                    'tactic': "",
                    'technique_id': "",
                    'technique_name': "",
                    'singleton': False,
                    'repeatable': False,
                    'delete_payload': False,
                    'description': step['description'],
                    'requirements': [],
                    'executors': []
                }

                # Construct the requirments and parsers for the command
                relationship_match = self.construct_requirements(step)
                ability['requirements'] = [{
                    'module': "plugins.stockpile.app.requirements.basic",
                    'relationship_match': relationship_match
                }] if relationship_match != [] else []
                parserconfigs = self.construct_parsers(step)
                parsers: Parser = [{
                    'module': "plugins.stockpile.app.parsers.basic",
                    'parserconfigs': parserconfigs
                }] if parserconfigs != [] else []

                # Append the list of ability ids used for the workflow step
                step['caldera_ability_ids'].append(ability['id'])

                # The list of arguments required to handle the command
                fn_args = [
                    command_string,
                    ability,
                    step,
                    parsers
                ]

                if command['type'] == "http-api":
                    handle_http_api_command(*fn_args)
                elif command['type'] == "ssh":
                    handle_ssh_command(*fn_args)
                elif command['type'] == "bash":
                    handle_bash_command(*fn_args)
                elif command['type'] == "openc2-json":
                    handle_openc2_json_command(*fn_args)

                # Write the ability to the Caldera library
                write_ability(ability)

    def handle_playbook_step(self, step: WorkflowStep) -> None:
        """
        Handle a workflow step with Workflow Step Type set to playbook
        """
        new_playbook_path: str = f"playbooks/{step['playbook_id']}"
        new_playbook: CacaoPlaybook = CacaoPlaybook(new_playbook_path)

        # Initialise 'facts' attribute if not initialised already
        if self.playbook.get('facts') is None:
            self.playbook['facts'] = []

        # Add the args of the embedded playbook as facts to the current playbook
        self.playbook['facts'].extend(self.construct_requirements(step))
        self.playbook['facts'].extend(self.construct_parsers(step))

        # Convert the workflow steps of the embedded playbook
        new_playbook.convert_workflow_steps()

        # Add any new facts from the embedded playbook to the current playbook
        self.playbook['facts'].extend(new_playbook.playbook['facts'])

    def handle_start_step(self, step: WorkflowStep) -> None:
        """
        Handle a workflow step with Workflow Step Type set to start
        """
        ability: Ability = {
            'id': generate_ability_id(),
            'name': "Start Step",
            'description': f"Start Step for Playbook: {self.playbook['name']}",
            'tactic': "Start",
            'technique_id': "",
            'technique_name': "",
            'singleton': False,
            'repeatable': False,
            'delete_payload': False,
            'requirements': [],
            'executors': []
        }

        # Create the list of ability ids used for the workflow step
        step['caldera_ability_ids'] = [ability['id']]

        # Construct the playbook facts from playbook
        self.playbook['facts'] = self.construct_playbook_facts()

        # Write the ability to the Caldera library
        write_ability(ability)

    def handle_end_step(self, step: WorkflowStep) -> None:
        """
        Handle a workflow step with Workflow Step Type set to end
        """
        ability: Ability = {
            'id': generate_ability_id(),
            'name': "End Step",
            'description': f"End Step for Playbook: {self.playbook['name']}",
            'tactic': "End",
            'technique_id': "",
            'technique_name': "",
            'singleton': False,
            'repeatable': False,
            'delete_payload': False,
            'requirements': [],
            'executors': []
        }

        # Append the list of ability ids used for the workflow step
        step['caldera_ability_ids']= [ability['id']]

        # Write the ability to the Caldera library
        write_ability(ability)

    def handle_parallel_step(self, step: WorkflowStep) -> None:
        """
        Handle a workflow step with Workflow Step Type set to parallel
        """
        for step_id in step['next_steps']:
            self.convert_workflow_step(step_id)

    def handle_if_condition_step(self, step: WorkflowStep) -> None:
        """
        Handle a workflow step with Workflow Step Type set to if-condition
        """
        # Convert the workflow steps from both conditions
        for step_id in step['on_true']:
            self.convert_workflow_step(step_id)
        for step_id in step['on_false']:
            self.convert_workflow_step(step_id)

    def handle_while_condition_step(self, step: WorkflowStep) -> None:
        """
        Handle a workflow step with Workflow Step Type set to while-condition
        """
        # Convert the workflow steps from both conditions
        for step_id in step['on_true']:
            self.convert_workflow_step(step_id)

        self.convert_workflow_step(step['on_false'])

    def handle_switch_condition_step(self, step: WorkflowStep) -> None:
        """
        Handle a workflow step with Workflow Step Type set to switch-condition
        """
        for step_ids in step['cases'].values():
            for step_id in step_ids:
                self.convert_workflow_step(step_id)

    def convert_workflow_step(self, step_id: str) -> None:
        """
        Convert a workflow step into a Mitre Ability
        """
        # Check if the step has been converted already
        if self.playbook['workflow'][step_id].get('converted') is None:
            self.playbook['workflow'][step_id]['converted'] = True
        else:
            return
        # Call the corresponding function handler depending on the Workflow
        # Step Type
        workflow_step_type: str = self.playbook['workflow'][step_id]['type']
        if workflow_step_type == "start":
            self.handle_start_step(self.playbook['workflow'][step_id])
        elif workflow_step_type == "end":
            self.handle_end_step(self.playbook['workflow'][step_id])
        elif workflow_step_type == "single":
            self.handle_single_step(self.playbook['workflow'][step_id])
        elif workflow_step_type == "playbook":
            self.handle_playbook_step(self.playbook['workflow'][step_id])
        elif workflow_step_type == "parallel":
            self.handle_parallel_step(self.playbook['workflow'][step_id])
        elif workflow_step_type == "if-condition":
            self.handle_if_condition_step(self.playbook['workflow'][step_id])
        elif workflow_step_type == "while-condition":
            self.handle_while_condition_step(self.playbook['workflow'][step_id])
        elif workflow_step_type == "switch-condition":
            self.handle_switch_condition_step(
                self.playbook['workflow'][step_id]
            )

        # Convert workflow step given for step completion, success or failure
        if self.playbook['workflow'][step_id].get('on_completion') is not None:
            self.convert_workflow_step(
                self.playbook['workflow'][step_id]['on_completion']
            )
        if self.playbook['workflow'][step_id].get('on_success') is not None:
            self.convert_workflow_step(
                self.playbook['workflow'][step_id]['on_success']
            )
        if self.playbook['workflow'][step_id].get('on_failure') is not None:
            self.convert_workflow_step(
                self.playbook['workflow'][step_id]['on_failure']
            )

    def convert_workflow_steps(self) -> None:
        """
        Convert the workflow steps of the Cacao playbook into a list of
        abilities
        """
        # Begin the cycle of converting workflow steps, beginning with the first
        # workflow step
        self.convert_workflow_step(self.playbook['workflow_start'])

        # Overwrite playbook with the included Caldera IDs
        path_to_playbook = f"playbooks/{self.playbook['id']}.json"
        os.makedirs("playbooks", exist_ok=True)
        with open(path_to_playbook, 'w') as playbook:
            playbook.write(json.dumps(self.playbook, indent=4))
