pypacc
======

A Python utility to read the contents of a PAC/FPC Closed Caption (subtitle) file.


Usage
=====

Takes a PAC/FPC file as an argument with specific encoding as an optional argument.

```
Usage: python readPac.py [options] pac_file

Options:
    -h, --help      show this help message and exit
    -e CODEPAGE, --encoding=CODEPAGE
                    encoding: latin, thai, chinese, cyrillic, utf-8
    -t, --text      write out text only
```

If no encoding is provided, the program will attempt to determine the proper
character set.


Author(s)
=========

- Ethan Hart
    - ported PAC decoding logic from C# to Python
    - wrote auto-dection/verification steps, rest of code

- Nikolaj Olsson
    - wrote the PAC decoding logic


Information
===========

This script will read the contents of a PAC/FPC subtitle file and can output
timing information and text. It does not retain alignment, justification, and
other formatting information. As of now, this converter works with PAC files
encoded using Latin (iso-8859-1), Chinese (big5), Cyrillic (iso-8859-5), Thai
(cp874), and UTF-8 character sets. Note: UTF-8 is likely only valid for FPC
files (a variation of the PAC format which uses Unicode as a standard).

The PAC format was developed by Screen Electronics.
This parser is based on code written by Nikolaj Olsson under the GNU General
Public License. I have simply ported the PAC file parsing components from C#
to Python. Please check out and support his project over at
http://www.nikse.dk/SubtitleEdit/

This work is sponsered by AppTek http://www.apptek.com
