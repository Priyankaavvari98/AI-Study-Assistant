
import ast
import coverage

filename = "app.py"

with open(filename, "r", encoding="utf-8") as file:
    tree = ast.parse(file.read())

function = next(
    node for node in ast.walk(tree)
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    and node.name == "register"
)

cov = coverage.Coverage()
cov.load()

measured_file, statements, excluded, missing, _ = cov.analysis2(filename)

function_lines = {
    line for line in statements
    if function.lineno <= line <= function.end_lineno
    and line not in excluded
}

covered_lines = function_lines - set(missing)

if not function_lines:
    print("No executable lines found for register(). Run the tests first.")
else:
    percentage = len(covered_lines) / len(function_lines) * 100
    print(f"Function: register()")
    print(f"Executable lines: {len(function_lines)}")
    print(f"Covered lines: {len(covered_lines)}")
    print(f"Missed lines: {len(function_lines - covered_lines)}")
    print(f"Function line coverage: {percentage:.1f}%")
