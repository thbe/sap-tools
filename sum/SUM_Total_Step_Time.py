#! /usr/bin/env python3

"""_summary_
Author:       Thomas Bendler <code@thbe.org>
Date:         Wed Dec 13 22:17:04 CET 2023

Release:      2.0.0

ChangeLog:    v0.1.0 - Initial release
              v1.0.0 - Validated against S01 S4HANA upgrade
              v1.2.0 - Switched to direct SAPupConsole.log processing
              v2.0.0 - Refactor into class

Purpose:      Get summarized times per SUM upgrade phase/ step
"""

import re
import datetime
from prettytable import PrettyTable


class Sum:
    '''
     The Sum object contains info about SUM run times for each phase.
     It uses the SAPupConsole.log to determine the run times.

     Args:

     Attributes:
     '''

    def __init__(self):
        self.data_raw = []
        self.data_analyzed = []

    def read_log_file(self):
        """Reads the SAPupConsole.log file and returns a list of lists."""
        filename = 'SAPupConsole.log'
        with open(filename, 'r') as fp:
            Lines = fp.readlines()
            timestamp_pattern = r'^<<|^>>'
            for line in Lines:
                match = re.search(timestamp_pattern, line)
                if match is not None:
                    line_clean = line.strip()
                    line_fix_start = line_clean.replace('START OF PHASE', 'S')
                    line_fix_end = line_fix_start.replace(
                        'END OF PHASE  ', 'E')
                    line_fix_spaces = re.sub(' +', ' ', line_fix_end)
                    line_field_date = line_fix_spaces.split(' ')[1]
                    line_field_time = line_fix_spaces.split(' ')[2]
                    line_field_action = line_fix_spaces.split(' ')[3]
                    line_field_phase = line_fix_spaces.split(' ')[4]
                    self.data_raw.append([line_field_date, line_field_time,
                                 line_field_action, line_field_phase])

    def analyze_phase_times(self):
        """Gets the total time consumed by each phase."""
        phase_times = {}
        for row in self.data_raw:
            if row[2] == 'S':
                phase_name = row[3]
                start_time = datetime.datetime.strptime(
                    row[0] + ' ' + row[1], '%Y/%m/%d %H:%M:%S')
            elif row[2] == 'E':
                phase_name = row[3]
                end_time = datetime.datetime.strptime(
                    row[0] + ' ' + row[1], '%Y/%m/%d %H:%M:%S')
                time_consumed = end_time - start_time
                if phase_name in phase_times:
                    phase_times[phase_name] += time_consumed
                else:
                    phase_times[phase_name] = time_consumed
        self.data_analyzed = phase_times

    def display_phase_times(self):
        output_table = PrettyTable(['Step', 'Time'])
        for step, time_consumed in self.data_analyzed.items():
            output_table.add_row([step, time_consumed])
            output_table.align['Step'] = "l"
            output_table.align['Time'] = "c"
        print(output_table)


def main():
    sum = Sum()
    sum.read_log_file()
    sum.analyze_phase_times()
    sum.display_phase_times()


if __name__ == '__main__':
    main()
