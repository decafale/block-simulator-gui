"""Canvas widget - main drawing area for blocks"""

from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor, QPen, QFont, QDrag
from PyQt6.QtCore import Qt, QRect, QPoint, QMimeData, pyqtSignal, QSize
from typing import Optional, Dict

from ..core.block_manager import BlockManager
from ..core.block_instance import BlockInstance
from ..utils.config import (
    GRID_SIZE, BLOCK_WIDTH, BLOCK_HEIGHT,
    CANVAS_BACKGROUND_COLOR, BLOCK_BACKGROUND_COLOR, BLOCK_TEXT_COLOR
)


class Canvas(QWidget):
    """Main canvas for drawing and interacting with blocks"""
    
    # Signals
    block_selected = pyqtSignal(str)  # block_id
    block_property_changed = pyqtSignal(str, str, object)  # block_id, property, value
    block_added = pyqtSignal(str)  # block_id
    block_removed = pyqtSignal(str)  # block_id
    
    def __init__(self, block_manager: BlockManager, parent=None):
        super().__init__(parent)
        self.block_manager = block_manager
        self.selected_block: Optional[str] = None
        self.dragging_block: Optional[str] = None
        self.drag_offset = QPoint(0, 0)
        self.block_rects: Dict[str, QRect] = {}  # Cache for block rectangles
        
        self.setAcceptDrops(True)
        self.setStyleSheet(f"background-color: {CANVAS_BACKGROUND_COLOR};")
        self.setMinimumSize(800, 600)
        self.setCursor(Qt.CursorShape.ArrowCursor)
    
    def paintEvent(self, event):
        """Draw canvas and blocks"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw grid
        self._draw_grid(painter)
        
        # Draw blocks
        self.block_rects.clear()
        for block in self.block_manager.get_all_blocks():
            self._draw_block(painter, block)
    
    def _draw_grid(self, painter: QPainter):
        """Draw background grid"""
        pen = QPen(QColor("#e0e0e0"))
        pen.setWidth(1)
        painter.setPen(pen)
        
        for x in range(0, self.width(), GRID_SIZE):
            painter.drawLine(x, 0, x, self.height())
        for y in range(0, self.height(), GRID_SIZE):
            painter.drawLine(0, y, self.width(), y)
    
    def _draw_block(self, painter: QPainter, block: BlockInstance):
        """Draw a single block"""
        x, y = int(block.x), int(block.y)
        rect = QRect(x, y, BLOCK_WIDTH, BLOCK_HEIGHT)
        self.block_rects[block.block_id] = rect
        
        # Draw block background
        is_selected = block.block_id == self.selected_block
        bg_color = QColor("#2980b9") if is_selected else QColor(BLOCK_BACKGROUND_COLOR)
        painter.fillRect(rect, bg_color)
        
        # Draw block border
        border_color = QColor("#ffffff") if is_selected else QColor("#2c3e50")
        border_width = 3 if is_selected else 2
        pen = QPen(border_color, border_width)
        painter.setPen(pen)
        painter.drawRect(rect)
        
        # Draw block label
        painter.setPen(QPen(QColor(BLOCK_TEXT_COLOR)))
        font = QFont()
        font.setPointSize(9)
        font.setBold(True)
        painter.setFont(font)
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, block.block_type)
        
        # Draw block ID (small text)
        font.setPointSize(7)
        font.setBold(False)
        painter.setFont(font)
        painter.setPen(QPen(QColor("#bdc3c7")))
        id_rect = QRect(x, y + BLOCK_HEIGHT - 15, BLOCK_WIDTH, 15)
        painter.drawText(id_rect, Qt.AlignmentFlag.AlignCenter, block.block_id)
    
    def mousePressEvent(self, event):
        """Handle mouse press"""
        if event.button() == Qt.MouseButton.LeftButton:
            # Check if clicking on a block
            block_id = self._get_block_at_position(event.pos())
            if block_id:
                self.selected_block = block_id
                self.dragging_block = block_id
                block = self.block_manager.get_block(block_id)
                self.drag_offset = event.pos() - QPoint(int(block.x), int(block.y))
                self.block_selected.emit(block_id)
            else:
                self.selected_block = None
                self.block_selected.emit("")
            
            self.update()
    
    def mouseMoveEvent(self, event):
        """Handle mouse move (dragging blocks)"""
        if self.dragging_block and event.buttons() == Qt.MouseButton.LeftButton:
            block = self.block_manager.get_block(self.dragging_block)
            new_x = event.pos().x() - self.drag_offset.x()
            new_y = event.pos().y() - self.drag_offset.y()
            
            # Snap to grid
            new_x = (new_x // GRID_SIZE) * GRID_SIZE
            new_y = (new_y // GRID_SIZE) * GRID_SIZE
            
            self.block_manager.update_block_position(self.dragging_block, new_x, new_y)
            self.update()
    
    def mouseReleaseEvent(self, event):
        """Handle mouse release"""
        self.dragging_block = None
    
    def dragEnterEvent(self, event):
        """Handle drag enter"""
        if event.mimeData().hasText():
            event.acceptProposedAction()
    
    def dropEvent(self, event):
        """Handle drop event - create new block"""
        if event.mimeData().hasText():
            block_type = event.mimeData().text()
            # Get position adjusted to grid
            x = (event.position().x() // GRID_SIZE) * GRID_SIZE
            y = (event.position().y() // GRID_SIZE) * GRID_SIZE
            
            try:
                block = self.block_manager.add_block(block_type, x, y)
                self.block_added.emit(block.block_id)
                self.update()
            except ValueError as e:
                print(f"Error adding block: {e}")
    
    def _get_block_at_position(self, pos: QPoint) -> Optional[str]:
        """Get block ID at given position"""
        for block_id, rect in self.block_rects.items():
            if rect.contains(pos):
                return block_id
        return None
    
    def sizeHint(self) -> QSize:
        """Suggest minimum size"""
        return QSize(800, 600)
