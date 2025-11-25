import wx
import os
import subprocess

from handler import jsonHandler

class MainFrame(wx.Frame):
    def __init__(self, prj_dir, blender_path):
        super().__init__(None, title='Dice Simulator', size=(500, 500))

        self.prj_dir = prj_dir
        self.blender_path = blender_path
        self.dice_model_path = os.path.join(self.prj_dir, "assets", "dice.blend")
        self.script_path = os.path.join(self.prj_dir, "src", "run_dice.py")

        self.blender_script_command = [self.blender_path, '-b', self.dice_model_path, '-P', self.script_path]

        self.panel = wx.Panel(self)
        self.txt = wx.StaticText(self.panel, label='Dice Roll: --')

        self.button = wx.Button(self.panel, label='Roll Dice')
        self.button.Bind(wx.EVT_BUTTON, self.onroll)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.txt, 0, wx.ALIGN_CENTER | wx.TOP, 20)
        self.sizer.Add(self.button, 0, wx.ALIGN_CENTER | wx.TOP, 20)
        self.panel.SetSizer(self.sizer)

    def onroll(self, event):
        result_number = None

        process = subprocess.Popen(
            self.blender_script_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        for line in process.stdout:
            print(line.strip())
            if 'RESULT:' in line:
                result_number = int(line.split(':')[1].strip())

        process.wait()

        if result_number is not None:
            self.txt.SetLabel(f'Rolled Number: {result_number}')
        else:
            self.txt.SetLabel("Dice couldn't be Rolled : ERROR")


if __name__ == "__main__":
    src_dir = os.path.dirname(os.path.abspath(__file__))
    prj_dir = os.path.dirname(src_dir)

    json_handle = jsonHandler(os.path.join(prj_dir, 'data', 'config.json'))
    config = json_handle.load()

    app = wx.App()
    frame = MainFrame(prj_dir=prj_dir, blender_path=config['path']['blender'])
    frame.Show()
    app.MainLoop()
