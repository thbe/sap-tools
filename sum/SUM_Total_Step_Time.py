#! /usr/bin/env python3

"""_summary_
Author:       Thomas Bendler <code@thbe.org>
Date:         Fri Aug  4 11:29:00 UTC 2023

Release:      1.2.0

ChangeLog:    v0.1.0 - Initial release
              v1.0.0 - Validated against S01 S4HANA upgrade
              v1.2.0 - Switched to direct SAPupConsole.log processing

Purpose:      Get summarized times per SUM upgrade phase/ step
"""

import re
import io
import datetime
from prettytable import PrettyTable


def read_console_file(filename):
    """Reads the SAPupConsole.log file and returns a list of lists."""
    timestamp_pattern = r'^<<|^>>'
    data = []
    with open(filename, 'r') as fp:
        Lines = fp.readlines()
        for line in Lines:
            match = re.search(timestamp_pattern, line)
            if match is not None:
                line_clean = line.strip()
                line_fix_start = line_clean.replace('START OF PHASE', 'S')
                line_fix_end = line_fix_start.replace('END OF PHASE  ', 'E')
                line_fix_spaces = re.sub(' +', ' ', line_fix_end)
                line_field_date = line_fix_spaces.split(' ')[1]
                line_field_time = line_fix_spaces.split(' ')[2]
                line_field_action = line_fix_spaces.split(' ')[3]
                line_field_phase = line_fix_spaces.split(' ')[4]
                data.append([line_field_date, line_field_time, line_field_action, line_field_phase])
    return data


def get_total_time_consumed_by_step(data):
    """Gets the total time consumed by each step."""
    step_times = {}
    for row in data:
        if row[2] == 'S':
            step_name = row[3]
            start_time = datetime.datetime.strptime(
                row[0] + ' ' + row[1], '%Y/%m/%d %H:%M:%S')
        elif row[2] == 'E':
            step_name = row[3]
            end_time = datetime.datetime.strptime(
                row[0] + ' ' + row[1], '%Y/%m/%d %H:%M:%S')
            time_consumed = end_time - start_time
            if step_name in step_times:
                step_times[step_name] += time_consumed
            else:
                step_times[step_name] = time_consumed
    return step_times


def main():
    """The main function."""
    filename = 'SAPupConsole.log'
    data = read_console_file(filename)
    output_table = PrettyTable(['Step', 'Time'])
    step_times = get_total_time_consumed_by_step(data)
    for step, time_consumed in step_times.items():
        output_table.add_row([step, time_consumed])
    output_table.align['Step'] = "l"
    output_table.align['Time'] = "c"
    print(output_table)


if __name__ == '__main__':
    main()

# Clean Up Regex
# grep -E "<<|>>" SAPupConsole.log
# | sed -e "s/START OF PHASE/S/g"
# | sed -e "s/END OF PHASE  /E/g"
# | sed -e "s/  */ /g"
# | cut -d ' ' -f2,3,4,5
# | sed -e "s/ /;/g"
# > SAPupConsole_log.csv
