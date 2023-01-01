# Employee Scheduler for Microsoft Excel
Version 0.0.1-alpha

# About:
This utility is used to automatically populate a weekly schedule, given the year and week number, or an entire year of schedules if given only a year.

It matches the date with the day of the week (Mon, Tue, Wed, etc) and then fills in the store hours based on this information.  
Given a list of holidays and their dates, it will also automatically adjust the store hours for those dates.

This utility cannot function properly without proper configuration of the following files:

	'Store.xlsx', located in '\employee_scheduler/work_schedule/store'
	'Employees.xlsx', located in '\employee_scheduler/work_schedule/employees'

Future releases and source code are available on my GitHub project page:

	https://github.com/hitzstuff/employee_scheduler

This program is Alpha, and has no warranty.  It may not function as intended.
The author takes no responsibility for any issues that may occur.

# Install Instructions:
Requirements:

- Python 3.9.13
  * NumPy 1.22.4
  * pandas 1.4.2
  * PySimpleGUI 4.55.1
	
- Microsoft Excel

# Legal:
Employee Scheduler for Microsoft Excel is licensed under the Apache License Version 2.0. The full text of this license is available in the LICENSE file.

Developed by Aaron Hitzeman <aaron.hitzeman@gmail.com>
