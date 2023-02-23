# python_scripts

## lint_diff.py

The script takes an optional argument `before`, which is used to get the list of modified files using the git diff command. For each file that ends with `.py`, the script runs `pylint` to get the `pylint` output, and then runs git diff to get the diff output. The script then processes each line in the diff output to find the line numbers of the changed range. Finally, the script outputs the pylint result for each line in the changed range. The output is prefixed with @@@@@.

This script was created for testing purposes on the following environment. No error checks were performed.

* Python 2.7
* Pylint 1.5.5

note:  
By the way, if you want to integrate the diff obtained by git diff and the result of pylint, it may be more accurate to execute pylint with `before` and `after` snapshots of the diff and obtain the diff of the results, rather than using this script. For example, if there is a pylint rule that produces different results outside the modified source line, this script cannot detect it.
