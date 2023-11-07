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

def problema1():
  """Función principal del Problema 1"""
  datos = [(2,'10'), (2,['010']), (3,['12']), (3,'012'), '', '', (5, ['01','43'])]

  while True:
    print('\nMENÚ:')
    print('- Cadenas Binarias, de longitud n, que:\n  1. Contengan la subcadena ’10’\n  2. Que No contengan ’010’')
    print('- Cadenas Ternarias, de longitud n, que:\n  3. No contengan la subcadena ’12’\n  4. Que contengan la subcadena ’012’\n  5. Que contengan un número par de unos')
    print('- Cadenas númericas, de longitud n, de base cinco que:\n  6. Tengan sus caracteres en orden creciente. Ejemplo ’01122234’\n  7. Que No contengan las subcadenas ’01’ ni ’43’')
    print('8. Salir del programa')

    opc = input('Ingrese la opción escogida: ') 
    while not opc in [str(i) for i in range(1,9)]: 
      opc = input('Opción inválida. Intente de nuevo.\nIngrese la opción escogida: ')
    opc = int(opc)

    if opc == 8:
      print('\n** FINALIZANDO EJECUCIÓN **')
      break
    n = input('Ingrese el valor de n: ')
    while not n.isdecimal(): 
      n = input('Ingrese el valor de n: ')
    n = int(n)

    print('Las cadenas generadas para esta opción son:')
    if opc in [2, 3, 7]:
      r = cad_sin_restr(n, datos[opc-1][0], datos[opc-1][1])
    elif opc in [1, 4]:
      r = cad_con_subcad(n, datos[opc-1][0], datos[opc-1][1])
      pass
    elif opc == 5:
      r = cad_par_unos(n)
    elif opc == 6:
      r = cad_crecientes(n)
    print(f'{r}\n({len(r)} cadenas resultantes)')