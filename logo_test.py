#!/usr/bin/env python3

"""Unit testing framework for the Logo interpreter.

Usage: python3 logo_test.py FILE

Interprets FILE as Logo source code, and compares each line of printed output to
an expected output described in a comment.  For example,

print 2+3
; expect 5

Differences between printed and expected outputs are printed with line numbers.
"""

import io
import sys
from ucb import main
from logo import Environment, read_eval_loop, strip_comment

def summarize(output, expected_output):
    """Summarize results of running tests."""
    num_failed, num_expected = 0, len(expected_output)
    for (actual, (expected, line_number)) in zip(output, expected_output):
        if actual != expected:
            num_failed += 1
            print('test failed at line {0}'.format(line_number))
            print('  expected: {0}'.format(expected))
            print('   printed: {0}'.format(actual))
    print('{0} tested; {1} failed.'.format(num_expected, num_failed))

EXPECT_STRING = '; expect'

@main
def run_tests(src_file = 'tests.lg'):
    """Run a read-eval loop that reads from src_file and collects outputs."""
    line_number, expected_output = 0, []

    def pop_line(src = open(src_file)):
        """Return the next line of src."""
        nonlocal line_number
        line_number += 1
        line = src.readline()
        if line.lstrip().startswith(EXPECT_STRING):
            expected = line.split(EXPECT_STRING, 1)[1][1:-1]
            expected_output.append((expected, line_number))
        if not line:
            raise EOFError
        return strip_comment(line)

    sys.stdout = io.StringIO()   # Substitute stdout to collect output
    read_eval_loop(Environment(pop_line), pop_line) 
    output = sys.stdout.getvalue().split('\n')
    sys.stdout = sys.__stdout__  # Revert stdout
    summarize(output, expected_output)
