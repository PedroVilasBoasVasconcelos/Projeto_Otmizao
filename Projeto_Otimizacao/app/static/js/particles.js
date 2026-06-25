const canvas = document.createElement("canvas");
canvas.id = "bg-canvas";
document.body.appendChild(canvas);

const ctx = canvas.getContext("2d");
let particlesArray = [];
const numberOfParticles = 60;

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

const mouse = {
  x: null,
  y: null,
  radius: 120,
};

window.addEventListener("mousemove", (event) => {
  mouse.x = event.x;
  mouse.y = event.y;
});

class Particle {
  constructor(x, y, size, speedX, speedY) {
    this.x = x;
    this.y = y;
    this.size = size;
    this.speedX = speedX;
    this.speedY = speedY;
  }

  draw() {
    ctx.beginPath();
    ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
    ctx.fillStyle = "rgba(255,255,255,0.8)";
    ctx.fill();
  }

  update() {
    this.x += this.speedX;
    this.y += this.speedY;

    // rebote nas bordas
    if (this.x < 0 || this.x > canvas.width) this.speedX *= -1;
    if (this.y < 0 || this.y > canvas.height) this.speedY *= -1;

    // interação com o mouse
    let dx = mouse.x - this.x;
    let dy = mouse.y - this.y;
    let distance = Math.sqrt(dx * dx + dy * dy);
    if (distance < mouse.radius) {
      this.x -= dx / 10;
      this.y -= dy / 10;
    }
  }
}

function init() {
  particlesArray = [];
  for (let i = 0; i < numberOfParticles; i++) {
    const size = Math.random() * 2 + 1;
    const x = Math.random() * canvas.width;
    const y = Math.random() * canvas.height;
    const speedX = (Math.random() - 0.5) * 0.6;
    const speedY = (Math.random() - 0.5) * 0.6;
    particlesArray.push(new Particle(x, y, size, speedX, speedY));
  }
}

function animate() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  for (let particle of particlesArray) {
    particle.update();
    particle.draw();
  }
  requestAnimationFrame(animate);
}

init();
animate();

window.addEventListener("resize", () => {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
  init();
});
