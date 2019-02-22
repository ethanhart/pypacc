#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Date: 2013-12-08
# Authors: Ethan Hart/ Nikolaj Olsson

# This script will read the contents of a PAC/FPC subtitle file and can output
# timing information and text. It does not retain alignment, justification, and
# other formatting components. As of now, this converter works with Latin,
# Chinese (big5), Cyrillic, Thai, and UTF-8 character sets. Note: UTF-8 is
# likely only valid for FPC files (a variation of the PAC format which uses
# Unicode as a standard).

# This work is sponsered by AppTek <http://www.apptek.com>.

# The PAC format was developed by Screen Electronics.
# This parser is based on code written by Nikolaj Olsson under the GNU General
# Public License. I have simply ported the PAC file parsing components from C#
# to Python for my purposes. Please check out and support his project over at
# <http://www.nikse.dk/SubtitleEdit/>


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


from optparse import OptionParser
import string
import sys
import re

CyrillicLetters = [" ",  # 0x20
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

CyrillicCodes = ['\x20',  # space
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
    """
    Reads in PAC file as binary data,
    extracts text and timing information
    """

    with open(subtitle_file, 'rb') as inf:
        block = inf.read()  # read(1024)
        real_bytes = []
        for ch in block:
            real_bytes.append(ch)

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
    """Some simple text normalization"""

    rep = {'çs': 'š', 'çS': 'Š', 'çz': 'ž',
           'çZ': 'Ž', 'çc': 'č', 'çC': 'Č',
           '€': '', '，': '', '？': '', '…': ''}
    rep = dict((re.escape(k), v) for k, v in rep.iteritems())
    pattern = re.compile("|".join(rep.keys()))
    text = pattern.sub(lambda m: rep[re.escape(m.group(0))], text)

    return text


def getTimeCode(timeCodeIndex, byte_list):
    """Extract time code"""

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

        return TimeCode(str(hours).rjust(2,"0"), str(minutes).rjust(2,"0"), str(seconds).rjust(2,"0"), str(milliseconds).rjust(3,"0"))

    else:
        return TimeCode(0, 0, 0, 0)


def decodeBig5(byte_list):
    """
    Given a list of bytes (2-byte sequence),
    return big5 char
    """

    zh_char = ''.join(byte_list).decode('big5')

    return zh_char.encode('utf-8')


def getString(encoding, byte_list, index):
    """
    Decode a single byte character w/ specified encoding,
    return a utf-8 string
    """

    byte = byte_list[index]
    try:
        char = ''.join(byte).decode(encoding)
    except UnicodeDecodeError:
        char = ''
    return char.encode('utf-8')


def getUTF8String(encoding, byte_list, index):
    """
    Decode a byte or sequence of bytes (up to 4) with utf-8,
    return a utf-8 string
    """

    for idx in range(4):
        byte = byte_list[index: index + idx]
        char = ''
        try:
            char = ''.join(byte).decode(encoding)
        except UnicodeDecodeError:
            pass
        if char.encode('utf-8') == '' or char.encode('utf-8') == '﻿':
            pass
        elif char != '':
            return char.encode('utf-8')

    return char.encode('utf-8')


def getCyrillicString(encoding, byte_list, index):
    """Extract Cyrillic string from byte sequence"""

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


def isTarget(correct, paragraphs, min_thresh):
    if float(correct) / paragraphs > min_thresh:
        return True
    else:
        return False


def isEncoding(paragraphs, lang):
    """
    Compare decoded characters with unicode characters. The decoded characters
    should have at least a minimmum amount of 'in range' characters.
    """

    # Define unicode blocks
    if lang == 'chinese':
        block = {'start': u'\u4e00', 'end': u'\u9fff'}
        len_thresh = 3
    elif lang == 'thai':
        block = {'start': u'\u0e01', 'end': u'\u0e5b'}
        len_thresh = 10
    elif lang == 'cyrillic':
        block = {'start': u'\u0400', 'end': u'\u04ff'}
        len_thresh = 10
    elif lang == 'latin':
        block = {'start': u'\u0000', 'end': u'\u007f'}  # Latin-1 char set
        len_thresh = 10

    correct = 0
    for entry in paragraphs:
        text = entry.text

        try:
            # Remove punctuation, numbers, euro, and space from text
            removables = string.punctuation + string.digits
            remove_punct_map = dict((ord(char), None) for char in (removables))
            text = ''.join([text.decode('utf-8').translate(remove_punct_map)])
            text = text.replace(' ', '')

            # Extract only specific characters from text
            if lang == 'latin':
                chars = ''.join(c for c in text if u'{0}'.format(c).isalpha())

                # Assume that a valid latin string will contain *some* latin_1
                # chars, so if no latin_1 chars are found, assume invalid
                # string
                latin_1 = ''.join(c for c in text if block['start'] <= c <=
                        block['end'])
                if len(latin_1) == 0:
                    chars = ''
            else:  # All encodings except latin
                chars = ''.join(c for c in text if block['start'] <= c <= block['end'])

            # Ratio of chars in unicode block
            if float(len(text)) == 0:
                 print "Could not determine character encoding from file"
                 sys.exit(1)
            
            ratio = float(len(chars)) / float(len(text))

            if len(text) < len_thresh:  # For short text, must be 100% accurate
                if ratio == 1.0:
                    isLang = True
                else:
                    isLang = False
                    #print 'Orig2: ', text.encode('utf-8')  # for debugging
                    #print 'Char2: ', chars.encode('utf-8')  # for debugging
            else:
                if ratio >= 0.90:
                    isLang = True
                else:
                    #print 'Orig: ', text.encode('utf-8')
                    #print 'Char: ', chars.encode('utf-8')
                    isLang = False

            if isLang:
                correct += 1

        except UnicodeDecodeError:  # Typically problems with 0xe7
            pass

    return isTarget(correct, len(paragraphs), 0.9)


def getPacParagraph(index, real_bytes, codePage):
    """Main PAC decoding function"""

    while index < 15:
        index += 1

    con = True
    while con:
        index += 1
        if index + 20 >= len(real_bytes):
            return None
        if real_bytes[index] == '\xfe' and \
           real_bytes[index - 15] == '\x60' or \
           real_bytes[index - 15] == '\x61':
            con = False
        if real_bytes[index] == '\xfe' and \
           real_bytes[index - 12] == '\x60' or \
           real_bytes[index - 12] == '\x61':
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
            #latin_char = getString('utf-8', real_bytes, index)
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
        elif codePage == 'utf-8' or codePage == 'utf8':
            string_buffer += getUTF8String('utf-8', real_bytes, index)
        else:
            pass

        index += 1

    if index + 20 >= len(real_bytes):
        return None

    p.text = normalizeText(string_buffer)
    #p.text = string_buffer
    return p


def rreplace(s, old, new, occurrence):
    li = s.rsplit(old, occurrence)
    return new.join(li)

# From http://stackoverflow.com/questions/2556108/how-to-replace-the-last-occurence-of-an-expression-in-a-string

def writeOut(paragraphs, outForm, file):
    i = 1
    strRtn = ""
    for line in paragraphs:
        if outForm == "text":
            strRtn += line.text
            i += 1
        elif outForm == "SRT":
            strRtn += str(i) + "\n"
            strRtn += rreplace(str(line.startTime),":",",",1) + " --> " + rreplace(str(line.endTime),":",",",1) + "\n"
            strRtn += line.text + "\n"
            strRtn += "\n"
            i += 1
        else:
            strRtn += line
            i += 1

    if file:
        target = open(file, 'w')
        target.write(strRtn)
        target.close()
    else:
        print strRtn

    exit()


def autoDetect(subtitle_file):
    """
    Automatically detect character encoding.
    Run through various encodings and compare decoded text with unicode
    character blocks (using isEncoding())
    """

    encodings = ['thai', 'cyrillic', 'latin']  # DO NOT CHANGE THIS ORDER

    attempts = 0
    for code in encodings:
        paragraphs = loadSubtitle(subtitle_file, code)
        if attempts == 0:
            # Chinese is detected regardless of specified encoding
            if isEncoding(paragraphs, 'chinese'):
                return paragraphs
        if isEncoding(paragraphs, code):
                return paragraphs
        attempts += 1

    # Try UTF-8 as last resort:
    paragraphs = loadSubtitle(subtitle_file, 'utf-8')
    return paragraphs


def main():
    usage = "usage: python readPac.py [options] pac_file"
    availableOutputs = ["SRT","SRT"]
    parser = OptionParser(usage=usage)
    parser.add_option("-e", "--encoding", dest="codePage",help="encoding: latin, thai, chinese, cyrillic, utf-8")
    parser.add_option("-t", "--text", action="store_true", dest="textOnly",help="Write out text only")
    parser.add_option("-f", "--outformat", dest="outFormat", help="Define output format, options: SRT")
    parser.add_option("-o", "--outfile", dest="outFile", help="Output to file, specify filename")
    (options, args) = parser.parse_args()
    if options.outFormat.upper() not in availableOutputs:
        print "Invalid output format: " + options.outFormat
        parser.print_help()
        sys.exit(2)
    elif len(args) == 0:
        parser.print_help()
        sys.exit(1)

    subtitle_file = args[0]
    file_type = subtitle_file[-3:]
    ###Work out encoding & Read File
    if options.codePage:
        codePage = options.codePage.lower()
        paragraphs = loadSubtitle(subtitle_file, codePage)
    elif file_type.lower() == 'fpc':
        # Assume fpc file uses utf-8 encoding
        paragraphs = loadSubtitle(subtitle_file, 'utf-8')
    else:
        # Auto-detecting
        paragraphs = autoDetect(subtitle_file)
        

    ##Determine outputs
    ##print options.outFile 
    if options.textOnly:
         writeOut(paragraphs,"text",options.outFile)
    elif options.outFormat :
        writeOut(paragraphs,options.outFormat,options.outFile)
    else :
        writeOut(paragraphs,"",options.outFile)


if __name__ == "__main__":
    main()
