from __future__ import annotations

import os
import re
from pathlib import Path


CODE_EXTENSIONS = (".py", ".js", ".ts", ".jsx", ".java", ".go")
IGNORED_PARTS = {".git", "node_modules", "venv", "__pycache__", "dist"}
PYTHON_IMPORT_RE = re.compile(r"^\s*import\s+([A-Za-z0-9_.,\s]+)", re.M)
PYTHON_FROM_RE = re.compile(r"^\s*from\s+([A-Za-z0-9_\.]+)\s+import", re.M)
JS_IMPORT_RE = re.compile(r"""(?:import|export)\s+.*?\s+from\s+['"](.+?)['"]""")
JS_SIDE_EFFECT_RE = re.compile(r"""^\s*import\s+['"](.+?)['"]""", re.M)
JS_REQUIRE_RE = re.compile(r"""require\(['"](.+?)['"]\)""")


def list_code_files(root="."):
    root_path = Path(root).resolve()
    files = []

    for base, dirs, names in os.walk(root_path):
        dirs[:] = [directory for directory in dirs if directory not in IGNORED_PARTS]

        for name in names:
            if name.endswith(CODE_EXTENSIONS):
                files.append(str(Path(base) / name))

    return sorted(files)


def _normalize_module_name(path: Path, root_path: Path) -> tuple[str, str]:
    relative = path.relative_to(root_path).as_posix()
    stem = path.with_suffix("").relative_to(root_path).as_posix()
    return relative, stem


def _build_lookup(root_path: Path, files: list[str]) -> dict[str, str]:
    lookup = {}

    for file_path in files:
        path = Path(file_path)
        relative, stem = _normalize_module_name(path, root_path)
        parts = stem.split("/")

        lookup[relative] = relative
        lookup[stem] = relative
        lookup[path.stem] = relative
        lookup[".".join(parts)] = relative

        if len(parts) > 1:
            lookup[".".join(parts[1:])] = relative
            lookup["/".join(parts[1:])] = relative

    return lookup


def _resolve_python_import(module_name: str, source_path: Path, root_path: Path, lookup: dict[str, str]) -> str | None:
    cleaned = module_name.strip().split(" as ")[0].strip(".")
    if not cleaned:
        return None

    candidates = {
        cleaned,
        cleaned.replace(".", "/"),
        cleaned.replace("/", "."),
    }

    source_parts = source_path.relative_to(root_path).with_suffix("").parts
    if source_parts:
        local_prefix = "/".join(source_parts[:-1])
        if local_prefix:
            candidates.add(f"{local_prefix}/{cleaned.replace('.', '/')}")
            candidates.add(f"{local_prefix}.{cleaned.replace('/', '.')}")

    for candidate in candidates:
        if candidate in lookup:
            return lookup[candidate]

    return None


def _resolve_js_import(import_path: str, source_path: Path, root_path: Path) -> str | None:
    if not import_path.startswith("."):
        return None

    base = (source_path.parent / import_path).resolve()
    candidates = [
        base,
        base.with_suffix(".js"),
        base.with_suffix(".jsx"),
        base.with_suffix(".ts"),
        base.with_suffix(".py"),
        base / "index.js",
        base / "index.jsx",
        base / "index.ts",
    ]

    for candidate in candidates:
        if candidate.exists() and candidate.is_file():
            return candidate.relative_to(root_path).as_posix()

    return None


def parse_imports(path, root_path, lookup):
    imports = set()
    file_path = Path(path)

    try:
        text = file_path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return imports

    if file_path.suffix == ".py":
        for module_group in PYTHON_IMPORT_RE.findall(text):
            for module_name in module_group.split(","):
                target = _resolve_python_import(module_name.strip(), file_path, root_path, lookup)
                if target:
                    imports.add(target)

        for module_name in PYTHON_FROM_RE.findall(text):
            target = _resolve_python_import(module_name, file_path, root_path, lookup)
            if target:
                imports.add(target)

        return imports

    for module_name in JS_IMPORT_RE.findall(text):
        target = _resolve_js_import(module_name, file_path, root_path)
        if target:
            imports.add(target)

    for module_name in JS_SIDE_EFFECT_RE.findall(text):
        target = _resolve_js_import(module_name, file_path, root_path)
        if target:
            imports.add(target)

    for module_name in JS_REQUIRE_RE.findall(text):
        target = _resolve_js_import(module_name, file_path, root_path)
        if target:
            imports.add(target)

    return imports


def _group_for_module(module: str) -> str:
    if module.startswith("backend/"):
        return "backend"
    if module.startswith("frontend/dashboard/src/components/"):
        return "frontend/components"
    if module.startswith("frontend/dashboard/src/"):
        return "frontend/core"
    if module.startswith("scripts/"):
        return "scripts"
    return module.split("/", 1)[0]


def build_arch_graph(root="."):
    root_path = Path(root).resolve()
    files = list_code_files(root)
    lookup = _build_lookup(root_path, files)

    node_objects = []
    edge_objects = []

    for file_path in files:
        path = Path(file_path)
        module = path.relative_to(root_path).as_posix()
        imports = sorted(parse_imports(file_path, root_path, lookup))
        node_objects.append(
            {
                "id": module,
                "label": path.name,
                "path": module,
                "group": _group_for_module(module),
                "imports": imports,
            }
        )

        for imported in imports:
            edge_objects.append({"from": module, "to": imported})

    groups = sorted({node["group"] for node in node_objects})
    print(f"[architecture] files scanned: {len(node_objects)}, edges built: {len(edge_objects)}")

    return {"nodes": node_objects, "edges": edge_objects, "groups": groups}
