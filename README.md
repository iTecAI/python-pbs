# python-pbs
Modern python wrapper for OpenPBS

## Environment Setup
- The PBS libraries MUST be in `$LD_LIBRARY_PATH`. These generally live in `/opt/pbs/lib`, but that may vary depending on the system.

## Development
- Clone the github repository
- Run `poetry build` in the main directory
- Run `poetry install --no-root` in the main directory
