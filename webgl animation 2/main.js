
var canvas;
var gl;

var program;

var near = 1;
var far = 110;
var fovy = 50;

var lightPosition2 = vec4(100.0, 100.0, 100.0, 1.0 );
var lightPosition = vec4(0.0, 100.0, 100.0, 1.0 );

var lightAmbient = vec4(0.2, 0.2, 0.2, 1.0 );
var lightDiffuse = vec4( 1.0, 1.0, 1.0, 1.0 );
var lightSpecular = vec4( 1.0, 1.0, 1.0, 1.0 );

var materialAmbient = vec4( 1.0, 1.0, 1.0, 1.0 );
var materialDiffuse = vec4( 1.0, 1.0, 1.0, 1.0 );
var materialSpecular = vec4( 0.2, 0.2, 0.2, 1.0 );
var materialShininess = 30.0;

var ambientColor, diffuseColor, specularColor;

var modelMatrix, viewMatrix, modelViewMatrix, projectionMatrix, normalMatrix;
var modelViewMatrixLoc, projectionMatrixLoc, normalMatrixLoc;
var eye;
var at = vec3(3.0, 4.0, 0.0);
var up = vec3(0.0, 1.0, 0.0);

var RX = 0;
var RY = 0;
var RZ = 0;

var MS = []; // The modeling matrix stack
var seconds = 1000;
var dt = 0.0
var prevTime = 0.0;
var resetTimerFlag = true;
var animFlag = true;
var controller;

// These are used to store the current state of objects.
// In animation it is often useful to think of an object as having some DOF
// Then the animation is simply evolving those DOF over time.

//camera
var camRotation = [0,0];

//dog
var dogPosition = [0,0.2];
var tailRotation = [0,0,0,0,0,0,0];
var tailPosition = [0,0.3,0];
var thighRotation = [0,0,0,0,0,0];
var calfRotation = [0,0,0,0,0,0];
var earRotation = [0,0,0];
var headRotation = [0,0];
var headPosition = [0.5,1.2,0];
var headAngle = 0.0;
var headDir = [0,0,0];

//propellor
var propRotation = [0,0];
var propPosition = [0,0];
var propSize = [0,0];

//ball
var bouncingCubePosition = [0,4,0];
var bouncyBallVelocity = 0;
var gravity = -9.8;

//clouds
var cloudPosition= [0,0,0];

//scene changes
var flying = 7.5*seconds;
var ballUp = false;
var gray = 3.5*seconds;
var zoom = 5*seconds;
var bounces = 0;

//FPS
var frames;
var frameRate;

//shader
var grassTexture = 0;
var cloudTexture = 0;
var waterTexture = 0;
var grayScale = 0;

// For this example we are going to store a few different textures here
var textureArray = [] ;

// Setting the colour which is needed during illumination of a surface
function setColor(c)
{
    ambientProduct = mult(lightAmbient, c);
    diffuseProduct = mult(lightDiffuse, c);
    specularProduct = mult(lightSpecular, materialSpecular);
    
    gl.uniform4fv( gl.getUniformLocation(program,
                                         "ambientProduct"),flatten(ambientProduct) );
    gl.uniform4fv( gl.getUniformLocation(program,
                                         "diffuseProduct"),flatten(diffuseProduct) );
    gl.uniform4fv( gl.getUniformLocation(program,
                                         "specularProduct"),flatten(specularProduct) );
    gl.uniform4fv( gl.getUniformLocation(program,
                                         "lightPosition"),flatten(lightPosition2) );
    gl.uniform1f( gl.getUniformLocation(program, 
                                        "shininess"),materialShininess );
}

// We are going to asynchronously load actual image files this will check if that call if an async call is complete
// You can use this for debugging
function isLoaded(im) {
    if (im.complete) {
        console.log("loaded") ;
        return true ;
    }
    else {
        console.log("still not loaded!!!!") ;
        return false ;
    }
}

// Helper function to load an actual file as a texture
// NOTE: The image is going to be loaded asyncronously (lazy) which could be
// after the program continues to the next functions. OUCH!
function loadFileTexture(tex, filename)
{
	//create and initalize a webgl texture object.
    tex.textureWebGL  = gl.createTexture();
    tex.image = new Image();
    tex.image.src = filename ;
    tex.isTextureReady = false ;
    tex.image.onload = function() { handleTextureLoaded(tex); }
}

// Once the above image file loaded with loadFileTexture is actually loaded,
// this funcion is the onload handler and will be called.
function handleTextureLoaded(textureObj) {
	//Binds a texture to a target. Target is then used in future calls.
		//Targets:
			// TEXTURE_2D           - A two-dimensional texture.
			// TEXTURE_CUBE_MAP     - A cube-mapped texture.
			// TEXTURE_3D           - A three-dimensional texture.
			// TEXTURE_2D_ARRAY     - A two-dimensional array texture.
    gl.bindTexture(gl.TEXTURE_2D, textureObj.textureWebGL);
	gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, true); // otherwise the image would be flipped upsdide down
	
	//texImage2D(Target, internalformat, width, height, border, format, type, ImageData source)
    //Internal Format: What type of format is the data in? We are using a vec4 with format [r,g,b,a].
        //Other formats: RGB, LUMINANCE_ALPHA, LUMINANCE, ALPHA
    //Border: Width of image border. Adds padding.
    //Format: Similar to Internal format. But this responds to the texel data, or what kind of data the shader gets.
    //Type: Data type of the texel data
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, textureObj.image);
	
	//Set texture parameters.
    //texParameteri(GLenum target, GLenum pname, GLint param);
    //pname: Texture parameter to set.
        // TEXTURE_MAG_FILTER : Texture Magnification Filter. What happens when you zoom into the texture
        // TEXTURE_MIN_FILTER : Texture minification filter. What happens when you zoom out of the texture
    //param: What to set it to.
        //For the Mag Filter: gl.LINEAR (default value), gl.NEAREST
        //For the Min Filter: 
            //gl.LINEAR, gl.NEAREST, gl.NEAREST_MIPMAP_NEAREST, gl.LINEAR_MIPMAP_NEAREST, gl.NEAREST_MIPMAP_LINEAR (default value), gl.LINEAR_MIPMAP_LINEAR.
    //Full list at: https://developer.mozilla.org/en-US/docs/Web/API/WebGLRenderingContext/texParameter
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.NEAREST);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.NEAREST_MIPMAP_NEAREST);
	
	//Generates a set of mipmaps for the texture object.
        /*
            Mipmaps are used to create distance with objects. 
        A higher-resolution mipmap is used for objects that are closer, 
        and a lower-resolution mipmap is used for objects that are farther away. 
        It starts with the resolution of the texture image and halves the resolution 
        until a 1x1 dimension texture image is created.
        */
    gl.generateMipmap(gl.TEXTURE_2D);
	
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE); //Prevents s-coordinate wrapping (repeating)
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE); //Prevents t-coordinate wrapping (repeating)
    gl.bindTexture(gl.TEXTURE_2D, null);
    console.log(textureObj.image.src) ;
    
    textureObj.isTextureReady = true ;
}

// Takes an array of textures and calls render if the textures are created/loaded
// This is useful if you have a bunch of textures, to ensure that those files are
// actually laoded from disk you can wait and delay the render function call
// Notice how we call this at the end of init instead of just calling requestAnimtimestamp like before
function waitForTextures(texs) {
    setTimeout(
		function() {
			   var n = 0 ;
               for ( var i = 0 ; i < texs.length ; i++ )
               {
                    console.log(texs[i].image.src) ;
                    n = n+texs[i].isTextureReady ;
               }
               wtime = (new Date()).getTime() ;
               if( n != texs.length )
               {
               		console.log(wtime + " not ready yet") ;
               		waitForTextures(texs) ;
               }
               else
               {
               		console.log("ready to render") ;
					render(0);
               }
		},
	5) ;
}

// This will use an array of existing image data to load and set parameters for a texture
// We'll use this function for procedural textures, since there is no async loading to deal with
function loadImageTexture(tex, image) {
	//create and initalize a webgl texture object.
    tex.textureWebGL  = gl.createTexture();
    tex.image = new Image();

	//Binds a texture to a target. Target is then used in future calls.
		//Targets:
			// TEXTURE_2D           - A two-dimensional texture.
			// TEXTURE_CUBE_MAP     - A cube-mapped texture.
			// TEXTURE_3D           - A three-dimensional texture.
			// TEXTURE_2D_ARRAY     - A two-dimensional array texture.
    gl.bindTexture(gl.TEXTURE_2D, tex.textureWebGL);

	//texImage2D(Target, internalformat, width, height, border, format, type, ImageData source)
    //Internal Format: What type of format is the data in? We are using a vec4 with format [r,g,b,a].
        //Other formats: RGB, LUMINANCE_ALPHA, LUMINANCE, ALPHA
    //Border: Width of image border. Adds padding.
    //Format: Similar to Internal format. But this responds to the texel data, or what kind of data the shader gets.
    //Type: Data type of the texel data
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, texSize, texSize, 0, gl.RGBA, gl.UNSIGNED_BYTE, image);
	
	//Generates a set of mipmaps for the texture object.
        /*
            Mipmaps are used to create distance with objects. 
        A higher-resolution mipmap is used for objects that are closer, 
        and a lower-resolution mipmap is used for objects that are farther away. 
        It starts with the resolution of the texture image and halves the resolution 
        until a 1x1 dimension texture image is created.
        */
    gl.generateMipmap(gl.TEXTURE_2D);
	
	//Set texture parameters.
    //texParameteri(GLenum target, GLenum pname, GLint param);
    //pname: Texture parameter to set.
        // TEXTURE_MAG_FILTER : Texture Magnification Filter. What happens when you zoom into the texture
        // TEXTURE_MIN_FILTER : Texture minification filter. What happens when you zoom out of the texture
    //param: What to set it to.
        //For the Mag Filter: gl.LINEAR (default value), gl.NEAREST
        //For the Min Filter: 
            //gl.LINEAR, gl.NEAREST, gl.NEAREST_MIPMAP_NEAREST, gl.LINEAR_MIPMAP_NEAREST, gl.NEAREST_MIPMAP_LINEAR (default value), gl.LINEAR_MIPMAP_LINEAR.
    //Full list at: https://developer.mozilla.org/en-US/docs/Web/API/WebGLRenderingContext/texParameter
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.NEAREST_MIPMAP_LINEAR);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.NEAREST);
	
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE); //Prevents s-coordinate wrapping (repeating)
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE); //Prevents t-coordinate wrapping (repeating)
    gl.bindTexture(gl.TEXTURE_2D, null);

    tex.isTextureReady = true;
}

// This just calls the appropriate texture loads for this example adn puts the textures in an array
function initTexturesForExample() {
    textureArray.push({}) ;
    loadFileTexture(textureArray[textureArray.length-1],"grass.png") ;
    
    textureArray.push({}) ;
    loadFileTexture(textureArray[textureArray.length-1],"clouds.png") ;

    textureArray.push({}) ;
    loadFileTexture(textureArray[textureArray.length-1],"water.png") ;
}

// Turn grass texture use on and off
function toggleTextureGrass() {
    grassTexture = (grassTexture + 1) % 2;
	gl.uniform1i(gl.getUniformLocation(program, "grassTexture"), grassTexture);
}

// Turn cloud texture use on and off
function toggleTextureCloud() {
    cloudTexture = (cloudTexture + 1) % 2;
	gl.uniform1i(gl.getUniformLocation(program, "cloudTexture"), cloudTexture);
}

// Turn water texture use on and off
function toggleTextureWater() {
    waterTexture = (waterTexture + 1) % 2;
	gl.uniform1i(gl.getUniformLocation(program, "waterTexture"), waterTexture);
}


// Turn grayScale use on and off
function initGrayScale() {
	gl.uniform1i(gl.getUniformLocation(program, "grayScale"), grayScale);
}

window.onload = function init() {

    frames = 0;

    canvas = document.getElementById( "gl-canvas" );
    
    gl = WebGLUtils.setupWebGL( canvas );
    if ( !gl ) { alert( "WebGL isn't available" ); }

    gl.viewport( 0, 0, canvas.width, canvas.height );
    gl.clearColor( 0.6, 0.8, 0.8, 1.0 );//bg colour
    
    gl.enable(gl.DEPTH_TEST);

    //
    //  Load shaders and initialize attribute buffers
    //
    program = initShaders( gl, "vertex-shader", "fragment-shader" );
    gl.useProgram( program );
    
    setColor(materialDiffuse);
	
	// Initialize some shapes, note that the curved ones are procedural which allows you to parameterize how nice they look
	// Those number will correspond to how many sides are used to "estimate" a curved surface. More = smoother
    Cube.init(program);
    Cylinder.init(20,program);
    Cone.init(20,program);
    Sphere.init(36,program);

    // Matrix uniforms
    modelViewMatrixLoc = gl.getUniformLocation( program, "modelViewMatrix" );
    normalMatrixLoc = gl.getUniformLocation( program, "normalMatrix" );
    projectionMatrixLoc = gl.getUniformLocation( program, "projectionMatrix" );
    
    // Lighting Uniforms
    gl.uniform4fv( gl.getUniformLocation(program, 
       "ambientProduct"),flatten(ambientProduct) );
    gl.uniform4fv( gl.getUniformLocation(program, 
       "diffuseProduct"),flatten(diffuseProduct) );
    gl.uniform4fv( gl.getUniformLocation(program, 
       "specularProduct"),flatten(specularProduct) );	
    gl.uniform4fv( gl.getUniformLocation(program, 
       "lightPosition"),flatten(lightPosition) );
    gl.uniform1f( gl.getUniformLocation(program, 
       "shininess"),materialShininess );

	// Helper function just for this example to load the set of textures
    initTexturesForExample() ;

    waitForTextures(textureArray);
}

// Sets the modelview and normal matrix in the shaders
function setMV() {
    modelViewMatrix = mult(viewMatrix,modelMatrix);
    gl.uniformMatrix4fv(modelViewMatrixLoc, false, flatten(modelViewMatrix) );
    normalMatrix = inverseTranspose(modelViewMatrix);
    gl.uniformMatrix4fv(normalMatrixLoc, false, flatten(normalMatrix) );
}

// Sets the projection, modelview and normal matrix in the shaders
function setAllMatrices() {
    gl.uniformMatrix4fv(projectionMatrixLoc, false, flatten(projectionMatrix) );
    setMV();   
}

// Draws a 2x2x2 cube center at the origin
// Sets the modelview matrix and the normal matrix of the global program
// Sets the attributes and calls draw arrays
function drawCube() {
    setMV();
    Cube.draw();
}

// Draws a sphere centered at the origin of radius 1.0.
// Sets the modelview matrix and the normal matrix of the global program
// Sets the attributes and calls draw arrays
function drawSphere() {
    setMV();
    Sphere.draw();
}

// Draws a cylinder along z of height 1 centered at the origin
// and radius 0.5.
// Sets the modelview matrix and the normal matrix of the global program
// Sets the attributes and calls draw arrays
function drawCylinder() {
    setMV();
    Cylinder.draw();
}

// Draws a cone along z of height 1 centered at the origin
// and base radius 1.0.
// Sets the modelview matrix and the normal matrix of the global program
// Sets the attributes and calls draw arrays
function drawCone() {
    setMV();
    Cone.draw();
}

// Draw a Bezier patch
function drawB3(b) {
	setMV() ;
	b.draw() ;
}

// Post multiples the modelview matrix with a translation matrix
// and replaces the modeling matrix with the result
function gTranslate(x,y,z) {
    modelMatrix = mult(modelMatrix,translate([x,y,z]));
}

// Post multiples the modelview matrix with a rotation matrix
// and replaces the modeling matrix with the result
function gRotate(theta,x,y,z) {
    modelMatrix = mult(modelMatrix,rotate(theta,[x,y,z]));
}

// Post multiples the modelview matrix with a scaling matrix
// and replaces the modeling matrix with the result
function gScale(sx,sy,sz) {
    modelMatrix = mult(modelMatrix,scale(sx,sy,sz));
}

// Pops MS and stores the result as the current modelMatrix
function gPop() {
    modelMatrix = MS.pop();
}

// pushes the current modelViewMatrix in the stack MS
function gPush() {
    MS.push(modelMatrix);
}

// camera controller function
function camController(eye,at,up,frames){
    setMV();
    if (frames > zoom && frames <= flying){
        eye = vec3(7,5,0);
        at = vec3(3,4,0);
        up = vec3(0,1,0);
        viewMatrix = lookAt(eye,at,up);
    } else if (frames > flying){
        eye = vec3(0.0,1.0,40);
        at = vec3(0.0, 15.0, 0.0);
        viewMatrix = lookAt(eye,at,up);
        if (frames > flying){
            camRotation[1] = camRotation[1] + 80*dt;
            viewMatrix = mult(lookAt(eye,at,up),rotate(camRotation[1],[0,1,0]));
        }
    }
}

//to display frame rate to canvas
function showFPS(dt){
    frameRate = 1/dt;
    const frameRateDisplay = document.getElementById("frameRateDisplay");
    frameRateDisplay.textContent = `Frame Rate: ${frameRate.toFixed(2)} FPS`;
    setTimeout(() => {
        frameRateDisplay.textContent = "";
    }, 1000);
}


//wave function
function wave(amp,freq,phase,frames) {
	return amp*Math.cos(frames/freq+phase);
}

//tail function
function drawTail(frames){
	for (let i = 1; i < 4; i++) {
		gTranslate(tailPosition[0],tailPosition[1], tailPosition[2]);
        if (!ballUp){
            tailRotation[i] = tailRotation[i] + wave(3,75,0,frames);
		    gRotate(tailRotation[i],1,0,0);
        } else if (frames < gray){
            tailRotation[i] = Math.max(tailRotation[i]-0.5*i,0);
            gRotate(tailRotation[i],1,0,0);
        } else if (frames > flying) {
            tailRotation[i+3] = tailRotation[i+3] + wave(0.6,200,0,frames);
		    gRotate(tailRotation[i+3],1,0,0);
        }
		gTranslate(tailPosition[0],tailPosition[1], tailPosition[2]);
		gPush();
		{
			gScale(0.3,0.3,0.3);
			drawSphere();
		}
		gPop();
	}
}

//draws a ball-joint
function drawJoint(){
    gPush();
        {
            gScale(0.3,0.3,0.3);
            drawSphere();
        }
    gPop();
}

//leg function
function drawLeg(frames,dir,i){
    drawJoint();
    if (frames > flying) {
        thighRotation[i] = thighRotation[i] + dir*wave(0.3,200,0,frames);
        gRotate(thighRotation[i], 0,0,1);//rotate thigh
    }
    gTranslate(0,-0.5,0);
        //draw thigh
        gPush();
            {
            gRotate(90,1,0,0);
            gScale(0.5,0.5,1.0);
            drawCylinder();
            }
        gPop();
        gTranslate(0.0,-0.5,0);//translate to joint
        drawJoint();
        if (frames > flying){
            calfRotation[i] = calfRotation[i]+ dir*wave(0.4,200,0,frames);
            gRotate(-50+calfRotation[i],0,0,1);//rotate calf
        }
        gTranslate(0.0,-0.5,0);
            //draw calf
            gPush();
            {
                gRotate(90,1,0,0);
                gScale(0.5,0.5,1.0);
                drawCylinder();
            }
            gPop();
            gTranslate(0.2,-0.5,0);
                //draw foot
                gPush();
                {
                    gScale(0.5,0.2,0.3);
                    drawCube();
                }
                gPop();
}

//draws an eye
function drawEye() {
	gScale(0.5,0.5,0.5);
	setColor(vec4(1.0,1.0,1.0,1.0));
	drawSphere();
		gPush();
		{
			setColor(vec4(0.0,0.0,0.0,1.0));
			gTranslate(0,0,0.5);
			gScale(0.75,0.75,0.75);
			drawSphere();
		}
		gPop();
}

//draws the propellor
function drawPropellor(dt){
    //show propellor in zoomed scene
    if (frames >= zoom){
        //move propellor up
        propPosition[1] = propPosition[1] + 0.5*dt;
        gTranslate(0,Math.min(1.3,propPosition[1]),0);
        //propellor stick
        gPush();
        {
            setColor(vec4(0.5,0.5,0.5,1.0));
            gScale(0.2,0.6,0.2)
            gRotate(90,1,0,0);
            drawCylinder();
        }
        gPop();
        //propellor blades
        gPush();
        {
            //spin blades
            propRotation[1] = propRotation[1] + 900*dt;
            gRotate(propRotation[1],0,1,0);
            gTranslate(0,0.3,0);
            gPush();
            {
                setColor(vec4(0.5,0.5,0.5));
                propSize[1] = propSize[1]+0.2*dt;
                gScale(Math.min(0.8,propSize[1]),0.05,0.2);
                drawCube();
            }
            gPop();
            gRotate(90,0,1,0);
            gPush();
            {
                setColor(vec4(0.5,0.5,0.5));
                gScale(Math.min(0.8,propSize[1]),0.05,0.2);
                drawCube();
            }
            gPop();
        }
        gPop();
    }
}

//draws a dog ear
function drawEar(frames,i,dir){
    if (frames >= flying){
        earRotation[i] = earRotation[i] + dir*wave(0.2,300,0,frames);
        gRotate(earRotation[1],1,0,0);
    }
    gTranslate(0,-0.3,dir*1);
    gPush();
    {
        setColor(vec4(0.8,0.5,0.0,1.0));
        gRotate(dir*-50,1,0,0);
        gScale(0.5,1,0.1);
        drawSphere();
    }
    gPop();
}

//draws the dog model
function drawDog(frames,dt){
    gPush();
    {
        //move dog upwards only if flying
        if (frames > flying){
            dogPosition[1] = dogPosition[1] + dogPosition[1]*dt;
            gTranslate(0,dogPosition[1],0);
        }
        //draw body
        gPush();
        {
            setColor(vec4(0.8,0.5,0.0,1.0));
            drawSphere();
        }
        gPop();
        //UPPER BODY
        gPush();
        {
            //neck
            gTranslate(0.4,1,0);
            gPush();
            {
                setColor(vec4(0.8,0.5,0.0,1.0));
                gRotate(90,1,0,0);
                gRotate(-20,0,1,0);
                gScale(0.8,0.8,1.0);
                drawCylinder();
            }
            gPop();
            //HEAD
            gPush();
            {
                gTranslate(0.5,1.2,0);
                //follow ball if ball is bouncing
                if (!ballUp){
                    //calculate x and y from head to ball
                    headDir[0] = bouncingCubePosition[0] - headPosition[0];
                    headDir[1] = bouncingCubePosition[1] - headPosition[1];
                    //get angle using tan
                    headAngle = Math.atan2(headDir[0],headDir[1])

                    gRotate(4*headAngle, 0,0,1);
                }
                //look up if ball is flying
                if (ballUp && frames <= zoom){
                    headRotation[1] = Math.min(headRotation [1] + 50*dt,50);
                    gRotate(headRotation[1]-10, 0,0,1);
                }
                //draw head
                gPush();
                {
                    setColor(vec4(0.8,0.5,0.0,1.0));
                    drawSphere();
                }
                gPop();
                //propellor
                gPush();
                {
                    drawPropellor(dt);
                }
                gPop();
                //eye1
                gPush();
                {
                    gTranslate(0.4,0,0.5);
                    gRotate(50,0,1,0);
                    drawEye();
                }
                gPop();
                //eye2
                gPush();
                {
                    gTranslate(0.4,0,-0.5);
                    gRotate(130,0,1,0);
                    drawEye();
                }
                gPop();
                //ear1
                gPush();
                {
                    gTranslate(-0.3,0.5,0.3);
                    drawEar(frames,1,1);

                }
                gPop();
                //ear2
                gPush();
                    gTranslate(-0.3,0.5,-0.3);
                    drawEar(frames,1,-1);
                gPop();
                //draw snout
                gTranslate(0.8,-0.5,0);
                gPush();
                {
                    setColor(vec4(0.8,0.5,0.0,1.0));
                    gScale(1.0,0.5,0.5);
                    drawSphere();
                }
                gPop();
                //nose
                gTranslate(0.9,0.1,0);
                gPush();
                {
                    setColor(vec4(0.0,0.0,0.0,1.0));
                    gScale(0.15,0.15,0.25);
                    drawSphere();
                }
                gPop();
            }
            gPop();
        }
        gPop();
        //LOWER BODY
        gPush();
        {
            gTranslate(-2.5,0.1,0);
            //body cylinder
            gPush();
            {
                setColor(vec4(0.8,0.5,0.0,1.0));
                gRotate(90,0,1,0);
                gScale(1.6,1.6,4.0);
                drawCylinder();
            }
            gPop();
            gTranslate(-2,0,0);
            //body sphere
            gPush();
            {
                setColor(vec4(0.8,0.5,0.0,1.0));
                gScale(0.8,0.8,0.8);
                drawSphere();
            }
            gPop();
            //tail
            gPush();
            {   
                setColor(vec4(0.8,0.5,0.0,1.0));
                gTranslate(-0.5,0.3,0);
                drawTail(frames);
            }
            gPop();
            //legs
            gPush();
            {
                gTranslate(0,-0.3,0);
                //back legs
                gPush();
                {
                    setColor(vec4(0.8,0.5,0.0,1.0));
                    gTranslate(0,0,0.8);
                    drawLeg(frames,1,1);
                }
                gPop();
                gPush();
                {
                    setColor(vec4(0.8,0.5,0.0,1.0));
                    gTranslate(0,0,-0.8);
                    drawLeg(frames,-1,2);
                }
                gPop();
                //front legs
                gTranslate(4.8,0,0);
                gPush();
                {
                    setColor(vec4(0.8,0.5,0.0,1.0));
                    gTranslate(0,0,1);
                    drawLeg(frames,-1,3);
                }
                gPop();
                gPush();
                {
                    setColor(vec4(0.8,0.5,0.0,1.0));
                    gTranslate(0,0,-1);
                    drawLeg(frames,1,4);
                }
                gPop();
            }
            gPop();
        }
        gPop();
    }
    gPop();
}

//draws a cloud
function drawCloud(){
    setColor(vec4(1.0,1.0,1.0,1.0)); 
    gPush();
    {
        gPush();
        {
            gRotate(90,0,1,0);
            gScale(1,1,1.5);
            drawSphere();
        }
        gPop();
        gPush();
        {
            gTranslate(-2,0,0);
            gRotate(90,0,1,0);
            gScale(1,1,1.5);
            drawSphere();
        }
        gPop();
        gPush();
        {
            gTranslate(-1,1,0);
            gRotate(90,0,1,0);
            gScale(1,1,1.5);
            drawSphere();
        }
        gPop();
        gPush();
        {
            gTranslate(-1,0,1);
            gRotate(90,0,1,0);
            gScale(1,1,1.5);
            drawSphere();
        }
        gPop();
        gPush();
        {
            gTranslate(-1,0,-1.5);
            gScale(0.6,0.6,0.6);
            drawSphere();
        }
        gPop();
    }
    gPop();
}

//draws all landscape elements (ground, clouds, pond)
function drawLandscape(){
    //ground
    gPush();
    {
        setColor(vec4(1.0,1.0,1.0,1.0));
        toggleTextureGrass();
        gPush();
        {
            gTranslate(0,-2,0);
            gScale(80,1,80);
            drawCube();
        
        }
        gPop();
        //hill
        gPush();
        {
            gTranslate(40,-10,-60);
            gScale(20,20,20);
            drawSphere();
        
        }
        gPop();
        //hill
        gPush();
        {
            gTranslate(60,-7.5,-50);
            gScale(15,15,15);
            drawSphere();
        
        }
        gPop();
        //hill
        gPush();
        {
            gTranslate(-70,-20,20);
            gScale(30,30,30);
            drawSphere();
        
        }
        gPop();
        //hill
        gPush();
        {
            gTranslate(-30,-30,80);
            gScale(50,50,50);
            drawSphere();
        
        }
        gPop();
        toggleTextureGrass();
    }
    gPop();
    //clouds
    gPush();
    {
        //move clouds back and forth along the x-axis
        cloudPosition[1] = cloudPosition[1] + wave(0.01,800,0,frames);
        cloudPosition[2] = cloudPosition[2] - wave(0.01,800,0,frames);
        toggleTextureCloud();
        gPush();
        {
            gTranslate(-2+cloudPosition[1],10,-5);
            drawCloud();
        }
        gPop();
        gPush();
        {
            gTranslate(-30+cloudPosition[2],40,0);
            drawCloud();
        }
        gPop();
        gPush();
        {
            gTranslate(6+cloudPosition[1],25,5);
            drawCloud();
        }
        gPop();
        gPush();
        {
            gTranslate(5+cloudPosition[2],10,-30);
            drawCloud();
        }
        gPop();
        gPush();
        {
            gTranslate(50+cloudPosition[1],5,-40);
            drawCloud();
        }
        gPop();
        gPush();
        {
            gTranslate(-30+cloudPosition[2],30,-40);
            drawCloud();
        }
        gPop();
        gPush();
        {
            gTranslate(-35+cloudPosition[1],40,40);
            drawCloud();
        }
        gPop();
        toggleTextureCloud();
    }
    gPop();
    //pond
    gPush();
    {
        //water
        toggleTextureWater();
        gTranslate(20,-1,-30);
        gPush();
        {
            gScale(10,0.05,10);
            drawSphere();
        }
        gPop();
        gTranslate(-10,0,3);
        gPush();
        {
            gScale(5,0.05,5);
            drawSphere();
        }
        gPop();
        toggleTextureWater();
        //rock
        gPush();
        {
            setColor(vec4(0.5,0.5,0.5,1.0));
            gTranslate(1,0,-5);
            gScale(2,1,1);
            drawSphere();
        }
        gPop();
        //rock
        gPush();
        {
            setColor(vec4(0.5,0.5,0.5,1.0));
            gTranslate(4,0,-10);
            gScale(1.2,0.6,0.6);
            drawSphere();
        }
        gPop();
    }
    gPop();
}

//draws the bouncing ball
function drawBall(dt){
    	//Note simplified velocity and acceleration ehre are just scalars, normally they are vectors in 3D
		bouncyBallVelocity += gravity*dt; // Update velocity using acceleration
		bouncingCubePosition[1] += bouncyBallVelocity*dt; // Update position using velocity
		// Check if ball hits an imaginary plane at y = 0, and also if the velocity is INTO the plane, and if it is moving at all
		if (bouncingCubePosition[1] < 0 && bouncyBallVelocity < 0)
		{
			bouncyBallVelocity = -bouncyBallVelocity; // If so, reflect the velocity back but lose some energy.
			bouncingCubePosition[1] = 0; // Ball has most likely penetrated surface because we take discrete time steps, move back to cylinder surface
            bounces++;//increment number of times ball has hit the ground
		}
        setColor(vec4(1.0, 0.0, 0.0, 1.0));
		gTranslate(8+bouncingCubePosition[0],bouncingCubePosition[1],bouncingCubePosition[2]); // Move the ball to its update position
        gScale(0.5,0.5,0.5);
		drawSphere();
        //ball shoots up after hitting the plane 4 times
        if (bounces == 4){
            ballUp = true;
            gravity = 9.8;
        }
}

function render(timestamp) {
    
    gl.clear( gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
    
    eye = vec3(3,8,20);
    MS = []; // Initialize modeling matrix stack
	
	// initialize the modeling matrix to identity
    modelMatrix = mat4();
    
    // set the camera matrix
    viewMatrix = lookAt(eye, at, up);
   
    // set the projection matrix
    projectionMatrix = perspective(fovy, 1, near, far);
    
    gl.uniform1f( gl.getUniformLocation(program, 
        "time"),timestamp);
    
    // set all the matrices
    setAllMatrices();
    
	if( animFlag )
    {
		// dt is the change in time or delta time from the last timestamp to this one
		// in animation typically we have some property or degree of freedom we want to evolve over time
		// For example imagine x is the position of a thing.
		// To get the new position of a thing we do something called integration
		// the simpelst form of this looks like:
		// x_new = x + v*dt
		// That is the new position equals the current position + the rate of of change of that position (often a velocity or speed), times the change in time
		// We can do this with angles or positions, the whole x,y,z position or just one dimension. It is up to us!
		dt = (timestamp - prevTime) / 1000.0;
		prevTime = timestamp;
	}
	
	// We need to bind our textures, ensure the right one is active before we draw
	//Activate a specified "texture unit".
    //Texture units are of form gl.TEXTUREi | where i is an integer.
	gl.activeTexture(gl.TEXTURE0);
	gl.bindTexture(gl.TEXTURE_2D, textureArray[0].textureWebGL);
	gl.uniform1i(gl.getUniformLocation(program, "texture1"), 0);
	
	gl.activeTexture(gl.TEXTURE1);
	gl.bindTexture(gl.TEXTURE_2D, textureArray[1].textureWebGL);
	gl.uniform1i(gl.getUniformLocation(program, "texture2"), 1);

    gl.activeTexture(gl.TEXTURE2);
	gl.bindTexture(gl.TEXTURE_2D, textureArray[2].textureWebGL);
	gl.uniform1i(gl.getUniformLocation(program, "texture3"), 2);
	
	// Now let's draw a shape animated!
	// You may be wondering where the texture coordinates are!
	// We've modified the object.js to add in support for this attribute array!

    //set camera fly
    camController(eye,at,up,frames);

    //grayScale shader effect
    initGrayScale();
    
    if (frames > gray){
        grayScale = true;
        gl.clearColor( 0.73, 0.73, 0.73, 1.0 );
    }
    if (frames >= zoom){
        gl.clearColor( 0.6, 0.8, 0.8, 1.0 );
        grayScale = false;
    }

    //draw static background elements
    drawLandscape();
    
    //draw ball
	gPush();
	{	
        drawBall(dt);
	}
	gPop();

    //draw dog
    gPush();
    {
        gTranslate(1.5,1.4,0);
        drawDog(frames,dt);
    }
    gPop();

    if( animFlag )
        frames+=10;
        //show FPS every 2 seconds
        if ((frames/1000)%2 == 1){
            showFPS(dt);
        }
        window.requestAnimationFrame(render);
}
