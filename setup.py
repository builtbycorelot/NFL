from setuptools import setup, find_packages

setup(
    name="nfl",
    version="0.2.0",
    description="NodeForm Language tools",
    author="builtbycorelot",
    license="MIT",
    packages=find_packages(include=["cli", "schema"]),
    package_data={"schema": ["*.json"]},
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=[
        "jsonschema",
        "flask",
        "flask-cors",
        "neo4j-driver",
        "gunicorn",
        "python-dotenv",
        "psycopg2-binary",
    ],
    extras_require={
        "test": [
            "pytest",
        ]
    },
    entry_points={"console_scripts": ["nfl-cli=cli.nfl_cli:main"]},
)
