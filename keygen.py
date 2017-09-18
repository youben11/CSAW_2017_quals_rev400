import numpy as np
from string import printable as pr

#       the equations
#      f8 f7 f6 f5 f4 f3 f2 
eq1 = [0, 1 , 1, 1, 1, 1, 1]
eq2 = [1, 0 , 1, 1, 1, 1, 1]
eq3 = [1, 1 , 0, 1, 1, 1, 1]
eq4 = [1, 1 , 1, 0, 1, 1, 1]
eq5 = [1, 1 , 1, 1, 0, 1, 1]
eq6 = [1, 1 , 1, 1, 1, 0, 1]
eq7 = [1, 1 , 1, 1, 1, 1, 0]

#the cst value of the b vector
#cst = [0x270 + 2, 0x255 + 2, 0x291 + 2, 0x233 + 2, 0x278 + 2, 0x221 + 2, 0x25d - 2]
cst = [0x211 + 2, 0x229 + 2, 0x25e + 1, 0x1f9 + 2, 0x27b + 2, 0x209 + 2, 0x290 - 2]

#the value to decrement to the f1
#dec = [0x55, 0x91, 0x33, 0x78, 0x21, 0x5d, 0x8f]
dec = [0x29, 0x5e, 0xf9, 0x7b, 0x09, 0x90, 0xdf]

b = [0, 0, 0, 0, 0, 0, 0]

cpt = 0

for f1 in pr:
    for i in range(7):
        b[i] = cst[i] - abs(ord(f1) - dec[i])
    
    #build the system of equation    
    sys_eq = np.array([eq1, eq2, eq3, eq4, eq5, eq6, eq7])
    b = np.array(b)
    
    x = np.linalg.solve(sys_eq, b)
    
    #valid them
    if np.allclose(np.dot(sys_eq, x), b):
        sol = []
        valid = True
        
        for a in [i for i in x]:
            if a < 32 or a > 127:
                valid = False
            
        if valid:
            sol += [int(i) for i in x]
            sol.append(ord(f1))
            print map(chr,sol)
            cpt += 1
        
print cpt, "solution found in the ascii"
    

