# Silver-hand

An advanced automated vulnerability assessment and PoC exploitation platform.

## Features

-   **Advanced Scanning:** Detects a wide range of vulnerabilities including XSS, SQL Injection, and LFI.
-   **PoC Generation:** Automatically generates Proof-of-Concept exploits for discovered vulnerabilities.
-   **AI-Powered Analysis:** Utilizes AI to provide intelligent analysis and recommendations.
-   **Dangerous Mode:** Includes a `--dangerous` mode for advanced and potentially disruptive tests.
-   **Customizable Reports:** Generates reports in various formats (JSON, XML, HTML, TXT).

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/your-username/silver-hand.git
    cd silver-hand
    ```

2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3.  Install the package in editable mode:
    ```bash
    pip install -e .
    ```

## Usage

### Basic Scan

```bash
python -m silverhand.cli --target http://example.com --scan-all
```

### Scan with PoC Generation

```bash
python -m silverhand.cli --target http://example.com --scan-all --poc
```

### Dangerous Mode

> **Warning:** Use with caution. This mode can perform disruptive tests.

```bash
python -m silverhand.cli --target http://example.com --scan-all --dangerous
```

### AI Chat

Start an interactive session with the AI security assistant.

```bash
python -m silverhand.cli --ai-chat
```

### List Modules

List all available scanning modules.

```bash
python -m silverhand.cli --list-modules
```

## Disclaimer

This tool is for educational and authorized testing purposes only. Do not use it on any system without explicit permission. The author is not responsible for any misuse or damage caused by this tool.
