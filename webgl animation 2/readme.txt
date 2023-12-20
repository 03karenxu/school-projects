readme.txt 

1. Hierarchical object with at least 2 levels of hierarchy was
    created (dog model).
2. 3 textures were used. 2 textures cloud.png and water.png oscillate in 
    the x and y directions. Cloud.png was scaled to account for the 
    non-uniform scale of the spheres in the cloud model. The grass texture was
    mapped to the ground cube with default coords.
3. ADS shader in vertex shader was converted to the fragment shader. I used the
    base code given in Lab 7 and made modifications to it so that lighting
    was calculated in the fragment shader instead. I also made modifications
    to handle my textures and the shader effect.
4. I converted the Phong to Blinn-Phong for the specular light
5. Shader effect was implemented as an if-statment in the fragment shader. The
    shader coverts all fragments to their equivalent gray-value by taking
    the average of R,G, and B at the given fragment and setting the average
    as the new RGB values. It turns the whole screen gray after the ball
    flies up.
6. cameraController() contains an if-statement that controlls the 360 camera fly,
    used in the last scene.
7. Animations that would use timestamp are animated with frames, incremented
    whenever a new animFrame is requested. I also used dt for my animations
    so the scene is still connected to real-time.
8. FPS is displayed every 2 seconds with the showFPS() function

I used the Lab7 code as a base for my assignment. I used the bouncing ball
animation from that lab as well, with a few modifications to fit my scene.
I also made modifications to my A1 code to animate parts of the legs and
tail (drawTail() is a modified version of my drawSeaweed() function from A1).
Attributions for the texture pngs are in main.js where the textures are added
to textureArray.