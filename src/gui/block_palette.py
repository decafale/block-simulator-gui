"""Block palette widget - list of available blocks"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem
from PyQt6.QtGui import QDrag, QMimeData
from PyQt6.QtCore import Qt, QMimeData

from ..core.block_manager import BlockManager


class BlockPalette(QWidget):
    """Sidebar showing available blocks from library"""
    
    def __init__(self, block_manager: BlockManager, parent=None):
        super().__init__(parent)
        self.block_manager = block_manager
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Available Blocks")
        title.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(title)
        
        # Block list
        self.block_list = QListWidget()
        self.block_list.itemPressed.connect(self._on_item_pressed)
        self.block_list.setDragDropMode(self.block_list.DragDropMode.DragOnly)
        
        # Populate list
        for block_type in self.block_manager.get_library_blocks():
            item = QListWidgetItem(block_type)
            item.setData(Qt.ItemDataRole.UserRole, block_type)
            self.block_list.addItem(item)
        
        layout.addWidget(self.block_list)
        self.setLayout(layout)
        self.setMaximumWidth(200)
        self.setMinimumWidth(180)
    
    def _on_item_pressed(self, item: QListWidgetItem):
        """Handle item pressed - start drag"""
        block_type = item.text()
        
        # Create drag
        drag = QDrag(self)
        mime_data = QMimeData()
        mime_data.setText(block_type)
        drag.setMimeData(mime_data)
        
        # Start drag
        drag.exec(Qt.DropAction.CopyAction)
