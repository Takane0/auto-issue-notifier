# Auto Issue Notifier

A small Python bot that scans source files in a GitHub repo for leftover TODO comments and/or unresolved merge conflicts (marked by `<<<<<<<` or `>>>>>>>`). If any are found, it creates or updates an issue via GitHub's API notifying contributors of the problem locations.

The issue body now includes a little more location detail, like the line number and a short nearby snippet when available, so it is easier to jump to the problem.

## How to use

1. **Clone this repository into your project or copy the relevant files.**
2. Create a [GitHub Personal Access Token](https://github.com/settings/tokens), and set it in a `.env` file or via the config.
3. Edit `config.yaml` to configure which checks you want (TODOs, merge conflicts), which paths to include or exclude, and your repo info.
4. Install requirements:

    ```bash
    pip install -r requirements.txt
    ```

5. Run the script from your repo root:

    ```bash
    python main.py
    ```

## Files
- `main.py`: Entrypoint for running the scan and reporting issues.
- `scanner.py`: Scans files for TODOs and/or merge conflicts.
- `github_api.py`: Handles creating or updating issues via the GitHub API.
- `config.yaml`: Project-specific configuration.
- `test_scanner.py`: Basic tests for the scanner.

## Notes
- Requires Python 3.7+
- Only supports repositories you have write access to (needed to create issues).
