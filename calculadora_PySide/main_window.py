from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget,QMessageBox
class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget | None = None, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)
       
        # Configurando o layout básico
        self.central_widget = QWidget()
        self.vLayout = QVBoxLayout()
        self.central_widget.setLayout(self.vLayout)
        self.setCentralWidget(self.central_widget)
        # self.central_widget.setStyleSheet('color:white;')
       
        # Título da janela
        self.setWindowTitle('Calculadora do brabo')
   
    def adjustFixedSize(self):
        # Última coisa a ser feita
        self.adjustSize()
        self.setFixedSize(self.width(), self.height())

    def addWidgetToVLayout(self, widget: QWidget):
        self.vLayout.addWidget(widget)      

    def makeMsgBox(self):
        return QMessageBox(self)