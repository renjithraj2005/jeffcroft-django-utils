from hashlib import sha1
from django.core.cache import get_cache 




def cacheable(seconds=300, cache_alias='default'):
  """
  Cache the result of a function call for the specified number of seconds, 
  using Django's caching mechanism.
  Assumes that the function never returns None (as the cache returns None to indicate a miss), and that the function's result only depends on its parameters.
  Note that the ordering of parameters is important. e.g. myFunction(x = 1, y = 2), myFunction(y = 2, x = 1), and myFunction(1,2) will each be cached separately. 

  Usage:

  @cache(600, memcached)
  def myExpensiveMethod(parm1, parm2, parm3):
      ....
      return expensiveResult
`
  """
  def doCache(f):
    def x(*args, **kwargs):
      key = sha1(str(f.__module__) + str(f.__name__) + str(args) + str(kwargs)).hexdigest()
      _djcache = get_cache(cache_alias)
      result = _djcache.get(key)
      if result is None:
        result = f(*args, **kwargs)
        _djcache.set(key, result, seconds)
      return result
    return x
  return doCache