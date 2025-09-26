import sys, os

# --- console toggle ---
if "-console" in sys.argv:
    import ctypes
    ctypes.windll.kernel32.AllocConsole()
    sys.stdout = open("CONOUT$", "w")
    sys.stderr = open("CONOUT$", "w")
    sys.stdin = open("CONIN$", "r")

# --- resource path helper ---
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

import turtle

# init
wn = turtle.Screen()
wn.title("Dreamy Choc Chip Cookie Clicker")
wn.bgcolor("black")

# use resource_path for gifs
wn.register_shape(resource_path("woolies.gif"))
wn.register_shape(resource_path("cookie.gif"))

upgrade1 = turtle.Turtle()
upgrade1.shape(resource_path("woolies.gif"))
upgrade1.speed(0)
upgrade1.goto(300, 0)

tierOne = False

cookie = turtle.Turtle()
cookie.shape(resource_path("cookie.gif"))
cookie.speed(0)

clicks = 0

pen = turtle.Turtle()
pen.hideturtle()
pen.color("white")
pen.penup()
pen.goto(0, 250)
pen.write(f"Clicks: {clicks}", align="center", font=("Courier New", 32, "normal"))

desc_pen = turtle.Turtle()
desc_pen.hideturtle()
desc_pen.color("yellow")
desc_pen.penup()
desc_pen.goto(320, 80)

def clicked(x, y):
    global clicks
    if tierOne:
        clicks += 2
    else:
        clicks += 1
    pen.clear()
    pen.write(f"Clicks: {clicks}", align="center", font=("Courier New", 32, "normal"))
    print(clicks)

def upgrade1_clicked(x, y):
    global tierOne
    tierOne = True

def show_description():
    desc_pen.clear()
    desc_pen.write("Doubles Cookies per tap", align="center", font=("Courier New", 18, "normal"))

def hide_description():
    desc_pen.clear()

def check_hover(x, y):
    if abs(x - 300) < 50 and abs(y - 0) < 50:
        show_description()
    else:
        hide_description()

def poll_mouse():
    x, y = wn._root.winfo_pointerx() - wn._root.winfo_rootx(), wn._root.winfo_pointery() - wn._root.winfo_rooty()
    tx = x - wn.window_width() // 2
    ty = wn.window_height() // 2 - y
    if abs(tx - 300) < 50 and abs(ty - 0) < 50:
        show_description()
    else:
        hide_description()
    wn.ontimer(poll_mouse, 100)

cookie.onclick(clicked)
upgrade1.onclick(upgrade1_clicked)
wn.onscreenclick(check_hover)
poll_mouse()

wn.mainloop()
