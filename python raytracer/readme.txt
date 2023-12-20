readme.txt

Images are output in ppm image format (P6).

My code is compiled by typing python Raytracer.py input.txt 
(txt files must be in same folder as Raytracer.py). I also wrote a script 
to run all the txt files (run_raytracer.py). To run the script, txt folders 
must be in a folder “Assignment3-Test-and-Keys”. I’m assuming the script 
won’t be used by I’m keeping it in the submission folder in case it helps. 

Running Raytracer.py does take around upwards of a minute, 
not sure if it’s just my laptop or not.

testAmbient: matches key
testBackground: matches key
testBehind: matches key
testDiffuse: matches key
testIllum: looks a little off
testImgPlane:  looks a little off (too big??? Matches otherwise)
testIntersection: matches key
testParsing: matches key
testReflection: matches key
testSample: matches key
testShadow: matches key
testSpecular: matches key

I tried a few different ways to deal with spheres intersecting the 
near plane but wasn’t really successful.