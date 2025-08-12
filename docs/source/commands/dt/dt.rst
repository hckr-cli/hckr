dt - Datetime Utilities
=======================

The ``hckr dt`` command provides comprehensive datetime utilities with timezone support and conversion capabilities.

Overview
--------

``hckr dt`` offers three main functionalities:

1. **Main dt command**: Display datetime information in specific formats and timezones
2. **now subcommand**: Show current time in any timezone  
3. **convert_time subcommand**: Convert datetime between different timezones

Main dt Command
---------------

**Usage:** ``hckr dt [DATE] [OPTIONS]``

**Description:** Display datetime information in a specific format and timezone.

**Arguments:**
  - ``DATE`` (optional): Datetime input string in ISO format

**Options:**
  - ``-d, --date``: Datetime input string (can also be passed as argument)
  - ``-f, --format``: Datetime format (default: ``%d %B %Y, %I:%M:%S %p %Z``)
  - ``-z, --timezone``: Timezone for datetime parsing

**Examples:**

.. code-block:: bash

   # Show current time in default format
   hckr dt

   # Show current time in UTC timezone
   hckr dt --timezone UTC

   # Show current time in Asia/Kolkata timezone
   hckr dt --timezone Asia/Kolkata

   # Format a specific date
   hckr dt "2024-12-25T15:30:00"

   # Format a specific date with custom timezone
   hckr dt "2024-01-01T12:00:00" --timezone UTC

   # Use custom format
   hckr dt --format "%Y-%m-%d %H:%M:%S" --timezone UTC

   # Using the -d option instead of argument
   hckr dt -d "2024-01-01T12:00:00" -z UTC

now Subcommand
--------------

**Usage:** ``hckr dt now [OPTIONS]``

**Description:** Show current time in the given timezone.

**Options:**
  - ``-t, --timezone``: Timezone to display time in (default: UTC)

**Examples:**

.. code-block:: bash

   # Show current time in UTC (default)
   hckr dt now

   # Show current time in specific timezone
   hckr dt now --timezone "US/Pacific"

   # Show current time in Asia/Kolkata
   hckr dt now -t "Asia/Kolkata"

convert_time Subcommand
-----------------------

**Usage:** ``hckr dt convert_time [OPTIONS]``

**Description:** Convert datetime between different timezones.

**Options:**
  - ``--datetime``: Datetime in ISO format (required)
  - ``--from-tz``: Source timezone (required)
  - ``--to-tz``: Destination timezone (required)

**Examples:**

.. code-block:: bash

   # Convert from UTC to US/Pacific
   hckr dt convert_time --datetime "2024-01-01 10:00:00" --from-tz UTC --to-tz "US/Pacific"

   # Convert from Asia/Kolkata to Europe/London
   hckr dt convert_time --datetime "2024-06-15 14:30:00" --from-tz "Asia/Kolkata" --to-tz "Europe/London"

   # Convert from US/Eastern to Asia/Tokyo
   hckr dt convert_time --datetime "2024-12-25 09:00:00" --from-tz "US/Eastern" --to-tz "Asia/Tokyo"

Default Format
--------------

The default format is ``%d %B %Y, %I:%M:%S %p %Z`` which produces output like:

- ``25 December 2024, 03:30:00 PM IST``
- ``01 January 2024, 12:00:00 PM UTC``

Error Handling
--------------

The commands provide helpful error messages for invalid inputs:

**Invalid Timezone Example:**

.. code-block:: bash

   # This will show an error with suggestions
   hckr dt --timezone "India"
   # Output: Invalid timezone: India
   # Did you mean: Asia/Kolkata, Asia/Calcutta?

**Invalid Date Format Example:**

.. code-block:: bash

   # This will show an error with format guidance
   hckr dt "invalid-date"
   # Output: Invalid datetime string. Expected ISO format YYYY-MM-DD HH:MM:SS

Timezone Support
----------------

All commands support IANA timezone database format. Common examples include:

- ``UTC`` - Coordinated Universal Time
- ``US/Pacific`` - Pacific Time (US)
- ``US/Eastern`` - Eastern Time (US)
- ``Europe/London`` - London Time
- ``Asia/Kolkata`` - India Standard Time
- ``Asia/Tokyo`` - Japan Standard Time

For a complete list of valid timezones, see `the IANA tz database <https://en.wikipedia.org/wiki/List_of_tz_database_time_zones>`_.

Getting Help
------------

You can get help for any command:

.. code-block:: bash

   # General help
   hckr dt --help

   # Help for specific subcommands
   hckr dt now --help
   hckr dt convert_time --help
