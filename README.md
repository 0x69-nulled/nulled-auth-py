# Nulled.to releases authentication module for python

[![PyPi Package](https://img.shields.io/pypi/v/nulled-auth.svg)](https://pypi.org/project/nulled-auth/)

## Requirements
* Python 3.6+

## Installation
* Install with pip: `pip install nulled-auth`


## Documentation
1. Download and install the package from pypi.com with `pip install nulled-auth`
2. Include the package in your project:
  * `from nulled_auth import auth`
3. Create a new object `authentication = auth.Auth(program_id='', program_secret='', minimum_group=auth.Ranks.NONE, minimum_likes=0, both_requirements=False)`
  * __Mandatory fields__:
    * _program_id_ : 
      * Definition:
        * Program id provided by staff
      * Type:
        * string
      * Default value:
        * _No default value_
    * _program_secret_ :
      * Definition:
        * Program secret provided by staff
      * Type:
        * string
      * Default value:
        * _No default value_
  * __Optional fields__:
    * _minimum_group_
      * Definition:
        * Minimum user group to access application
      * Type:
        * `Enum`
          * `auth.Ranks.NOVA`
          * `auth.Ranks.AQUA`
          * `auth.Ranks.VIP`
          * `auth.Ranks.NONE`
      * Default value:
        * `auth.Ranks.NONE`

    * _minimum_likes_ (Default: 0):
      * Definition:
        * Minimum number of likes to access application
      * Type:
        * `integer`
      * Default value:
        * `0`
    * _both_requirements_
      * Definition:
        * if `True`
          * Will make mandatory both `minimum_group` and `minimum_likes` requirements
        * if `False`
          * Will authenticate if it haves one of the 2 requirements `minimum_group` or `minimum_likes`
      * Type:
        * `boolean`
      * Default value:
        * `True`

4. Check if `key` is valid for the authentication `authentication.get_auth(key)`
  * Returns `boolean, [string]`
  * First return value: 
    * Either if it has passed the authentication process or not `True` or `False`
  * Second value value:
    * In case of not passing the authentication it returns an array of 1 or more messages of why it didnt authenticate
    * In case of passing the authentication it returns an array with one message with the text: `Success!`


## Getting help
* In case there is any problem or cant get it to work, send a PM to 0x69 on Nulled.to