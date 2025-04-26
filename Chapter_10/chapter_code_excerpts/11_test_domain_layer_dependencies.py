import ast
from pathlib import Path


def test_domain_layer_dependencies(self):
    """Verify domain layer has no outward dependencies."""
    domain_path = Path("todo_app/domain")
    violations = []

    for py_file in domain_path.rglob("*.py"):
        with open(py_file) as f:
            tree = ast.parse(f.read())

        for node in ast.walk(tree):
            if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                module = node.names[0].name
                if module.startswith("todo_app."):
                    layer = module.split(".")[1]
                    if layer in ["infrastructure", "interfaces", "application"]:
                        violations.append(
                            f"{py_file.relative_to(domain_path)}: "
                            f"Domain layer cannot import from {layer} layer"
                        )
    self.assertEqual(violations, [], "\nDependency Rule Violations:\n" + "\n".join(violations))
