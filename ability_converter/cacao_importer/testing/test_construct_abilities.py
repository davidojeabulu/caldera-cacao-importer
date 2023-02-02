"""
Module to test the construct_abilities.py module
"""
import builtins
import json
import random
import unittest.mock as mock

from copy import deepcopy
from typing import Dict

# pylint: disable=import-error, wrong-import-position
import ability_converter.cacao_importer.construct_abilities as construct_abilities

from ability_converter.cacao_importer.construct_abilities import (
    CacaoPlaybook
)
from ability_converter.cacao_importer.cacao_types import (
    CacaoPlaybookAttributes, CommandData, WorkflowStep
)

CacaoPlaybookClass: construct_abilities.CacaoPlaybook = (
    'ability_converter.cacao_importer.construct_abilities.CacaoPlaybook'
)
EXPECTED_GENERATED_ID = "01234567-89ab-4cde-fghi-jklmnopqrstu"

BASE_ABILITY = {
    'technique_id': "",
    'technique_name': "",
    'singleton': False,
    'repeatable': False,
    'delete_payload': False,
    'requirements': [],
    'executors': []
}

TEST_COMMANDS: Dict[str, CommandData] = {
    "Test Command 1": {
        'type': "http-api",
        'command': "Test HTTP-API Command",

    },
    "Test Command 2": {
        'type': "ssh",
        'command': "Test SSH Command",
    },
    "Test Command 3": {
        'type': "bash",
        'command': "Test Bash Command",
    },
    "Test Command 4": {
        'type': "openc2-json",
        'command': "Test OpenC2-JSON",
    },
    "Test Command 5": {
        'type': "attack-cmd",
        'command_b64': {
            'id': "Test Attack-CMD ID"
        },
    },
}

TEST_WORKFLOW: Dict[str, WorkflowStep] = {
    "step_01": {
        'type': "start",
        'name': "Test Start Step",
        'description': "Test Start Description",
        "on_completion": "step_02",
    },
    "step_02": {
        'type': "single",
        "name": "Test Single 1",
        "description": "Test Single Step 1 Description",
        "timeout": 0,
        "on_success": "step_03",
        "on_failure": "step_02",
        "commands": [
            TEST_COMMANDS["Test Command 1"],
            TEST_COMMANDS["Test Command 3"],
            TEST_COMMANDS["Test Command 5"],
        ],
        "out_args": [ "$$Test_Var_3$$" ]
    },
    "step_03": {
        'type': "single",
        "name": "Test Single 2",
        "description": "Test Single Step 2 Description",
        "timeout": 10,
        "on_completion": "step_04",
        "commands": [
            TEST_COMMANDS["Test Command 2"],
            TEST_COMMANDS["Test Command 4"],
        ],
        "in_args": [ "$$Test_Var_4$$" ],
    },
    "step_04": {
        'type': "playbook",
        "name": "",
        "description": "",
        "timeout": 0,
        "on_success": "step_05",
        "on_failure": "step_09",
        "in_args": [ "test_in_arg", "$$Test_Var_3$$" ],
        "out_args": [ "$$Test_Var_2$$", "$$Test_Var_1$$" ],
        "playbook_id": ""
    },
    "step_05": {
        'type': "parallel",
        "name": "Test Parallel",
        "description": "Test Parallel Description",
        "timeout": 0,
        "on_completion": "step_08",
        "next_steps": [ "step_02", "step_04" ]
    },
    "step_06": {
        'type': "if-condition",
        "name": "Test If Condition",
        "description": "Test If Condition Description",
        "timeout": 0,
        "on_completion": "step_07",
        "on_true": [ "step_02", "step_03"],
        "on_false": [ "step_04", "step_05" ]
    },
    "step_07": {
        'type': "while-condition",
        "name": "Test While Condition",
        "description": "Test While Condition Description",
        "timeout": 0,
        "on_success": "step_08",
        "on_failure": "step_09",
        "on_true": [ "step_02" ],
        "on_false": "step_09"
    },
    "step_08": {
        'type': "switch-condition",
        "name": "",
        "description": "",
        "timeout": 0,
        "on_completion": "step_09",
        "cases": {
            "1": [ "step_06" ],
            "2": [ "step_02", "step_04" ],
            "default": [ "step_03" ],
        },
    },
    "step_09": {
        'type': "end",
        'name': "Test End Step",
        'description': "Test End Description"
    },
}

TEST_PLAYBOOK_COPY: CacaoPlaybookAttributes = {
    'id': "Test Playbook ID",
    'name': "Test Playbook Name",
    'description': "Test Playbook Description",
    'playbook_variables': {
        "$$Test_Var_1$$": "",
        "$$Test_Var_2$$": "",
        "$$Test_Var_3$$": "",
        "$$Test_Var_4$$": "",
        "$$Test_Var_5$$": "",
    },
    'workflow_start': "step_01",
    'workflow': TEST_WORKFLOW
}

def test_generate_ability_id() -> None:
    """
    Test the generated_id function
    """
    with (mock.patch.object(random, attribute="sample",
    side_effect=construct_abilities.ALPHANUMERIC_CHARS)):
        generated_id = construct_abilities.generate_ability_id()

    assert generated_id == EXPECTED_GENERATED_ID

def test_wrong_path_to_playbook() -> None:
    """
    Test whether an exception is raised when attempting to load a playbook
    from an address which doesn't exist
    """
    # Patch the loading of the playbook to raise FileNotFoundError
    # Test succeeds if the exception is raised
    try:
        with mock.patch.object(
            builtins, attribute='open', side_effect=FileNotFoundError
        ):
            CacaoPlaybook("path_to_file")
    except FileNotFoundError:
        pass

def test_json_decoder_error() -> None:
    """
    Test whether an exception is raised when attempting to load a playbook
    from an address that's not in JSON format
    """
    # Patch the loading of the playbook to raise JSONDecoderError
    # Test succeeds if the exception is raised
    try:
        with mock.patch.object(
            json, attribute='loads', side_effect=json.decoder.JSONDecodeError
        ), mock.patch.object(builtins, attribute='open'
        ):
            CacaoPlaybook("path_to_file")
    except Exception:
        pass

def test_construct_requirements() -> None:
    """
    Test whether CacaoPlaybook method construct_requirements constructs the
    requirements correctly
    """
    test_playbook = deepcopy(TEST_PLAYBOOK_COPY)
    # Patch the loading of the playbook to return the test_playbook
    with mock.patch.object(builtins, attribute='open'
    ), mock.patch.object(
        json, attribute='loads', return_value=test_playbook
    ):
        playbook = CacaoPlaybook("path_to_file")
        generated_requirements = playbook.construct_requirements(
            TEST_WORKFLOW['step_04']
        )
        expected_requirments = [
            {'source': "Test Playbook Name.test_in_arg"},
            {'source': 'Test Playbook Name.Test_Var_3'},
        ]

    assert generated_requirements == expected_requirments

def test_construct_parsers() -> None:
    """
    Test whether CacaoPlaybook method construct_parsers constructs the
    parsers correctly
    """
    test_playbook = deepcopy(TEST_PLAYBOOK_COPY)
    # Patch the loading of the playbook to return the test_playbook
    with mock.patch.object(builtins, attribute='open'
    ), mock.patch.object(json, attribute='loads', return_value=test_playbook):
        playbook = CacaoPlaybook("path_to_file")
        generated_parsers = playbook.construct_parsers(
            TEST_WORKFLOW['step_04']
        )
        expected_parsers = [
            {'source': "Test Playbook Name.Test_Var_2"},
            {'source': 'Test Playbook Name.Test_Var_1'},
        ]

    assert generated_parsers == expected_parsers

def test_construct_playbook_facts() -> None:
    """
    Test whether CacaoPlaybook method construct_parsers constructs the
    playbook facts correctly
    """
    test_playbook = deepcopy(TEST_PLAYBOOK_COPY)
    # Patch the loading of the playbook to return the test_playbook
    with mock.patch.object(builtins, attribute='open'
    ), mock.patch.object(json, attribute='loads', return_value=test_playbook):
        playbook = CacaoPlaybook("path_to_file")
        generated_facts = playbook.construct_playbook_facts()
        expected_facts = [
            {'trait': "Test_Var_1", 'value': "", 'score': 1},
            {'trait': "Test_Var_2", 'value': "", 'score': 1},
            {'trait': "Test_Var_3", 'value': "", 'score': 1},
            {'trait': "Test_Var_4", 'value': "", 'score': 1},
            {'trait': "Test_Var_5", 'value': "", 'score': 1},
        ]

    assert generated_facts == expected_facts

def test_convert_workflow_step_type() -> None:
    """
    Test whether CacaoPlaybook method convert_workflow_step successfully calls
    the right step handler for each different value of the step attribute 'type'
    """
    test_playbook = deepcopy(TEST_PLAYBOOK_COPY)
    # Patch all of the methods that are expected to be called
    with mock.patch.object(builtins, attribute='open'
    ), mock.patch.object(json, attribute='loads', return_value=test_playbook
    ), mock.patch.object(CacaoPlaybook, attribute='handle_start_step'
    ) as mock1, mock.patch.object(CacaoPlaybook, attribute='handle_end_step'
    ) as mock2, mock.patch.object(
        CacaoPlaybook, attribute='handle_single_step'
    ) as mock3, mock.patch.object(
        CacaoPlaybook, attribute='handle_playbook_step'
    ) as mock4, mock.patch.object(
        CacaoPlaybook, attribute='handle_parallel_step'
    ) as mock5, mock.patch.object(
        CacaoPlaybook, attribute='handle_if_condition_step'
    ) as mock6, mock.patch.object(
        CacaoPlaybook, attribute='handle_while_condition_step'
    ) as mock7, mock.patch.object(
        CacaoPlaybook, attribute='handle_switch_condition_step'
    ) as mock8:
        playbook = CacaoPlaybook("path_to_file")

        # Convert each of the workflow steps exactly once
        for step_id in TEST_WORKFLOW:
            playbook.convert_workflow_step(step_id)

        # Assert that each handler was called the right number of times
        mocks = [mock1, mock2, mock4, mock5, mock6, mock7, mock8,]
        for mock_object in mocks:
            mock_object.assert_called_once()
        mock3.assert_has_calls([
            mock.call(test_playbook["workflow"]['step_02']),
            mock.call(test_playbook["workflow"]['step_03']),
        ])

def test_convert_workflow_step_converted() -> None:
    """
    Test that a step's attributed 'converted' is correctly updated and
    no handlers are called when a step has been converted already
    """
    test_playbook = deepcopy(TEST_PLAYBOOK_COPY)
    # Patch the loading of the playbook to return the test_playbook and
    # the expected callback for the step type
    with mock.patch.object(builtins, attribute='open'
    ), mock.patch.object(json, attribute='loads', return_value=test_playbook
    ), mock.patch.object(CacaoPlaybook, attribute='handle_start_step'
    ) as mock1:
        playbook = CacaoPlaybook("path_to_file")

        # Convert the same step twice
        playbook.convert_workflow_step("step_02")
        playbook.convert_workflow_step("step_02")

        # Check that the handler was called exactly once and 'converted'
        # attribute updated.
        mock1.assert_called_once()
        assert playbook.playbook['workflow']['step_02']['converted']

def test_handle_start_step() -> None:
    """
    Test whether CacaoPlaybook method handle_start_step correctly handles a
    workflow step with 'type' as 'start'
    """
    test_playbook = deepcopy(TEST_PLAYBOOK_COPY)
    # Patch the loading of the playbook to return the test_playbook and the
    # write_ability callback to ensure that it's called with the right arguments
    with mock.patch.object(builtins, attribute='open'
    ), mock.patch.object(json, attribute='loads', return_value=test_playbook
    ), mock.patch.object(construct_abilities, attribute='write_ability'
    ) as mock1, mock.patch.object(
        construct_abilities, attribute='generate_ability_id',
        return_value=EXPECTED_GENERATED_ID
    ):
        playbook = CacaoPlaybook("path_to_file")
        playbook.handle_start_step(playbook.playbook['workflow']["step_01"])

        expected_generated_ability = {
            'id': EXPECTED_GENERATED_ID,
            'name': 'Start Step',
            'description': "Start Step for Playbook: Test Playbook Name",
            'tactic': "Start",
            **BASE_ABILITY
        }
        mock1.assert_called_once_with(expected_generated_ability)

def test_handle_end_step() -> None:
    """
    Test whether CacaoPlaybook method handle_end_step correctly handles a
    workflow step with 'type' as 'end'
    """
    test_playbook = deepcopy(TEST_PLAYBOOK_COPY)
    # Patch the loading of the playbook to return the test_playbook and the
    # write_ability callback to ensure that it's called with the right arguments
    with mock.patch.object(builtins, attribute='open'
    ), mock.patch.object(json, attribute='loads', return_value=test_playbook
    ), mock.patch.object(construct_abilities, attribute='write_ability'
    ) as mock1, mock.patch.object(
        construct_abilities, attribute='generate_ability_id',
        return_value=EXPECTED_GENERATED_ID
    ):
        playbook = CacaoPlaybook("path_to_file")
        playbook.handle_end_step(playbook.playbook['workflow']["step_09"])

        expected_generated_ability = {
            'id': EXPECTED_GENERATED_ID,
            'name': 'End Step',
            'description': "End Step for Playbook: Test Playbook Name",
            'tactic': "End",
            **BASE_ABILITY
        }
        mock1.assert_called_once_with(expected_generated_ability)

def test_handle_parallel_step() -> None:
    """
    Test whether CacaoPlaybook method handle_parallel_step correctly handles a
    workflow step with 'type' as 'parallel'
    """
    test_playbook = deepcopy(TEST_PLAYBOOK_COPY)
    # Patch the loading of the playbook to return the test_playbook and the
    # handler callback to ensure that it's called with the right arguments
    with mock.patch.object(builtins, attribute='open'
    ), mock.patch.object(json, attribute='loads', return_value=test_playbook
    ), mock.patch.object(CacaoPlaybook, attribute='convert_workflow_step'
    ) as mock1:
        playbook = CacaoPlaybook("path_to_file")
        playbook.handle_parallel_step(TEST_WORKFLOW['step_05'])

        mock1.assert_has_calls([
            mock.call("step_02"),
            mock.call("step_04")
        ])

def test_handle_if_condition_step() -> None:
    """
    Test whether CacaoPlaybook method handle_if_condition_step correctly
    handles a workflow step with 'type' as 'if_condition'
    """
    test_playbook = deepcopy(TEST_PLAYBOOK_COPY)
    # Patch the loading of the playbook to return the test_playbook and the
    # handler callback to ensure that it's called with the right arguments
    with mock.patch.object(builtins, attribute='open'
    ), mock.patch.object(json, attribute='loads', return_value=test_playbook
    ), mock.patch.object(CacaoPlaybook, attribute='convert_workflow_step'
    ) as mock1:
        playbook = CacaoPlaybook("path_to_file")
        playbook.handle_if_condition_step(TEST_WORKFLOW['step_06'])

        mock1.assert_has_calls([
            mock.call("step_02"),
            mock.call("step_03"),
            mock.call("step_04"),
            mock.call("step_05")
        ])

def test_handle_while_condition_step() -> None:
    """
    Test whether CacaoPlaybook method handle_while_condition_step correctly
    handles a workflow step with 'type' as 'while_condition'
    """
    test_playbook = deepcopy(TEST_PLAYBOOK_COPY)
    # Patch the loading of the playbook to return the test_playbook and the
    # handler callback to ensure that it's called with the right arguments
    with mock.patch.object(builtins, attribute='open'
    ), mock.patch.object(json, attribute='loads', return_value=test_playbook
    ), mock.patch.object(CacaoPlaybook, attribute='convert_workflow_step'
    ) as mock1:
        playbook = CacaoPlaybook("path_to_file")
        playbook.handle_while_condition_step(TEST_WORKFLOW['step_07'])

        mock1.assert_has_calls([
            mock.call("step_02"),
            mock.call("step_09")
        ])

def test_handle_switch_condition_step() -> None:
    """
    Test whether CacaoPlaybook method handle_switch_condition_step correctly
    handles a workflow step with 'type' as 'switch_condition'
    """
    test_playbook = deepcopy(TEST_PLAYBOOK_COPY)
    # Patch the loading of the playbook to return the test_playbook and the
    # handler callback to ensure that it's called with the right arguments
    with mock.patch.object(builtins, attribute='open'
    ), mock.patch.object(json, attribute='loads', return_value=test_playbook
    ), mock.patch.object(CacaoPlaybook, attribute='convert_workflow_step'
    ) as mock1:
        playbook = CacaoPlaybook("path_to_file")
        playbook.handle_switch_condition_step(TEST_WORKFLOW['step_08'])

        mock1.assert_has_calls([
            mock.call("step_06"),
            mock.call("step_02"),
            mock.call("step_04"),
            mock.call("step_03")
        ])

def test_handle_single_step_bash() -> None:
    """
    Test whether CacaoPlaybook method handle_single_step correctly
    handles a workflow step with the 'type' of the command set to 'bash'
    """
    test_playbook = deepcopy(TEST_PLAYBOOK_COPY)
    executor_base = {
        'name': 'bash',
        'payloads': [],
        'uploads': [],
        'command': "Test Bash Command",
        'timeout': 0,
        'cleanup': [],
        'parsers': []
    }
    expected_executors = [
        {'platform': 'linux', **executor_base},
        {'platform': 'darwin', **executor_base},
        {'platform': 'windows', **executor_base},
    ]
    expected_ability = {
        'id': EXPECTED_GENERATED_ID,
        'name': "Test Single 1: 2",
        'tactic': "",
        **BASE_ABILITY,
        'description': "Test Single Step 1 Description",
        'executors': expected_executors
    }
    expected_unused_ability = {
        'id': EXPECTED_GENERATED_ID,
        'name': "Test Single 1: 1",
        'tactic': "",
        **BASE_ABILITY,
        'description': "Test Single Step 1 Description"
    }
    # Patch the loading of the playbook to return the test_playbook, the
    # write_ability callback to ensure that it's called with the right arguments
    # and the callbacks that handle the other command types
    with mock.patch.object(builtins, attribute='open'
    ), mock.patch.object(json, attribute='loads', return_value=test_playbook
    ), mock.patch.object(
        construct_abilities, attribute='handle_http_api_command'
    ), mock.patch.object(construct_abilities, attribute='write_ability'
    ) as mock1, mock.patch.object(
        construct_abilities, attribute='generate_ability_id',
        return_value=EXPECTED_GENERATED_ID
    ), mock.patch.object(
        CacaoPlaybook, 'construct_requirements', return_value=[]
    ), mock.patch.object(CacaoPlaybook, 'construct_parsers', return_value=[]
    ):
        playbook = CacaoPlaybook("path_to_file")
        playbook.handle_single_step(playbook.playbook['workflow']["step_02"])

        mock1.assert_has_calls([
            mock.call(expected_unused_ability),
            mock.call(expected_ability)
        ])

def test_handle_single_step_ssh() -> None:
    """
    Test whether CacaoPlaybook method handle_single_step correctly
    handles a workflow step with the 'type' of the command set to 'ssh'
    """
    test_playbook = deepcopy(TEST_PLAYBOOK_COPY)
    executor_base = {
        'payloads': [],
        'uploads': [],
        'command': "Test SSH Command",
        'timeout': 10,
        'cleanup': [],
        'parsers': []
    }
    expected_executors = [
        {'platform': 'linux', 'name': 'sh', **executor_base},
        {'platform': 'darwin', 'name': 'sh', **executor_base},
        {'platform': 'windows', 'name': 'pwsh', **executor_base},
    ]
    expected_ability = {
        'id': EXPECTED_GENERATED_ID,
        'name': "Test Single 2: 1",
        'tactic': "",
        **BASE_ABILITY,
        'description': "Test Single Step 2 Description",
        'executors': expected_executors
    }

    expected_unused_ability = {
        'id': EXPECTED_GENERATED_ID,
        'name': "Test Single 2: 2",
        'tactic': "",
        **BASE_ABILITY,
        'description': "Test Single Step 2 Description",
    }
    # Patch the loading of the playbook to return the test_playbook, the
    # write_ability callback to ensure that it's called with the right arguments
    # and the callbacks that handle the other command types
    with mock.patch.object(builtins, attribute='open'
    ), mock.patch.object(json, attribute='loads', return_value=test_playbook
    ), mock.patch.object(
        construct_abilities, attribute='handle_openc2_json_command'
    ), mock.patch.object(construct_abilities, attribute='write_ability'
    ) as mock1, mock.patch.object(
        construct_abilities, attribute='generate_ability_id',
        return_value=EXPECTED_GENERATED_ID
    ), mock.patch.object(
        CacaoPlaybook, 'construct_requirements', return_value=[]
    ), mock.patch.object(CacaoPlaybook, 'construct_parsers', return_value=[]
    ):
        playbook = CacaoPlaybook("path_to_file")
        playbook.handle_single_step(playbook.playbook['workflow']["step_03"])

        mock1.assert_has_calls([
            mock.call(expected_ability),
            mock.call(expected_unused_ability)
        ])

def test_handle_single_step_http_api() -> None:
    """
    Test whether CacaoPlaybook method handle_single_step correctly
    handles a workflow step with the 'type' of the command set to 'http-api'
    """
    test_playbook = deepcopy(TEST_PLAYBOOK_COPY)
    executor_base = {
        'payloads': [],
        'uploads': [],
        'command': "Test HTTP-API Command",
        'timeout': 0,
        'cleanup': [],
        'parsers': []
    }
    expected_executors = [
        {'platform': 'linux', 'name': 'sh', **executor_base},
        {'platform': 'darwin', 'name': 'sh', **executor_base},
        {'platform': 'windows', 'name': 'pwsh', **executor_base},
    ]
    expected_ability = {
        'id': EXPECTED_GENERATED_ID,
        'name': "Test Single 1: 1",
        'tactic': "",
        **BASE_ABILITY,
        'description': "Test Single Step 1 Description",
        'executors': expected_executors
    }

    expected_unused_ability = {
        'id': EXPECTED_GENERATED_ID,
        'name': "Test Single 1: 2",
        'tactic': "",
        **BASE_ABILITY,
        'description': "Test Single Step 1 Description"
    }

    # Patch the loading of the playbook to return the test_playbook, the
    # write_ability callback to ensure that it's called with the right arguments
    # and the callbacks that handle the other command types
    with mock.patch.object(builtins, attribute='open'
    ), mock.patch.object(json, attribute='loads', return_value=test_playbook
    ), mock.patch.object(construct_abilities, attribute='handle_bash_command'
    ), mock.patch.object(construct_abilities, attribute='write_ability'
    ) as mock1, mock.patch.object(
        construct_abilities, attribute='generate_ability_id',
        return_value=EXPECTED_GENERATED_ID
    ), mock.patch.object(
        CacaoPlaybook, 'construct_requirements', return_value=[]
    ), mock.patch.object(CacaoPlaybook, 'construct_parsers', return_value=[]
    ):
        playbook = CacaoPlaybook("path_to_file")
        playbook.handle_single_step(playbook.playbook['workflow']["step_02"])

        mock1.assert_has_calls([
            mock.call(expected_ability),
            mock.call(expected_unused_ability)
        ])

def test_handle_single_step_openc2_json() -> None:
    """
    Test whether CacaoPlaybook method handle_single_step correctly
    handles a workflow step with the 'type' of the command set to 'openc2-json'
    """
    test_playbook = deepcopy(TEST_PLAYBOOK_COPY)
    executor_base = {
        'name': 'native',
        'payloads': [],
        'uploads': [],
        'command': "Test OpenC2-JSON",
        'timeout': 10,
        'cleanup': [],
        'parsers': []
    }
    expected_executors = [
        {'platform': 'linux', **executor_base},
        {'platform': 'darwin', **executor_base},
        {'platform': 'windows', **executor_base},
    ]
    expected_ability = {
        'id': EXPECTED_GENERATED_ID,
        'name': "Test Single 2: 2",
        'tactic': "",
        **BASE_ABILITY,
        'description': "Test Single Step 2 Description",
        'executors': expected_executors
    }

    expected_unused_ability = {
        'id': EXPECTED_GENERATED_ID,
        'name': "Test Single 2: 1",
        'tactic': "",
        **BASE_ABILITY,
        'description': "Test Single Step 2 Description"
    }

    # Patch the loading of the playbook to return the test_playbook, the
    # write_ability callback to ensure that it's called with the right arguments
    # and the callbacks that handle the other command types
    with mock.patch.object(builtins, attribute='open'
    ), mock.patch.object(json, attribute='loads', return_value=test_playbook
    ), mock.patch.object(construct_abilities, attribute='handle_ssh_command'
    ), mock.patch.object(construct_abilities, attribute='write_ability'
    ) as mock1, mock.patch.object(
        construct_abilities, attribute='generate_ability_id',
        return_value=EXPECTED_GENERATED_ID
    ), mock.patch.object(
        CacaoPlaybook, 'construct_requirements', return_value=[]
    ), mock.patch.object(CacaoPlaybook, 'construct_parsers', return_value=[]
    ):
        playbook = CacaoPlaybook("path_to_file")
        playbook.handle_single_step(playbook.playbook['workflow']["step_03"])

        mock1.assert_has_calls([
            mock.call(expected_unused_ability),
            mock.call(expected_ability)
        ])

def test_handle_single_step_attack_cmd() -> None:
    """
    Test whether CacaoPlaybook method handle_single_step correctly
    handles a workflow step with the 'type' of the command set to 'attack-cmd'
    """
    test_playbook = deepcopy(TEST_PLAYBOOK_COPY)
    # Patch the loading of the playbook to return the test_playbook, the
    # write_ability callback to ensure that it's called the right number of
    # times
    with mock.patch.object(builtins, attribute='open'
    ), mock.patch.object(json, attribute='loads', return_value=test_playbook
    ), mock.patch.object(
        construct_abilities, attribute='handle_http_api_command'
    ), mock.patch.object(construct_abilities, attribute='handle_bash_command'
    ), mock.patch.object(construct_abilities, attribute='write_ability'
    ) as mock1:
        playbook = CacaoPlaybook("path_to_file")
        playbook.handle_single_step(playbook.playbook['workflow']["step_02"])

        assert mock1.call_count == 2
