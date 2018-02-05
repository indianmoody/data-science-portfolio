import numpy as np 

data = { 'india': [(1,1),(1,2),(1,3),(2,1),(2,2)], 'abroad': [(3,2),(3,4),(4,2),(4,3)]}

#print(np.linalg.norm(np.array((0,0)) - np.array((1,1))))

'''
d = {'a':10, 'b': 5, 'c': 8, 'd': 15, 'e': 3}
print(sorted(d.items(), key=lambda x: x[1], reverse=True))
'''


def knn(data, k, pt):
  kdict = {}
  
  for lists in data.values():
    for elem in lists:
      dist = np.linalg.norm(np.array(elem) - np.array(pt))
      kdict[elem] = dist
      
  klist = sorted(kdict.keys(), key=lambda x: kdict[x])[:k]
  
  india = 0
  abroad = 0 
  shit = 0
  
  for i in klist:
    if i in data['india']:
      india += 1 
    elif i in data['abroad']:
      abroad += 1 
    else:
      shit += 1
  
  print("india: {}\nabroad: {}\nshit: {}\n".format(india, abroad, shit))
  
knn(data, 3, (1.5,2))

  

'''
d = {(4,5): 82, (1,2): 100, (2,3): 98}
print(sorted(d.keys(), key=lambda x: d[x], reverse=True))
'''