#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs


import sys, os, re

_long_format = re.compile(r'--[a-z0-9_-]+=')
_short_eq_format = re.compile(r'-[a-z]=')
_short_colon_format = re.compile(r'-[a-z]:')
_short_nospace_format = re.compile(r'-[a-z].')

# python list of int or floats (also empty list): [1, 2, 3.5]
_list_format = re.compile(r'^\[(\d+\.?\d*)(\s*,\s*(\d+\.?\d*))*\]|\[\]')
_list_format_convert = eval

# python list of int or floats (also empty list) WITHOUT braces: 1,2,3.5
_list_nobrace_format = re.compile(r'^(\d+\.?\d*)(\s*,\s*(\d+\.?\d*))*$')
_list_nobrace_format_convert = lambda x: eval('[{}]'.format(x))

# python list of int or floats WITHOUT commas: [1 2 3.5]
_list_space_format = re.compile(r'^\[(\d+\.?\d*)(\s+(\d+\.?\d*))*\]|\[\]')
_list_space_format_convert = lambda x: eval(re.sub('\s+', ',', x))

# python single int or float: 1 or 2.5
_list_single_digit = re.compile(r'^\d+\.?\d*$')
_list_single_digit_convert = lambda x: [eval(x)]

# range format such as 1:3
_list_range_short = re.compile(r'^(\d+):(\d+)$')
def _list_range_short_convert(x):
    args = [int(y) for y in _list_range_short.match(x).groups()]
    return list(range(args[0], args[1]+1))

# range format such as 1:10:2
_list_range_long = re.compile(r'^(\d+):(\d+):(\d+)$')
def _list_range_long_convert(x):
    args = [int(y) for y in _list_range_long.match(x).groups()]
    return list(range(args[0], args[1]+1, args[2]))

# all list supported format
_list_formats = [
    [_list_format, _list_format_convert],
    [_list_space_format, _list_space_format_convert],
    [_list_single_digit, _list_single_digit_convert],
    [_list_range_short, _list_range_short_convert],
    [_list_range_long, _list_range_long_convert],
    [_list_nobrace_format, _list_nobrace_format_convert]
]


class ArgOption(object):
    def __init__(self, short, long, type=str, default=None, name=None, subtype=str, docs='', placeholder=None):
        self.short = short
        self.long = long
        self.type = type
        self.subtype = subtype
        self.default = default
        self.docs = docs

        if self.type is True or self.type is False:
            self.value = not self.type
        elif self.type is list:
            self.value = list()
        else:
            self.value = default
        self.name = name or self.long[2:] or self.short[1:]
        self.placeholder = placeholder or self.name

    def is_primitive(self):
        return self.type in (True, False)

    def parse_list(self, value):
        for fmt, conv in _list_formats:
            if fmt.match(value):
                try:
                    lst = conv(value)
                    if type(lst) is not list:
                        raise Exception('Invalid format {}'.format(value))
                    lst = [self.subtype(x) for x in lst]
                    return lst
                except:
                    raise Exception('Invalid format {}'.format(value))
        raise Exception('Invalid format {}'.format(value))

    def __repr__(self):
        lsn = ''
        if self.long and self.short:
            if self.is_primitive():
                lsn = '{self.short}, {self.long}'.format(self=self)
            else:
                lsn = '{self.short}, {self.long} {name}'.format(self=self, name=self.placeholder.upper())
        else:
            value = self.short or self.long
            if self.is_primitive():
                lsn = '{value}'.format(value=value)
            else:
                lsn = '{value} {name}'.format(value=value, name=self.placeholder.upper())

        lsn = '  {:30s}'.format(lsn)
        blank = 32 * ' '
        if self.docs:
            if type(self.docs) is str:
                return '{} {self.docs}'.format(lsn, self=self)
            else:
                result = ''
                for l in self.docs:
                    result += '{} {}\n'.format(lsn, l)
                    lsn = blank
                return result.rstrip()


class ArgOptions(dict):
    def __getitem__(self, item):
        return self.get(item)


class ArgParser(object):
    def __init__(self, usage):
        self._args = [str(x) for x in sys.argv[1:]]
        self.args = list()
        self.options = ArgOptions()
        self.options_map = {}
        self.others = []
        self.rest = []
        self.source = None
        self.i = None
        self.keys = None
        self._usage = usage
        self.all_options = list()

    def add(self, short='', long='', type=str, default=None, name=None, subtype=str, docs='', placeholder=''):
        ao = ArgOption(short, long, type, default, name, subtype, docs, placeholder)

        self.all_options.append(ao)
        if name:
            self.options[name] = ao
            self.options_map[name] = ao
        if short:
            self.options_map[short] = ao
        if long:
            self.options_map[long] = ao

    def add_section(self, name):
        self.all_options.append('\n{}:'.format(name))

    def usage(self):
        usage_lst = [self._usage]
        for option in self.all_options:
            usage_lst.append('{option}\n'.format(option=option))
        return '\n'.join(usage_lst)


    def current(self):
        """
        :rtype : str
        """
        return self.source[self.i]

    def next(self):
        """
        :rtype : str
        """
        return self.source[self.i+1]

    def move_on(self):
        self.i += 1

    def process_option(self, option):
        """
        :type option: ArgOption
        """
        if option.type is True:
            option.value = True
        elif option.type is False:
            option.value = False
        elif option.type in (int, float, long, str):
            option.value = option.type(self.next())
            self.move_on()
        elif option.type is list:
            option.value.extend(option.parse_list(self.next()))
            self.move_on()
        elif type(option.type) is list:
            # next arg is probably not argument but other flag
            if self.next().startswith('-'):
                option.value = option.type[0]
            else:
                option.value = self.next()
                self.move_on()


        return option.value

    def split_current(self):
        arg = self.current()
        result = list()
        # double dash format
        if arg.startswith('--'):
            # format is --NAME=VALUE
            if _long_format.match(arg):
                result.extend(arg.split('=', 1))
            # format does not contain = sign
            else:
                raise Exception("Invalid input format {}".format(arg))

        # single dash format
        elif arg.startswith('-'):
            # format is -f=VALUE
            if _short_eq_format.match(arg):
                result.extend(arg.split('=', 1))
            # format is -f:VALUE
            elif _short_colon_format.match(arg):
                result.extend(arg.split(':', 1))
            elif _short_nospace_format.match(arg):
                result.append(arg[0:2])
                result.append(arg[2:])
            else:
                raise Exception("Invalid input format {}".format(arg))
        else:
            raise Exception("Invalid input format {}".format(arg))

        # extend source arg list
        pre = self.source[0:self.i]
        curr = result
        post = self.source[self.i + 1:]
        self.source = pre + curr + post

    def parse(self, args=None):
        self.args = []
        self.i = 0
        self.keys = sorted(self.options_map.keys(), reverse=True)
        self.source = args or self._args

        while self.i < len(self.source):
            find = False
            if self.options_map.has_key(self.current()):
                find = True
                self.process_option(self.options_map[self.current()])
            else:
                for k in self.keys:
                    if k.startswith('--'):
                        if self.current().startswith(k + "=") or self.current().startswith(k + ":"):
                            self.split_current()
                            self.process_option(self.options_map[self.current()])
                            find = True
                            break
                    elif k.startswith('-'):
                        if self.current().startswith(k):
                            self.split_current()
                            self.process_option(self.options_map[self.current()])
                            find = True
                            break

            # add to others if not found
            if not find:
                # end of parsing section
                if self.current() == '--':
                    self.rest = self.source[self.i+1:]
                    return self.options, self.others, self.rest
                # just add to others
                else:
                    self.others.append(self.current())
            self.i += 1

        return self.options, self.others, self.rest

    def __getattr__(self, item):
        for i in self.options.values():
            if item == i.name:
                return i.value


# args = ['-p', '5', '456', '--fff', '45', '-l4456', '-j=6', '--foo-56=789', '--foo=456=9']
# args = ['-p', '-foo', '--foo', '456', '--true']
# args = ['--foo=56', '-k', 'cas', '--fo=789', '--', 'foo bar', '-f', 'vsdei']
# args = ['--ll', '1:5:2', '--', 'fooooooo']
# ap = ArgParser()
# # ap.add(long='--foo', tp=int)
# # ap.add(long='--fo', tp=int)
# # ap.add('-l', tp=False)
# # ap.add('-l', tp=False)
# ap.add(long='--ll', type=list, subtype=int, name="foo")
# options, others, rest = ap.parse(args)
# print options.foo