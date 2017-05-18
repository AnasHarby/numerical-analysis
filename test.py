from Equations import *
from EquSys import *
from equations_util import *
from sympy.abc import x, y, z

methods = {'Newton-Raphson': newton, 'Secant': secant, 'Bisection': bisection,
           'Regula-Falsi': regula_falsi, 'Modified Newton 1': newton_mod1,
           'Modified Newton 2': newton_mod2}

# testing gauss elimination with partial pivoting.
# m = sympy.Matrix([[25, 5, 1, 106.8], [64, 8, 1, 177.2], [144, 12, 1, 279.2]])
# m = sympy.Matrix([[1, 2, 2, 106.8], [2, 4, 1, 177.2], [4, 2, 1, 279.2]])
m = sympy.Matrix([[8, 4, -1, 11], [-2, 3, 1, 4], [2, -1, 6, 7]])
aug, sym = equations_to_aug_matrix(["x1 + x2 + 2 * x3 = 8", "-x1 - 2 * x2 + 3 * x3 = 1", "3*x1+7*x2+4*x3 = 10"])
# sympy.pprint(sympy.N(gauss_jordan(m), 4))
# print(sympy.solve_linear_system(m, x, y, z))
# print(sympy.Matrix(reversed(m.col(m.shape[0]))))
# print(m.col(m.shape[0]).tolist()[0][0])
#sympy.pprint(sympy.N(gauss_jordan(m), 4))
#sympy.pprint(sympy.N(gauss(m), 4))
#sympy.pprint(sympy.N(lu_decomp(m), 4))
#print(gauss_seidel(m, sym))
#print(jacobi(m, sym))
print(sympy.solve_linear_system(aug, *sym))#"4*x+12*y+16*z=104"
# print(sympy.Matrix(reversed(m.col(m.shape[0]))))
# print(m.col(m.shape[0]).tolist()[0][0])
#sympy.pprint(sympy.N(gauss_jordan(aug), 4))
#sympy.pprint(sympy.N(gauss(aug), 4))
#sympy.pprint(sympy.N(lu_decomp(aug), 4))
#print(gauss_seidel(aug, sym))
# out = jacobi(aug, sym)
# print(out.title)
# print(out.dataframes)
# print(out.execution_time)
# print(out.roots)
# print(out.errors)
#
# out = gauss_seidel(aug, sym)
# print(out.title)
# print(out.dataframes)
# print(out.execution_time)
# print(out.roots)
# print(out.errors)
