import time
import pip._vendor.requests as requests
from enum import Enum
from nulled_auth.util import get_hwid, get_hash
from nulled_auth.exceptions import HTTPStatusNotCorrectException, HashNotMatchingException, InvalidKeyException, KeyNotRegisteredException, LikesUnderRequiredException, RankUnderRequiredException, StatusNotCorrectException

class Ranks(Enum):
  """
  The ranks of the user.
  """
  NOVA = 1338
  AQUA = 1337
  VIP = 1336 # "Placeholder" number
  NONE = 0

class Auth:

  def __init__(self, program_id, program_secret, minimum_group=Ranks.NONE, minimum_likes=0, both_requirements=True):
    self.program_id = program_id
    self.program_secret = program_secret
    self.minimum_group = minimum_group
    self.minimum_likes = minimum_likes
    self.user_info = None
    self.both_requirements = both_requirements
    self.try_register_once = False

  def __validate_user(self, auth_key) -> str:
    """
    Validates the auth_key with the hwid and returns the user data if it's valid
    """
    url = 'https://www.nulled.to/authkeys.php'
    data = {
      'validate': '1',
      'key': auth_key,
      'hwid': get_hwid(),
      'program_id': self.program_id
    }
    response = requests.post(url, data)
    if response.status_code != 200:
      raise Exception('Error while validating user')
    else:
      data = response.json()
      if data['status'] != True:
        if '#723' in data['data']['message']:
          raise InvalidKeyException('Invalid auth key')
        elif '#722' in data['data']['message']:
          raise KeyNotRegisteredException('Key not registered')
        else:
          raise Exception(data['data']['message'])
      else:
        return data['data']



  def __register_user(self, auth_key) -> None:
    """
    Ties the auth_key with the hwid
    """
    url = 'https://www.nulled.to/authkeys.php'
    data = {
      'register': '1',
      'key': auth_key,
      'hwid': get_hwid(),
      'program_id': self.program_id
    }
    response = requests.post(url, data)
    if response.status_code != 200:
      raise HTTPStatusNotCorrectException('Error while registering user')
    else:
      data = response.json()
      if data['status'] != True:
        raise StatusNotCorrectException(data['data']['message'])
        


  def __validate_rank(self) -> bool:
    """
    Validates the user rank vs. the required rank
    """
    extra = int(self.user_info['extra'])
    
    # User has no extra field -> pleb
    if self.minimum_group != Ranks.NONE.value and 'extra' not in self.user_info:
      raise RankUnderRequiredException('User rank is under the required rank ' + str(self.minimum_group) + ', please upgrade your account here: https://www.nulled.to/gateway.php')


    if self.minimum_group == Ranks.NONE: # Required group is pleb
      return True
    elif self.minimum_group == Ranks.NOVA: # Required group is nova
      if extra == Ranks.NOVA.value:
        return True
      else:
        raise RankUnderRequiredException('User rank is not NOVA+, to use this NOVA+ tool upgrade here: https://www.nulled.to/gateway.php')
    elif self.minimum_group == Ranks.AQUA: # Required group is aqua
      if extra == Ranks.NOVA.value or extra == Ranks.AQUA.value:
        return True
      else:
        raise RankUnderRequiredException('User rank is not AQUA+, to use this AQUA+ tool upgrade here: https://www.nulled.to/gateway.php')
    else: # Required group is vip
      if extra == Ranks.NOVA.value or extra == Ranks.AQUA.value:
        return True
      elif extra != "":
        now = time.time() # im not too sure if this is correct
        if now > extra:
          raise RankUnderRequiredException('User rank VIP expired, to use this tool upgrade here: https://www.nulled.to/gateway.php')
      else:
        raise RankUnderRequiredException('User rank is under the required rank ' + str(self.minimum_group) + ', please upgrade your account here: https://www.nulled.to/gateway.php')
        
  def __validate_likes(self) -> bool:
    """
    Validates the user likes vs. the required number of likes
    """
    likes = int(self.user_info['Likes'])

    if likes < self.minimum_likes:
      raise LikesUnderRequiredException('User likes are under the required number of likes (' + str(self.minimum_likes) + ' likes), please contribute more :)')
    else:
      return True



  def __validate_hash(self, auth_key) -> bool:
    """
    Validates de hash of the user vs. the hash of the server
    """
    hash = get_hash(self.program_secret, auth_key)
    if hash == self.user_info['hash']:
      return True
    else:
      raise HashNotMatchingException('Invalid hash')



  def get_auth(self, auth_key):
    # Validate auth key, if not registered then register it and try again
    try:
      self.user_info = self.__validate_user(auth_key) # Try to validate existing auth key
    except InvalidKeyException as e: # If key not valid, False auth
      return False, ['Invalid key provided']
    except KeyNotRegisteredException as e: # If key not registered, register it
      try:
        if self.try_register_once: # If already tried to register once, False auth to prevent infinite loop
          return False, ['Key could not be registered']

        self.__register_user(auth_key)
        self.try_register_once = True
        return self.get_auth(auth_key) # Try validating again after registering
      except StatusNotCorrectException as e: # If error while registering key, False auth
        return False, [str(e)]
      except Exception as e:
        return False, [str(e)]
    except Exception as e: # If any other error, False auth
      return False, [str(e)]
    
    # Validate hash
    try:
      self.__validate_hash(auth_key) # If everything above correct, then validate the hash with the server
    except HashNotMatchingException as e: # If hash not valid, False auth
      return False, [str(e)]
    except Exception as e: # If any other error, False auth
      return False, [str(e)]


    # Validate group
    group_valid = True
    group_message = ''
    try:
      self.__validate_rank()
    except RankUnderRequiredException as e:
      group_valid = False
      group_message = str(e)
    except Exception as e:
      return False, [str(e)]

    # Validate likes
    likes_valid = True
    likes_message = ''
    try:
      self.__validate_likes()
    except LikesUnderRequiredException as e:
      likes_valid = False
      likes_message = str(e)
    except Exception as e:
      return False, [str(e)]

    
    if self.both_requirements:
      if group_valid and likes_valid:
        return True, ['Success!']
      else:
        return False, [group_message, likes_message]
    else:
      if group_valid or likes_valid:
        return True, ['Success!']
      else:
        return False, [group_message, likes_message]