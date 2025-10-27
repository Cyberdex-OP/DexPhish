# Copilot Instructions for DexPhish

## Overview
DexPhish is a pentesting phishing framework designed to simulate phishing campaigns and harvest data for security testing purposes. The project is structured into several key components, each serving a specific role in the framework's functionality.

## Architecture
- **`dexphish/modules`**: Contains the core modules of the framework, including:
  - `campaign.py`: Manages phishing campaigns.
  - `cloner.py`: Handles cloning of target websites.
  - `email.py`: Manages email-related functionality for phishing campaigns.
  - `harvester.py`: Collects and processes harvested data.
  - `server.py`: Implements the Flask-based web server for hosting phishing pages.
- **`dexphish/data`**: Stores data related to campaigns, including harvested data and cloned sites.
- **`dexphish/templates`**: Contains HTML templates for the phishing pages.
- **`dexphish/static`**: Holds static assets like CSS files.

## Developer Workflows
### Running the Application
To run the Flask server:
```bash
/bin/python3 dexphish/modules/server.py
```

### Installing Dependencies
Ensure all required Python packages are installed:
```bash
pip install -r requirements.txt
```

### Debugging
- Use logging to debug issues. Logs are configured in `server.py` using Python's `logging` module.
- Common issues include missing directories for templates or static files. Ensure these paths exist:
  - `dexphish/templates`
  - `dexphish/static`

### Testing
- No explicit test framework is set up. Add tests as needed for individual modules.

## Project-Specific Conventions
- **Logging**: All modules use Python's `logging` module for error reporting and debugging.
- **Directory Validation**: `server.py` includes functions to validate the existence of required directories before starting the server.

## Integration Points
- **Flask**: The web server is built using Flask. Ensure Flask is installed in the Python environment.
- **Data Storage**: Campaign data and harvested information are stored in JSON files under `dexphish/data`.

## Key Files
- `dexphish/modules/server.py`: Entry point for running the Flask server.
- `dexphish/data/campaigns.json`: Stores campaign configurations.
- `dexphish/templates/dashboard.html`: Main dashboard template.

## External Dependencies
- Flask: Used for the web server.
- Python 3.12: Ensure compatibility with this version.

## Example Commands
- Start the server:
  ```bash
  /bin/python3 dexphish/modules/server.py
  ```
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

## Notes
- Ensure the Python environment is correctly configured before running the application.
- Update `requirements.txt` if new dependencies are added.
