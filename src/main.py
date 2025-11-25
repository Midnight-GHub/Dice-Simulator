import wx
class DiceFrame(wx.Frame):
    def __init__(self):
        super().__init__(None,title='Dice Simulator',size=(500,500))
        panel=wx.Panel(self)
        self.txt=wx.StaticText(panel,label='Dice Roll: --')
        button=wx.Button(panel,label='Roll Dice')
        button.Bind(wx.EVT_BUTTON,self.onroll)
        sizer=wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.txt,0,wx.ALIGN_CENTER | wx.TOP,20)
        sizer.Add(button,0,wx.ALIGN_CENTER | wx.TOP,20)
        panel.SetSizer(sizer)

    def onroll(self,event):
        import subprocess
        #change directory before running
        blenderpath=r'C:\Users\Arun\blender\blender-4.2.16-windows-x64\blender.exe'
        blendfile=r'C:\Users\Arun\Desktop\Project\jackfruit_4.2.blend'
        scriptfile=r'C:\Users\Arun\Desktop\Project\rolldice.py'#dice roller

        command=[blenderpath,'-b',blendfile,'-P',scriptfile]

        process=subprocess.Popen(command,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE,
                                 text=True)
        
        result_number=None

        for line in process.stdout:
            print(line.strip())
            if 'RESULT:' in line:
                result_number=int((line.split(':')[1]).strip())
        process.wait()

        if result_number is not None:
            self.txt.SetLabel(f'Rolled Number:{result_number}')
        else:
            self.txt.SetLabel("Dice couldn't be Rolled : ERROR")

if __name__=="__main__":
    App=wx.App()
    frame=DiceFrame()
    frame.Show()
    App.MainLoop()