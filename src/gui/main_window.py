"""Main application window"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QLabel, QScrollArea
)
from PyQt6.QtCore import Qt

from ..core.block_manager import BlockManager
from .canvas import Canvas
from .block_palette import BlockPalette


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Block Simulator - Visual Programming Interface")
        self.setGeometry(100, 100, 1200, 800)
        
        # Initialize block manager
        self.block_manager = BlockManager()
        
        # Create main widget
        main_widget = QWidget()
        main_layout = QHBoxLayout()
        
        # Left panel: Block palette
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        self.palette = BlockPalette(self.block_manager)
        left_layout.addWidget(self.palette)
        
        # Clear button
        clear_btn = QPushButton("Clear All")
        clear_btn.clicked.connect(self._clear_all_blocks)
        left_layout.addWidget(clear_btn)
        
        left_layout.addStretch()
        left_panel.setLayout(left_layout)
        
        # Center: Canvas
        self.canvas = Canvas(self.block_manager)
        self.canvas.block_selected.connect(self._on_block_selected)
        self.canvas.block_added.connect(self._on_block_added)
        self.canvas.block_removed.connect(self._on_block_removed)
        
        # Right panel: Properties (will be added when block is selected)
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        right_layout.addWidget(QLabel("Properties"))
        self.properties_label = QLabel("Select a block to edit properties")
        self.properties_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.properties_label.setWordWrap(True)
        right_layout.addWidget(self.properties_label)
        right_layout.addStretch()
        right_panel.setLayout(right_layout)
        right_panel.setMaximumWidth(250)
        right_panel.setMinimumWidth(200)
        
        # Add panels to main layout
        main_layout.addWidget(left_panel, 0)
        main_layout.addWidget(self.canvas, 1)
        main_layout.addWidget(right_panel, 0)
        
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        
        # Status bar
        self.statusBar().showMessage("Ready")
    
    def _on_block_selected(self, block_id: str):
        """Handle block selection"""
        if block_id:
            block = self.block_manager.get_block(block_id)
            if block:
                text = f"<b>Block: {block.block_type}</b><br>"
                text += f"<b>ID:</b> {block.block_id}<br><br>"
                text += "<b>Position:</b><br>"
                text += f"X: {int(block.x)}, Y: {int(block.y)}<br><br>"
                text += "<b>Properties:</b><br>"
                for key, value in block.properties.items():
                    text += f"{key}: {value}<br>"
                self.properties_label.setText(text)
                self.statusBar().showMessage(f"Selected: {block.block_type} ({block_id})")
        else:
            self.properties_label.setText("Select a block to edit properties")
            self.statusBar().showMessage("Ready")
    
    def _on_block_added(self, block_id: str):
        """Handle block addition"""
        self.statusBar().showMessage(f"Block added: {block_id}")
    
    def _on_block_removed(self, block_id: str):
        """Handle block removal"""
        self.statusBar().showMessage(f"Block removed: {block_id}")
    
    def _clear_all_blocks(self):
        """Clear all blocks"""
        self.block_manager.blocks.clear()
        self.canvas.selected_block = None
        self.canvas.update()
        self.properties_label.setText("Select a block to edit properties")
        self.statusBar().showMessage("All blocks cleared")
