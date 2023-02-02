"""
Module defining the types used in the package.

For details on the Cacao playbook, see:
https://docs.oasis-open.org/cacao/security-playbooks/v1.0/security-playbooks-v1.0.html
"""
# pylint: disable=missing-class-docstring
from typing import Dict, List, Optional, TypedDict, Union

class Fact(TypedDict):
    """Class defining attributes of a Fact used in constructing Sources"""
    trait: str
    value: Optional[str]
    score: int

class Relationship(TypedDict):
    """
    Class defining attributes of a Relationship used in constructing
    Sources
    """
    source: Fact
    edge: Optional[str]
    target: Fact
    score: int

class Variable(TypedDict):
    pass

class ExternalReferences(TypedDict):
    pass

class PlaybookFeatures(TypedDict):
    pass

class Signature(TypedDict):
    pass

class CommandData(TypedDict):
    type: str
    command: Optional[str]
    command_b64: Optional[bytes]
    version: Optional[str]

class Target(TypedDict):
    pass

class WorkflowStep(TypedDict):
    type: str
    name: Optional[str]
    description: Optional[str]
    external_references: Optional[List[ExternalReferences]]
    delay: Optional[int]
    timeout: Optional[int]
    step_variables: Optional[Variable]
    owner: Optional[str]
    on_completion: Optional[str]
    on_success: Optional[str]
    on_failure: Optional[str]
    step_extensions: Optional[Dict]
    # The following properties are defined when value of key 'type' is 'sing;e'
    commands: Optional[List[CommandData]]
    target: Optional[Target]
    target_ids: Optional[List[str]]
    in_args: Optional[List[str]]
    out_args: Optional[List[str]]
    # The following property is defined when value of key 'type' is 'playbook'
    playbook_id: Optional[str]
    # The following property is defined when value of key 'type' is 'parallel'
    next_steps: Optional[List[str]]
    # The following properties are defined when value of key 'type' is
    # 'if-condition' or 'while-condition'
    condition: Optional[str]
    on_true: Optional[List[str]]
    on_false: Optional[Union[str, List[str]]]
    # The following properties are defined when value of key 'type' is
    # 'switch-condition'
    switch: Optional[str]
    cases: Optional[Dict[str, List[str]]]
    # The list of ids of the abilities used in this workflow step within Caldera
    # in order of execution
    caldera_ability_ids: Optional[List[str]]
    # Boolean value to indicate whether the step has been converted
    converted: Optional[bool]

class CacaoPlaybookAttributes(TypedDict):
    type: str
    spec_version: str
    id: str
    name: str
    description: Optional[str]
    playbook_types: List[str]
    created_by: str
    created: str
    modified: str
    revoked: Optional[bool]
    valid_from: Optional[str]
    valid_until: Optional[str]
    derived_from: Optional[List[str]]
    priority: Optional[int]
    severity: Optional[int]
    impact: Optional[int]
    labels: Optional[int]
    external_references: Optional[List[ExternalReferences]]
    features: Optional[List[PlaybookFeatures]]
    markings: Optional[List[str]]
    playbook_variables: Optional[Dict[str, Variable]]
    workflow_start: Optional[str]
    workflow_exception: Optional[str]
    workflow: Optional[Dict[str, WorkflowStep]]
    targets: Optional[Dict]
    extension_definitions: Optional[Dict]
    data_marking_definitions: Optional[Dict]
    signatures: Optional[List[Signature]]
    # A unique ID to be used within Caldera
    caldera_id: Optional[str]
    # A unique ID to reference the sources used within Caldera
    sources_id: Optional[str]
    # A unique ID toreference the operation used within Caldera
    objective_id: Optional[str]
    # Attributes to store the facts/relationships within the playbook
    facts: Optional[List[Fact]]
    relationships: Optional[List[Relationship]]
