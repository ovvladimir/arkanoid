from browser import document, bind, window
from random import choice, randrange
from math import pi

ballRadius = 10
paddleHeight = 10
paddleWidth = 75
brickRowCount = 5
brickColumnCount = 4
brickWidth = 75
brickHeight = 20
brickPadding = 10
brickOffsetTop = 30
brickOffsetLeft = 30
brickSpeed = 10

colors = ['#198754', '#dc3545', '#0dcaf0', '#ffc107', '#fd7e14', '#2526F7', '#d63384']


class Brick:

    def __init__(self):
        self.x = 0
        self.y = 0
        self.status = 1
        self.color = choice(colors)


class Panel:

    def __init__(self):
        self.x = W / 2.
        self.y = H - paddleHeight - ballRadius
        self.dx = 3
        self.dy = -3
        self.paddleX = (W - paddleWidth) / 2.
        self.rightPressed = False
        self.leftPressed = False
        self.changing_color = False
        self.score = 0
        self.level = 1
        self.lives = 3
        self.bricks = [[Brick() for _ in range(brickRowCount)] for _ in range(brickColumnCount)]
        self.stop = False

    def collisionDetection(self):
        for c in range(brickColumnCount):
            for r in range(brickRowCount):
                b = self.bricks[c][r]
                if b.status == 1:
                    """
                    if b.x < self.x < b.x + brickWidth and b.y < self.y < b.y + brickHeight:
                        self.dy = -self.dy
                        b.status = 0
                        self.score += 1
                    """
                    nx = max(b.x, min(self.x, b.x + brickWidth))
                    ny = max(b.y, min(self.y, b.y + brickHeight))
                    dtc = (nx - self.x) ** 2 + (ny - self.y) ** 2
                    if dtc <= ballRadius ** 2:
                        self.dy = -self.dy
                        b.status = 0
                        self.score += 1

                        if self.score == brickRowCount * brickColumnCount * self.level:
                            self.x = W / 2.
                            self.y = H - paddleHeight - ballRadius
                            self.level += 1
                            self.dy = -abs(self.dy) - 1
                            test.innerHTML = f'Уровень {self.level}. Скорость {abs(self.dy)}.'
                            self.bricks = [[Brick() for _ in range(brickRowCount)] for _ in range(brickColumnCount)]

    def drawBall(self):
        ctx.fillStyle = "#ffff00" if self.changing_color else "#ff0000"
        ctx.beginPath()
        ctx.arc(self.x, self.y, ballRadius, 0, pi * 2)
        ctx.closePath()
        ctx.fill()

    def drawPaddle(self):
        gradient = ctx.createLinearGradient(self.paddleX, 0, self.paddleX + paddleWidth, 0)
        gradient.addColorStop(0, "#0000ff")
        gradient.addColorStop(1, "#00bfff")
        ctx.fillStyle = gradient
        ctx.fillRect(self.paddleX, H - paddleHeight, paddleWidth, paddleHeight)
        ctx.strokeStyle = "#6610f2"
        ctx.strokeRect(self.paddleX, H - paddleHeight, paddleWidth, paddleHeight)

    def drawBricks(self):
        for c in range(brickColumnCount):
            for r in range(brickRowCount):
                if self.bricks[c][r].status == 1:
                    brickX = r * (brickWidth + brickPadding) + brickOffsetLeft
                    brickY = c * (brickHeight + brickPadding) + brickOffsetTop
                    self.bricks[c][r].x = brickX
                    self.bricks[c][r].y = brickY
                    ctx.fillStyle = self.bricks[c][r].color
                    ctx.fillRect(brickX, brickY, brickWidth, brickHeight)

    def drawScore(self):
        ctx.font = "18px Arial"
        ctx.fillStyle = "#fff"
        ctx.fillText(f"score: {self.score}", 7, 20)

    def drawLives(self):
        ctx.font = "18px Arial"
        ctx.fillStyle = "#fff"
        ctx.fillText(f"lives: {self.lives}", W - 70, 20)

    def draw(self, *args):
        ctx.clearRect(0, 0, W, H)
        self.drawBricks()
        self.drawBall()
        self.drawPaddle()
        self.drawScore()
        self.drawLives()
        self.collisionDetection()

        if self.stop:
            window.cancelAnimationFrame()
        else:
            self.x += self.dx
            self.y += self.dy
            window.requestAnimationFrame(self.draw)

        self.changing_color = False
        if self.x >= W - ballRadius or self.x <= ballRadius:
            self.dx = -self.dx
        elif self.y <= ballRadius:
            self.y += 1  # убирает залипание
            self.dy = -self.dy
        elif self.y >= H - paddleHeight - ballRadius \
                and self.paddleX < self.x <= self.paddleX + paddleWidth / 2.:
            self.y -= abs(self.dy)
            self.dy = -self.dy
            self.dx = randrange(-abs(self.dy), -1)
        elif self.y >= H - paddleHeight - ballRadius \
                and self.paddleX + paddleWidth / 2. < self.x < self.paddleX + paddleWidth:
            self.y -= abs(self.dy)
            self.dy = -self.dy
            self.dx = randrange(2, abs(self.dy) + 1)
        elif self.y >= H - ballRadius:
            self.lives -= 1
            if not self.lives:
                test.innerHTML = "GAME OVER"
                self.stop = True
                # document.location.reload()
            else:
                self.y -= 1
                self.dy = -self.dy
                self.changing_color = True

        if self.rightPressed and self.paddleX < W - paddleWidth:
            self.paddleX += brickSpeed
        elif self.leftPressed and self.paddleX > 0:
            self.paddleX -= brickSpeed

    def start(self, *args):
        if self.stop:
            self.__init__()
            test.innerHTML = f'Уровень {self.level}. Скорость {abs(self.dy)}.'
            self.draw()


@bind(document, "keydown")
def keyDownHandler(e):
    if e.keyCode == 39:
        panel.rightPressed = True
    elif e.keyCode == 37:
        panel.leftPressed = True


@bind(document, "keyup")
def keyUpHandler(e):
    if e.keyCode == 39:
        panel.rightPressed = False
    elif e.keyCode == 37:
        panel.leftPressed = False


@bind(document, "mousemove")
def mouseMoveHandler(e):
    panel.paddleX = e.x
    if panel.paddleX < 0:
        panel.paddleX = 0
    elif panel.paddleX > W - paddleWidth:
        panel.paddleX = W - paddleWidth


'''
def range_html(e=None):
    # test.innerHTML = inp.value + " px"
    # test.innerHTML = str(round(float(inp.value), 1)) + " px"
    panel.paddleX = float(inp.value)
'''


test = document["test"]
canvas = document["myCanvas"]
btn = document["start"]
inp = document["customRange3"]
ctx = canvas.getContext("2d")
W, H = canvas.width, canvas.height
panel = Panel()
panel.stop = True
btn.bind("click", panel.start)
# inp.addEventListener("input", range_html)
panel.draw()
