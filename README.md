pypacc
======

A python utility to read the contents of a PAC Closed Caption (subtitle) file

usage:

    $ python readPac.py pac_file [encoding]

encoding: can be latin, thai, chinese, or cyrillic

If not encoding is provided, the program will attempt to determine the proper
character set.


Author(s)
=========

- Ethan Hart
    - ported portions of code from C# to python

- Nikolaj Olsson
    - wrote the PAC decoding logic


Information
===========

This script will read the contents of a PAC subtitle file and can output
timing information and text. It does not retain alignment, justification, and
other formatting components. As of now, this converter works with Latin
(iso-8859-1), Chinese (big5), Cyrillic (iso-8859-5), and Thai (cp874) character
sets. This program currently requires the user to specify the character encoding.

The PAC format was developed my Screen Electronics.
This parser is based on code written by Nikolaj Olsson under the GNU General
Public License. I have simply ported the PAC file parsing components from C#
to Python for my purposes. Please check out and support his project over at
http://www.nikse.dk/SubtitleEdit/


TO-DO
=====

- Add heuristics to determine if an encoding was successful or not
    - This will be used so the user does not need to know apriori what the
      encoding of the file is

- Implement parallel decoding in mulitple encodings

- Add Arabic and Hebrew support
