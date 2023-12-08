#! /usr/bin/env python3

"""_summary_
Author:       Thomas Bendler <code@thbe.org>
Date:         Fri Aug  4 11:29:00 UTC 2023

Release:      1.0.0

ChangeLog:    v0.1.0 - Initial release
              v1.0.0 - Validated against S01 S4HANA upgrade

Purpose:      Get summarized times per SUM upgrade phase/ step
"""

import csv
import datetime
from prettytable import PrettyTable

def read_csv_file(filename):
  """Reads a CSV file and returns a list of lists."""
  with open(filename, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    data = []
    for row in reader:
      data.append(row)
  return data

def get_total_time_consumed_by_step(data):
  """Gets the total time consumed by each step."""
  step_times = {}
  for row in data:
    if row[2] == 'S':
      step_name = row[3]
      start_time = datetime.datetime.strptime(row[0] + ' ' + row[1], '%Y/%m/%d %H:%M:%S')
    elif row[2] == 'E':
      step_name = row[3]
      end_time = datetime.datetime.strptime(row[0] + ' ' + row[1], '%Y/%m/%d %H:%M:%S')
      time_consumed = end_time - start_time
      if step_name in step_times:
        step_times[step_name] += time_consumed
      else:
        step_times[step_name] = time_consumed
  return step_times

def main():
  """The main function."""
  filename = 'SAPupConsole_log.csv'
  data = read_csv_file(filename)
  output_table = PrettyTable(['Step', 'Time'])
  step_times = get_total_time_consumed_by_step(data)
  for step, time_consumed in step_times.items():
    output_table.add_row([step, time_consumed])
  output_table.align['Step'] = "l"
  output_table.align['Time'] = "c"
  print(output_table)

if __name__ == '__main__':
