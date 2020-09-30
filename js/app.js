THREE.Object3D.prototype.rotateAroundWorldAxis = function() {

    // rotate object around axis in world space (the axis passes through point)
    // axis is assumed to be normalized
    // assumes object does not have a rotated parent

    var q = new THREE.Quaternion();

    return function rotateAroundWorldAxis( point, axis, angle ) {

        q.setFromAxisAngle( axis, angle );

        this.applyQuaternion( q );

        this.position.sub( point );
        this.position.applyQuaternion( q );
        this.position.add( point );

        return this;

    }

}(); // patch

var scene = new THREE.Scene();
var camera = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 0.1, 1000 );
camera.position.z = 5;

var renderer = new THREE.WebGLRenderer({antialias: true});
renderer.setSize( window.innerWidth, window.innerHeight );
document.body.appendChild( renderer.domElement );

var cube = new THREE.Group();
function createCube() {
    for (var i = -1; i < 2; i++) {
        for (var j = -1; j < 2; j++) {
            for (var k = -1; k < 2; k++) {
                var geometry = new THREE.CubeGeometry(0.95, 0.95, 0.95);
                var material = new THREE.MeshBasicMaterial({color:0xffffff, vertexColors: true});
                geometry.faces[0].color.setHex(0x33FF57);
                geometry.faces[1].color.setHex(0x33FF57);
                geometry.faces[2].color.setHex(0x336DFF);
                geometry.faces[3].color.setHex(0x336DFF);
                geometry.faces[4].color.setHex(0xFF3361);
                geometry.faces[5].color.setHex(0xFF3361);
                geometry.faces[6].color.setHex(0xFF7D33);
                geometry.faces[7].color.setHex(0xFF7D33);
                geometry.faces[8].color.setHex(0xFFFFFF);
                geometry.faces[9].color.setHex(0xFFFFFF);
                geometry.faces[10].color.setHex(0xF9FF33);
                geometry.faces[11].color.setHex(0xF9FF33);
                var cubbie = new THREE.Mesh(geometry, material);
                cubbie.position.set(i, j, k);
                cube.add(cubbie);
            }
        }
    }
    scene.add(cube);
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function rotate(indices, point, axis, degree) {
    for (var i = 0; i < indices.length; i++) {
        cube.children[indices[i]].rotateAroundWorldAxis(point, axis, degree);
    }
    var length = indices.length;

    console.log(cube.children);
    var tmp = cube.children[indices[length-1]];
    for (var i = length-1; i >= 2; i-=2) {
        console.log(indices[i], cube.children[indices[i]])
        console.log(indices[i-2], cube.children[indices[i-2]])
        cube.children[indices[i]] = cube.children[indices[i-2]];
    }
    cube.children[indices[1]] = tmp;

    tmp = cube.children[indices[length-2]];
    for (var i = length-2; i >= 2; i-=2) {
        cube.children[indices[i]] = cube.children[indices[i-2]];
    }
    cube.children[indices[0]] = tmp;
    console.log(cube.children);
}

function U() {
    var point = new THREE.Vector3(0, 0, 0);
    var axis = new THREE.Vector3(0, 1, 0);
    var degree = -Math.PI/2;
    indices = [6, 15, 24, 25, 26, 17, 8, 7];
    rotate(indices, point, axis, degree);
}

function D() {
    var point = new THREE.Vector3(0, 0, 0);
    var axis = new THREE.Vector3(0, 1, 0);
    var degree = Math.PI/2;
    indices = [0, 1, 2, 11, 20, 19, 18, 9];
    rotate(indices, point, axis, degree);
}

function L() {
    var point = new THREE.Vector3(0, 0, 0);
    var axis = new THREE.Vector3(1, 0, 0);
    var degree = Math.PI/2;
    indices = [0, 3, 6, 7, 8, 5, 2, 1];
    rotate(indices, point, axis, degree);
}

function R() {
    var point = new THREE.Vector3(0, 0, 0);
    var axis = new THREE.Vector3(1, 0, 0);
    var degree = -Math.PI/2;
    indices = [18, 19, 20, 23, 26, 25, 24, 21];
    rotate(indices, point, axis, degree);
}

function F() {
    var point = new THREE.Vector3(0, 0, 0);
    var axis = new THREE.Vector3(0, 0, 1);
    var degree = -Math.PI/2;
    indices = [2, 5, 8, 17, 26, 23, 20, 11];
    rotate(indices, point, axis, degree);
}

function B() {
    var point = new THREE.Vector3(0, 0, 0);
    var axis = new THREE.Vector3(0, 0, 1);
    var degree = Math.PI/2;
    indices = [0, 9, 18, 21, 24, 15, 6, 3];
    rotate(indices, point, axis, degree);
}

async function onKeyDown(event) {
    if (event.keyCode == 85) { // up
        U();
        console.log("U");
    } else if (event.keyCode == 68) { // down
        D();
        console.log("D");
    } else if (event.keyCode == 76) { // left
        L();
        console.log("L");
    } else if (event.keyCode == 82) { // right
        R();
        console.log("R");
    } else if (event.keyCode == 70) { // front
        F();
        console.log("F");
    } else if (event.keyCode == 66) { // back
        B();
        console.log("B");
    } else if (event.keyCode == 37) { // y-- 
        cube.rotation.y -= 0.1;
    } else if (event.keyCode == 39) { // y++ 
        cube.rotation.y += 0.1;
    } else if (event.keyCode == 38) { // x-- 
        cube.rotation.x -= 0.1;
    } else if (event.keyCode == 40) { // x++ 
        cube.rotation.x += 0.1;
    }
}

function animate() {
    requestAnimationFrame(animate);
	renderer.render(scene, camera);
}

createCube();
animate();

document.addEventListener("keydown", onKeyDown);