import sys
from PyQt5 import QtCore, QtWidgets
from pymem import Pymem
from pymem.process import module_from_name


class TyPos(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.mem = Pymem("Ty.exe")
        self.module = module_from_name(self.mem.process_handle, "Ty.exe").lpBaseOfDll
        self.x_address = self.module + 0x270B78
        self.y_address = self.module + 0x270B7C
        self.z_address = self.module + 0x270B80
        self.r1_address = self.module + 0x271C20

        self.initUI()

    def initUI(self):
        self.setWindowTitle('TyPos')
        self.setGeometry(860, 190, 100, 69)
        self.label = QtWidgets.QLabel(self)
        self.update_values()
        self.activateWindow()
        self.raise_()
        self.setWindowFlags(
            QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.WindowCloseButtonHint)

        self.setVisible(True)

    def update_values(self):
        x = round(self.mem.read_float(self.x_address), 2)
        y = round(self.mem.read_float(self.y_address), 2)
        z = round(self.mem.read_float(self.z_address), 2)
        r = round(self.mem.read_float(self.r1_address), 5)

        if QtWidgets.QApplication.keyboardModifiers() == QtCore.Qt.ShiftModifier and QtWidgets.QApplication.keyboardModifiers() != QtCore.Qt.NoModifier:
            QtWidgets.QApplication.clipboard().setText(f"{x}\n{y}\n{z}\n{r}")
            self.label.setText("Copied!")
        else:
            self.label.setText(f"X:  {x}\nY:  {y}\nZ:  {z}\n\nRotation:  {r}")
        QtCore.QTimer.singleShot(10, self.update_values)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    typos = TyPos()
    typos.show()
    typos.raise_()
    sys.exit(app.exec_())
