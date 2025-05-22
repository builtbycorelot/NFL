from setuptools import setup, find_packages

setup(
    name="nfl",
    version="0.1.0",
    description="NodeForm Language tools",
    author="builtbycorelot",
    license="MIT",
    packages=find_packages(include=["cli", "schema"]),
    package_data={"schema": ["*.json"]},
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=["jsonschema"],
    entry_points={"console_scripts": ["nfl-cli=cli.nfl_cli:main"]},
)
