import subprocess
from hashlib import sha256
import os
import shutil
import time
import winreg
from sys import platform
import platform as pltf

def get_c_name() -> str:
  """
  Get the computer name.
  """
  return pltf.node() # Multiplatform
    

def get_p_rev() -> str:
  """
  Get the processor revision of the device.
  Returns the platform if its not Windows.
  """
  if platform == 'win32':
    return os.getenv('PROCESSOR_REVISION')
  elif platform == 'linux':
    val = subprocess.check_output(["cat /proc/cpuinfo | grep 'model name' | cut -f 2-"], shell=True)
    if val:
      return val.decode('utf-8').strip()

  # Anything else or error
  return platform

def get_disk_size() -> int:
  """
  Get the size of the main disk.
  """
  return shutil.disk_usage("/").total

def get_uuid():
  """
  Get the UUID of the device.
  Returns the platform if its not Windows.
  """
  if platform == 'win32':
    return os.getenv('PROCESSOR_IDENTIFIER')
  else:
    return platform

def get_guid():
  """
  Get the GUID of the device.
  Returns the platform if its not Windows.
  """
  if platform == 'win32':
    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Cryptography")
    value, _ = winreg.QueryValueEx(key, "MachineGuid")
    return value.upper()
  else:
    return platform


def get_hwid() -> str:
  """
  Get the hardware ID of the device.
  """
  c_name = get_c_name()
  u_name = os.getlogin()
  p_rev = get_p_rev()
  disk = get_disk_size()
  uuid = get_uuid()
  guid = get_guid()

  str = f"{c_name}{u_name}{p_rev}{disk}{uuid}{guid}"
  return sha256(str.encode('utf-8')).hexdigest().upper()

def get_hash(secret: str, auth_key: str) -> str:
  """
  Generate a hash based on the secret and the auth key.
  """
  u_timestamp = round(time.time() / 200) * 200
  program_secret = secret
  auth_key = auth_key
  hwid = get_hwid()
  
  str = f"{program_secret}{auth_key}{hwid}{u_timestamp}"
  return sha256(str.encode('utf-8')).hexdigest().upper()