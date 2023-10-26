import math

from PySide6.QtWidgets import QPushButton,QGridLayout
from PySide6.QtCore import Slot
from variaveis import MEDIO_FONT_SIZE
from utils import isNumOrDot, isEmpty, isValidNumber, convertToNumber


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main_window import MainWindow
    from  display import Display
    from info import Info
class My_Button(QPushButton):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.config_style_button()

    def config_style_button(self):
        # define a fonte do botao
        font = self.font()
        font.setPixelSize(MEDIO_FONT_SIZE)
        self.setFont(font)

        # define a altura e largura minima
        self.setMinimumSize(75,75)

        


class Button_Grid(QGridLayout):
    def __init__(self,display:'Display', info:'Info',window: 'MainWindow',*args,
                  **kwargs
                 ) -> None:
        super().__init__(*args, **kwargs)

        self._gridMask = [
            ['C', 'D', '^', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['N',  '0', '.', '='],
        ]
        
        self.display = display
        self.info = info
        self.window = window
        self._equation = ''
        self._equationInitialValue = 'Sua conta'
        self._right = None
        self._left = None
        self._op = None
        
        
        self._equation = self._equationInitialValue
        self._makeGrid()

    @property
    def equation(self):
        return self._equation
    
    @equation.setter
    def equation(self,valor):
        self._equation = valor
        self.info.setText(valor)

    

    def _makeGrid(self):
        self.display.eqPressed.connect(self._eq)
        self.display.delPressed.connect(self._backspace)
        self.display.clearPressed.connect(self._clear)
        self.display.numPressed.connect(self._insertToDisplay)
        self.display.operatorPressed.connect(self._cofigLeftOp)
        
        for rowNumber, rowData in enumerate(self._gridMask):
            for colNumber, buttonText in enumerate(rowData):
                button = My_Button(buttonText)

                if buttonText not in '0123456789.':
                    button.setStyleSheet("background-color: #3498db;color:blue")

                self.addWidget(button, rowNumber, colNumber)
                 # Adiciona o botão à interface gráfica na posição da grade
                
                
                slot = self._makeSlot(self._insertToDisplay,buttonText)
                # Cria um "slot" para lidar com o clique do botão
                # um metodo que é associado a um sinal para emitir a comunicação
                # entre objetos por meio de eventos(nesse caso clicks)
                self._connectButtonClicked(button,slot)
                self._configSpecialButton(button)

    def _connectButtonClicked(self, button, slot):
        button.clicked.connect(slot)  # type: ignore

    
    def _configSpecialButton(self, button):
        text = button.text()
        if text == 'C':
            self._connectButtonClicked(button, self._clear)
        if text == 'D':
            self._connectButtonClicked(button, self.display.backspace)
        if text == 'N':
            self._connectButtonClicked(button,self._ivertNumber)
        
        if text in '+-/*^':
            self._connectButtonClicked(
                button,
                self._makeSlot(self._cofigLeftOp, text)
            )
        if text == '=':
            self._connectButtonClicked(button, self._eq)
    
    def _makeSlot(self, func, *args, **kwargs):
        @ Slot(bool)
        def realSlot(_):
            func(*args, **kwargs)
        return realSlot

    @Slot()
    def _ivertNumber(self):
        displayText = self.display.text()


        if not isValidNumber(displayText):
            self._showError('Você não digitou nada.')
            return
        
        number = convertToNumber(displayText) *-1

        self.display.setText(str(number))


    @Slot()
    def _insertToDisplay(self, text):
        newDisplayValue = self.display.text() + text
        if not isValidNumber(newDisplayValue):
            return
        self.display.insert(text)
        self.display.setFocus()

    @Slot()
    def _clear(self):
        self._left = None
        self._right = None
        self._op = None
        self.equation = self._equationInitialValue
        self.display.clear()
        self.display.setFocus()

    @Slot()
    def _cofigLeftOp(self, text):
         # +-/* (etc...)
        displayText = self.display.text()  # Deverá ser meu número _left
        self.display.clear()  # Limpa o display
        self.display.setFocus()
        # Se a pessoa clicou no operador sem
        # configurar qualquer número
        if not isValidNumber(displayText) and self._left is None:
            print('Não tem nada para colocar no valor da esquerda')
            self._showError('Você não digitou nada.')
            return

        # Se houver algo no número da esquerda,
        # não fazemos nada. Aguardaremos o número da direita.
        if self._left is None:
            self._left = convertToNumber(displayText)
        self._op = text
        self.equation = f'{self._left} {self._op} ??'

    @Slot()
    def _eq(self):
        displayText = self.display.text()


        if (not isValidNumber(displayText) or self._op is None or
        self._left is None):
            print('Conta incompleta')
            self._showError('Conta incompleta, você deve adicionar uma equação'
              ' completa.Exemplo 5 + 5 =')
            return


        self._right = convertToNumber(displayText)
        self.equation = f'{self._left} {self._op} {self._right}'
        result = 'error'
        try:
            if '^' in self.equation and isinstance(self._left, int | float):
                result = math.pow(self._left, self._right)
                result = convertToNumber(str(result))
            else:
                result = eval(self.equation)
        except ZeroDivisionError:
            print('Zero Division Error')
            self._showError('Divisão por zero.')
        except OverflowError:
            print('Número muito grande')
            self._showError('Essa conta não pode ser realizada.')

        self.display.clear()
        self.info.setText(f'{self.equation} = {result}')
        self._left = result
        self._right = None
        self.display.setFocus()

        if result == 'error':
            self._left = None

    @Slot()
    def _backspace(self):
        self.display.backspace()
        self.display.setFocus()

    def _makeDialog(self, text):
        msgBox = self.window.makeMsgBox()
        msgBox.setText(text)
        return msgBox

    def _showError(self, text):
        msgBox = self._makeDialog(text)
        msgBox.setIcon(msgBox.Icon.Critical)
        msgBox.exec()
        self.display.setFocus()
        
    def _showInfo(self, text):
        msgBox = self._makeDialog(text)
        msgBox.setIcon(msgBox.Icon.Information)
        msgBox.exec()
        self.display.setFocus()