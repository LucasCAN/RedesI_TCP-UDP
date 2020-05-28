# Python3 program to check if 
# a point lies inside a circle  
# or not 
  
def isInside(coord, center, rad): 

    lat = coord[0]
    lon = coord[1]
    x = center[0]
    y = center[1]
      
    # Compare radius of circle 
    # with distance of its center 
    # from given point 
    if ((x - lat) * (x - lat) + 
        (y - lon) * (y - lon) <= rad * rad): 
        return True; 
    else: 
        return False; 
  
# Driver Code 
x = 1;  
y = 1; 
lat = 4;  
lon = 4;  
rad = 10; 
if(isInside(coord, center, rad)): 
    print("Inside"); 
else: 
    print("Outside"); 
  
# This code is contributed 
# by mits. 