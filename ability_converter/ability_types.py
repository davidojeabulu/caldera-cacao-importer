"""
Module defining the types used in the package.

Details of an ability are found here:
https://caldera.readthedocs.io/en/latest/Basic-Usage.html
"""
from typing import List, Optional, TypedDict

class Fact(TypedDict):
    """Custom class defining keys of a fact"""
    source: str
    edge: Optional[str]
    target: Optional[str]


class Parser(TypedDict):
    """Custom class defining keys of a parser"""
    module: str
    parserconfigs: List[Fact]

class Requirement(TypedDict):
    """Custom class defining keys of a requirement"""
    module: str
    relationship_match: List[Fact]


class Executor(TypedDict):
    """Custom class defining keys of an executor"""
    platform: str
    name: str
    payloads: List[str]
    uploads: List[str]
    command: List[str]
    timeout: Optional[int]
    cleanup: List[str]
    parsers: List[Parser]


class Ability(TypedDict):
    """Custom class defining keys of an ability"""
    id: str
    name: str
    description: str
    tactic: str
    technique_id: str
    technique_name: str
    singleton: bool
    repeatable: bool
    delete_payload: bool
    requirements: List[Requirement]
    executors: List[Executor]
