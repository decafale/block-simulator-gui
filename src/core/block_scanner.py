"""Block scanner - discovers and extracts block class definitions"""

import os
import sys
import inspect
import json
from pathlib import Path
from typing import List, Dict, Any, Tuple
from importlib.util import spec_from_file_location, module_from_spec


class BlockScanner:
    """Scans Python files and extracts block class definitions"""
    
    def __init__(self):
        self.blocks_found: List[Dict[str, Any]] = []
    
    def scan_directory(self, root_path: str) -> List[Dict[str, Any]]:
        """Recursively scan directory for block classes"""
        self.blocks_found = []
        root_path = Path(root_path)
        
        if not root_path.exists():
            print(f"Error: Path does not exist: {root_path}")
            return []
        
        print(f"Scanning directory: {root_path}")
        
        for py_file in root_path.rglob("*.py"):
            # Skip __pycache__ and __init__ files
            if "__pycache__" in str(py_file) or py_file.name.startswith("__"):
                continue
            
            print(f"  Scanning: {py_file}")
            blocks = self._extract_blocks_from_file(str(py_file), root_path)
            self.blocks_found.extend(blocks)
        
        print(f"Found {len(self.blocks_found)} blocks")
        return self.blocks_found
    
    def _extract_blocks_from_file(self, file_path: str, root_path: Path) -> List[Dict[str, Any]]:
        """Extract block classes from a Python file"""
        blocks = []
        
        try:
            # Load module from file
            spec = spec_from_file_location("module", file_path)
            if spec is None or spec.loader is None:
                return blocks
            
            module = module_from_spec(spec)
            sys.modules["module"] = module
            spec.loader.exec_module(module)
            
            # Find all classes with run_routine method
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if hasattr(obj, 'run_routine') and callable(getattr(obj, 'run_routine')):
                    # Extract block info
                    block_info = self._extract_class_info(name, obj, file_path, root_path)
                    if block_info:
                        blocks.append(block_info)
        
        except Exception as e:
            print(f"    Error scanning {file_path}: {e}")
        
        return blocks
    
    def _extract_class_info(self, class_name: str, cls: type, file_path: str, root_path: Path) -> Dict[str, Any]:
        """Extract information from a block class"""
        
        try:
            # Get module path
            file_path_obj = Path(file_path)
            relative_path = file_path_obj.relative_to(root_path)
            module_parts = relative_path.with_suffix('').parts
            module_path = ".".join(module_parts)
            
            # Get __init__ signature
            sig = inspect.signature(cls.__init__)
            
            # Extract parameters (skip 'self')
            parameters = []
            for param_name, param in sig.parameters.items():
                if param_name == 'self':
                    continue
                
                param_info = {
                    "name": param_name,
                    "required": param.default == inspect.Parameter.empty,
                    "default": None if param.default == inspect.Parameter.empty else param.default,
                }
                
                parameters.append(param_info)
            
            # Get docstring
            docstring = inspect.getdoc(cls) or f"Block: {class_name}"
            
            block_info = {
                "name": class_name,
                "module_path": module_path,
                "class_name": class_name,
                "file_path": str(file_path_obj),
                "description": docstring.split('\n')[0],  # First line of docstring
                "parameters": parameters,
                "has_run_routine": True,
            }
            
            print(f"      Found block: {class_name} with {len(parameters)} parameters")
            return block_info
        
        except Exception as e:
            print(f"      Error extracting info from {class_name}: {e}")
            return None
    
    def generate_library_json(self, blocks: List[Dict[str, Any]], output_path: str):
        """Generate blocks_library.json"""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        library = {
            "blocks": blocks,
            "metadata": {
                "total_blocks": len(blocks),
                "format_version": "1.0"
            }
        }
        
        with open(output_path, 'w') as f:
            json.dump(library, f, indent=2)
        
        print(f"Library saved to: {output_path}")
        return output_path


def main():
    """Main entry point for block scanner"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Scan Python files and generate block library")
    parser.add_argument("scan_path", help="Path to scan for block classes")
    parser.add_argument("-o", "--output", default="data/blocks_library.json", 
                        help="Output JSON file path")
    
    args = parser.parse_args()
    
    scanner = BlockScanner()
    blocks = scanner.scan_directory(args.scan_path)
    scanner.generate_library_json(blocks, args.output)
    
    print(f"\nGenerated library with {len(blocks)} blocks")


if __name__ == "__main__":
    main()
