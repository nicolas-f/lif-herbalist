__author__ = 'CUMU'

from constraint import *

problem = Problem()
herbs = ["a", "b", "c", "d"]
effects = [1, 2, 3, 4, 5, 6]
problem.addVariables(herbs, effects)

# Begin tests
# Mix A and B, nothing happens
#problem.addConstraint(left_not_in_right, ["a", "b"])
# Mix A and C, found effect #2
problem.addConstraint(SomeInSetConstraint([2, 3]), ["a", "c"])
problem.addConstraint(SomeInSetConstraint([4]), ["b", "c"])
#problem.addConstraint(NotInSetConstraint([1]), "b")
#problem.addConstraint(InSetConstraint([2]), "c")
# Mix B and C, found effects #4 #6
#problem.addConstraint(InSetConstraint([4, 6]), "b")
#problem.addConstraint(InSetConstraint([4, 6]), "c")

solutions = dict()
for herb in herbs:
    solutions[herb] = set()

for solution in problem.getSolutions():
    for herb, effect in solution.iteritems():
        solutions[herb].add(effect)
print solutions
