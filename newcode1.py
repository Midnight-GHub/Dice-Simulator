import wx
import threading
import subprocess

class DiceFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title='Dice Roll Simulator', size=(550,600))
        self.SetBackgroundColour("#C9E9FF")
        self.Center()

        panel = wx.Panel(self)
        panel.SetBackgroundColour("#C9E9FF")

        # Title
        title = wx.StaticText(panel, label='🎲 Dice Roll Simulator')
        font = wx.Font(26, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        title.SetFont(font)

        # Dice Display Box
        self.diceimage = wx.StaticBitmap(panel, bitmap=wx.Bitmap("dice1.png"))
        self.diceimage.SetMinSize((180, 180))

        # Result Label
        self.txt = wx.StaticText(panel, label='Result: --')
        font2 = wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.txt.SetFont(font2)

        # Buttons
        self.roll_btn = wx.Button(panel, label="Roll Dice")
        self.roll_btn.SetBackgroundColour("#0055AA")
        self.roll_btn.SetForegroundColour("white")
        self.roll_btn.Bind(wx.EVT_BUTTON, self.onroll)

        reset_btn = wx.Button(panel, label="Reset Stats")
        reset_btn.SetBackgroundColour("#AA0000")
        reset_btn.SetForegroundColour("white")
        reset_btn.Bind(wx.EVT_BUTTON, self.onreset)

        # Loading Text
        self.loading_txt = wx.StaticText(panel, label='')
        self.loading_txt.SetForegroundColour("#333333")

        # Statistics
        stats_label = wx.StaticText(panel, label="📊 Statistics")
        stats_label.SetFont(wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

        self.roll_count = 0
        self.count = {i:0 for i in range(1,7)}
        self.stats_txt = wx.StaticText(panel, label="No rolls yet.")
        self.stats_txt.SetForegroundColour("#111111")

        box = wx.StaticBox(panel, label="")
        box_sizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        box_sizer.Add(stats_label, 0, wx.ALIGN_CENTER | wx.TOP, 5)
        box_sizer.Add(self.stats_txt, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        # Layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(title, 0, wx.ALIGN_CENTER | wx.TOP, 15)
        sizer.Add(self.diceimage, 0, wx.ALIGN_CENTER | wx.TOP, 20)
        sizer.Add(self.txt, 0, wx.ALIGN_CENTER | wx.TOP, 15)
        sizer.Add(self.roll_btn, 0, wx.ALIGN_CENTER | wx.TOP, 20)
        sizer.Add(reset_btn, 0, wx.ALIGN_CENTER | wx.TOP, 10)
        sizer.Add(self.loading_txt, 0, wx.ALIGN_CENTER | wx.TOP, 10)
        sizer.Add(box_sizer, 0, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 20)

        panel.SetSizer(sizer)

        # Load dice images
        self.dice_images = {i: wx.Bitmap(f"dice{i}.png") for i in range(1,7)}

    def onreset(self, event):
        self.roll_count = 0
        self.count = {i:0 for i in range(1,7)}
        self.stats_txt.SetLabel("No rolls yet.")
        self.txt.SetLabel("Result: --")
        self.diceimage.SetBitmap(wx.Bitmap("dice1.png"))

    def onroll(self, event):
        self.loading_txt.SetLabel("Rolling... Please wait 🎬")
        t = threading.Thread(target=self.run_blender, daemon=True)
        t.start()

    def run_blender(self):
        blenderpath = r'C:\Users\Arun\blender\blender-4.2.16-windows-x64\blender.exe'
        blendfile = r'C:\Users\Arun\Desktop\Jackfruit Final\OG.blend'
        script = r'C:\Users\Arun\Desktop\Jackfruit Final\rolldicelt.py'

        cmd = [blenderpath, blendfile, "-P", script]
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = proc.communicate()

        result_number = None
        for line in stdout.splitlines():
            if "RESULT:" in line:
                result_number = int(line.split(":")[1].strip())
                break

        wx.CallAfter(self.finish_roll, result_number)

    def finish_roll(self, result):
        self.loading_txt.SetLabel("")
        if result and result in self.dice_images:
            self.roll_count += 1
            self.count[result] += 1
            self.txt.SetLabel(f"Result: {result}")
            self.diceimage.SetBitmap(self.dice_images[result])
            self.update_stats()
        else:
            self.txt.SetLabel("Roll Failed ❌")

    def update_stats(self):
        text = f"Total Rolls: {self.roll_count}\n\n"
        for i in range(1, 7):
            c = self.count[i]
            pct = (c / self.roll_count) * 100 if self.roll_count > 0 else 0
            text += f"{i}: {c} times ({pct:.1f}%)\n"
        self.stats_txt.SetLabel(text)


if __name__ == "__main__":
    app = wx.App()
    frame = DiceFrame()
    frame.Show()
    app.MainLoop()
