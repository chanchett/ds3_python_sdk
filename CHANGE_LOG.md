Change Log
----------

* Rev 2.0: Support common SDK functional format
* Rev 1.5: Removed some pretty_print statements for XML where the DS3 appliance does not return any XML which was causing some exceptions to be thrown.
* Rev 1.4: Fixed an error where the `delete_bucket` command stated it needed a file argument.  Also corrected some spelling mistakes.
* Rev 1.3: Added in support for http proxies.  Updated the bulk commands to the latest FreeBSD build.  Added bulk put command to the cli.
* Rev 1.2: Improved how basic GETs copy files to a client.
* Rev 1.1: Initial release supporting basic list operations and basic gets and puts.
