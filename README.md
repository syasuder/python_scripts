# python_scripts

## lint_diff.py

The script takes an optional argument `before`, which is used to get the list of modified files using the git diff command. For each file that ends with `.py`, the script runs `pylint` to get the `pylint` output, and then runs git diff to get the diff output. The script then processes each line in the diff output to find the line numbers of the changed range. Finally, the script outputs the pylint result for each line in the changed range. The output is prefixed with @@@@@.

This script was created for testing purposes on the following environment. No error checks were performed.

* Python 2.7
* Pylint 1.5.5

note:  
By the way, if you want to integrate the difference obtained by `git diff` with the results of `pylint`, it is believed that obtaining the diff of the results by executing `pylint` on the snapshots of both `before` and `after` diffs is more accurate than using this script. For example, if the results of `pylint` differ outside the changed source line, this script cannot detect it.
