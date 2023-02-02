"""
Module to test the construct_profile.py module
"""
from typing import Dict

# pylint: disable=import-error, wrong-import-position
from ability_converter.cacao_importer import construct_profile

from ability_converter.cacao_importer.cacao_types import WorkflowStep

TEST_WORKFLOW_STEPS: Dict[str, WorkflowStep] = {
    "step_id_01": {
        'type': 'test_type',
        'caldera_ability_ids': ["Test Id 1", "Test Id 2"]
    },
    "step_id_02": {
        'type': 'test_type',
        'caldera_ability_ids': ["Test Id 3"]
    },
    "step_id_03": {
        'type': 'test_type',
        'caldera_ability_ids': []
    },
}

def test_collate_caldera_ids() -> None:
    """
    Test the collate_caldera_ids function
    """
    collated_ids = construct_profile.collate_caldera_ids(TEST_WORKFLOW_STEPS)
    expected_caldera_ids = ["Test Id 1", "Test Id 2", "Test Id 3"]
    assert collated_ids == expected_caldera_ids
