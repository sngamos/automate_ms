import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets

class SnippingTool(QtWidgets.QWidget):
    def __init__(self):
        super(SnippingTool, self).__init__()
        self.setWindowTitle("Snipping Tool")
        # Make the window frameless, full screen and always on top
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | 
                            QtCore.Qt.FramelessWindowHint | 
                            QtCore.Qt.Tool)
        self.setWindowState(QtCore.Qt.WindowFullScreen)
        
        # Variables to store the selection start and end points.
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        
        # Capture the full screen pixmap.
        screen = QtWidgets.QApplication.primaryScreen()
        self.fullScreenPixmap = screen.grabWindow(0)
        
        # Set a cross cursor for better visual feedback.
        self.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.show()

    def paintEvent(self, event):
        """Draw the full-screen screenshot and, if available, the selection rectangle."""
        painter = QtGui.QPainter(self)
        # Draw the screenshot as the background.
        painter.drawPixmap(0, 0, self.fullScreenPixmap)
        
        if not self.begin.isNull() and not self.end.isNull():
            rect = QtCore.QRect(self.begin, self.end)
            # Draw a translucent red rectangle to show selection.
            painter.setPen(QtGui.QPen(QtGui.QColor(255, 0, 0), 2))
            painter.setBrush(QtGui.QColor(255, 0, 0, 100))
            painter.drawRect(rect)

    def mousePressEvent(self, event):
        """Record the starting point of the selection."""
        self.begin = event.pos()
        self.end = self.begin
        self.update()

    def mouseMoveEvent(self, event):
        """Update the current endpoint as the user drags the mouse."""
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        """When the user releases the mouse, finalize the selection and capture."""
        self.end = event.pos()
        self.update()
        QtWidgets.QApplication.processEvents()
        self.capture()

    def capture(self):
        """Crop the selected area from the screenshot and save it to .tmp_cv folder."""
        x1 = min(self.begin.x(), self.end.x())
        y1 = min(self.begin.y(), self.end.y())
        x2 = max(self.begin.x(), self.end.x())
        y2 = max(self.begin.y(), self.end.y())
        rect = QtCore.QRect(x1, y1, x2 - x1, y2 - y1)
        
        # If the user did not select a valid area, close the tool.
        if rect.width() == 0 or rect.height() == 0:
            self.close()
            return

        # Crop the full-screen pixmap with the selected rectangle.
        cropped = self.fullScreenPixmap.copy(rect)
        
        # Ensure the temporary folder exists.
        folder = os.path.join(os.getcwd(), ".tmp_cv")
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        # Save the cropped image. Here we use a fixed file name "snip.png",
        # but you might generate a unique name (for example, using a timestamp).
        filename = os.path.join(folder, "snip.png")
        cropped.save(filename, "PNG")
        print(f"Saved snip to: {filename}")
        
        self.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    tool = SnippingTool()
    sys.exit(app.exec_())
