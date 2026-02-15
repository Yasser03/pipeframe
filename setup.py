"""
PipeFrame - Pipe Your Data Naturally

For backwards compatibility with older pip versions.
Modern installations should use pyproject.toml.
"""

from setuptools import setup

# Read requirements
with open('requirements.txt') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name='pipeframe',
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    install_requires=requirements,
)
