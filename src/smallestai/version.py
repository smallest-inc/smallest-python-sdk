# Hand-maintained (see .fernignore). The generator emits
# `metadata.version("smallest-ai")`, but the published distribution is named
# `smallestai`, so that lookup raises PackageNotFoundError and breaks
# `import smallestai; smallestai.__version__`. Look up the correct name and fall
# back gracefully when metadata is unavailable (e.g. running from source).
from importlib import metadata

try:
    __version__ = metadata.version("smallestai")
except metadata.PackageNotFoundError:
    # Running from a source checkout (not pip-installed). Use a distinct sentinel
    # rather than "0.0.0" so the backend can tell checkout traffic apart from a
    # real install in the X-Fern-SDK-Version dimension.
    __version__ = "0.0.0-dev"
