import distutils.sysconfig

gcv = distutils.sysconfig.get_config_vars
def my_get_config_vars(*args):
  def replace(thing, value, args, vars):
    if not args: 
      vars[thing] = value
    elif thing in args:
      vars[list(args).index(thing)] = value
  def prepend(thing, value, args, vars):    
    if not args: 
      vars[thing] = value + vars[thing]
    elif thing in args:
      vars[list(args).index(thing)] = value + vars[list(args).index(thing)]
  def append(thing, value, args, vars):    
    if not args: 
      vars[thing] = vars[thing] + value
    elif thing in args:
      vars[list(args).index(thing)] = vars[list(args).index(thing)] + value
  vars = gcv(*args)
  replace('UNIVERSALSDK', '/Developer/SDKs/MacOSX10.4u.sdk', args, vars)
  prepend('LDFLAGS', '-arch i386 -arch ppc -isysroot /Developer/SDKs/MacOSX10.4u.sdk ', args, vars)
  prepend('BASECFLAGS', '-arch ppc -arch i386 -isysroot /Developer/SDKs/MacOSX10.4u.sdk ', args, vars)
  prepend('CFLAGS', '-arch ppc -arch i386 -isysroot /Developer/SDKs/MacOSX10.4u.sdk ', args, vars)
  return vars
distutils.sysconfig.get_config_vars = my_get_config_vars

import setup
