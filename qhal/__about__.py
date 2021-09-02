
"""Summary information about the package
    Attributes
    ----------
    __license__ : str
        Short description of our license.
    __copyright__ : str
        Copyright notice
    __url__ : str
        Project URL
    __contributors__ : str
        Single-line list of all project contributors.
    __contributors_lines__ : str
        Multi-line list of all project contributors.
    __email__ : str
        Contact email for the project.
    __version__ : str
        Package version in format ``<major>.<minor>.<micro>``
    __version_description__ : str
        Short description for the current version.
    __short_description__ : str
        Short summary of the package.
    __doc__ : Str
        Longer description of the package.
    __platforms__ : List[str]
        List of supported platforms
"""

__all__ = [
    "__license__",
    "__copyright__",
    "__url__",
    "__download_url__",
    "__docs_url__",
    "__contributors__",
    "__contributors_lines__",
    "__email__",
    "__version__",
    "__version_description__",
    "__short_description__",
    "__doc__",
    "__platforms__"
]

__license__ = "Apache 2.0"
__copyright__ = "2021, ISCF committee"

# Source URL
__url__ = "https://github.com/riverlane/QHAL"
# Package Hosting URL
__download_url__ = ""

contributors = [""]
__contributors__ = ", ".join(contributors)
__contributors_lines__ = "\n".join(contributors)
__email__ = ""

version_info = (0, 1, 2)
"""Tuple[int, int, int] : version information
The three components of the version:
``major``, ``minor`` and ``micro``: Module level variable documented inline.
"""
__version__ = ".".join(map(str, version_info[:3]))
__version_description__ = ""


__short_description__ = "Quantum HAL"
__doc__ = ""
__docs_url__ = ""

__platforms__ = ['']
