#создай тут фоторедактор Easy Editor!
from PIL import Image
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import os
from PIL import ImageFilter
from PIL.ImageFilter import *
from PyQt5.QtWidgets import QFileDialog, QLabel, QListWidget, QPushButton, QApplication, QWidget, QHBoxLayout, QVBoxLayout
#Функции
class ImageProcessor():
    def __init__(self):
        self.image = None
        self.dir = None  
        self.filename = None
        self.save_dir = "Modified/"
    def LoadImage(self, dir, filename):
        self.dir = dir
        self.filename = filename
        image_path = os.path.join(dir, filename)
        self.image = Image.open(image_path)
    def ShowImage(self, path):
        lb_image.hide()
        pixmapimage = QPixmap(path)
        w, h = lb_image.width(), lb_image.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        lb_image.setPixmap(pixmapimage)
        lb_image.show()
    def saveImage(self):
        path = os.path.join(workdir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        fullname = os.path.join(path, self.filename)
        self.image.save(fullname)
    def do_bw(self):
        self.image = self.image.convert('L')
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.ShowImage(image_path)
    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.ShowImage(image_path)
    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.ShowImage(image_path)
    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.ShowImage(image_path)
    def do_sharp(self):
        self.image = self.image.filter(SHARPEN)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.ShowImage(image_path)
def ShowChosenImage():
    if list_files.currentRow()>=0:
        filename = list_files.currentItem().text()
        workimage.LoadImage(workdir, filename)
        image_path = os.path.join(workdir, filename)
        workimage.ShowImage(image_path)
def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()
def filter(files, extensions):
    result = []
    for filename in files:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
    return result
def showfilenameList():
    extensions =['.jpg','.jpeg','.bmp','.png','.gif']
    chooseWorkdir()
    filenames = filter(os.listdir(workdir), extensions)
    list_files.clear()
    for filename in filenames:
        list_files.addItem(filename)
#Настройки окна
app = QApplication([])
win = QWidget()
win.resize(800, 500)
win.setWindowTitle('Демо версия Photoshop')
#Создание объектов
lb_image = QLabel('Место для картинки (-_-)')
button_dir = QPushButton('Папка')
list_files = QListWidget()
#Кнопки для работы с картинкой
button_left = QPushButton('Вертать влево')
button_right = QPushButton('Вертать вправо')
button_flip = QPushButton('Отзеркалить')
button_bw = QPushButton('Ч/Б')
button_sharp = QPushButton('Резкость')
#Шампуры
row1 = QHBoxLayout()
row2 = QHBoxLayout()
col1 = QVBoxLayout()
col2 = QVBoxLayout()
#Готовка шашлыка
col1.addWidget(button_dir)
col1.addWidget(list_files)
row2.addWidget(button_left)
row2.addWidget(button_right)
row2.addWidget(button_flip)
row2.addWidget(button_sharp)
row2.addWidget(button_bw)
col2.addWidget(lb_image, 95)
col2.addLayout(row2)
row1.addLayout(col1, 20)
row1.addLayout(col2, 80)
win.setLayout(row1)
#Пустая переменная
workdir = ''
workimage = ImageProcessor()

button_dir.clicked.connect(showfilenameList)
list_files.currentRowChanged.connect(ShowChosenImage)
button_bw.clicked.connect(workimage.do_bw)
button_left.clicked.connect(workimage.do_left)
button_right.clicked.connect(workimage.do_right)
button_flip.clicked.connect(workimage.do_flip)
button_sharp.clicked.connect(workimage.do_sharp)
win.show()
app.exec_()