#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Date: 2013-12-08
# Authors: Ethan Hart/ Nikolaj Olsson

# This script will read the contents of a PAC subtitle file and can output
# timing information and text. It does not retain alignment, justification, and
# other formatting components. As of now, this converter works with Latin,
# Chinese (big5), Cyrillic, and Thai character sets.

# The PAC format was developed my Screen Electronics.
# This parser is based on code written by Nikolaj Olsson under the GNU General
# Public License. I have simply ported the PAC file parsing components from C#
# to Python for my purposes. Please check out and support his project over at
# http://www.nikse.dk/SubtitleEdit/


# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from sys import argv
import string
import re


CyrillicLetters =   [" ",  # 0x20
                    "!",  # 0x21
                    "Э",  # 0x22
                    "/",  # 0x23
                    "?",  # 0x24
                    ":",  # 0x25
                    ".",  # 0x26
                    "э",  # 0x27
                    "(",  # 0x28
                    ")",  # 0x29
                    ",",  # 0x2c
                    "_",  # 0x2d
                    "ю",  # 0x2e
                    ">",  # 0x3c
                    "Ф",  # 0x41
                    "И",  # 0x42
                    "C",  # 0x43
                    "B",  # 0x44
                    "У",  # 0x45
                    "F",  # 0x46
                    "Р",  # 0x48
                    "Ш",  # 0x49
                    "О",  # 0x4a
                    "Ь",  # 0x4d
                    "Т",  # 0x4e
                    "Ы",  # 0x53
                    "Ц",  # 0x57
                    "Ч",  # 0x58
                    "Я",  # 0x5a
                    "х",  # 0x5b
                    "ъ",  # 0x5d
                    ",",  # 0x5e
                    "-",  # 0x5f
                    "ф",  # 0x61
                    "и",  # 0x62
                    "с",  # 0x63
                    "в",  # 0x64
                    "у",  # 0x65
                    "a",  # 0x66
                    "п",  # 0x67
                    "p",  # 0x68
                    "ш",  # 0x69
                    "д",  # 0x6c
                    "ь",  # 0x6d
                    "т",  # 0x6e
                    "э",  # 0x6f
                    "з",  # 0x70
                    "ы",  # 0x73
                    "e",  # 0x74
                    "г",  # 0x75
                    "ц",  # 0x77
                    "ч",  # 0x78
                    "н",  # 0x79
                    "я",  # 0x7a
                    "Х",  # 0x7b
                    "Ъ",  # 0x7d
                    "Ю",  # 0x81
                    "ђ",  # 0x92
                    ",",  # 0x94
                    "-",  # 0x95
                    "і",  # 0x96
                    "ј",  # 0x98
                    "љ",  # 0x99
                    "ћ",  # 0x9b
                    "њ",  # 0x9a
                    "§",  # 0x9d
                    "џ",  # 0x9f
                    "C",  # 0xac
                    "D",  # 0xad
                    "E",  # 0xae
                    "F",  # 0xaf
                    "G",  # 0xb0
                    "H",  # 0xb1
                    "'",  # 0xb2
                    '"',  # 0xb3
                    "I",  # 0xb4
                    "J",  # 0xb5
                    "K",  # 0xb6
                    "L",  # 0xb7
                    "M",  # 0xb8
                    "N",  # 0xb9
                    "P",  # 0xba
                    "Q",  # 0xbb
                    "R",  # 0xbc
                    "S",  # 0xbd
                    "T",  # 0xbe
                    "U",  # 0xbf
                    "V",  # 0xc0
                    "W",  # 0xc2
                    "X",  # 0xc3
                    "Y",  # 0xc4
                    "Z",  # 0xc5
                    "b",  # 0xc6
                    "c",  # 0xc7
                    "d",  # 0xc8
                    "e",  # 0xc9
                    "f",  # 0xca
                    "g",  # 0xcb
                    "h",  # 0xcc
                    "i",  # 0xcd
                    "j",  # 0xce
                    "k",  # 0xcf
                    "l",  # 0xd1
                    "m",  # 0xd2
                    "n",  # 0xd3
                    "o",  # 0xd4
                    "p",  # 0xd5
                    "q",  # 0xd6
                    "r",  # 0xd7
                    "s",  # 0xd8
                    "t",  # 0xd9
                    "u",  # 0xda
                    "v",  # 0xdb
                    "w",  # 0xdc
                    "э",  # 0xdd
                    "ю",  # 0xde
                    "z",  # 0xdf
                    "ў",  # 0xe065
                    "ё",  # 0xe574
                    "ќ",  # 0xe272
                    "ѓ",  # 0xe275
                    "ї",  # 0xe596
                    "ш"]  # 0x6938

CyrillicCodes =     ['\x20',  # space
                    '\x21',  # !
                    '\x22',  # Э
                    '\x23',  # /
                    '\x24',  # ?
                    '\x25',  # :
                    '\x26',  # .
                    '\x27',  # э
                    '\x28',  # (
                    '\x29',  # )
                    '\x2c',  # ,
                    '\x2d',  # _
                    '\x2e',  # ю
                    '\x3c',  # >
                    '\x41',  # Ф
                    '\x42',  # И
                    '\x43',  # C
                    '\x44',  # В
                    '\x45',  # У
                    '\x46',  # F
                    '\x48',  # Р
                    '\x49',  # Ш
                    '\x4a',  # О
                    '\x4d',  # Ь
                    '\x4e',  # Т
                    '\x53',  # Ы
                    '\x57',  # Ц
                    '\x58',  # Ч
                    '\x5a',  # Я
                    '\x5b',  # х
                    '\x5d',  # ъ
                    '\x5e',  # ,
                    '\x5f',  # -
                    '\x61',  # ф
                    '\x62',  # и
                    '\x63',  # c
                    '\x64',  # в
                    '\x65',  # у
                    '\x66',  # a
                    '\x67',  # п
                    '\x68',  # p
                    '\x69',  # ш
                    '\x6c',  # д
                    '\x6d',  # ь
                    '\x6e',  # т
                    '\x6f',  # э
                    '\x70',  # з
                    '\x73',  # ы
                    '\x74',  # e
                    '\x75',  # г
                    '\x77',  # ц
                    '\x78',  # ч
                    '\x79',  # н
                    '\x7a',  # я
                    '\x7b',  # Х
                    '\x7d',  # Ъ
                    '\x81',  # Ю
                    '\x92',  # ђ
                    '\x94',  # ,
                    '\x95',  # -
                    '\x96',  # і
                    '\x98',  # ј
                    '\x99',  # љ
                    '\x9a',  # њ
                    '\x9b',  # ћ
                    '\x9d',  # §
                    '\x9f',  # џ
                    '\xac',  # C
                    '\xad',  # D
                    '\xae',  # E
                    '\xaf',  # F
                    '\xb0',  # G
                    '\xb1',  # H
                    '\xb2',  # '
                    '\xb3',  # "
                    '\xb4',  # I
                    '\xb5',  # J
                    '\xb6',  # K
                    '\xb7',  # L
                    '\xb8',  # M
                    '\xb9',  # N
                    '\xba',  # P
                    '\xbb',  # Q
                    '\xbc',  # R
                    '\xbd',  # S
                    '\xbe',  # T
                    '\xbf',  # U
                    '\xc0',  # V
                    '\xc2',  # W
                    '\xc3',  # X
                    '\xc4',  # Y
                    '\xc5',  # Z
                    '\xc6',  # b
                    '\xc7',  # c
                    '\xc8',  # d
                    '\xc9',  # e
                    '\xca',  # f
                    '\xcb',  # g
                    '\xcc',  # h
                    '\xcd',  # i
                    '\xce',  # j
                    '\xcf',  # k
                    '\xd1',  # l
                    '\xd2',  # m
                    '\xd3',  # n
                    '\xd4',  # o
                    '\xd5',  # p
                    '\xd6',  # q
                    '\xd7',  # r
                    '\xd8',  # s
                    '\xd9',  # t
                    '\xda',  # u
                    '\xdb',  # v
                    '\xdc',  # w
                    '\xdd',  # э
                    '\xde',  # ю
                    '\xdf',  # z
                    '\xe065',  # ў
                    '\xe574',  # ё
                    '\xe272',  # ќ
                    '\xe275',  # ѓ
                    '\xe596',  # ї
                    '\x6938']  # ш


class Paragraph:
    def __init__(self):
        return

    def __str__(self):
        return '{0} {1} {2}'.format(self.startTime, self.endTime, self.text)

    def __eq__(self, other):
        if self.text == other.text:
            return True
        else:
            return False


class TimeCode:
    def __init__(self, hours, minutes, seconds, milliseconds):
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds
        self.milliseconds = milliseconds

    def __str__(self):
        return '{0}:{1}:{2}:{3}'.format(self.hours, self.minutes, self.seconds,
                                        self.milliseconds)


def loadSubtitle(subtitle_file, codePage):
    with open(subtitle_file, 'rb') as inf:
        block = inf.read()  # read(1024)
        hex_bytes = []
        real_bytes = []
        for ch in block:
            code = hex(ord(ch))
            real_bytes.append(ch)
            hex_bytes.append(code)

    index = 0
    all_pars = []
    while index < len(real_bytes):
        paragraph = getPacParagraph(index, real_bytes, codePage)
        if paragraph is not None and len(paragraph.text) > 0:
            if len(all_pars) == 0:
                all_pars.append(paragraph)
            elif paragraph == all_pars[-1]:
                pass
            else:
                all_pars.append(paragraph)
        index += 1

    return all_pars


def normalizeText(text):
    text = text.replace('çs', 'š')
    text = text.replace('çS', 'Š')
    text = text.replace('çz', 'ž')
    text = text.replace('çZ', 'Ž')
    text = text.replace('çc', 'č')
    text = text.replace('çC', 'Č')

    return text


def getTimeCode(timeCodeIndex, byte_list):
    if timeCodeIndex > 0:
        highPart = ord(byte_list[timeCodeIndex]) + ord(byte_list[timeCodeIndex + 1]) * 256
        lowPart = ord(byte_list[timeCodeIndex + 2]) + ord(byte_list[timeCodeIndex + 3]) * 256
        highPart = str(highPart).zfill(6)
        lowPart = str(lowPart).zfill(6)

        hours = int(highPart[0:4])      # 0:4
        minutes = int(highPart[4:6])    # 4:2
        seconds = int(lowPart[2:4])     # 2:2
        frames = int(lowPart[4:6])      # 4:2

        frameRate = 25

        milliseconds = int((1000.0 / frameRate) * frames)

        return TimeCode(hours, minutes, seconds, milliseconds)

    else:
        return TimeCode(0, 0, 0, 0)


def decodeBig5(byte_list):
    # Given a list of bytes (2), return big5 char
    zh_char = ''.join(byte_list).decode('big5')

    return zh_char.encode('utf-8')


def getString(encoding, byte_list, index):
    """Decode a single byte character w/ specified encoding,
    return a utf-8 string"""

    byte = byte_list[index]
    try:
        char = ''.join(byte).decode(encoding)
    except UnicodeDecodeError:
        char = ''
    return char.encode('utf-8')


def getCyrillicString(encoding, byte_list, index):
    b = byte_list[index]
    if b >= '\x30' and b <= '\x39':
        return b.decode('ascii').encode('utf-8')

    try:
        idx = CyrillicCodes.index(b)
        if idx >= 0:
            char = CyrillicLetters[idx]
            #return b.decode('iso-8859-5').encode('utf-8')
            return char

        if len(byte_list) > index + 1:
            idx = CyrillicCodes.index(b * 256 + byte_list[index + 1])
            if idx >= 0:
                index += 1
                char = CyrillicLetters[idx]
                #return b.decode('iso-8859-5').encode('utf-8')
                return char
    except ValueError:
        return b


def isTarget(correct, paragraphs):
    if float(correct) / len(paragraphs) > 0.9:
        return True
    else:
        return False


def isThai(paragraphs):
    correct = 0
    for entry in paragraphs:
        text = entry.text

        # Remove punctuation, numbers, euro, and space from text
        text = text.replace('€', '')
        removables = string.punctuation + string.digits + ' '
        remove_punctuation_map = dict((ord(char), None) for char in (removables))
        text = ''.join([text.decode('utf-8').translate(remove_punctuation_map)])
        
        # Extract only thai characters from text
        thai_chars = ''.join(c for c in text if u'\u0e01' <= c <= u'\u0e5b')
        #print len(text), text
        #print len(thai_chars), thai_chars

        ratio = float(len(thai_chars)) / float(len(text)) # percentage of thai chars

        if len(text) < 10:
            if ratio != 1.0:
                isThai = False
            else:
                isThai = True
        else:
            if ratio >= 0.90:
                isThai = True
            else:
                isThai = False

        if isThai:
            correct += 1

    return isTarget(correct, paragraphs)


def getPacParagraph(index, real_bytes, codePage):
    while index < 15:
        index += 1

    con = True
    while con:
        index += 1
        if index + 20 >= len(real_bytes):
            return None
        if real_bytes[index] == '\xfe' and real_bytes[index - 15] == '\x60' or real_bytes[index - 15] == '\x61':
            con = False
        if real_bytes[index] == '\xfe' and real_bytes[index - 12] == '\x60' or real_bytes[index - 12] == '\x61':
            con = False

    feIndex = index

    # Not currently used
    #endDelimiter = '\x00'
    #alignment = real_bytes[feIndex + 1]
    #verticalAlignment = real_bytes[feIndex - 1]

    p = Paragraph()
    timeStartIndex = feIndex - 15

    if real_bytes[timeStartIndex] == '\x60':
        p.startTime = getTimeCode(timeStartIndex + 1, real_bytes)
        p.endTime = getTimeCode(timeStartIndex + 5, real_bytes)

    elif real_bytes[timeStartIndex + 3] == '\x60':
        timeStartIndex += 3
        p.startTime = getTimeCode(timeStartIndex + 1, real_bytes)
        p.endTime = getTimeCode(timeStartIndex + 5, real_bytes)
    else:
        return None

    textLength = ord(real_bytes[timeStartIndex + 9]) + ord(real_bytes[timeStartIndex + 10]) * 256
    maxIndex = timeStartIndex + 10 + textLength

    string_buffer = ''
    index = feIndex + 3
    preTextCode = ''.join(real_bytes[index + 1: index + 4])

    if preTextCode == 'W16':
        index += 5
    while index < len(real_bytes) and index <= maxIndex:
        if preTextCode == 'W16':
            if real_bytes[index] == '\xfe':
                string_buffer += ' '
                preTextCode = ''.join(real_bytes[index + 4: index + 7])
                if preTextCode == 'W16':
                    index += 7
                index += 2
            else:
                if ord(real_bytes[index]) == 0:
                    text = ''.join(real_bytes[index + 1: index + 2])
                    string_buffer += text
                else:
                    # Should be Chinese
                    byte_list = real_bytes[index: index + 2]
                    zh_char = decodeBig5(byte_list)
                    string_buffer += zh_char

                index += 1

        elif real_bytes[index] == '\xff':
            string_buffer += ' '

        elif real_bytes[index] == '\xfe':
            string_buffer += ' '
            index += 2

        elif codePage == 'latin':
            latin_char = getString('iso-8859-1', real_bytes, index)
            string_buffer += latin_char
        elif codePage == 'arabic':
            print 'Not currently supported'
            exit()
        elif codePage == 'hebrew':
            print 'Not currently supported'
            exit()
        elif codePage == 'cyrillic':
            cyril_char = getCyrillicString('iso-8859-5', real_bytes, index)
            string_buffer += cyril_char
            pass
        elif codePage == 'thai':
            string_buffer += getString('cp874', real_bytes, index)
        else:
            # Get encoding
            #string_buffer += 'char'
            pass

        index += 1

    if index + 20 >= len(real_bytes):
        return None

    p.text = normalizeText(string_buffer)
    return p


def main():
    subtitle_file = argv[1]
    if len(argv) > 2:
        codePage = argv[2]
        paragraphs = loadSubtitle(subtitle_file, codePage)
        for par in paragraphs:
            print par

    else:
        print 'Auto-detect encoding'

        # Try Latin:
        #paragraphs = loadSubtitle(subtitle_file, 'latin')

        # Check Chinese first, as Chinese does required codePage to be specified
        #print 'Chinese: ', isChinese(paragraphs)
        #isLatin(paragraphs)

        # Try Thai
        paragraphs = loadSubtitle(subtitle_file, 'thai')
        print 'Thai: ', isThai(paragraphs)


if __name__ == "__main__":
    main()
