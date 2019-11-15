class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class NotInitializedError(Error):
    def __init__(self, msg):
        Exception.__init__(self, msg)