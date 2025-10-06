"""
Error handling utilities for consistent error messages and user feedback.

This module provides standardized error handling to improve user experience
and maintain consistency across the application.
"""

import time
from typing import Optional


def show_error_message(message: str, delay: float = 0.3) -> None:
    """
    Display an error message to the user with consistent formatting.
    
    :param message: Error message to display
    :param delay: Time to pause after showing the message (in seconds)
    :return: None
    """
    print(f"\n❌ {message}")
    time.sleep(delay)


def show_success_message(message: str, delay: float = 0.3) -> None:
    """
    Display a success message to the user with consistent formatting.
    
    :param message: Success message to display
    :param delay: Time to pause after showing the message (in seconds)
    :return: None
    """
    print(f"\n✓ {message}")
    time.sleep(delay)


def show_warning_message(message: str, delay: float = 0.3) -> None:
    """
    Display a warning message to the user with consistent formatting.
    
    :param message: Warning message to display
    :param delay: Time to pause after showing the message (in seconds)
    :return: None
    """
    print(f"\n⚠️  {message}")
    time.sleep(delay)


def handle_invalid_option(delay: float = 0.3) -> None:
    """
    Display standard message for invalid menu option.
    
    :param delay: Time to pause after showing the message (in seconds)
    :return: None
    """
    show_error_message("Unsupported option selected. Please try again.", delay)


def handle_invalid_ip(delay: float = 0.3) -> None:
    """
    Display standard message for invalid IP address.
    
    :param delay: Time to pause after showing the message (in seconds)
    :return: None
    """
    show_error_message("Invalid IP address, range, or subnet. Please try again.", delay)


def handle_sudo_required(delay: float = 0.3) -> None:
    """
    Display standard message when sudo privileges are required.
    
    :param delay: Time to pause after showing the message (in seconds)
    :return: None
    """
    show_warning_message(
        "Sudo not detected. Try another option or switch to SUDO.",
        delay
    )


def handle_missing_binary(binary_name: str, install_hint: Optional[str] = None, delay: float = 0.3) -> None:
    """
    Display message when a required binary is not found.
    
    :param binary_name: Name of the missing binary
    :param install_hint: Optional installation command hint
    :param delay: Time to pause after showing the message (in seconds)
    :return: None
    """
    message = f"{binary_name} not found."
    if install_hint:
        message += f" Install with: {install_hint}"
    show_error_message(message, delay)


def handle_keyboard_interrupt(message: str = "Operation cancelled by user.", delay: float = 0.3) -> None:
    """
    Handle keyboard interrupt (Ctrl+C) with a consistent message.
    
    :param message: Message to display
    :param delay: Time to pause after showing the message (in seconds)
    :return: None
    """
    print(f"\n\n{message}")
    time.sleep(delay)


if __name__ == "__main__":
    # This file is not meant to be run directly
    # It should be imported and used in other modules
    print("Wrong file selected for running\nPlease run 'main.py' file by using 'python main.py' command")
