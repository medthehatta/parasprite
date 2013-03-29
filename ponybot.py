#!/usr/bin/env python
import time
import pickle
import re

def load_ponies():
  return pickle.load(open('ponysodes.pkl','rb'))

def save_ponies(current):
  ponies = load_ponies()
  ponies.update({'current':current})
  return pickle.dump(ponies,open('ponysodes.pkl','wb'))

def countdown(phenny, input):
  """Does a countdown for 5 seconds"""
  phenny.say("Counting down...")
  for i in xrange(5,0,-1):
    phenny.say("{0}...".format(i))
    time.sleep(1)
  phenny.say("GO!")
countdown.commands = ['countdown']

def episode(phenny, input):
  """Which episode are we on?"""
  ponies = load_ponies()
  current = ponies['current']
  episodes = ponies['episodes']
  phenny.say("S{0}E{1} - {2}".format(current[0],current[1],episodes[current[0]][current[1]-1]))
episode.commands = ['ep\?','episode','ep']

def episode_plus(phenny, input):
  ponies = load_ponies()
  current = ponies['current']
  episodes = ponies['episodes']
  
  advance = 1
  if len(input.groups())>1: 
    advance = int(input.group(2))

  if input.group(1).lower()=='s':
    if current[0]+advance < len(episodes.keys()):
      current = (current[0]+advance,1)
    else:
      phenny.say("Season {0} hasn't been made yet!".format(current[0]+advance))
      return
  else:
    if current[1]+advance < len(episodes[current[0]]):
      current = (current[0],current[1]+advance)
    else:
      phenny.say("Season {0} has no episode {1}!  Try Season {2}!".format(current[0],current[1]+advance,current[0]+1))
      return
  save_ponies(current)
  episode(phenny,input)
episode_plus.rule = r'^\.(e|s) ((?:\+|\-)?[0-9]+)?'

def episode_next(phenny, input):
  ponies = load_ponies()
  current = ponies['current']
  episodes = ponies['episodes']

  advance = 1
  if current[1]+advance < len(episodes[current[0]]):
    current = (current[0],current[1]+advance)
  else:
    phenny.say("Season {0} has no episode {1}!  Try Season {2}!".format(current[0],current[1]+advance,current[0]+1))
    return
  save_ponies(current)
  episode(phenny,input)
episode_next.commands = ['next']

def girls(phenny, input):
  """Girls!"""
  phenny.say("**SHOT**")
girls.rule = r'.*[Gg]irls.*'

def grammar(phenny, input):
  """everybody->everypony""" 
  read = str(input)
  changed = False
  replacements = [("everybody","every*pony*"),
                  ("nobody", "no*pony*"),
                  ("a hand", "a *hoof*")]
  for (match,replace) in replacements:
    if re.findall(match,read): 
      changed = True
      read = re.sub(match,replace,read)
  if changed == True:
    phenny.say("Don't you mean: \""+read+"\"?")
grammar.rule = r'.*'



if __name__ == '__main__': 
   print __doc__.strip()
