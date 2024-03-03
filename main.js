const canvas = document.getElementById("myCanvas");
const ctx = canvas.getContext("2d");

// Parámetros de la pelota
let ballRadius = 20;
let x = canvas.width / 2;
let y = canvas.height / 2;
let ballSpeedX = Math.random() * 6 + 2; // Velocidad inicial aleatoria
let ballSpeedY = Math.random() * 6 + 2;

// Parámetros del rectángulo
let rectWidth = 75;
let rectHeight = 50;
let rectX = (canvas.width - rectWidth)/3 ;
let rectY = (canvas.height - rectHeight) / 2;
let rectSpeedX = 5;

// Funciones de dibujo 2do rectangulo 
let rect2Width = 75;
let rect2Height = 50;
let rect2X = (canvas.width - rectWidth) / 2 + rectWidth;
let rect2Y = (canvas.height - rectHeight) / 2;
let rect2SpeedX = 5;

let rect3Width = 75;
let rect3Height = 50;
let rect3X = (canvas.width - rectWidth) / 2 + rectWidth;
let rect3Y = (canvas.height - rectHeight) / 2;


// Métodos de la pelota
function drawBall() {
    ctx.beginPath();
    ctx.arc(x, y, ballRadius, 0, Math.PI * 2);
    ctx.fillStyle = "red";
    ctx.fill();
    ctx.closePath();
}

// Métodos del rectángulo
function drawRect() {
    ctx.beginPath();
    ctx.rect(rectX, rectY, rectWidth, rectHeight);
    ctx.fillStyle = "green";
    ctx.fill();
    ctx.closePath();

    ctx.beginPath();
    ctx.rect(rect2X, rect2Y, rect2Width, rect2Height);
    ctx.fillStyle = "green";
    ctx.fill();
    ctx.closePath();

    ctx.beginPath();    
    ctx.rect(rect3X, rect3Y, rect3Width, rect3Height);
    ctx.fillStyle = "green";
    ctx.fill();
    ctx.closePath();
}

// Función de dibujar
function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawBall();
    drawRect();

    x += ballSpeedX;
    y += ballSpeedY;

    if (x + ballRadius > canvas.width || x - ballRadius < 0) {
        ballSpeedX = -ballSpeedX;
    }
    if (y + ballRadius > canvas.height || y - ballRadius < 0) {
        ballSpeedY = -ballSpeedY;
    }

    // Colisión de la pelota con el rectángulo
    if (
        x >= rectX &&
        x <= rectX + rectWidth &&
        y >= rectY &&
        y <= rectY + rectHeight
    ) {
        ballSpeedX = -ballSpeedX;
    }

    // Movimiento del rectángulo con las teclas
    window.addEventListener("keydown", function (event) {
        if (event.key === "ArrowLeft") {
            rectX -= rectSpeedX;
        } else if (event.key === "ArrowRight") {
            rectX += rectSpeedX;
        }
    });
   
    
    
    rect2X += rect2SpeedX;  
    if (rect2X + rect2Width > canvas.width || rect2X < 0) {
        rect2SpeedX = -rect2SpeedX;
    }

    
    

    
    


    requestAnimationFrame(draw);
}

draw(); // Iniciar la animación
