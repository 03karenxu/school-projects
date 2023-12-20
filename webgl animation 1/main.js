var canvas;
var gl;

var program;

var near = 1;
var far = 100;


var left = -9.0;
var right = 15.0;
var ytop = 20.0;
var bottom = -4.0;


var lightPosition2 = vec4(100.0, 100.0, 100.0, 1.0 );
var lightPosition = vec4(0.0, 0.0, 100.0, 1.0 );

var lightAmbient = vec4(0.2, 0.2, 0.2, 1.0 );
var lightDiffuse = vec4( 1.0, 1.0, 1.0, 1.0 );
var lightSpecular = vec4( 1.0, 1.0, 1.0, 1.0 );

var materialAmbient = vec4( 1.0, 0.0, 1.0, 1.0 );
var materialDiffuse = vec4( 1.0, 0.8, 0.0, 1.0 );
var materialSpecular = vec4( 0.4, 0.4, 0.4, 1.0 );
var materialShininess = 30.0;

var ambientColor, diffuseColor, specularColor;

var modelMatrix, viewMatrix, modelViewMatrix, projectionMatrix, normalMatrix;
var modelViewMatrixLoc, projectionMatrixLoc, normalMatrixLoc;
var eye;
var at = vec3(0.0, 0.0, 0.0);
var up = vec3(0.0, 1.0, 0.0);

var RX = 0;
var RY = 0;
var RZ = 0;

var MS = []; // The modeling matrix stack
var TIME = 0.0; // Realtime
var dt = 0.0
var prevTime = 0.0;
var resetTimerFlag = true;
var animFlag = false;
var controller;

// These are used to store the current state of objects.
// In animation it is often useful to think of an object as having some DOF
// Then the animation is simply evolving those DOF over time.

//ground
var groundPosition = [0.0,-11.0,0.0];
//person
var thighRotation = [0,0,0];
var calfRotation = [0,0,0];
var bodyPosition = [8,8,0];

//fish
var fishRotation = [0,0,0];
var tailRotation = [0,0,0];
var fishPosition = [4,4,0];

//seaweed
var swRotation = [0,0,0,0,0,0,0,0,0,0,0];
var swPosition = [0.0,0.6,0.0];
var strandPosition = [0.0,0.0,0.0];//median position of all 3 strands

//bubbles
var bubblePosition = [8,10.5,1];
var bubbles = [];
var lastBubTime = 0;
var timeElapsed = 0;
var numBubbles = 0;
var spacing = 0;


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
                                         "lightPosition"),flatten(lightPosition) );
    gl.uniform1f( gl.getUniformLocation(program, 
                                        "shininess"),materialShininess );
}

window.onload = function init() {

    canvas = document.getElementById( "gl-canvas" );
    
    gl = WebGLUtils.setupWebGL( canvas );
    if ( !gl ) { alert( "WebGL isn't available" ); }

    gl.viewport( 0, 0, canvas.width, canvas.height );
    gl.clearColor( 0.5, 0.5, 1.0, 1.0 );
    
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

    render(0);
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

//wave function
function wave(amp,freq,phase,timestamp) {
	return amp*Math.cos(timestamp/freq+phase);
}

//draws a fish eye
function drawEye() {
	setMV();
	gScale(0.3,0.3,0.3);
	setColor(vec4(1.0,1.0,1.0,1.0));
	drawSphere();
		gPush();
		{
			setColor(vec4(0.0,0.0,0.0,1.0));
			gTranslate(0,0,0.5);
			gScale(0.7,0.7,0.7);
			drawSphere();
		}
		gPop();

}

//draws a seaweed strand
function drawSeaweed(timestamp){
	setColor(vec4(0.0,0.5,0.3,1.0));
	gTranslate(swPosition[0],swPosition[1], swPosition[2]);
	//draw first segment (stationary)
		gPush();
		{
			gScale(0.25,0.6,0.25);
			drawSphere();
		}
		gPop();
	//draw other segments
	for (let i = 1; i < 10; i++) {
		gTranslate(swPosition[0],swPosition[1], swPosition[2]);
		swRotation[i] = swRotation[i] + wave(0.05,800,i+1500,timestamp);
		gRotate(swRotation[i],0,0,1);
		gTranslate(swPosition[0],swPosition[1], swPosition[2]);
		gPush();
		{
			gScale(0.25,0.6,0.25);
			drawSphere();
		}
		gPop();
	}
}

function generateBubbles(bodyX) {
	numBubbles = Math.floor(Math.random()*5 + 1);

	if (bodyX >= 8) {
		spacing = -0.1;
	} else {
		spacing = 0.1;
	}
	for (i=0; i<numBubbles; i++){
		setTimeout(function (i) {
				return function () {
				var bx = bodyX + i*spacing;
				var by = 0;
				var bz = 0;
				bubbles.push({bx,by,bz});
			};
		}(i), i*200);
	}
}


function render(timestamp) {

	animFlag=true;

    gl.clear( gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
    
    eye = vec3(0,0,10);
    MS = []; // Initialize modeling matrix stack
	
	// initialize the modeling matrix to identity
    modelMatrix = mat4();
    
    // set the camera matrix
    viewMatrix = lookAt(eye, at , up);
   
    // set the projection matrix
    projectionMatrix = ortho(left, right, bottom, ytop, near, far);
    
    
    // set all the matrices
    setAllMatrices();
    
	if( animFlag )
    {
		// dt is the change in time or delta time from the last frame to this one
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

	//ground
	gPush();
		gTranslate(groundPosition[0],groundPosition[1],groundPosition[2]);
		//draw ground
		gPush();
		{
			setColor(vec4(0.0,1.0,0.0,1.0));
			gScale(20,10,10);
			drawCube();
		}
		gPop();
	gPop();

	// big rock
	gPush();
		gPush();
		{
			setColor(vec4(0.5,0.5,0.5,1.0));
			drawSphere();
		}
		gPop();
	gPop();

	//seaweed
	gPush();
		//strand 1
		gPush();
			gTranslate(strandPosition[0],strandPosition[1]+1,strandPosition[2]);
			gPush();
			{
				drawSeaweed(timestamp);
			}
			gPop();
		gPop();
		//strand 2
		gPush();
			gTranslate(strandPosition[0]-1,strandPosition[1],strandPosition[2]);
			gPush();
			{
				drawSeaweed(timestamp);
			}
			gPop();
		gPop();
		//strand 3
		gPush();
			gTranslate(strandPosition[0]+1,strandPosition[1],strandPosition[2]);
			gPush();
			{
				drawSeaweed(timestamp);
			}
			gPop();
		gPop();
	gPop();
	
	//fish
	gPush();
		//rotate fish around seaweed
		fishRotation[1] = fishRotation[1] + 60*dt;
		gRotate(-fishRotation[1],0,1,0);
		//translate fish up and down as it rotates
		fishPosition[1] = fishPosition[1] + wave(0.02,600,0,timestamp);
		gTranslate(fishPosition[0],fishPosition[1],fishPosition[2]);
			//draw head
			gPush();
			{
				setColor(vec4(1.0,0.0,0.0,1.0));
				drawCone();
			}
			gPop();
			//draw eyes
			gPush();
			gTranslate(-0.6,0.1,-0.1);
				gPush();
				{
					drawEye();
				}
				gPop();
				gTranslate(1.2,0,0);
				gPush();
				{
					drawEye();
				}
				gPop();
			gPop();
			//draw body
			gPush();
			gTranslate(0,0,-1.5);
				gPush();
				{
					setColor(vec4(1.0,0.0,0.0,1.0));
					gRotate(180, 0,1,0);
					gScale(1,1,2);
					drawCone();
				}
				gPop();
			gPop();
			//draw fins
			gPush();
			gTranslate(0,0,-2); //point of rotation
			tailRotation[1] = tailRotation[1] + wave(3,100,0,timestamp);
			gRotate(tailRotation[1],0,1,0);
			gTranslate(0,0.25,-0.9);
				gPush();
				{	
					setColor(vec4(1.0,0.0,0.0,1.0));
					gRotate(230,1,0,0);
					gScale(0.1,0.3,1);
					drawCone();
				}
				gPop();
			gTranslate(0,-0.5,0);
				gPush();
				{	
					setColor(vec4(1.0,0.0,0.0,1.0));
					gRotate(-230,1,0,0);
					gScale(0.1,0.3,1);
					drawCone();
				}
				gPop();
			gPop();
	gPop();

	//person
	gPush();
		setColor(vec4(1.5,0.7,1.0,1.0));
		bodyPosition[0] = bodyPosition[0] + wave(0.01,800,0,timestamp);
		bodyPosition[1] = bodyPosition[1] + wave(0.015,500,0,timestamp);
		gTranslate(bodyPosition[0],bodyPosition[1],bodyPosition[2]);
		gRotate(-30.0,0,1,0);
		//draw body
		gPush();
		{
			gScale(1.5,2.0,0.5);
			drawCube();
		}
		gPop();
		//draw head
		gTranslate(0.0,2.8,0.0);
		gPush();
		{
			gScale(0.8,0.8,0.8);
			drawSphere();
		}
		gPop();
		//right leg
		gPush();
		gTranslate(-1.0,-4.8,0.4);//translate to joint
		thighRotation[1] = thighRotation[1] + wave(0.2,800,0,timestamp);
		gRotate(30+thighRotation[1], 1.0,0.0,0.0);//rotate on joint
		gTranslate(0,-1,-0.4);//translate to joint
			//draw thigh
			gPush();
			{
				gScale(0.3,1.0,0.3);
				drawCube();
			}
			gPop();
		gTranslate(0.0,-1.0,0.5);//translate to joint
		calfRotation[1] = calfRotation[1] + wave(0.3,800,0,timestamp);
		gRotate(25+calfRotation[1],1,0,0);//rotate on joint
		gTranslate(0.0,-1.0,-0.5);//translate to joint
			//draw calf
			gPush();
			{
				gScale(0.3,1.0,0.3);
				drawCube();
			}
			gPop();
		gTranslate(0.0,-1.0,0.4);
			//draw foot
			gPush();
			{
				gScale(0.5,0.1,0.8);
				drawCube();
			}
			gPop();
		gPop();
		//left leg
		gPush();
		gTranslate(1.0,-4.8,0.4);//translate to joint
		thighRotation[2] = thighRotation[2] - wave(0.2,800,0,timestamp);
		gRotate(30+thighRotation[2], 1.0,0.0,0.0);//rotate on joint
		gTranslate(0.0,-1.0,-0.4);//translate to joint
			//draw thigh
			gPush();
			{
				gScale(0.3,1.0,0.3);
				drawCube();
			}
			gPop();
		gTranslate(0.0,-1.0,0.5);//translate to joint
		calfRotation[2] = calfRotation[2] - wave(0.3,800,0,timestamp);
		gRotate(25+calfRotation[2],1,0,0);//rotate on joint
		gTranslate(0.0,-1.0,-0.5);//translate to joint
			//draw calf
			gPush();
			{
				gScale(0.3,1.0,0.3);
				drawCube();
			}
			gPop();
		gTranslate(0.0,-1.0,0.4);
			//draw foot
			gPush();
			{
				gScale(0.5,0.1,0.8);
				drawCube();
			}
			gPop();
		gPop();
	gPop();
			
	// bubbles
	gPush();
		setColor(vec4(1.0,1.0,1.0,1.0));
		bubblePosition[0] = bubblePosition[0] + wave(0.01,800,0,timestamp);
		gTranslate(0, bubblePosition[1], bubblePosition[2]);

		//bubble Timer, generate a group of bubbles every 2 seconds
		timeElapsed = timestamp - lastBubTime;

		if (timeElapsed >= 2*1000) {
			generateBubbles(bodyPosition[0]);
			lastBubTime = timestamp;
		}

		//draw bubbles
		for (let i = 0; i<bubbles.length;i++) {
			var bubble = bubbles[i];
			bubble.by = bubble.by + 2*dt;

			gPush();
			{
				gTranslate(bubble.bx,bubble.by,bubble.bz);
				gScale(0.2,0.2,0.2);
				drawSphere();
			}
			gPop();

			if (bubble.by > 10.0) {
				bubbles.splice(i,1);
				i--;
			}
		}	

	gPop();

	// small rock
	gPush();
		setColor(vec4(0.5,0.5,0.5,1.0));
		gTranslate(-2.0,-0.3,0.0);
		//draw rock
		gPush();
		{
			gScale(0.7, 0.7, 0.7);
			drawSphere();	
		}
		gPop();
	gPop();

    if( animFlag )
    window.requestAnimFrame(render);
}
