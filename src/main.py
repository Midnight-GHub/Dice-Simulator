import wx
import os
from random import randint

def loadImage(path):
    '''
    Load and slice the dice image into individual dice face bitmaps.
    path: str, path to the dice image file.
    Returns: list of wx.Bitmap, list of dice face bitmaps.
    '''

    X_RANGES = [(33, 83), (103, 153), (173, 223)]
    Y_RANGES = [(7, 58), (70, 121)]

    img = wx.Image(path, wx.BITMAP_TYPE_PNG)
    dice_img = []

    for y1, y2 in Y_RANGES:
        for x1, x2 in X_RANGES:
            w = x2 - x1 + 1
            h = y2 - y1 + 1
            sub_img = img.GetSubImage(wx.Rect(x1, y1, w, h))
            bmp = wx.Bitmap(sub_img)
            dice_img.append(bmp)

    return dice_img

def onGenerate(event, dice_static_bitmaps):
    '''
    Event handler for the "Generate" button click.
    Randomly selects a dice face and hides all other faces.
    event: wx.Event, the button click event.
    dice_static_bitmaps: dict, mapping of dice face values to wx.StaticBitmap objects.
    Returns: None
    '''

    dice_value = randint(1, 6)
    for i in range(1, 7):
        dice_static_bitmaps[i].Hide()
    dice_static_bitmaps[dice_value].Show()

def mainFrame(prj_dir):
    '''
    Create the main application frame.
    prj_dir: str, path to the project directory.
    Returns: wx.Frame, the main application frame.
    '''

    frame = wx.Frame(None, title="Dice Simulator", size=(300,300))

    panel = wx.Panel(frame)

    display_panel = wx.Panel(panel, pos=(10, 10), size=(51, 52))
    display_panel.SetBackgroundColour(wx.Colour(0, 0, 0))
    dice_img = loadImage(os.path.join(prj_dir, "assets", "dice.png"))
    dice_static_bitmaps = {}

    # Create StaticBitmap for each dice face and hide them initially
    for i, bmp in enumerate(dice_img, start=1):
        static_bitmap = wx.StaticBitmap(display_panel, bitmap=bmp)
        static_bitmap.Hide()
        dice_static_bitmaps[i] = static_bitmap

    dice_static_bitmaps[1].Show() # show initial dice face

    generate_button = wx.Button(panel, label="Generate", pos=(10,150))
    generate_button.Bind(wx.EVT_BUTTON, lambda event: onGenerate(event, dice_static_bitmaps))

    return frame

if __name__ == "__main__":
    src_dir = os.path.dirname(os.path.abspath(__file__))
    prj_dir = os.path.dirname(src_dir)

    app = wx.App(False)
    frame = mainFrame(prj_dir=prj_dir)
    frame.Show()
    app.MainLoop()