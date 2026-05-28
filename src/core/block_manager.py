"""Block manager - manages all block instances"""

import json
from typing import List, Dict, Any, Optional
from pathlib import Path

from .block_instance import BlockInstance


class BlockManager:
    """Manages all block instances and the block library"""
    
    def __init__(self):
        self.blocks: List[BlockInstance] = []
        self.library: Dict[str, Any] = {}
        self._load_library()
    
    def _load_library(self, library_path: Optional[Path] = None):
        """Load block library from JSON"""
        if library_path is None:
            from ..utils.config import BLOCKS_LIBRARY_PATH
            library_path = BLOCKS_LIBRARY_PATH
        
        if library_path.exists():
            with open(library_path, 'r') as f:
                self.library = json.load(f)
        else:
            # Default empty library
            self.library = {"blocks": []}
    
    def get_block_definition(self, block_type: str) -> Optional[Dict[str, Any]]:
        """Get block definition from library"""
        for block_def in self.library.get("blocks", []):
            if block_def.get("name") == block_type:
                return block_def
        return None
    
    def add_block(self, block_type: str, x: float = 0, y: float = 0) -> BlockInstance:
        """Add a new block instance"""
        definition = self.get_block_definition(block_type)
        if not definition:
            raise ValueError(f"Block type '{block_type}' not found in library")
        
        # Initialize properties with defaults
        properties = {}
        for param in definition.get("parameters", []):
            properties[param["name"]] = param.get("default", "")
        
        block = BlockInstance(
            block_type=block_type,
            x=x,
            y=y,
            properties=properties,
        )
        self.blocks.append(block)
        return block
    
    def remove_block(self, block_id: str) -> bool:
        """Remove a block by ID"""
        for i, block in enumerate(self.blocks):
            if block.block_id == block_id:
                self.blocks.pop(i)
                return True
        return False
    
    def get_block(self, block_id: str) -> Optional[BlockInstance]:
        """Get a block by ID"""
        for block in self.blocks:
            if block.block_id == block_id:
                return block
        return None
    
    def update_block_position(self, block_id: str, x: float, y: float):
        """Update block position"""
        block = self.get_block(block_id)
        if block:
            block.x = x
            block.y = y
    
    def update_block_property(self, block_id: str, property_name: str, value: Any):
        """Update a block property"""
        block = self.get_block(block_id)
        if block:
            block.properties[property_name] = value
    
    def get_all_blocks(self) -> List[BlockInstance]:
        """Get all block instances"""
        return self.blocks.copy()
    
    def get_library_blocks(self) -> List[str]:
        """Get list of available block types"""
        return [block["name"] for block in self.library.get("blocks", [])]
    
    def save_project(self, path: Path):
        """Save project to file"""
        project_data = {
            "blocks": [block.to_dict() for block in self.blocks]
        }
        with open(path, 'w') as f:
            json.dump(project_data, f, indent=2)
    
    def load_project(self, path: Path):
        """Load project from file"""
        if path.exists():
            with open(path, 'r') as f:
                project_data = json.load(f)
            self.blocks = [BlockInstance.from_dict(b) for b in project_data.get("blocks", [])]
