from PyQt4.QtCore import *
from PyQt4.QtGui import *

class ImageViewerWidget(QGraphicsView):
  def __init__(self, type, parent = None):
    super(ImageViewerWidget, self).__init__(parent)
    
    self.lastClick = None
    
    self.setCursor(Qt.OpenHandCursor)
    self.setCenter(QPointF(0, 0))
    self.setMouseTracking(True)

  def setCenter(self, centerPoint):
    visibleArea = self.mapToScene(self.rect()).boundingRect()
    sceneBounds = self.sceneRect()
   
    boundX = visibleArea.width() / 2.0
    boundY = visibleArea.height() / 2.0
    boundWidth = sceneBounds.width() - 2.0 * boundX
    boundHeight = sceneBounds.height() - 2.0 * boundY
   
    bounds = QRectF(boundX, boundY, boundWidth, boundHeight)
   
    if bounds.contains(centerPoint):
      self.currentCenter = centerPoint
    else:
      if visibleArea.contains(sceneBounds):
        self.currentCenter = sceneBounds.center()
      else:
        self.currentCenter = centerPoint
   
        if centerPoint.x() > bounds.x() + bounds.width():
          self.currentCenter.setX(bounds.x() + bounds.width())
        elif centerPoint.x() < bounds.x():
          self.currentCenter.setX(bounds.x())
   
        if centerPoint.y() > bounds.y() + bounds.height():
          self.currentCenter.setY(bounds.y() + bounds.height())
        elif centerPoint.y() < bounds.y():
          self.currentCenter.setY(bounds.y())
   
    self.centerOn(self.currentCenter)
  
  def wheelEvent(self, event):
    pointBeforeScale = QPointF(self.mapToScene(event.pos()))
    screenCenter = self.currentCenter
    scaleFactor = 1.10
    
    if event.delta() > 0:
      self.scale(scaleFactor, scaleFactor)
    else:
      self.scale(1.0 / scaleFactor, 1.0 / scaleFactor)
   
    pointAfterScale = self.mapToScene(event.pos())
    offset = pointBeforeScale - pointAfterScale
    newCenter = screenCenter + offset
    
    self.setCenter(newCenter)
  
  def pointWheelEvent(self, point):
    pointBeforeScale = QPointF(self.mapToScene(point))
    screenCenter = self.currentCenter
    scaleFactor = 1.10
    
    pointAfterScale = self.mapToScene(point)
    offset = pointBeforeScale - pointAfterScale
    newCenter = screenCenter + offset
    
    self.setCenter(newCenter)
  
  def mousePressEvent(self, event):
    self.lastClick = event.pos()
    self.setCursor(Qt.ClosedHandCursor)
  
  def mouseReleaseEvent(self, event):
    self.setCursor(Qt.OpenHandCursor)
    self.lastClick = None
  
  def mouseMoveEvent(self, event):
    if self.lastClick != None:
      delta = QPointF(self.mapToScene(self.lastClick) - self.mapToScene(event.pos()))
      self.lastClick = event.pos()

      self.setCenter(self.currentCenter + delta)

  
  def resizeEvent(self, event):
    self.setCenter(self.mapToScene(self.rect()).boundingRect().center())
