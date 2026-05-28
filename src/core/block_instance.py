"""Block instance class - represents a single instantiated block"""

from dataclasses import dataclass, field
from typing import Any, Dict
import uuid


@dataclass
class BlockInstance:
    """Represents a single instantiated block in the canvas"""
    
    block_type: str  # Type of block (e.g., "InputBlock", "ProcessorBlock")
    block_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    x: float = 0.0
    y: float = 0.0
    properties: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Initialize properties with defaults from block definition"""
        pass
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert block instance to dictionary"""
        return {
            "id": self.block_id,
            "type": self.block_type,
            "position": {"x": self.x, "y": self.y},
            "properties": self.properties,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BlockInstance":
        """Create block instance from dictionary"""
        return cls(
            block_type=data["type"],
            block_id=data.get("id", str(uuid.uuid4())[:8]),
            x=data.get("position", {}).get("x", 0),
            y=data.get("position", {}).get("y", 0),
            properties=data.get("properties", {}),
        )
