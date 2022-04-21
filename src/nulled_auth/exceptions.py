class InvalidKeyException(Exception):
  """Raise when an invalid auth_key is provided"""

class KeyNotRegisteredException(Exception):
  """Raise when the key is not registered in the auth service"""

class HTTPStatusNotCorrectException(Exception):
  """Raise when the HTTP status is not 200 OK"""

class StatusNotCorrectException(Exception):
  """Raise when the status is not true"""

class HashNotMatchingException(Exception):
  """Raise when the hash of the user is not matching the hash of the server"""

class RankUnderRequiredException(Exception):
  """Raise when the user rank is under the required rank"""

class LikesUnderRequiredException(Exception):
  """Raise when the user likes are under the required number of likes"""