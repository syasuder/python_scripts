#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import re
import sys
import json
from pathlib import Path

# Get the list of changed files.
before = sys.argv[1] if len(sys.argv) > 1 else None

# Get the list of changed files.
files = subprocess.check_output(['git', 'diff', '--name-only', '--diff-filter=ACM', before])

python_files = [file for file in files.split('\n') if file.endswith('.py')]

# Get the output of pylint.
pylint_output_jsons =  subprocess.Popen(['pylint', '-f', 'json'] + python_files, stdout=subprocess.PIPE).communicate()[0]

pylint_output_dict_list = json.loads(pylint_output_jsons)

# filter only error and warning
pylint_output_dict_list = list(filter(lambda x: x['type'] in ['error', 'warning'], pylint_output_dict_list))

# Process each file.
for f in python_files:

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
            for entry in filter(lambda x: x['line'] == i and Path(x['path']) == Path(f), pylint_output_dict_list):
              msg = ','.join([entry['type'], str(Path(f)), str(entry['line']), str(entry['column']), entry['message']])
              print '@@@@@', msg
