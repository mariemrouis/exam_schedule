# Timetable Scheduling with OR-Tools :writing_hand:
## 	:eyes: Overview
This Python script utilizes the OR-Tools library to solve a timetable scheduling problem. <br />
The problem involves scheduling courses taught by teachers in specific rooms over a given number of hours.  <br />
The constraints ensure that each teacher, room, and course is assigned to at most one time slot, and all courses are scheduled at least once. <br />

## Dependencies
OR-Tools - Google's Optimization Tools library. <br />
:point_right: Use the package manager [pip](https://pip.pypa.io/en/stable/) to install OR-Tools. <br />

```bash

pip install ortools


```
## Usage
:point_right: To run the script, ensure you have OR-Tools installed and then execute the following command:
```bash

python main.py


```
## :point_down: Output
The script outputs the solutions found, along with detailed statistics. The key statistics include: <br />

 .Conflicts: The number of conflicts in the schedule. <br />
 .Branches: The number of branches explored during the optimization process. <br />
 .Wall Time: The total time taken to find the solution. <br />

 
