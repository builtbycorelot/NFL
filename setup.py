from setuptools import setup, find_packages

setup(
    name="nfl",
    version="0.3.0",
    description="NodeForm Language tools",
    author="builtbycorelot",
    license="MIT",
    packages=find_packages(include=["nfl", "schema"]),
    package_data={"schema": ["*.json"]},
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=["jsonschema"],
)
