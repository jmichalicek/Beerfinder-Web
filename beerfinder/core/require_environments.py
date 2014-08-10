"""
custom django-require env
"""

from require.environments import Environment

class DebianNodeEnvironment(Environment):
    """
    Custom node environment becaus debian has a non-standard name for the nodejs env.
    This if from 2010, but it is still true and probably will not change.
    https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=597571
    """
    def args(self):
        # Start of the command to run the compiler in Node.
        return ["nodejs"]
