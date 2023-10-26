import sys

from display import Display
from info import Info
from main_window import MainWindow
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from buttons import My_Button,Button_Grid
from my_style import setup_theme
from variaveis import CAMINHO_ICONE
if __name__ == '__main__':
    # Cria a aplicação
    app = QApplication(sys.argv)
    setup_theme() #tema dark da calculadora 
    window = MainWindow()
   
    # Define o ícone
    icon = QIcon(str(CAMINHO_ICONE))
    window.setWindowIcon(icon)
    app.setWindowIcon(icon)
 
    if sys.platform.startswith('win'):
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
            u'CompanyName.ProductName.SubProduct.VersionInformation')

    # Info
    info = Info('Sua conta')
    window.addWidgetToVLayout(info)

    # Display
    display = Display()
    window.addWidgetToVLayout(display)
    
    # Grid
    my_grid = Button_Grid(display,info,window)
    window.vLayout.addLayout(my_grid) #a grade tambem é um layout
    # voce adiciona esse layout(a grade no caso) dentro do vLayout


    # Executa tudo
    window.adjustFixedSize()
    window.show()
    app.exec()