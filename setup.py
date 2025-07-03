from setuptools import setup, find_packages

setup(
    name="nfl",
    version="0.3.0",
    description="NodeForm Language tools",
    author="builtbycorelot",
    license="MIT",
    packages=find_packages(include=["nfl", "cli", "api", "schema"]),
    package_data={"schema": ["*.json"], "api": ["docs/openapi.json"]},
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=[
        "fastapi",
        "uvicorn",
        "jsonschema",
        "requests",
    ],
    extras_require={"test": ["pytest"]},
    entry_points={"console_scripts": ["nfl=cli.nfl_cli:main"]},
)
