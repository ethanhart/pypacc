pypacc
======

A Python utility to read the contents of a PAC Closed Caption (subtitle) file.


Usage
=====

Takes a PAC/FPC file as an argument with specific encoding as an optional argument.

    $ python readPac.py pac_file [encoding]

encoding: latin, thai, chinese, cyrillic, utf-8

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

The PAC format was developed my Screen Electronics.
This parser is based on code written by Nikolaj Olsson under the GNU General
Public License. I have simply ported the PAC file parsing components from C#
to Python. Please check out and support his project over at
http://www.nikse.dk/SubtitleEdit/


TO-DO
=====

- [X] Add heuristics to determine if an encoding was successful (needed if user
    doesn't know apriori what the encoding of the file is)
    - [X] Thai
    - [X] Chinese
    - [X] Latin
    - [X] Cyrillic

- [ ] Implement parallel decoding in mulitple encodings

- [ ] Add additional language/encodings support
    - [ ] Arabic
    - [ ] Hebrew
    - [ ] Greek
    - [X] UTF-8
