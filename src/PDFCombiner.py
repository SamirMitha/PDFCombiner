# Authors:
# Programming: Samir Mitha
# UI Design: Jayra Almanzor

import sys, os
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QListWidgetItem, QPushButton, QDialog, QMessageBox, QLabel, QFileDialog
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtCore import Qt, QUrl
from PyPDF2 import PdfFileMerger

hard_links = []

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class ListboxWidget(QListWidget):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setAcceptDrops(True)
		self.setGeometry(10, 10, 880, 290)
		self.setViewMode(QListWidget.IconMode)
		self.setStyleSheet(
				"""
				QListWidget{
				background: #545a63;
				color: white;
				border-radius: 15px;
				border-bottom-left-radius: 0px;
				border-bottom-right-radius: 0px;
				}
				"""
			)

	# drag and drop functions
	def dragEnterEvent(self, event):
		if event.mimeData().hasUrls:
			event.accept()
		else:
			event.ignore()

	def dragMoveEvent(self, event):
		if event.mimeData().hasUrls:
			event.setDropAction(Qt.CopyAction)
			event.accept()
		else:
			event.ignore()

	def dropEvent(self, event):
		if event.mimeData().hasUrls():
			event.setDropAction(Qt.CopyAction)
			event.accept()

			links = []

			for url in event.mimeData().urls():
				if url.isLocalFile():
					if str(url.toLocalFile()).endswith('.pdf'):
						links.append(str(url.toLocalFile()))
						base = os.path.basename(str(url.toLocalFile()))
						QListWidgetItem(QIcon(resource_path('pdf.png')), base, self)
			hard_links.extend(links)
			# print(hard_links)
		else:
			event.ignore()

class CustomDialog(QMessageBox):
	def __init__(self):
		super().__init__()

		self.about(self, "Error", "File queue is empty.")

class AppDemo(QMainWindow):
	def __init__(self):
		super().__init__()
		self.setWindowIcon(QIcon(resource_path('PDF Combiner Logo.png')))
		self.setWindowTitle("PDF Combiner")
		self.resize(900,420)
		self.setStyleSheet(
				"""
				QMainWindow{
				background: #34383d;
				}
				"""
			)

		self.lstbox_view = ListboxWidget(self)

		self.instrLabel = QLabel(self)

		self.plusimg = QLabel(self)

		# label creation
		self.instrLabel.setText("Add files by using the Add Files button or drag and drop files into the box above.")
		self.instrLabel.setGeometry(10, 300, 880, 30)
		self.instrLabel.setAlignment(Qt.AlignCenter)
		self.instrLabel.setStyleSheet(
				"""
				QLabel{
				background: #34383d;
				color: white;
				border: 1px dashed gray;
				border-radius: 15px;
				border-top-left-radius: 0px;
				border-top-right-radius: 0px;
				}
				"""
			)

		# plus image creation
		self.pixmap = QPixmap(resource_path('watta.png'))
		self.plusimg.setPixmap(self.pixmap)
		self.plusimg.setGeometry(418, 100, 100, 100)

		# button creation
		self.btnCombine = QPushButton('Combine', self)
		self.btnCombine.setGeometry(350, 350, 200, 50)
		self.btnClear = QPushButton('Clear', self)
		self.btnClear.setGeometry(600, 350, 200, 50)
		self.btnAdd = QPushButton('Add Files', self)
		self.btnAdd.setGeometry(100, 350, 200, 50)

		# button colours
		self.btnCombine.setStyleSheet(
				"""
				QPushButton{
				background-color: #5cb57e;
				color: white;
				border-radius: 15px;
				}
				QPushButton:hover{
				background-color: #87cca1;
				color: white;
				border-radius: 15px;
				}
				QPushButton:pressed{
				background-color: #72ad89;
				color: white;
				border-radius: 15px;
				}
				"""
			)
		self.btnCombine.setFont(QFont('Arial', 12))

		self.btnClear.setStyleSheet(
				"""
				QPushButton{
				background-color: #f55d42;
				color: white;
				border-radius: 15px;
				}
				QPushButton:hover{
				background-color: #f0826e;
				color: white;
				border-radius: 15px;
				}
				QPushButton:pressed{
				background-color: #c96d5d;
				color: white;
				border-radius: 15px;
				}
				"""
			)
		self.btnClear.setFont(QFont('Arial', 12))

		self.btnAdd.setStyleSheet(
				"""
				QPushButton{
				background-color: #4298f5;
				color: white;
				border-radius: 15px;
				}
				QPushButton:hover{
				background-color: #78b1f0;
				color: white;
				border-radius: 15px;
				}
				QPushButton:pressed{
				background-color: #6495cc;
				color: white;
				border-radius: 15px;
				}
				"""
			)
		self.btnAdd.setFont(QFont('Arial', 12))

		# button actions
		self.btnCombine.clicked.connect(lambda: print(self.combinePDF()))
		self.btnClear.clicked.connect(lambda: {self.lstbox_view.clear(), hard_links.clear(), self.plusimg.show()})
		self.btnAdd.clicked.connect(lambda: self.getDirectory())

	def combinePDF(self):
		items = []
		filter = "PDF (*.pdf)"
		for x in hard_links:
		    items.append(x)
		if not items:
			dlg = CustomDialog()
		else:
			merger = PdfFileMerger()
			for pdf in items:
				merger.append(pdf)
			save_dlg = QFileDialog()
			save_dlg.setFileMode(QFileDialog.AnyFile)
			save_name = save_dlg.getSaveFileName(self, "Save file", "merged.pdf", filter)
			print(save_name)
			merger.write(save_name[0])
			merger.close()

	def getDirectory(self):
		filter = "PDF (*.pdf)"
		files = QFileDialog()
		files.setFileMode(QFileDialog.ExistingFiles)
		files_names = files.getOpenFileNames(self, "Open files", "", filter)
		files_names = files_names[0]
		for file in files_names:
			base = os.path.basename(file)
			QListWidgetItem(QIcon(resource_path('pdf.png')), base, self.lstbox_view)
			self.plusimg.hide()
		hard_links.extend(files_names)
		# print(hard_links)

app = QApplication(sys.argv)

demo = AppDemo()
demo.show()

sys.exit(app.exec())