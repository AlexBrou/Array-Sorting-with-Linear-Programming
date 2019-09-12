from pulp import LpProblem, lpSum, LpMinimize, LpVariable, LpInteger, LpStatus


def mipSort(inStuff, ascending=True, printResult=False):
    # LpSolverDefault.msg = 1
    prob = LpProblem("Sorting with Mixed Integer Programming", LpMinimize)

    prob += 0, "Arbitrary Objective"

    floatVars = (
        []
    )  # so, each variable will take the value of one of the numbers, in ascending order

    for ii in range(len(inStuff)):
        floatVars.append(LpVariable("FloatVar_" + str(ii), 0, None))  # , LpInteger))

    for i in range(1, len(floatVars)):
        if ascending:
            prob += (
                floatVars[i] >= floatVars[i - 1]
            )  # this is the constraint that makes the float variables be in order
        else:
            prob += (
                floatVars[i] <= floatVars[i - 1]
            )  # this is the constraint that makes the float variables be in order

    boolVars = []

    counter_i = 0
    for i in inStuff:
        toAppend = []
        for iii in range(len(inStuff)):
            toAppend.append(
                LpVariable(
                    "BoolVar_FloatVar" + str(counter_i) + "_Input" + str(iii),
                    0,
                    1,
                    LpInteger,
                )
            )  # this creates a N x N matrix of boolean values
        prob += (
            lpSum(toAppend) == 1
        )  # and on each row only one of them will be 1, the rest will be zero
        boolVars.append(toAppend)
        counter_i += 1

    boolVarsNew = []
    for ii in range(len(boolVars)):
        toSum = []
        for jj in range(
            len(boolVars)
        ):  # on the same N x N matrix, on each column only one will be 1, the rest zero
            toSum.append(boolVars[jj][ii])
        prob += lpSum(toSum) == 1
        boolVarsNew.append(toSum)

    for i in range(len(floatVars)):
        varvar = floatVars[i]
        arrayToSum = []
        counter_ii = 0
        for jj in boolVarsNew:
            arrayToSum.append(
                jj[i] * inStuff[counter_ii]
            )  # now, we multiply every row's boolean values by the correspondent coeficient,
            counter_ii += (
                1
            )  # which is the number on the input array. every sum of rows corresponds to a different number of the
        prob += varvar == lpSum(
            arrayToSum
        )  # input array, and since we already inserted constraints giving them ascending or descending
        # order, each floatVar will have the value of one of the input numbers, but ordered
    prob.solve()

    if printResult:
        print("Status:", LpStatus[prob.status])

        if LpStatus[prob.status] == "Optimal":
            for v in prob.variables():
                if "Bool" in v.name and v.varValue == 1.0:
                    print(v.name, "=", v.varValue)
            for vv in floatVars:
                print(vv.name, "=", vv.varValue)

    result = [x.varValue for x in floatVars]
    return result


if __name__ == "__main__":
    inStuff = [7, 5, 6.6, 5, 4, 3.5, 3]
    result = mipSort(inStuff)  # ascending, no prints
    print(result)
    # mipSort(inStuff, ascending=False, printResult=True)
