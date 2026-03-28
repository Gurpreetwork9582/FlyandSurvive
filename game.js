const config = {
    type: Phaser.AUTO,
    width: 400,
    height: 600,
    parent: "game-container",
    physics: {
        default: "arcade",
        arcade: {
            gravity: { y: 370 },
            debug: false
        }
    },
    scene: {
        preload,
        create,
        update
    }
};

const game = new Phaser.Game(config);

let player;
let topPipes;
let bottomPipes;
let score = 0;
let scoreText;
let gameOver = false;
let pipesPassed = new Set();
let startText;
let gameOverText;
let bg1;
let bg2;
let restartButton;
let isGameStarted = false;

function preload() {
    this.load.image("bird", "Bird.gif");
    this.load.image("pipeup", "pipeup.png");
    this.load.image("pipedown", "pipedown.png");
    this.load.image("background", "flappy-bird-background.jpg");
}

function create() {
    // Add scrolling background
    bg1 = this.add.image(0, 0, "background").setOrigin(0, 0);
    bg2 = this.add.image(400, 0, "background").setOrigin(0, 0);
    bg1.setDisplaySize(400, 600);
    bg2.setDisplaySize(400, 600);

    player = this.physics.add.sprite(60, 80, "bird").setScale(0.1);
    player.setCollideWorldBounds(true);
    player.setBounce(0.2);

    topPipes = this.physics.add.group();
    bottomPipes = this.physics.add.group();

    // Start instruction
    startText = this.add.text(200, 100, "Press ENTER to Start\n\nSPACE to Flap", { 
        fontSize: "16px", 
        fill: "#000",
        align: "center",
        backgroundColor: "#ffffff",
        padding: { x: 10, y: 10 }
    });
    startText.setOrigin(0.5);

    // Score text
    scoreText = this.add.text(30, 30, "Score: 0", { 
        fontSize: "20px", 
        fill: "#000",
        fontStyle: "bold"
    });

    // Game over text (hidden initially)
    gameOverText = this.add.text(200, 250, "", { 
        fontSize: "24px", 
        fill: "#ff0000",
        align: "center",
        fontStyle: "bold",
        backgroundColor: "#ffffff",
        padding: { x: 15, y: 15 }
    });
    gameOverText.setOrigin(0.5);
    gameOverText.setVisible(false);

    // Restart button
    restartButton = this.add.text(200, 550, "Restart", { 
        fontSize: "15px", 
        fill: "#000",
        backgroundColor: "#888888",
        padding: { x: 20, y: 10 }
    });
    restartButton.setOrigin(0.5);
    restartButton.setVisible(false);
    restartButton.setInteractive();

    this.input.keyboard.on("keydown-ENTER", () => {
        if (!isGameStarted) {
            isGameStarted = true;
            startText.setVisible(false);
        }
    });

    this.input.keyboard.on("keydown-SPACE", () => {
        if (isGameStarted && !gameOver) {
            player.setVelocityY(-260);
        }
    });

    restartButton.on("pointerdown", () => {
        this.scene.restart();
    });

    this.time.addEvent({
        delay: 1500,
        callback: () => spawnPipes.call(this),
        loop: true,
        paused: true
    });

    this.pipeTimer = this.time.addEvent({
        delay: 1500,
        callback: () => spawnPipes.call(this),
        loop: true
    });
    this.pipeTimer.paused = true;

    // Collision with pipes
    this.physics.add.overlap(player, topPipes, () => {
        endGame.call(this);
    });
    
    this.physics.add.overlap(player, bottomPipes, () => {
        endGame.call(this);
    });

    this.gameOverText = gameOverText;
    this.startText = startText;
    this.restartButton = restartButton;
    this.scene = this.scene;
}

function update() {
    // Move background
    if (isGameStarted && !gameOver) {
        bg1.x -= 2;
        bg2.x -= 2;

        if (bg1.x < -400) {
            bg1.x = bg2.x + 400;
        }
        if (bg2.x < -400) {
            bg2.x = bg1.x + 400;
        }

        // Start pipe spawning when game starts
        if (!this.pipeTimer || this.pipeTimer.paused) {
            this.pipeTimer = this.time.addEvent({
                delay: 1500,
                callback: () => spawnPipes.call(this),
                loop: true
            });
        }
    }

    // Check collision with ground
    if (player.y >= 600) {
        endGame.call(this);
    }
    if (player.y <= 0) {
        endGame.call(this);
    }

    // Remove pipes that are off-screen
    topPipes.children.entries.forEach(pipe => {
        if (pipe.x < -100) {
            pipe.destroy();
        }
    });

    bottomPipes.children.entries.forEach(pipe => {
        if (pipe.x < -100) {
            pipe.destroy();
        }
    });
}

function spawnPipes() {
    if (!isGameStarted || gameOver) return;

    const distance = 50;
    const randomYDown = Phaser.Math.Between(80, 150);
    const randomYUp = 700 - randomYDown - distance;

    const randomX = Phaser.Math.Between(350, 400);

    // Top pipe
    let topPipe = topPipes.create(randomX, randomYUp, "pipeup");
    topPipe.setScale(0.15);
    topPipe.setVelocityX(-200);
    topPipe.setImmovable(true);
    topPipe.body.allowGravity = false;
    topPipe.pipeId = Date.now();

    // Bottom pipe
    let bottomPipe = bottomPipes.create(randomX, randomYDown, "pipedown");
    bottomPipe.setScale(0.15);
    bottomPipe.setVelocityX(-200);
    bottomPipe.setImmovable(true);
    bottomPipe.body.allowGravity = false;
    bottomPipe.pipeId = topPipe.pipeId;

    // Check when pipe is passed
    const checkScore = setInterval(() => {
        if (player && player.x > topPipe.x && !pipesPassed.has(topPipe.pipeId)) {
            pipesPassed.add(topPipe.pipeId);
            score++;
            scoreText.setText("Score: " + score);
            clearInterval(checkScore);
        }
        if (topPipe.x < -100) {
            clearInterval(checkScore);
        }
    }, 50);
}

function endGame() {
    if (!gameOver && isGameStarted) {
        gameOver = true;
        player.setTint(0xff0000);
        gameOverText.setText("GAME OVER!\nScore: " + score);
        gameOverText.setVisible(true);
        gameOverText.y = 250;
        restartButton.setVisible(true);
        player.setVelocityY(0);
    }
}