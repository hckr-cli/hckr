.. hckr documentation master file, created by
   sphinx-quickstart on Wed Jun 12 20:06:39 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


Datetime Commands
=================
``hckr`` provides comprehensive utilities to work with different timezones and datetime operations.

The ``dt`` command suite includes:

- **Main dt command**: Display and format datetime information with timezone support
- **now subcommand**: Show current time in any timezone
- **convert_time subcommand**: Convert datetime between different timezones

All commands support the IANA timezone database format. For a complete list of valid timezones see `the IANA tz database <https://en.wikipedia.org/wiki/List_of_tz_database_time_zones>`_.

Key Features:

- **Timezone Support**: Full IANA timezone database support with intelligent error handling
- **Flexible Formatting**: Customizable datetime output formats
- **Error Handling**: Helpful error messages with timezone suggestions
- **Multiple Input Methods**: Support for both arguments and options for datetime input

commands
---------------
.. toctree::
    dt
