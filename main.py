from os import environ, getcwd
from os.path import basename
from PyQt5.QtWidgets import QApplication, QMainWindow,QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap,QCursor
import sys
from PIL import Image
from threading import Thread
from Library.IQtTool.WigetCombobox import WigetCombobox
from Library.IQtTool.WigetInputbox import WigetInputbox
from Library.IQtTool.WigetMessagebox import WigetMessagebox
from Library.Quet.lite.LiteLog import LiteLog
from gui import Ui_MainWindow
from qt_material import apply_stylesheet,list_themes

class PixelTool(QMainWindow,Ui_MainWindow):
    def __init__(self,parent=None) -> None:
        super(PixelTool,self).__init__(parent)
        self.setupUi(self)
        self.myLog=LiteLog(name=__name__)
        self.myLog.bindQTlog(self.LogBrowser)
        self.s1ze=10
        self.m_flag=False
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.controlvar.setMinimum(1)
        self.InputBtn.clicked.connect(self.chose_img)
        self.Outbtn.clicked.connect(self.chose_dir)
        self.RefreshBtn.clicked.connect(self.ImgThread_control)
        self.controlvar.sliderReleased.connect(self.ImgThread_control)
        self.controlvar.valueChanged.connect(self.logvaule)
        self.MenuAbout.triggered.connect(self.about)
        self.MenuClose.triggered.connect(self.close)
        self.MenuSeize.triggered.connect(self.reseizes1ze)
        self.MenuInput.triggered.connect(self.chose_img)
        self.MenuOut.triggered.connect(self.chose_dir)
        self.MenuSwichDL.triggered.connect(self.myTheme)
        self.MenuSwichTE.triggered.connect(self.swichTheme)
        self.MenuFullscreen.triggered.connect(self.showFullScreen)
        self.MenudonotFull.triggered.connect(self.showNormal)
        self.Menuwtlog.triggered.connect(lambda:self.myLog.write_cache_log(QFileDialog.getExistingDirectory(self,"选择日志输出目录",getcwd()),True))
        self.rawimg.setScaledContents(True)
        self.afterimg.setScaledContents(True)
        self.imgpath=""
        self.imgout=None
    def logvaule(self):
        self.myLog.infolog("滑块目前值为%s" % self.controlvar.value())
    def reseizes1ze(self):
        self.wib=WigetInputbox(title="与滑块最大值有关,当前值%s" % self.s1ze,callmethod=self.doresize,color=environ["QTMATERIAL_PRIMARYCOLOR"],calllog=self.myLog)
        self.wib.show()
    def mouseDoubleClickEvent(self, QMouseEvent):
       if self.isFullScreen():
           self.showNormal()
       else:
           self.showFullScreen()
    def doresize(self,vaule):
        if vaule == "":
            return
        try:
            vaule=int(vaule)
        except:
            return
        if vaule <= 0:
            return
        else:
            self.s1ze=vaule
    def mousePressEvent(self, event):
        if event.button()==Qt.LeftButton:
            self.m_flag=True
            self.m_Position=event.globalPos()-self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))
    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:  
            self.move(QMouseEvent.globalPos()-self.m_Position)
            QMouseEvent.accept()
    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag=False
        self.setCursor(QCursor(Qt.ArrowCursor))
    def about(self):
        self.wmb=WigetMessagebox(title="关于",desc=["此软件开源免费","仓库地址(https://github.com/IAXRetailer/QPixelTool)","作者H2Sxxa(https://github.com/IAXRetailer)","如果这个软件帮到你了不妨考虑考虑赞助(https://afdian.net/@H2Sxxa)","如果你习惯使用某站也可以点个关注(https://space.bilibili.com/393570351)"],color=environ["QTMATERIAL_PRIMARYCOLOR"])
        self.wmb.show()
    def swichTheme(self):
        themelist=list_themes()
        themelist.remove(environ["QTMATERIAL_THEME"])
        themelist.insert(0,environ["QTMATERIAL_THEME"])
        self.wmb=WigetCombobox(title="主题选择",ChoiceList=themelist,calllog=self.myLog,callmethod=self.runSwichTheme,color=environ["QTMATERIAL_PRIMARYCOLOR"])
        self.wmb.show()
    def runSwichTheme(self,themename):
        apply_stylesheet(app=app,theme=themename)
    def myTheme(self):
        nowTheme=environ["QTMATERIAL_THEME"]
        themelist=list_themes()
        if "dark" in nowTheme:
            targetTheme=nowTheme.replace("dark","light",1)
            if targetTheme not in themelist:
                self.wmb=WigetMessagebox([f"目标主题{targetTheme}未找到"],title="错误",color=environ["QTMATERIAL_PRIMARYCOLOR"])
                self.wmb.show()
                return
            else:
                apply_stylesheet(app=app,theme=targetTheme)
                return
        if "light" in nowTheme:
            if "_500" in nowTheme:
                nowTheme=nowTheme.replace("_500","")
            targetTheme=nowTheme.replace("light","dark",1)
            if targetTheme not in themelist:
                self.wmb=WigetMessagebox([f"目标主题{targetTheme}未找到"],title="错误",color=environ["QTMATERIAL_PRIMARYCOLOR"])
                self.wmb.show()
                return
            else:
                apply_stylesheet(app=app,theme=targetTheme)
                return
    def ImgThread_control(self):
        self.myLog.infolog("开始处理%s" % self.imgpath)
        self.myLog.infolog("块大小为%s" % self.controlvar.value())
        Thread(target=self.UpdateImg).start()
    def chose_dir(self):
        if self.imgpath == "":
            return
        targetpath=QFileDialog.getExistingDirectory(self,"选择输出文件夹",getcwd())
        if self.imgout == None:
            return
        self.myLog.infolog("导出为%s" % targetpath+"/Pixel "+basename(self.imgpath))
        self.imgout.save(targetpath+"/Pixel "+basename(self.imgpath))
    def chose_img(self):
        imgpath=QFileDialog.getOpenFileName(self,"选择图片",getcwd())[0]
        if imgpath == "":
            return
        self.imgpath=imgpath
        self.setSliderValue()
        self.rawimg.setPixmap(QPixmap(self.imgpath))
    def setSliderValue(self):
        img = Image.open(self.imgpath)
        if img.height >= img.width:
            maxv=img.height
        else:
            maxv=img.width
        try:
            self.controlvar.setMaximum(int(float(maxv/self.s1ze)))
        except Exception as e:
            self.myLog.errorlog(str(e))
            self.controlvar.setMaximum(int(float(maxv/10)))
    def UpdateImg(self):
        if self.imgpath == "":
            return
        block_size=self.controlvar.value()
        img = Image.open(self.imgpath).convert('RGBA')
        width, height = img.size
        img_array = img.load()
        max_width = width + block_size
        max_height = height + block_size
        for x in range(block_size - 1, max_width, block_size):
            for y in range(block_size - 1, max_height, block_size):
                if x == max_width - max_width % block_size - 1:
                    x = width - 1
                if y == max_height - max_height % block_size - 1:
                    y = height - 1
                self.change_block(x, y, block_size, img_array)
                y += block_size
            x += block_size
        img.save("cache.png")
        self.imgout=img
        self.afterimg.setPixmap(QPixmap("cache.png"))
    def change_block(self,x,y,block_size,img_array) -> None:
        color_dist = {}
        block_pos_list = []
        for pos_x in range(-block_size + 1, 1):
            for pos_y in range(-block_size + 1, 1):
                block_pos_list.append([x + pos_x, y + pos_y])
        for pixel in block_pos_list:
            if not str(img_array[pixel[0], pixel[1]]) in color_dist.keys():
                color_dist[str(img_array[pixel[0], pixel[1]])] = 1
            else:
                color_dist[str(img_array[pixel[0], pixel[1]])] += 1
        new_dict = {v: k for k, v in color_dist.items()}
        max_color = new_dict[max(color_dist.values())]
        for a in block_pos_list:
            img_array[a[0], a[1]] = tuple(list(map(int, max_color[1:len(max_color) - 1].split(","))))

if __name__ == "__main__":
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app=QApplication(sys.argv)
    apply_stylesheet(app,theme='light_cyan_500.xml')
    ui=PixelTool()
    ui.show()
    sys.exit(app.exec_())