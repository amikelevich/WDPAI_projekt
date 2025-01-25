#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

#pozwala na interakcję z komendami terminalowymi, odpala wszystko
#gdy wykonam komendę to idzie do settingsów, a tam jest podpięte m.in. api i inne opcje komunikacyjne
def main():
    """Run administrative tasks."""
    #settingsy backengu tutaj wrzucone
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
