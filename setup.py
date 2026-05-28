from setuptools import setup, find_packages

setup(
    name="block-simulator-gui",
    version="0.1.0",
    description="GUI simulator for block-based visual programming",
    author="decafale",
    packages=find_packages(),
    install_requires=[
        "PyQt6>=6.7.0",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "block-simulator=src.main:main",
        ],
    },
)
