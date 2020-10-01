THREE.Object3D.prototype.rotateAroundWorldAxis = function() {
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
var nav = document.getElementById("navbar");
var navHeight = nav.scrollHeight*1.5;
var camera = new THREE.PerspectiveCamera( 75, window.innerWidth / (window.innerHeight-navHeight), 0.1, 1000 );
camera.position.z = 5;

var renderer = new THREE.WebGLRenderer({antialias: true, alpha: true});
renderer.setSize( window.innerWidth, (window.innerHeight-navHeight) );
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
                geometry.faces[8].color.setHex(0xEEEEEE);
                geometry.faces[9].color.setHex(0xEEEEEE);
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

    //console.log(cube.children);
    var tmp = cube.children[indices[length-1]];
    for (var i = length-1; i >= 2; i-=2) {
        //console.log(indices[i], cube.children[indices[i]])
        //console.log(indices[i-2], cube.children[indices[i-2]])
        cube.children[indices[i]] = cube.children[indices[i-2]];
    }
    cube.children[indices[1]] = tmp;

    tmp = cube.children[indices[length-2]];
    for (var i = length-2; i >= 2; i-=2) {
        cube.children[indices[i]] = cube.children[indices[i-2]];
    }
    cube.children[indices[0]] = tmp;
    //console.log(cube.children);
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

function move_by_num(move_num) {
    switch(move_num) {
        case 0: U(); break;
        case 1: U(); U(); break;
        case 2: U(); U(); U(); break;
        case 3: L(); break;
        case 4: L(); L(); break;
        case 5: L(); L(); L(); break;
        case 6: F(); break;
        case 7: F(); F(); break;
        case 8: F(); F(); F(); break;
        case 9: R(); break;
        case 10: R(); R(); break;
        case 11: R(); R(); R(); break;
        case 12: B(); break;
        case 13: B(); B(); break;
        case 14: B(); B(); B(); break;
        case 15: D(); break;
        case 16: D(); D(); break;
        case 17: D(); D(); D(); break;
    }
    if (move_str.length == 0) move_str += move_num.toString();
    else move_str += "_"+move_num.toString();
}

async function onKeyDown(event) {
    if (event.keyCode == 85) { // up
        move_by_num(0);
        console.log("U");
    } else if (event.keyCode == 68) { // down
        move_by_num(15);
        console.log("D");
    } else if (event.keyCode == 76) { // left
        move_by_num(3);
        console.log("L");
    } else if (event.keyCode == 82) { // right
        move_by_num(9);
        console.log("R");
    } else if (event.keyCode == 70) { // front
        move_by_num(6);
        console.log("F");
    } else if (event.keyCode == 66) { // back
        move_by_num(12);
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
window.addEventListener('resize', function() {
   renderer.setSize(window.innerWidth, (window.innerHeight-navHeight));
   camera.aspect = window.innerWidth / (window.innerHeight-navHeight);
   camera.updateProjectionMatrix();
});

move_str = ""
function shuffleRequest() {
    move_str = ""
    for (var i = 0; i < 20; i++) {
        var move_num = Math.floor(Math.random()*18);
        move_by_num(move_num);
    }
}

function move_solution(solution) {
    var move_list = solution.split(",");
    console.log(move_list);
    move_list.forEach(move => move_by_num(parseInt(move)));
}

function solveRequest() {
    url = "http://localhost:8000/solve" + move_str;
    console.log(url);
    fetch(url)
    .then(response => response.text())
    .then(move_solution)
    //.catch(console.log("something went wrong"))
    move_str = "";
}

var shuffleBtn = document.getElementById("shuffleBtn");
shuffleBtn.addEventListener("click", shuffleRequest);
var solveBtn = document.getElementById("solveBtn");
solveBtn.addEventListener("click", solveRequest);