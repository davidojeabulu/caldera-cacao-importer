This package contains the necessary scripts required to construct a Mitre Caldera profile with the necessary abilities
that are within a Cacao playbook.

For more information on Mitre Caldera, see: https://github.com/mitre/caldera

## Installation

Ensure you are in the caldera directory then clone this repository into your workspace
```Bash
git clone https://github.com/davidojeabulu/caldera-cacao-importer.git --recursive
```

## Conversion of playbook

Ensure the path to playbook is not in a subdirectory of the caldera directory named 'playbooks' as
the updated playbooks will be stored here.

To convert the Cacao playbook, from the caldera directory, run the following command:
```Bash
python3 ability_converter/cacao_importer/main.py {PATH TO PLAYBOOK}.json  
```
If you wish to convert multiple playbooks concurrently, add all the paths to the different
playbooks in the command above

You will find in the directory data/adversaries .yml files describing each of the profiles
for each of the playbooks converted.

## Usage of profile within Caldera

* Within Caldera, navigate to the adversary page.
* In the search bar, search for the adversary with the same name as the playbook. (This is the 'name' attribute of the playbook)
* On selection, the list of generated abilties should present themselves. Amend each ability as necessary.
* Within Caldera, navigate to the fact sources page.
* Select 'Create Source' and then the button 'Add facts from Adversary' can now be selected.
* Search for the adversary which represents the created playbook and add all the facts.
* Then, set the desired fact values for the adversary.
* If necessary, do the same with rules and relationships.

The profile is now ready for use within an operation. Note that manual commands must be completed by
the user manually.
