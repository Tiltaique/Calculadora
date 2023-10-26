from PySide6.QtCore import Qt, Signal
import PySide6.QtGui
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QLineEdit
from variaveis import BIG_FONT_SIZE, MEDIO_FONT_SIZE, TEXT_MARGIM,LARGURA_MINIMA
from utils import isEmpty, isNumOrDot


class Display(QLineEdit):
    eqPressed = Signal()# cria um signal
    delPressed = Signal()
    clearPressed = Signal()
    numPressed = Signal(str)
    operatorPressed = Signal(str)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configStyle()

    def configStyle(self):
       
        margins = [TEXT_MARGIM for _ in range(4)]
        # configura a fonte
        self.setStyleSheet(f'font-size: {BIG_FONT_SIZE}px;')
        
        # configura a altura
        self.setMinimumHeight(BIG_FONT_SIZE * 2)

        # configura a largura
        self.setMinimumWidth(LARGURA_MINIMA)

        # configura para digitar da direita pra esquerda
        self.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        # configura a distancia da margem
        self.setTextMargins(*margins)

        self.setPlaceholderText('Digite algo')

    def keyPressEvent(self, event: QKeyEvent) -> None:
        keyText = event.text().strip()#apaga os espaços das laterais
        key = event.key()
        KEYS = Qt.Key   

        isEnter =  key in [KEYS.Key_Enter,KEYS.Key_Return, KEYS.Key_Equal]
        isDelete =  key in [KEYS.Key_Backspace,KEYS.Key_Delete, KEYS.Key_D]
        isEsc =  key in [KEYS.Key_Escape,KEYS.Key_C]
        isOperator = key in [KEYS.Key_Plus, KEYS.Key_Minus, KEYS.Key_Slash,
                             KEYS.Key_Asterisk, KEYS.Key_P
                             ]

        if isEnter:
            self.eqPressed.emit()#emite o signal paa o buttongrid
            return event.ignore()#ignora o signal no display
        
        if isDelete:
            self.delPressed.emit()#emite o signal para o button grid
            return event.ignore()#ignora o signal no display
       
        if isEsc:
            self.clearPressed.emit()#emite o signal para o buttongrid
            return event.ignore()#ignora o signal no display
        
       
        if isOperator:
            if keyText.lower() == 'p':
                keyText = '^'
            self.operatorPressed.emit(keyText)#emite o signal para o buttongrid
            return event.ignore()#ignora o signal no display
        
        
        # não passar daqui se não tiver texto
        if isEmpty(keyText):
            return event.ignore()



        if isNumOrDot(keyText): 
            self.numPressed.emit(keyText)#emite o signal para o buttongrid
            return event.ignore()#ignora o signal no display
            

