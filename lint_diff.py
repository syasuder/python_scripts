#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import re
import sys

# Get the list of changed files.
before = sys.argv[1] if len(sys.argv) > 1 else None

# Get the list of changed files.
files = subprocess.check_output(['git', 'diff', '--name-only', '--diff-filter=ACM', before])

# Process each file.
for f in files.split('\n'):
  # Only process Python files.
  if not f.endswith('.py'):
    continue

  # Get the output of pylint.
  pylint_output =  subprocess.Popen(['pylint', f], stdout=subprocess.PIPE).communicate()[0]
  pylint_lines_dict = {}
  for pyline in pylint_output.split('\n'):
    if pyline[:2] in ['E:', 'W:']:
      line_number = pyline.split(':')[1].split(',')[0]
      if not str(line_number) in pylint_lines_dict:
        pylint_lines_dict[str(line_number)] = []
      pylint_lines_dict[str(line_number)].append(pyline)

  # Get the output of git diff command.
  diff_output = subprocess.check_output(['git', 'diff', before, f])

  # Process each line.
  for line in diff_output.split('\n'):
    # If the line is changed, get the line numbers of the changed range.
    if line.startswith('@@'):
      # Get the line numbers of the changed range
      line_numbers = re.findall(r'\+[0-9]+,[0-9]+?', line)
      # Output the line numbers separated by commas
      for ln in line_numbers:
        ln = ln[1:]  # Remove the +
        if ',' in ln:
          start, count = map(int, ln.split(','))
          for i in range(start, start + count):
            # Print the pylint result if the line is relevant
            if str(i) in pylint_lines_dict:
              print '@@@@@', pylint_lines_dict[str(i)]
