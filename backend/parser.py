from __future__ import annotations

import re


IGNORE_FILES = {
    ".DS_Store",
    ".gitignore",
    "package-lock.json",
    "yarn.lock",
    "pnpm-lock.yaml",
}

CODE_EXTENSIONS = {".py", ".js", ".ts", ".jsx", ".java", ".go"}
FASTAPI_ROUTE_RE = re.compile(r'^\+\s*@\w+\.(get|post|put|delete|patch)\(\s*["\']([^"\']+)["\']')
EXPRESS_ROUTE_RE = re.compile(r'^\+\s*(?:router|app)\.(get|post|put|delete|patch)\(\s*["\']([^"\']+)["\']')
HTTP_ROUTE_RE = re.compile(r'\b(GET|POST|PUT|DELETE|PATCH)\s+(/\S+)')
PYTHON_FUNCTION_RE = re.compile(r'^\+\s*def\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(')


def _is_code_file(path: str) -> bool:
    return any(path.endswith(extension) for extension in CODE_EXTENSIONS)


def parse_changes(diff: str) -> dict[str, list[str]]:
    files: list[str] = []
    functions: list[str] = []
    apis: list[str] = []

    for line in diff.splitlines():
        if line.startswith("diff --git "):
            parts = line.split()
            if len(parts) >= 4:
                file_path = parts[3].removeprefix("b/")
                file_name = file_path.rsplit("/", 1)[-1]

                if file_name in IGNORE_FILES or not _is_code_file(file_path):
                    continue

                files.append(file_path)

        function_match = PYTHON_FUNCTION_RE.match(line)
        if function_match:
            functions.append(function_match.group(1))

        route_match = FASTAPI_ROUTE_RE.match(line) or EXPRESS_ROUTE_RE.match(line)
        if route_match:
            apis.append(f"{route_match.group(1).upper()} {route_match.group(2)}")
            continue

        http_route_match = HTTP_ROUTE_RE.search(line)
        if http_route_match:
            apis.append(f"{http_route_match.group(1)} {http_route_match.group(2)}")

    unique_files = sorted(set(files))
    unique_functions = sorted(set(functions))
    unique_apis = sorted(set(apis))

    print(f"[parser] detected files: {unique_files}")
    print(f"[parser] parsed API routes: {unique_apis}")

    return {
        "files": unique_files,
        "functions": unique_functions,
        "apis": unique_apis,
    }
