THREE.Object3D.prototype.rotateAroundWorldAxis = function() {
    let q = new THREE.Quaternion();
    return function rotateAroundWorldAxis( point, axis, angle ) {
        q.setFromAxisAngle( axis, angle );

        this.applyQuaternion( q );

        this.position.sub( point );
        this.position.applyQuaternion( q );
        this.position.add( point );

        return this;
    }
}(); // patch for rotation around a point in space

function createCube() {
    for (let i = -1; i < 2; i++) {
        for (let j = -1; j < 2; j++) {
            for (let k = -1; k < 2; k++) {
                let geometry = new THREE.CubeGeometry(0.97, 0.97, 0.97);
                let material = new THREE.MeshBasicMaterial({color:0xffffff, vertexColors: true});
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
                let cubbie = new THREE.Mesh(geometry, material);
                cubbie.position.set(i, j, k);
                cube.add(cubbie);
            }
        }
    }
    scene.add(cube);
}

let moves_per_sec = 5;
let fps = 100;
let frame_time = 1/fps;
async function rotate(center, sides, point, axis, degree) {
    let frames_per_move = fps/moves_per_sec;
    let increment = degree/frames_per_move;
    let total_rot = 0;
    while (Math.abs(total_rot) < Math.abs(degree)) {
        cube.children[center].rotateAroundWorldAxis(point, axis, increment);
        for (let j = 0; j < sides.length; j++) {
            cube.children[sides[j]].rotateAroundWorldAxis(point, axis, increment);
        }
        total_rot += increment;
        await (new Promise(resolve => setTimeout(resolve, frame_time)));
    }

    cube.children[center].rotateAroundWorldAxis(point, axis, degree-total_rot);
    for (let j = 0; j < sides.length; j++) {
        cube.children[sides[j]].rotateAroundWorldAxis(point, axis, degree-total_rot);
    } // fix over rotation

    // console.log("done");
    
    let length = sides.length;

    //console.log(cube.children);
    let tmp = cube.children[sides[length-1]];
    for (let i = length-1; i >= 2; i-=2) {
        //console.log(sides[i], cube.children[sides[i]])
        //console.log(sides[i-2], cube.children[sides[i-2]])
        cube.children[sides[i]] = cube.children[sides[i-2]];
    }
    cube.children[sides[1]] = tmp;

    tmp = cube.children[sides[length-2]];
    for (let i = length-2; i >= 2; i-=2) {
        cube.children[sides[i]] = cube.children[sides[i-2]];
    }
    cube.children[sides[0]] = tmp;
    //console.log(cube.children);
}

async function U() {
    let point = new THREE.Vector3(0, 0, 0);
    let axis = new THREE.Vector3(0, 1, 0);
    let degree = -Math.PI/2;
    center = 16;
    sides = [6, 15, 24, 25, 26, 17, 8, 7];
    await rotate(center, sides, point, axis, degree);
}

async function D() {
    let point = new THREE.Vector3(0, 0, 0);
    let axis = new THREE.Vector3(0, 1, 0);
    let degree = Math.PI/2;
    center = 10;
    sides = [0, 1, 2, 11, 20, 19, 18, 9];
    await rotate(center, sides, point, axis, degree);
}

async function L() {
    let point = new THREE.Vector3(0, 0, 0);
    let axis = new THREE.Vector3(1, 0, 0);
    let degree = Math.PI/2;
    center = 4;
    sides = [0, 3, 6, 7, 8, 5, 2, 1];
    await rotate(center, sides, point, axis, degree);
}

async function R() {
    let point = new THREE.Vector3(0, 0, 0);
    let axis = new THREE.Vector3(1, 0, 0);
    let degree = -Math.PI/2;
    center = 22;
    sides = [18, 19, 20, 23, 26, 25, 24, 21];
    await rotate(center, sides, point, axis, degree);
}

async function F() {
    let point = new THREE.Vector3(0, 0, 0);
    let axis = new THREE.Vector3(0, 0, 1);
    let degree = -Math.PI/2;
    center = 14;
    sides = [2, 5, 8, 17, 26, 23, 20, 11];
    await rotate(center, sides, point, axis, degree);
}

async function B() {
    let point = new THREE.Vector3(0, 0, 0);
    let axis = new THREE.Vector3(0, 0, 1);
    let degree = Math.PI/2;
    center = 12;
    sides = [0, 9, 18, 21, 24, 15, 6, 3];
    await rotate(center, sides, point, axis, degree);
}

function changeText(str) {
    let moveDisplay = document.querySelector("nav>p");
    moveDisplay.innerHTML = str;
}

async function move_by_num(move_num, logging=true) {
    switch(move_num) {
        case 0: await U(); break;
        case 1: await U(); await U(); break;
        case 2: await U(); await U(); await U(); break;
        case 3: await L(); break;
        case 4: await L(); await L(); break;
        case 5: await L(); await L(); await L(); break;
        case 6: await F(); break;
        case 7: await F(); await F(); break;
        case 8: await F(); await F(); await F(); break;
        case 9: await R(); break;
        case 10: await R(); await R(); break;
        case 11: await R(); await R(); await R(); break;
        case 12: await B(); break;
        case 13: await B(); await B(); break;
        case 14: await B(); await B(); await B(); break;
        case 15: await D(); break;
        case 16: await D(); await D(); break;
        case 17: await D(); await D(); await D(); break;
    }
    if (!logging) return; // stop right there if no logging required
    
    if (move_str.length == 0) move_str = move_num.toString();
    else move_str += "_"+move_num.toString();
    changeText("moves: " + move_str);
}

still_rotating = false
async function onKeyDown(event) {
    if (still_rotating) return;
    still_rotating = true;
    if (event.keyCode == 85) { // up
        await move_by_num(0);
        console.log("U");
    } else if (event.keyCode == 68) { // down
        await move_by_num(15);
        console.log("D");
    } else if (event.keyCode == 76) { // left
        await move_by_num(3);
        console.log("L");
    } else if (event.keyCode == 82) { // right
        await move_by_num(9);
        console.log("R");
    } else if (event.keyCode == 70) { // front
        await move_by_num(6);
        console.log("F");
    } else if (event.keyCode == 66) { // back
        await move_by_num(12);
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
    still_rotating = false;
}

function onMouseMove(event) {
    if (!downFlag) return; // nothing to do
    if (event.target.id === "myRange") return;
    let cur_x = event.offsetX;
    let cur_y = event.offsetY; // get new coordinates
    let dx = cur_x-last_x;
    let dy = cur_y-last_y; // calculate change
    last_x = cur_x;
    last_y = cur_y; // reset last coordinates

    cube.rotation.y += dx/200;
    cube.rotation.x += dy/200;
}

function windowResize() {
    renderer.setSize(window.innerWidth, (window.innerHeight-2*navHeight));
    camera.aspect = window.innerWidth / (window.innerHeight-2*navHeight);
    camera.updateProjectionMatrix();
}

let still_solving = false;
let still_shuffling = false;
async function shuffleRequest() {
    if (still_shuffling || still_solving) return;
    still_shuffling = true;
    for (let i = 0; i < 20; i++) {
        let move_num = Math.floor(Math.random()*18);
        await move_by_num(move_num);
    }
    still_shuffling = false;
}

function solveRequest() {
    if (still_solving || still_shuffling) return;
    still_solving = true
    url = "http://localhost:8080/solve" + move_str;
    console.log(url);
    fetch(url)
    .then(response => response.text())
    .then(move_solution)
    .then(() => still_solving = false);
    //.catch(console.log("something went wrong"))
    move_str = "";
}

async function move_solution(solution) {
    changeText("solution: " + solution);
    let move_list = solution.split(",");
    // console.log(move_list);
    for (let i = 0; i < move_list.length; i++) {
        await move_by_num(parseInt(move_list[i]), false)
    }
}

function animate() {
    requestAnimationFrame(animate);
	renderer.render(scene, camera);
}

let scene = new THREE.Scene();
let nav = document.getElementById("navbar");
let navHeight = nav.offsetHeight;
let camera = new THREE.PerspectiveCamera( 70, window.innerWidth / (window.innerHeight-2*navHeight), 1, 1000 );
camera.position.z = 5;

let renderer = new THREE.WebGLRenderer({antialias: true, alpha: true});
renderer.setSize( window.innerWidth, (window.innerHeight-2*navHeight) );
document.body.appendChild( renderer.domElement );

let move_str = ""
document.getElementById("shuffleBtn").addEventListener("click", shuffleRequest);
document.getElementById("solveBtn").addEventListener("click", solveRequest);

document.getElementById("myRange").value = moves_per_sec;
document.getElementById("mps").innerHTML = moves_per_sec;
document.getElementById("myRange").addEventListener("input", (e) => {
    moves_per_sec = e.target.value;
    document.getElementById("mps").innerHTML = moves_per_sec;
});

let downFlag = false;
let last_x, last_y;
document.addEventListener("mousedown", event => {
    downFlag = true;
    last_x = event.offsetX;
    last_y = event.offsetY; // log last x, y position
});
document.addEventListener("mouseup", _ => downFlag = false);
document.addEventListener("mousemove", onMouseMove);
document.addEventListener("keydown", onKeyDown);
document.addEventListener("wheel", event => {
    camera.position.z += event.deltaY/500;
    if (camera.position.z <= 4) camera.position.z = 4;
    else if (camera.position.z >= 10) camera.position.z = 10;
})
window.addEventListener('resize', windowResize);

let cube = new THREE.Group(); // make a container for cube
createCube(); // add all pieces to the cube
animate();