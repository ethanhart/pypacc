pypacc
======

A python utility to read the contents of a PAC Closed Caption (subtitle) file


Author(s)
=========

Ethan Hart (ported portions of code from C# to python)
Nikolaj Olsson (wrote the software this project is based on)


Information
===========

This script will read the contents of a PAC subtitle file and can output
timing information and text. It does not retain alignment, justification, and
other formatting components. As of now, this converter works with Latin,
Chinese (big5), Cyrillic, and Thai character sets. This program currently
requires the user to specify the character encoding.

The PAC format was developed my Screen Electronics.
This parser is based on code written by Nikolaj Olsson under the GNU General
Public License. I have simply ported the PAC file parsing components from C#
to Python for my purposes. Please check out and support his project over at
http://www.nikse.dk/SubtitleEdit/


TO-DO
=====

- Add heuristics to determine if an encoding was successful or not
    - This will be used so the user does not need to know aprior what the
      encoding of the file is

- Implement parallel decoding in mulitple encodings

- Add Arabic and Hebrew support
