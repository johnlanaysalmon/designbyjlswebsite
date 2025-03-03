const canvas = document.getElementById("circleCanvas");
const ctx = canvas.getContext("2d");

const centerX = canvas.width / 2;
const centerY = canvas.height / 2;
const radius = 100; // Circle radius
const ballRadius = 10; // Ball size
let angle = 0; // Starting angle
const speed = 0.05; // Speed of rotation

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw the central point (for reference)
    ctx.beginPath();
    ctx.arc(centerX, centerY, 3, 0, Math.PI * 2);
    ctx.fillStyle = "red";
    ctx.fill();

    // Calculate ball position
    const ballX = centerX + radius * Math.cos(angle);
    const ballY = centerY + radius * Math.sin(angle);

    // Draw the moving ball
    ctx.beginPath();
    ctx.arc(ballX, ballY, ballRadius, 0, Math.PI * 2);
    ctx.fillStyle = "blue";
    ctx.fill();

    angle += speed; // Update angle for rotation

    requestAnimationFrame(draw); // Loop animation
}

// Start the animation
draw();
