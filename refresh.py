"""
Refresh script for hyperpm_core.

Ensures the VS Code Kanbn Boards extension is installed.
Run via: python adhd_framework.py refresh --module hyperpm_core
"""

from __future__ import annotations

import platform
import shutil
import subprocess
import sys
from pathlib import Path

# Ensure project root is in sys.path
if str(Path.cwd()) not in sys.path:
    sys.path.append(str(Path.cwd()))

from utils.logger_util.logger import Logger

VSCODE_KANBN_EXTENSION_ID = "samgiz.vscode-kanbn-boards"


def _get_vscode_cli_command() -> str | None:
    """
    Determine the VS Code CLI command based on OS.
    Returns the command string if found, None otherwise.
    """
    system = platform.system()
    
    if system == "Linux" or system == "Darwin":
        # Linux and macOS: 'code' should be in PATH
        if shutil.which("code"):
            return "code"
        # Check for code-insiders as fallback
        if shutil.which("code-insiders"):
            return "code-insiders"
    elif system == "Windows":
        # Windows: Check common locations
        if shutil.which("code"):
            return "code"
        if shutil.which("code.cmd"):
            return "code.cmd"
        if shutil.which("code-insiders"):
            return "code-insiders"
        if shutil.which("code-insiders.cmd"):
            return "code-insiders.cmd"
    
    return None


def _is_extension_installed(code_cmd: str, extension_id: str) -> bool:
    """Check if a VS Code extension is already installed."""
    try:
        result = subprocess.run(
            [code_cmd, "--list-extensions"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        installed_extensions = result.stdout.strip().split("\n")
        return extension_id.lower() in [ext.lower() for ext in installed_extensions]
    except (subprocess.TimeoutExpired, subprocess.SubprocessError):
        return False


def _install_extension(code_cmd: str, extension_id: str, logger: Logger) -> bool:
    """Install a VS Code extension. Returns True on success."""
    try:
        result = subprocess.run(
            [code_cmd, "--install-extension", extension_id],
            capture_output=True,
            text=True,
            timeout=120,
        )
        if result.returncode == 0:
            return True
        else:
            logger.warning(f"Extension install returned non-zero: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        logger.warning("Extension installation timed out")
        return False
    except subprocess.SubprocessError as e:
        logger.warning(f"Extension installation failed: {e}")
        return False


def main() -> None:
    """Ensure VS Code Kanbn Boards extension is installed."""
    logger = Logger(name="hyperpm_coreRefresh")
    logger.info("Starting hyperpm_core refresh...")

    system = platform.system()
    logger.info(f"Detected OS: {system}")

    # Find VS Code CLI
    code_cmd = _get_vscode_cli_command()
    if not code_cmd:
        logger.warning(
            "VS Code CLI not found in PATH. "
            "Please install VS Code and ensure 'code' command is available. "
            f"Extension '{VSCODE_KANBN_EXTENSION_ID}' may need manual installation."
        )
        logger.info("hyperpm_core refresh completed (skipped extension check).")
        return

    logger.info(f"Found VS Code CLI: {code_cmd}")

    # Check if extension is already installed
    if _is_extension_installed(code_cmd, VSCODE_KANBN_EXTENSION_ID):
        logger.info(f"Extension '{VSCODE_KANBN_EXTENSION_ID}' is already installed.")
    else:
        logger.info(f"Extension '{VSCODE_KANBN_EXTENSION_ID}' not found. Installing...")
        if _install_extension(code_cmd, VSCODE_KANBN_EXTENSION_ID, logger):
            logger.info(f"✅ Extension '{VSCODE_KANBN_EXTENSION_ID}' installed successfully.")
        else:
            logger.warning(
                f"⚠️ Could not install extension '{VSCODE_KANBN_EXTENSION_ID}'. "
                "Please install it manually from VS Code Extensions marketplace."
            )

    logger.info("hyperpm_core refresh completed successfully.")


if __name__ == "__main__":
    main()
