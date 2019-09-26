"""
reference_handler
A Python package that facilitates the citation of scientific material.
"""

# Add imports here
from .reference_handler import Reference_Handler  # noqa: F401

# Handle versioneer
from ._version import get_versions
versions = get_versions()
__version__ = versions['version']
__git_revision__ = versions['full-revisionid']
del get_versions, versions
