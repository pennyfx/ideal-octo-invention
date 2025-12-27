#!/usr/bin/env python3
"""
FreeCAD House Designer
A Python script that uses FreeCAD API to design a simple house with walls, roof, floor, doors, and windows.
"""

import sys
import os
import math

try:
    import FreeCAD
    import Part
except ImportError:
    print("Error: FreeCAD module not found.")
    print("This script requires FreeCAD to be installed.")
    print("Please install FreeCAD or run this script within FreeCAD environment.")
    sys.exit(1)


class HouseDesigner:
    """Main class for designing a house using FreeCAD API"""
    
    def __init__(self, doc_name="House"):
        """Initialize the house designer with a new FreeCAD document"""
        self.doc = FreeCAD.newDocument(doc_name)
        self.wall_thickness = 200  # mm
        self.wall_height = 3000  # mm
        self.house_width = 8000  # mm
        self.house_length = 10000  # mm
        self.door_width = 900  # mm
        self.door_height = 2100  # mm
        self.window_width = 1200  # mm
        self.window_height = 1500  # mm
        
    def create_floor(self):
        """Create the floor of the house"""
        print("Creating floor...")
        floor = Part.makeBox(
            self.house_length,
            self.house_width,
            100  # Floor thickness
        )
        floor_obj = self.doc.addObject("Part::Feature", "Floor")
        floor_obj.Shape = floor
        return floor_obj
    
    def create_wall(self, name, length, position, rotation=0):
        """Create a wall with specified dimensions and position"""
        print(f"Creating {name}...")
        wall = Part.makeBox(length, self.wall_thickness, self.wall_height)
        wall_obj = self.doc.addObject("Part::Feature", name)
        wall_obj.Shape = wall
        wall_obj.Placement.Base = FreeCAD.Vector(position[0], position[1], 100)
        
        if rotation != 0:
            wall_obj.Placement.Rotation = FreeCAD.Rotation(FreeCAD.Vector(0, 0, 1), rotation)
        
        return wall_obj
    
    def create_door(self, name, position):
        """Create a door opening"""
        print(f"Creating {name}...")
        door = Part.makeBox(
            self.wall_thickness + 10,
            self.door_width,
            self.door_height
        )
        door_obj = self.doc.addObject("Part::Feature", name)
        door_obj.Shape = door
        door_obj.Placement.Base = FreeCAD.Vector(position[0], position[1], 100)
        return door_obj
    
    def create_window(self, name, position, rotation=0):
        """Create a window opening"""
        print(f"Creating {name}...")
        window = Part.makeBox(
            self.wall_thickness + 10,
            self.window_width,
            self.window_height
        )
        window_obj = self.doc.addObject("Part::Feature", name)
        window_obj.Shape = window
        window_obj.Placement.Base = FreeCAD.Vector(
            position[0],
            position[1],
            100 + 900  # 900mm from floor
        )
        
        if rotation != 0:
            window_obj.Placement.Rotation = FreeCAD.Rotation(FreeCAD.Vector(0, 0, 1), rotation)
        
        return window_obj
    
    def create_roof(self):
        """Create a pitched roof for the house"""
        print("Creating roof...")
        
        # Create roof peak height
        roof_height = 2000  # mm
        roof_overhang = 500  # mm
        
        # Create roof as two sloped planes
        roof_length = self.house_length + 2 * roof_overhang
        roof_slope_width = ((self.house_width / 2 + roof_overhang) ** 2 + roof_height ** 2) ** 0.5
        
        # Left roof plane
        left_roof = Part.makeBox(roof_length, roof_slope_width, 50)  # 50mm thick roof
        left_roof_obj = self.doc.addObject("Part::Feature", "LeftRoof")
        left_roof_obj.Shape = left_roof
        left_roof_obj.Placement.Base = FreeCAD.Vector(-roof_overhang, -roof_overhang, self.wall_height + 100)
        
        # Calculate rotation angle
        angle = math.degrees(math.atan(roof_height / (self.house_width / 2 + roof_overhang)))
        left_roof_obj.Placement.Rotation = FreeCAD.Rotation(FreeCAD.Vector(1, 0, 0), angle)
        
        # Right roof plane
        right_roof = Part.makeBox(roof_length, roof_slope_width, 50)
        right_roof_obj = self.doc.addObject("Part::Feature", "RightRoof")
        right_roof_obj.Shape = right_roof
        right_roof_obj.Placement.Base = FreeCAD.Vector(-roof_overhang, self.house_width / 2, self.wall_height + 100 + roof_height)
        right_roof_obj.Placement.Rotation = FreeCAD.Rotation(FreeCAD.Vector(1, 0, 0), -angle)
        
        return left_roof_obj, right_roof_obj
    
    def create_walls_with_openings(self):
        """Create all walls with doors and windows"""
        # Front wall (with door)
        front_wall = self.create_wall(
            "FrontWall",
            self.house_length,
            [0, 0]
        )
        
        # Create door opening in front wall
        door = self.create_door(
            "FrontDoor",
            [-5, self.house_length / 2 - self.door_width / 2]
        )
        
        # Back wall (with window)
        back_wall = self.create_wall(
            "BackWall",
            self.house_length,
            [0, self.house_width - self.wall_thickness]
        )
        
        # Create window in back wall
        back_window = self.create_window(
            "BackWindow",
            [-5, self.house_width - self.wall_thickness - self.window_width / 2]
        )
        
        # Left wall (with window)
        left_wall = self.create_wall(
            "LeftWall",
            self.house_width,
            [0, 0],
            rotation=90
        )
        
        # Create window in left wall
        left_window = self.create_window(
            "LeftWindow",
            [0, self.house_width / 2 - self.window_width / 2],
            rotation=90
        )
        
        # Right wall (with window)
        right_wall = self.create_wall(
            "RightWall",
            self.house_width,
            [self.house_length - self.wall_thickness, 0],
            rotation=90
        )
        
        # Create window in right wall
        right_window = self.create_window(
            "RightWindow",
            [self.house_length - self.wall_thickness, self.house_width / 2 - self.window_width / 2],
            rotation=90
        )
        
        return {
            'walls': [front_wall, back_wall, left_wall, right_wall],
            'door': door,
            'windows': [back_window, left_window, right_window]
        }
    
    def build_house(self):
        """Build the complete house"""
        print("=" * 60)
        print("Starting House Design with FreeCAD API")
        print("=" * 60)
        
        # Create floor
        floor = self.create_floor()
        
        # Create walls with openings
        structure = self.create_walls_with_openings()
        
        # Create roof
        roof = self.create_roof()
        
        # Recompute the document
        self.doc.recompute()
        
        print("=" * 60)
        print("House design completed successfully!")
        print(f"Document name: {self.doc.Name}")
        print(f"Total objects: {len(self.doc.Objects)}")
        print("=" * 60)
        
        return self.doc
    
    def save_design(self, filename="house_design.FCStd"):
        """Save the house design to a FreeCAD file"""
        filepath = os.path.abspath(filename)
        self.doc.saveAs(filepath)
        print(f"Design saved to: {filepath}")
        return filepath
    
    def export_step(self, filename="house_design.step"):
        """Export the house design to STEP format"""
        filepath = os.path.abspath(filename)
        try:
            import ImportSTEP
            ImportSTEP.export(self.doc.Objects, filepath)
            print(f"Design exported to STEP: {filepath}")
            return filepath
        except ImportError:
            print("Warning: ImportSTEP module not available")
            return None


def main():
    """Main function to run the house designer"""
    print("\nFreeCAD House Designer")
    print("=" * 60)
    
    # Create house designer instance
    designer = HouseDesigner(doc_name="SimpleHouse")
    
    # Build the house
    doc = designer.build_house()
    
    # Save the design
    try:
        designer.save_design("house_design.FCStd")
    except Exception as e:
        print(f"Warning: Could not save FreeCAD file: {e}")
    
    # Try to export to STEP format
    try:
        designer.export_step("house_design.step")
    except Exception as e:
        print(f"Warning: Could not export to STEP: {e}")
    
    print("\nTo view the design:")
    print("1. Open FreeCAD application")
    print("2. File -> Open -> house_design.FCStd")
    print("\nOr run this script directly in FreeCAD:")
    print("   freecadcmd house_designer.py")
    print("=" * 60)


if __name__ == "__main__":
    main()
