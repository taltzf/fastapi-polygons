const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const finishBtn = document.getElementById('finishPolygon');
const listDiv = document.getElementById('list');

let currentPolygon = [];
let polygons = [];

// Load background image
const bg = new Image();
bg.src = 'https://picsum.photos/1920/1080';
bg.onload = () => draw();

// Fetch existing polygons
async function loadPolygons() {
    const res = await fetch('/api/polygons/');
    polygons = await res.json();
    draw();
    updateList();
}

function draw() {
    // Draw background
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(bg, 0, 0, canvas.width, canvas.height);

    // Draw existing polygons
    polygons.forEach(p => {
        ctx.beginPath();
        p.points.forEach((pt, i) => {
            const [x, y] = [pt[0]*canvas.width/1920, pt[1]*canvas.height/1080];
            if(i===0) ctx.moveTo(x, y);
            else ctx.lineTo(x, y);
        });
        ctx.closePath();
        ctx.strokeStyle = 'red';
        ctx.lineWidth = 2;
        ctx.stroke();
    });

    // Draw current polygon
    if(currentPolygon.length>0){
        ctx.beginPath();
        currentPolygon.forEach((pt, i) => {
            const [x, y] = pt;
            if(i===0) ctx.moveTo(x, y);
            else ctx.lineTo(x, y);
        });
        ctx.strokeStyle = 'blue';
        ctx.lineWidth = 2;
        ctx.stroke();
    }
}

// Handle canvas clicks
canvas.addEventListener('click', e => {
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    currentPolygon.push([x, y]);
    draw();
});

// Finish polygon
finishBtn.addEventListener('click', async () => {
    if(currentPolygon.length < 3) {
        alert('Polygon must have at least 3 points');
        return;
    }
    // Convert to original 1920x1080 scale
    const scaled = currentPolygon.map(pt => [pt[0]*1920/canvas.width, pt[1]*1080/canvas.height]);
    const name = prompt("Polygon name:");
    if(!name) return;
    await fetch('/api/polygon/', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({name, points: scaled})
    });
    currentPolygon = [];
    loadPolygons();
});

// Update polygon list
function updateList() {
    listDiv.innerHTML = '';
    polygons.forEach(p => {
        const div = document.createElement('div');
        div.className = 'polygon-item';
        div.innerHTML = `${p.name} <button onclick="deletePolygon(${p.id})">Delete</button>`;
        listDiv.appendChild(div);
    });
}

// Delete polygon
async function deletePolygon(id) {
    await fetch(`/api/polygon/${id}`, {method: 'DELETE'});
    loadPolygons();
}

// Load polygons initially
loadPolygons();
