#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs

from __future__ import absolute_import
import pathfix
# ----------------------------------------------
from utils.argparser import ArgParser


parser = ArgParser("exec_parallel.py <parameters>  -- <executable> <executable arguments>")
# ----------------------------------------------
parser.add_section('General arguments')
parser.add('-n', '--cpu', type=int, name='cpu', default=1, placeholder='<cpu>', docs=[
    'Run executable in <cpu> processes',
])
parser.add('-q', '--queue', type=[True, str], name='queue', placeholder='[<queue>]', docs=[
    'Optional PBS queue name to use. If the parameter is not used, ',
    'the application is executed in the same process and without PBS.',
    '',
    'If used without <queue> argument it is executed in the ',
    'background preferably under PBS with the queue selected ',
    'automatically for the given wall clock time limit and number of processes.'
])
parser.add('', '--host', type=str, name='host', placeholder='<host>', docs=[
    'Name of the running host that is used to select system ',
    'specific setup script. Default value of this parameter ',
    'is obtained by first getting the hostname ',
    '(using platform.node() or socket.gethostname()) and then search',
    'it in the table "host_table.json" which assign logical hostname',
    'possibly to multiple different real hostnames. ',
    '',
    'If the real host name is not found in the table ',
    'it is used directly otherwise the logical ',
    'hostname is used to select the setup script.',
])
parser.add('', '--mpirun', type=True, name='mpirun', docs=[
    'Use mpirun instead of mpiexec in flo123d/bin directory'
])
# ----------------------------------------------
parser.add_section('Passable arguments to exec_with_limit.py')
parser.add('-t', '--limit-time', type=float, name='time_limit', placeholder='<time>', docs=[
    'Obligatory wall clock time limit for execution in seconds',
    'For precision use float value'
])
parser.add('-m', '--limit-memory', type=float, name='memory_limit', placeholder='<memory>', docs=[
    'Optional memory limit per node in MB',
    'For precision use float value'
])
parser.add_section('Proposed arguments')
parser.add('', '--root', type=str, name='root', placeholder='<root>', docs=[
    'Optional hint for flow123d path, if not specified, default value will be',
    'Extracted from this file path, assuming it is located in flow123d bin/python dir',
    '',
    'Script will always change-dir itself to location of root, so all path match'
])
# ----------------------------------------------

if __name__ == '__main__':
    from scripts.exec_parallel_module import do_work
    do_work(__file__, parser)