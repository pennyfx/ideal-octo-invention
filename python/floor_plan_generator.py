#!/usr/bin/env python3
"""
Floor Plan Generator
Generates room layouts based on house requirements
"""

import math
from typing import List, Dict, Tuple
from ai_house_parser import HouseRequirements


class Room:
    """Represents a room in the house"""
    
    def __init__(self, name: str, sqft: float, room_type: str):
        self.name = name
        self.sqft = sqft
        self.room_type = room_type
        self.x = 0  # Position in floor plan
        self.y = 0
        self.width = 0  # Dimensions
        self.length = 0
        self.doors = []  # Connected rooms
        self.windows = 0  # Number of windows
        
    def __repr__(self):
        return f"Room({self.name}, {self.sqft}sqft, {self.width}x{self.length}mm)"


class FloorPlanGenerator:
    """Generates floor plans from house requirements"""
    
    def __init__(self, requirements: HouseRequirements):
        self.requirements = requirements
        self.rooms = []
        
        # Room size guidelines (in square feet)
        self.room_sizes = {
            'master_bedroom': 300,
            'bedroom': 150,
            'bathroom': 40,
            'jack_and_jill_bathroom': 80,
            'master_bathroom': 100,
            'half_bathroom': 25,
            'kitchen': 200,
            'living_room': 300,
            'dining_room': 150,
            'garage': 250,  # per car
            'gameroom': 250,
            'den': 150,
            'office': 120,
            'study': 120,
            'library': 150,
            'media_room': 200,
            'home_theater': 300,
            'gym': 200,
            'mudroom': 50,
            'laundry': 50,
            'pantry': 30,
            'hallway': 50,
            'foyer': 80,
        }
    
    def generate_floor_plan(self) -> List[Room]:
        """Generate a complete floor plan"""
        self.rooms = []
        
        # Add essential rooms
        self._add_bedrooms()
        self._add_bathrooms()
        self._add_kitchen()
        self._add_living_areas()
        self._add_garage()
        self._add_special_rooms()
        self._add_circulation_spaces()
        
        # Calculate room dimensions
        self._calculate_room_dimensions()
        
        # Arrange rooms in floor plan
        self._arrange_rooms()
        
        return self.rooms
    
    def _add_bedrooms(self):
        """Add bedrooms to the floor plan"""
        # One master bedroom
        master = Room("Master Bedroom", self.room_sizes['master_bedroom'], 'master_bedroom')
        master.windows = 2
        self.rooms.append(master)
        
        # Additional bedrooms
        for i in range(self.requirements.bedrooms - 1):
            bedroom = Room(f"Bedroom {i + 2}", self.room_sizes['bedroom'], 'bedroom')
            bedroom.windows = 1
            self.rooms.append(bedroom)
    
    def _add_bathrooms(self):
        """Add bathrooms to the floor plan"""
        bathroom_count = int(self.requirements.bathrooms)
        half_bath_count = 1 if (self.requirements.bathrooms % 1 >= 0.5) else 0
        
        # Master bathroom
        master_bath = Room("Master Bathroom", self.room_sizes['master_bathroom'], 'master_bathroom')
        master_bath.windows = 1
        self.rooms.append(master_bath)
        bathroom_count -= 1
        
        # Jack and Jill bathroom if specified
        if 'jack_and_jill' in self.requirements.bathroom_types and bathroom_count > 0:
            jnj_bath = Room("Jack and Jill Bathroom", 
                          self.room_sizes['jack_and_jill_bathroom'], 
                          'jack_and_jill_bathroom')
            jnj_bath.windows = 1
            self.rooms.append(jnj_bath)
            bathroom_count -= 1
        
        # Additional full bathrooms
        for i in range(bathroom_count):
            bathroom = Room(f"Bathroom {i + 2}", self.room_sizes['bathroom'], 'bathroom')
            bathroom.windows = 1
            self.rooms.append(bathroom)
        
        # Half bathrooms
        for i in range(half_bath_count):
            half_bath = Room(f"Powder Room", self.room_sizes['half_bathroom'], 'half_bathroom')
            half_bath.windows = 0
            self.rooms.append(half_bath)
    
    def _add_kitchen(self):
        """Add kitchen and dining areas"""
        kitchen = Room("Kitchen", self.room_sizes['kitchen'], 'kitchen')
        kitchen.windows = 2
        self.rooms.append(kitchen)
        
        dining = Room("Dining Room", self.room_sizes['dining_room'], 'dining_room')
        dining.windows = 1
        self.rooms.append(dining)
    
    def _add_living_areas(self):
        """Add living room and family areas"""
        living = Room("Living Room", self.room_sizes['living_room'], 'living_room')
        living.windows = 3
        self.rooms.append(living)
    
    def _add_garage(self):
        """Add garage"""
        if self.requirements.garage_cars > 0:
            garage_size = self.room_sizes['garage'] * self.requirements.garage_cars
            garage = Room(f"{self.requirements.garage_cars} Car Garage", 
                         garage_size, 'garage')
            garage.windows = 0
            self.rooms.append(garage)
    
    def _add_special_rooms(self):
        """Add special rooms like gameroom, den, office, etc."""
        for room_type in self.requirements.special_rooms:
            if room_type in self.room_sizes:
                room_name = room_type.replace('_', ' ').title()
                room = Room(room_name, self.room_sizes[room_type], room_type)
                room.windows = 1
                self.rooms.append(room)
    
    def _add_circulation_spaces(self):
        """Add hallways, foyer, etc."""
        foyer = Room("Foyer", self.room_sizes['foyer'], 'foyer')
        foyer.windows = 0
        self.rooms.append(foyer)
        
        # Add hallways if needed (multi-bedroom houses need hallways)
        if self.requirements.bedrooms >= 3:
            hallway = Room("Hallway", self.room_sizes['hallway'], 'hallway')
            hallway.windows = 0
            self.rooms.append(hallway)
    
    def _calculate_room_dimensions(self):
        """Calculate length and width for each room based on square footage"""
        for room in self.rooms:
            # Use reasonable aspect ratios for different room types
            if room.room_type == 'garage':
                # Garages are typically deeper than wide
                aspect_ratio = 1.5  # length = 1.5 * width
            elif room.room_type in ['hallway', 'mudroom']:
                # Hallways are long and narrow
                aspect_ratio = 3.0
            elif room.room_type in ['master_bedroom', 'living_room']:
                # Larger rooms can be more square
                aspect_ratio = 1.2
            else:
                # Default aspect ratio
                aspect_ratio = 1.3
            
            # Calculate dimensions (convert sqft to mm)
            sqft_to_mm2 = 92903.04  # 1 sqft = 92903.04 mm²
            area_mm2 = room.sqft * sqft_to_mm2
            
            # width * (aspect_ratio * width) = area
            room.width = int(math.sqrt(area_mm2 / aspect_ratio))
            room.length = int(area_mm2 / room.width)
    
    def _arrange_rooms(self):
        """Arrange rooms in a 2D floor plan"""
        if not self.rooms:
            return
        
        # Simple arrangement: place rooms in a grid-like pattern
        # For Ranch style, try to create a rectangular layout
        
        # Sort rooms by size (largest first)
        sorted_rooms = sorted(self.rooms, key=lambda r: r.sqft, reverse=True)
        
        # Calculate approximate house dimensions
        total_area = sum(r.sqft for r in self.rooms)
        
        # Adjust if specified square footage is larger (account for walls, hallways)
        if self.requirements.total_sqft > total_area:
            scale_factor = math.sqrt(self.requirements.total_sqft / total_area)
            for room in self.rooms:
                room.width = int(room.width * scale_factor)
                room.length = int(room.length * scale_factor)
        
        # Simple row-based layout
        current_x = 0
        current_y = 0
        row_height = 0
        max_width = int(math.sqrt(self.requirements.total_sqft * 92903.04) * 1.3)
        
        for room in sorted_rooms:
            if current_x + room.length > max_width and current_x > 0:
                # Start new row
                current_x = 0
                current_y += row_height + 200  # 200mm gap for walls
                row_height = 0
            
            room.x = current_x
            room.y = current_y
            
            current_x += room.length + 200  # 200mm gap for walls
            row_height = max(row_height, room.width)
    
    def print_floor_plan(self):
        """Print a summary of the floor plan"""
        print("\n" + "=" * 60)
        print("FLOOR PLAN")
        print("=" * 60)
        
        total_sqft = sum(r.sqft for r in self.rooms)
        print(f"Total rooms: {len(self.rooms)}")
        print(f"Total area: {total_sqft:.0f} sq ft")
        print(f"\nRoom List:")
        print("-" * 60)
        
        for room in self.rooms:
            print(f"{room.name:30} {room.sqft:6.0f} sq ft  "
                  f"{room.width/1000:.1f}m x {room.length/1000:.1f}m  "
                  f"Windows: {room.windows}")
        
        print("=" * 60)
    
    def get_house_dimensions(self) -> Tuple[int, int]:
        """Get overall house dimensions"""
        if not self.rooms:
            return (10000, 8000)  # Default
        
        max_x = max(r.x + r.length for r in self.rooms)
        max_y = max(r.y + r.width for r in self.rooms)
        
        return (max_x + 1000, max_y + 1000)  # Add margin


# Example usage
if __name__ == "__main__":
    from ai_house_parser import AIHouseParser
    
    parser = AIHouseParser()
    description = "3000 sqft Ranch style house, 4 bedrooms, 4 bathrooms. Jack and Jill bathroom. Gameroom. 3 car garage. Attic man den."
    
    print(f"Input: {description}\n")
    requirements = parser.parse(description)
    parser.print_summary(requirements)
    
    generator = FloorPlanGenerator(requirements)
    rooms = generator.generate_floor_plan()
    generator.print_floor_plan()
    
    house_dims = generator.get_house_dimensions()
    print(f"\nHouse dimensions: {house_dims[0]/1000:.1f}m x {house_dims[1]/1000:.1f}m")
