def cad_par_unos(n):
  if n == 0:
    return ['']

  if n == 1:
    return ['0', '2']
  prev = [str(i) for i in range(3)]
  new = prev

  for lon in range(n-1):
    new = []
    for z in prev:
      for char in [str(i) for i in range(3)]:
        if len(z) == n-1:
          if z.count('1')%2 == 0:
            if char != '1':
              new.append(z+char)
          else:
            if char == '1':
              new.append(z+char)
        else:
          new.append(z+char)
    prev = new.copy()
  return new

def cad_crecientes(n):
  if n == 0:
    return ['']
  prev = [str(i) for i in range(5)]
  new = prev.copy()

  for lon in range(n-1):
    new = []
    for z in prev:
      for char in [str(i) for i in range(5)]:
        if int(z[-1]) <= int(char):
          new.append(z+char)
    prev = new.copy()
  return new

def cad_con_subcad(n, b, subcad):

  if n < len(subcad):
    return []

  if n == len(subcad):
    return [subcad]
  prev = [str(i) for i in range(b)]
  new = prev

  for lon in range(n-1):
    new = []
    for z in prev:
      for char in [str(i) for i in range(b)]:
        if len(z) > n-len(subcad) and subcad not in z:
          try:
            si = len(z) - 1 - z[::-1].index(subcad[0])
          except:
            continue
          fi = si
          while fi < len(z) and fi-si < len(subcad):
            if z[fi] != subcad[fi-si]:
              break
            fi += 1
          if fi >= len(z) and char == subcad[fi-si]:
            new.append(z+char)
        else:
          new.append(z+char)
      prev = new.copy()
  return new

def cad_sin_restr(n, b, restr):

  if n == 0:
    return ['']
  if n == 1:
    return [str(i) for i in range(b) if str(i) not in restr]
  prev = cad_sin_restr(n-1, b, restr)
  new = []
  for z in prev:
    for char in [str(i) for i in range(b) if str(i) not in restr]:
      can_append = True
      for r in restr:
        if z[-1] == r[-2] and char == r[-1]:
          if r[:-2] == z[-len(r)+1:-1]:
            can_append = False
          break
      if can_append:
        new.append(z+char)
  return new