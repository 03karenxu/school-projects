**README**

**Date completed: December 4th, 2023**

Final assignment for my graphics class. Task was to write a raytracer from scratch that handles spheres and transformed spheres. Does not handle refracted light, but does handle reflected light and local illumination. 

**INPUT FILE SPECIFICATIONS:**

Files must be in folder named Tests-and-Keys. Folder already contains example test.txt files and the .png keys for each test with the expected output.

Content:
* integer      ** float(s)                *** float(s) between 0 and 1

1. The near plane**, left**, right**, top**, and bottom**
2. The resolution of the image nColumns* X nRows*
3. The position** and scaling** (non-uniform), color***, Ka***, Kd***, Ks***, Kr*** and the specular exponent n* of a sphere
4. The position** and intensity*** of a point light source
5. The background colour***
6. The scene’s ambient intensity***
7. The output file name (you should limit this to 20 characters with no spaces)

Format:

NEAR \<n\>

LEFT \<l\>

RIGHT \<r\>

BOTTOM \<b\>

TOP \<t\>

RES \<x\> \<y\>

SPHERE \<name\> \<pos x=""\> \<pos y=""\> \<pos z=""\> \<scl x=""\> \<scl y=""\> \<scl z=""\> \<r\> \<g\> \<b\> \<ka\> \<kd\> \<ks\> \<kr\> \<n\>

… // up to 14 additional sphere specifications

LIGHT \<name\> \<pos x=""\> \<pos y=""\> \<pos z=""\> \<ir\> \<ig\> \<ib\>

… // up to 9 additional light specifications

BACK \<r\> \<g\> \<b\>

AMBIENT \<ir\> \<ig\> \<ib\>

OUTPUT \<name\>

**TO RUN:**

Navigate to the python raytracer directory in the command line and enter:
```
  $ python Raytracer.py <input.txt>
```
Note: \<input.txt\> is a placeholder. Replace with the desired test file (test___.txt) in "Assignment3-Tests-and-Keys".

I also included a script to run the raytracer on all given input files. To run, enter:
```
  $ python run_raytracer.py
```

**OUTPUT:**
Images are output in .ppm image format (P6) depending on which test.txt file is given as input.
Eg. If raytracer is run on testDiffuse.txt, the program will generate testDiffuse.ppm with the resulting image.

Example output below:

![keySample](https://github.com/03karenxu/school-projects/assets/117241687/1dcd627d-18d2-406e-b2c2-d989a76f6e56)

testSample.txt outputs testSample.ppm


