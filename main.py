from ortools.sat.python import cp_model


#This class extends cp_model.CpSolverSolutionCallback and is responsible for printing solutions during the optimization process.
class MySolutionPrinter(cp_model.CpSolverSolutionCallback):
    # Constructor method to initialize the solution callback.
    def __init__(self, my_timetable, my_num_teachers, my_num_hours, my_num_rooms, my_num_courses, my_limit):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self._my_timetable = my_timetable
        self._my_num_hours = my_num_hours
        self._my_num_teachers = my_num_teachers
        self._my_num_rooms = my_num_rooms
        self._my_num_courses = my_num_courses
        self._my_solution_count = 0
        self._my_solution_limit = my_limit
   #Callback method triggered on each solution found. Prints the current solution.
    def on_solution_callback(self):
        self._my_solution_count += 1
        print(f"My Solution {self._my_solution_count}")
        for h in range(self._my_num_hours):
            for t in range(len(self._my_num_teachers)):
                for r in range(len(self._my_num_rooms)):  # Fix here
                    for c in range(len(self._my_num_courses)):  # Fix here
                        if self.Value(self._my_timetable[(h, c, r, t)]):
                            print(f"hour: {h}, teacher: {t}, course {c}, room {r}.")
        if self._my_solution_count >= self._my_solution_limit:
            print(f"Stop search after {self._my_solution_limit} solutions")
            self.StopSearch()

    # Returns the count of solutions found
    def solution_count(self):
        return self._my_solution_count

#This is the main entry point of the script. It defines the data, sets up the OR-Tools model, adds constraints, creates a solver, and finds solutions using the SolutionPrinter callback.
def main():
    # Data

    my_num_teachers = ['teachers_1', 'teachers_2', 'teachers_3']
    my_num_rooms = ['rooms_1', 'rooms_2', 'rooms_3', 'rooms_4']
    my_num_courses = ['courses_1', 'courses_2', 'courses_3']
    my_num_hours = 28

    all_teachers = range(len(my_num_teachers))
    all_rooms = range(len(my_num_rooms))
    all_courses = range(len(my_num_courses))
    all_hours = range(my_num_hours)

    # Creates the model.
    model = cp_model.CpModel()

    my_timetable = {}

    for h in all_hours:
        for c in all_courses:
            for r in all_rooms:
                for t in all_teachers:
                    my_timetable[(h, c, r, t)] = model.NewBoolVar(
                        f"h{h}_c{c}_r{r}_t{t}")

    # constraint 1
    #Teachers cannot teach more than one course in the same time slot.
    for t in all_teachers:
        for h in all_hours:
            model.AddAtMostOne(my_timetable[(h, c, r, t)]
                               for r in all_rooms for c in all_courses)

    # constraint 2
    #Rooms cannot host more than one course in the same time slot.
    for r in all_rooms:
        for h in all_hours:
            model.AddAtMostOne(my_timetable[(h, c, r, t)]
                               for t in all_teachers for c in all_courses)

    # constraint 3
    #Courses cannot be taught by more than one teacher in the same time slot.
    for c in all_courses:
        for h in all_hours:
            model.AddAtMostOne(my_timetable[(h, c, r, t)]
                               for t in all_teachers for r in all_rooms)

    # constraint 4
    # Each course must be scheduled at least once
    for c in all_courses:
        model.AddAtLeastOne(my_timetable[(h, c, r, t)] for t in all_teachers for h in all_hours for r in all_rooms
                            )
    # constraint 5
    # Utilize the maximum number of hours available.
    for h in all_hours:
        model.AddAtLeastOne(my_timetable[(h, c, r, t)] for c in all_courses for r in all_rooms for t in all_teachers)

    # Creates the solver and solve.
    solver = cp_model.CpSolver()
    # Sets the linearization level of the solver
    solver.parameters.linearization_level = 0
    # Enumerates all possible solutions.
    solver.parameters.enumerate_all_solutions = True

    #Limits the script to display the first 10 solutions
    solution_limit = 10
    solution_printer = MySolutionPrinter(
        my_timetable, my_num_teachers, my_num_hours, my_num_rooms, my_num_courses, solution_limit
    )

    solver.Solve(model, solution_printer)

    # Statistics.
    print("\nOptimization Statistics:")
    print(f"  - Number of Conflicts      : {solver.NumConflicts()}")
    print(f"  - Number of Branches       : {solver.NumBranches()}")
    print(f"  - Wall Time (elapsed)      : {solver.WallTime()} seconds")
    print(f"  - Total Solutions Found    : {solution_printer.solution_count()}")


if __name__ == "__main__":
    main()
