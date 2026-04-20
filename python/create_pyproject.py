from pathlib import Path

INLINE_TABLE_KEYS = {
    "license",
    "authors",
    "urls",
    "package-dir",
}


def quote(value):
    return '"' + str(value).replace('"', '\\"') + '"'


def format_value(value):
    if isinstance(value, str):
        return quote(value)
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, list):
        return "[" + ", ".join(format_value(item) for item in value) + "]"
    if isinstance(value, dict):
        items = [f"{quote_key(k)} = {format_value(v)}" for k, v in value.items()]
        return "{ " + ", ".join(items) + " }"
    raise TypeError(f"Tipo não suportado: {type(value)}")


def quote_key(key):
    if key == "" or any(ch in key for ch in " -"):
        return quote(key)
    return key


def dumps_toml(data):
    lines = []

    def write_section(prefix, obj):
        simple_items = {}
        nested_items = {}

        for key, value in obj.items():
            if isinstance(value, dict) and key not in INLINE_TABLE_KEYS:
                nested_items[key] = value
            else:
                simple_items[key] = value

        if prefix:
            lines.append(f"[{prefix}]")

        for key, value in simple_items.items():
            lines.append(f"{quote_key(key)} = {format_value(value)}")

        if prefix and nested_items:
            lines.append("")

        for i, (key, value) in enumerate(nested_items.items()):
            child_prefix = f"{prefix}.{quote_key(key)}" if prefix else quote_key(key)
            write_section(child_prefix, value)
            if i < len(nested_items) - 1:
                lines.append("")

    write_section("", data)
    return "\n".join(lines).rstrip() + "\n"


project_data = {
    "build-system": {
        "requires": ["setuptools>=68", "wheel"],
        "build-backend": "setuptools.build_meta",
    },
    "project": {
        "name": "ppgcr-utils",
        "version": "0.1.0",
        "description": "Utilities for signal processing and data analysis in Python.",
        "readme": "README.md",
        "requires-python": ">=3.10",
        "license": {"text": "MIT"},
        "authors": [{"name": "Conrado Torres"}],
        "keywords": ["signal processing", "EMG", "COP", "biomechanics", "data analysis"],
        "classifiers": [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Science/Research",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Programming Language :: Python :: 3.12",
            "Topic :: Scientific/Engineering",
        ],
        "dependencies": ["numpy>=1.24", "scipy>=1.10", "matplotlib>=3.7"],
        "urls": {
            "Homepage": "https://github.com/SEU_USUARIO/PPGCR_utils",
            "Repository": "https://github.com/SEU_USUARIO/PPGCR_utils",
        },
    },
    "tool": {
        "setuptools": {
            "package-dir": {"": "src"},
            "include-package-data": False,
            "packages": {
                "find": {
                    "where": ["src"],
                    "exclude": ["tests*", "examples*"],
                }
            },
        }
    },
}

output = Path(__file__).with_name("pyproject.toml")
output.write_text(dumps_toml(project_data), encoding="utf-8")
print(f"Arquivo gerado em: {output}")
