#!/usr/bin/env python3
"""
AI-Powered House Designer
Integrates natural language parsing, floor plan generation, and FreeCAD 3D modeling
"""

import sys
import os
import math

# Import our modules
from ai_house_parser import AIHouseParser, HouseRequirements
from floor_plan_generator import FloorPlanGenerator, Room

# Try to import FreeCAD
try:
    import FreeCAD
    import Part
    FREECAD_AVAILABLE = True
except ImportError:
    FREECAD_AVAILABLE = False
    print("Warning: FreeCAD module not available. 3D modeling will be skipped.")
    print("Install FreeCAD or run this script within FreeCAD environment.")


class AIHouseDesigner:
    """AI-powered house designer that creates 3D models from natural language"""
    
    def __init__(self):
        self.parser = AIHouseParser()
        self.requirements = None
        self.floor_plan_generator = None
        self.rooms = []
        self.doc = None
        
    def design_from_description(self, description: str):
        """Main method: takes text description and creates complete house design"""
        print("\n" + "=" * 70)
        print("AI-POWERED HOUSE DESIGNER")
        print("=" * 70)
        print(f"\nInput Description:")
        print(f'  "{description}"')
        print()
        
        # Step 1: Parse the description
        print("Step 1: Parsing house requirements...")
        self.requirements = self.parser.parse(description)
        self.parser.print_summary(self.requirements)
        
        # Step 2: Generate floor plan
        print("\nStep 2: Generating floor plan...")
        self.floor_plan_generator = FloorPlanGenerator(self.requirements)
        self.rooms = self.floor_plan_generator.generate_floor_plan()
        self.floor_plan_generator.print_floor_plan()
        
        # Step 3: Create 3D model
        if FREECAD_AVAILABLE:
            print("\nStep 3: Creating 3D model in FreeCAD...")
            self._create_3d_model()
            print("\n3D model created successfully!")
        else:
            print("\nStep 3: Skipping 3D model creation (FreeCAD not available)")
        
        print("\n" + "=" * 70)
        print("HOUSE DESIGN COMPLETED")
        print("=" * 70)
        
        return self.requirements, self.rooms, self.doc
    
    def _create_3d_model(self):
        """Create 3D model using FreeCAD"""
        if not FREECAD_AVAILABLE:
            return
        
        # Create new document
        doc_name = f"{self.requirements.style}House"
        self.doc = FreeCAD.newDocument(doc_name)
        
        # Get house dimensions
        house_length, house_width = self.floor_plan_generator.get_house_dimensions()
        
        # Create foundation/floor
        self._create_floor(house_length, house_width)
        
        # Create rooms with walls
        self._create_rooms_3d()
        
        # Create roof
        self._create_roof(house_length, house_width)
        
        # Recompute
        self.doc.recompute()
    
    def _create_floor(self, length: int, width: int):
        """Create the floor/foundation"""
        floor_thickness = 150  # mm
        floor = Part.makeBox(length, width, floor_thickness)
        floor_obj = self.doc.addObject("Part::Feature", "Foundation")
        floor_obj.Shape = floor
        print(f"  Created foundation: {length/1000:.1f}m x {width/1000:.1f}m")
    
    def _create_rooms_3d(self):
        """Create 3D representation of rooms"""
        wall_height = 2700  # mm (9 feet)
        wall_thickness = 150  # mm
        
        for room in self.rooms:
            # Skip garage for now (different height)
            if room.room_type == 'garage':
                continue
            
            # Create room as a box (walls)
            # Create outer box
            outer = Part.makeBox(
                room.length + 2 * wall_thickness,
                room.width + 2 * wall_thickness,
                wall_height
            )
            
            # Create inner box (room interior)
            inner = Part.makeBox(
                room.length,
                room.width,
                wall_height
            )
            inner_shape = inner.translated(FreeCAD.Vector(wall_thickness, wall_thickness, 0))
            
            # Subtract to create walls
            walls = outer.cut(inner_shape)
            
            # Create the room object
            room_obj = self.doc.addObject("Part::Feature", room.name.replace(" ", "_"))
            room_obj.Shape = walls
            room_obj.Placement.Base = FreeCAD.Vector(room.x, room.y, 150)  # On top of foundation
            
            # Add windows
            self._add_windows_to_room(room, room_obj, wall_height, wall_thickness)
        
        print(f"  Created {len(self.rooms)} rooms with walls")
    
    def _add_windows_to_room(self, room: Room, room_obj, wall_height: int, wall_thickness: int):
        """Add window openings to a room"""
        if room.windows == 0:
            return
        
        window_width = 1200  # mm
        window_height = 1200  # mm
        window_sill_height = 900  # mm from floor
        
        # Add windows on the outer wall (simplified - just on one wall)
        for i in range(room.windows):
            window = Part.makeBox(
                wall_thickness + 20,
                window_width,
                window_height
            )
            
            # Position window
            x_pos = room.x + (i + 1) * room.length / (room.windows + 1)
            window_obj = self.doc.addObject("Part::Feature", f"{room.name}_Window{i+1}".replace(" ", "_"))
            window_obj.Shape = window
            window_obj.Placement.Base = FreeCAD.Vector(
                x_pos - 10,
                room.y - 10,
                150 + window_sill_height
            )
    
    def _create_roof(self, length: int, width: int):
        """Create a simple pitched roof"""
        
        roof_height = 2000  # mm peak height
        roof_overhang = 600  # mm
        wall_height = 2700  # mm
        
        # Calculate roof dimensions
        roof_length = length + 2 * roof_overhang
        roof_slope_width = math.sqrt((width / 2 + roof_overhang) ** 2 + roof_height ** 2)
        roof_thickness = 50  # mm
        
        # Left roof plane
        left_roof = Part.makeBox(roof_length, roof_slope_width, roof_thickness)
        left_roof_obj = self.doc.addObject("Part::Feature", "LeftRoof")
        left_roof_obj.Shape = left_roof
        left_roof_obj.Placement.Base = FreeCAD.Vector(-roof_overhang, -roof_overhang, 150 + wall_height)
        
        # Calculate pitch angle
        angle = math.degrees(math.atan(roof_height / (width / 2 + roof_overhang)))
        left_roof_obj.Placement.Rotation = FreeCAD.Rotation(FreeCAD.Vector(1, 0, 0), angle)
        
        # Right roof plane
        right_roof = Part.makeBox(roof_length, roof_slope_width, roof_thickness)
        right_roof_obj = self.doc.addObject("Part::Feature", "RightRoof")
        right_roof_obj.Shape = right_roof
        right_roof_obj.Placement.Base = FreeCAD.Vector(
            -roof_overhang,
            width / 2,
            150 + wall_height + roof_height
        )
        right_roof_obj.Placement.Rotation = FreeCAD.Rotation(FreeCAD.Vector(1, 0, 0), -angle)
        
        print(f"  Created pitched roof with {roof_height/1000:.1f}m peak")
    
    def save_design(self, filename: str = None):
        """Save the 3D model"""
        if not FREECAD_AVAILABLE or not self.doc:
            print("Cannot save: No 3D model created")
            return None
        
        if filename is None:
            filename = f"{self.requirements.style.lower()}_house_{self.requirements.total_sqft}sqft.FCStd"
        
        filepath = os.path.abspath(filename)
        self.doc.saveAs(filepath)
        print(f"\nDesign saved to: {filepath}")
        return filepath
    
    def export_summary(self, filename: str = "house_design_summary.txt"):
        """Export a text summary of the design"""
        filepath = os.path.abspath(filename)
        
        with open(filepath, 'w') as f:
            f.write("=" * 70 + "\n")
            f.write("HOUSE DESIGN SUMMARY\n")
            f.write("=" * 70 + "\n\n")
            
            # Requirements
            f.write("REQUIREMENTS:\n")
            f.write("-" * 70 + "\n")
            f.write(f"Style:           {self.requirements.style}\n")
            f.write(f"Total Size:      {self.requirements.total_sqft} sq ft\n")
            f.write(f"Stories:         {self.requirements.stories}\n")
            f.write(f"Bedrooms:        {self.requirements.bedrooms}\n")
            f.write(f"Bathrooms:       {self.requirements.bathrooms}\n")
            f.write(f"Garage:          {self.requirements.garage_cars} car(s)\n")
            
            if self.requirements.special_rooms:
                f.write(f"Special Rooms:   {', '.join(self.requirements.special_rooms)}\n")
            
            if self.requirements.bathroom_types:
                f.write(f"Bathroom Types:  {', '.join(self.requirements.bathroom_types)}\n")
            
            f.write("\n")
            
            # Floor plan
            f.write("FLOOR PLAN:\n")
            f.write("-" * 70 + "\n")
            f.write(f"Total rooms:     {len(self.rooms)}\n")
            total_sqft = sum(r.sqft for r in self.rooms)
            f.write(f"Total area:      {total_sqft:.0f} sq ft\n\n")
            
            f.write("ROOM LIST:\n")
            for room in self.rooms:
                f.write(f"  {room.name:30} {room.sqft:6.0f} sq ft  "
                       f"{room.width/1000:.1f}m x {room.length/1000:.1f}m  "
                       f"Windows: {room.windows}\n")
            
            f.write("\n" + "=" * 70 + "\n")
        
        print(f"Summary exported to: {filepath}")
        return filepath


def main():
    """Main function for AI house designer"""
    # Example descriptions
    examples = [
        "3000 sqft Ranch style house, 4 bedrooms, 4 bathrooms. Jack and Jill bathroom. Gameroom. 3 car garage. Attic man den.",
        "2500 sq ft Colonial, 3 bed, 2.5 bath, 2 car garage, office, mudroom",
        "Modern 1800 sqft home with 3 bedrooms, 2 bathrooms, 2 car garage",
    ]
    
    print("\nAI-Powered House Designer")
    print("=" * 70)
    print("\nExample descriptions:")
    for i, ex in enumerate(examples, 1):
        print(f"  {i}. {ex}")
    
    # Get user input
    try:
        choice = input("\nSelect an example (1-3) or enter your own description: ").strip()
        
        if choice in ['1', '2', '3']:
            description = examples[int(choice) - 1]
        else:
            description = choice
    except (EOFError, KeyboardInterrupt):
        # Use default for non-interactive environments
        description = examples[0]
        print(f"\nUsing default: {description}")
    
    # Create designer and build house
    designer = AIHouseDesigner()
    requirements, rooms, doc = designer.design_from_description(description)
    
    # Save outputs
    if FREECAD_AVAILABLE and doc:
        designer.save_design()
    
    designer.export_summary()
    
    print("\nDone! Check the output files.")


if __name__ == "__main__":
    main()
