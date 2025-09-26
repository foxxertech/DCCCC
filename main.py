import sys, os

# --- console toggle ---
if "-console" in sys.argv:
    import ctypes
    ctypes.windll.kernel32.AllocConsole()
    sys.stdout = open("CONOUT$", "w")
    sys.stderr = open("CONOUT$", "w")
    sys.stdin = open("CONIN$", "r")
print("Hello! If you are in here, you are etiher fixing a bug or developing!")
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
turtle.screensize(800, 800)

# Set window icon (must be .ico format)
wn.getcanvas().winfo_toplevel().iconbitmap(resource_path("logo.ico"))

# use resource_path for gifs
wn.register_shape(resource_path("bakery.gif"))
wn.register_shape(resource_path("woolies.gif"))
wn.register_shape(resource_path("cookie.gif"))

bakery = turtle.Turtle()
bakery.shape(resource_path("bakery.gif"))
bakery.speed(0)
bakery.goto(300, 180)

upgrade1 = turtle.Turtle()
upgrade1.shape(resource_path("woolies.gif"))
upgrade1.speed(0)
upgrade1.goto(300, 0)

tierOne = False

cookie = turtle.Turtle()
cookie.shape(resource_path("cookie.gif"))
cookie.speed(0)
cookie.goto(-340, 0)

clicks = 0

pen = turtle.Turtle()
pen.hideturtle()
pen.color("white")
pen.penup()
pen.goto(-340, 250)
pen.write(f"Clicks: {clicks}", align="center", font=("Courier New", 32, "normal"))

desc_pen = turtle.Turtle()
desc_pen.hideturtle()
desc_pen.color("yellow")
desc_pen.penup()
desc_pen.goto(320, 80)
# Do NOT write the description here by default

# Add a separate pen for error messages
error_pen = turtle.Turtle()
error_pen.hideturtle()
error_pen.color("red")
error_pen.penup()

bakery_purchased = False

def clicked(x, y):
    global clicks
    if tierOne:
        clicks += 2
    else:
        clicks += 1
    pen.clear()
    pen.write(f"Clicks: {clicks}", align="center", font=("Courier New", 32, "normal"))
    print(clicks)

def show_description():
    desc_pen.clear()
    desc_pen.goto(435, 80)
    desc_pen.write("Doubles Cookies per tap, costs 10 clicks", align="center", font=("Courier New", 18, "normal"))

def hide_description():
    desc_pen.clear()

def show_not_enough_clicks():

    error_pen.clear()
    error_pen.goto(0, -280)  # Position under the cookie
    error_pen.write("Not enough clicks!", align="center", font=("Courier New", 18, "normal"))
    wn.ontimer(hide_not_enough_clicks, 2000)
    print("not enough")

def hide_not_enough_clicks():
    error_pen.clear()

def upgrade1_clicked(x, y):
    global tierOne, clicks
    if not tierOne and clicks >= 10:
        tierOne = True
        clicks -= 10
        pen.clear()
        pen.write(f"Clicks: {clicks}", align="center", font=("Courier New", 32, "normal"))
    elif not tierOne:
        show_not_enough_clicks()

def bakery_clicked(x, y):
    global clicks, bakery_purchased
    if not bakery_purchased and clicks >= 50:
        clicks -= 50
        pen.clear()
        pen.write(f"Clicks: {clicks}", align="center", font=("Courier New", 32, "normal"))
        bakery_purchased = True
        give_bakery_click()
    elif not bakery_purchased:
        error_pen.clear()
        error_pen.goto(0, -280)  # Below bakery
        error_pen.write("Not enough clicks!", align="center", font=("Courier New", 18, "normal"))
        wn.ontimer(hide_not_enough_clicks, 2000)
        print("not enough")

def give_bakery_click():
    global clicks
    if bakery_purchased:
        clicks += 1
        pen.clear()
        pen.write(f"Clicks: {clicks}", align="center", font=("Courier New", 32, "normal"))
        wn.ontimer(give_bakery_click, 1000)  # Repeat every second

def check_hover(x, y):
    if abs(x - 300) < 50 and abs(y - 0) < 50:
        show_description()
    else:
        hide_description()

def poll_mouse():
    x, y = wn._root.winfo_pointerx() - wn._root.winfo_rootx(), wn._root.winfo_pointery() - wn._root.winfo_rooty()
    tx = x - wn.window_width() // 2
    ty = wn.window_height() // 2 - y
    # Show woolies description when hovering over woolies
    if abs(tx - 300) < 50 and abs(ty - 0) < 50:
        show_description()
    # Show bakery description when hovering over bakery
    elif abs(tx - 300) < 50 and abs(ty - 180) < 50:
        show_bakery_description()
    else:
        hide_description()
    wn.ontimer(poll_mouse, 500)

def show_bakery_description():
    desc_pen.clear()
    desc_pen.goto(435, 220)  # Right of bakery
    desc_pen.write("Gives +1 click per second, costs 50 clicks", align="center", font=("Courier New", 18, "normal"))

cookie.onclick(clicked)
upgrade1.onclick(upgrade1_clicked)
bakery.onclick(bakery_clicked)
poll_mouse()

wn.mainloop()
