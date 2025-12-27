#!/usr/bin/env python3
"""
AI House Parser
Parses natural language house descriptions and extracts structured requirements
"""

import re
from typing import Dict, List, Tuple, Optional


class HouseRequirements:
    """Structured representation of house requirements"""
    
    def __init__(self):
        self.total_sqft = 2000
        self.style = "Ranch"
        self.bedrooms = 3
        self.bathrooms = 2
        self.garage_cars = 2
        self.has_attic = False
        self.has_basement = False
        self.special_rooms = []  # gameroom, den, office, etc.
        self.bathroom_types = []  # jack_and_jill, ensuite, etc.
        self.stories = 1
        
    def __repr__(self):
        return (f"HouseRequirements(sqft={self.total_sqft}, style={self.style}, "
                f"bedrooms={self.bedrooms}, bathrooms={self.bathrooms})")


class AIHouseParser:
    """Parses natural language descriptions of houses"""
    
    def __init__(self):
        self.style_keywords = {
            'ranch': 'Ranch',
            'colonial': 'Colonial',
            'victorian': 'Victorian',
            'modern': 'Modern',
            'contemporary': 'Contemporary',
            'craftsman': 'Craftsman',
            'cape cod': 'Cape Cod',
            'mediterranean': 'Mediterranean',
            'tudor': 'Tudor',
        }
        
        self.special_room_keywords = {
            'gameroom': 'gameroom',
            'game room': 'gameroom',
            'den': 'den',
            'man den': 'den',
            'office': 'office',
            'study': 'study',
            'library': 'library',
            'media room': 'media_room',
            'home theater': 'home_theater',
            'gym': 'gym',
            'exercise room': 'gym',
            'mudroom': 'mudroom',
            'laundry': 'laundry',
            'pantry': 'pantry',
        }
        
        self.bathroom_type_keywords = {
            'jack and jill': 'jack_and_jill',
            'ensuite': 'ensuite',
            'master bath': 'master',
            'half bath': 'half',
            'powder room': 'powder',
        }
    
    def parse(self, description: str) -> HouseRequirements:
        """Parse a natural language house description"""
        requirements = HouseRequirements()
        description_lower = description.lower()
        
        # Parse square footage
        sqft_match = re.search(r'(\d+)\s*sq\s*ft', description_lower)
        if sqft_match:
            requirements.total_sqft = int(sqft_match.group(1))
        
        # Parse style
        for keyword, style in self.style_keywords.items():
            if keyword in description_lower:
                requirements.style = style
                break
        
        # Parse bedrooms
        bedroom_match = re.search(r'(\d+)\s*bed', description_lower)
        if bedroom_match:
            requirements.bedrooms = int(bedroom_match.group(1))
        
        # Parse bathrooms
        bathroom_match = re.search(r'(\d+(?:\.\d+)?)\s*bath', description_lower)
        if bathroom_match:
            requirements.bathrooms = float(bathroom_match.group(1))
        
        # Parse garage
        garage_match = re.search(r'(\d+)\s*car\s*garage', description_lower)
        if garage_match:
            requirements.garage_cars = int(garage_match.group(1))
        
        # Check for attic
        if 'attic' in description_lower:
            requirements.has_attic = True
        
        # Check for basement
        if 'basement' in description_lower:
            requirements.has_basement = True
        
        # Parse special rooms
        for keyword, room_type in self.special_room_keywords.items():
            if keyword in description_lower:
                if room_type not in requirements.special_rooms:
                    requirements.special_rooms.append(room_type)
        
        # Parse bathroom types
        for keyword, bath_type in self.bathroom_type_keywords.items():
            if keyword in description_lower:
                if bath_type not in requirements.bathroom_types:
                    requirements.bathroom_types.append(bath_type)
        
        # Parse stories
        if 'two story' in description_lower or '2 story' in description_lower:
            requirements.stories = 2
        elif 'three story' in description_lower or '3 story' in description_lower:
            requirements.stories = 3
        elif 'ranch' in description_lower or 'single story' in description_lower:
            requirements.stories = 1
        
        return requirements
    
    def print_summary(self, requirements: HouseRequirements):
        """Print a human-readable summary of the requirements"""
        print("\n" + "=" * 60)
        print("HOUSE REQUIREMENTS SUMMARY")
        print("=" * 60)
        print(f"Style:           {requirements.style}")
        print(f"Total Size:      {requirements.total_sqft} sq ft")
        print(f"Stories:         {requirements.stories}")
        print(f"Bedrooms:        {requirements.bedrooms}")
        print(f"Bathrooms:       {requirements.bathrooms}")
        print(f"Garage:          {requirements.garage_cars} car(s)")
        
        if requirements.special_rooms:
            print(f"Special Rooms:   {', '.join(requirements.special_rooms)}")
        
        if requirements.bathroom_types:
            print(f"Bathroom Types:  {', '.join(requirements.bathroom_types)}")
        
        if requirements.has_attic:
            print("Attic:           Yes")
        
        if requirements.has_basement:
            print("Basement:        Yes")
        
        print("=" * 60)


# Example usage
if __name__ == "__main__":
    parser = AIHouseParser()
    
    # Test examples
    test_descriptions = [
        "3000 sqft Ranch style house, 4 bedrooms, 4 bathrooms. Jack and Jill bathroom. Gameroom. 3 car garage. Attic man den.",
        "2500 sq ft Colonial, 3 bed, 2.5 bath, 2 car garage, office, mudroom",
        "Modern 4000 sqft home with 5 bedrooms, 3 bathrooms, home theater, gym, 3 car garage",
    ]
    
    for desc in test_descriptions:
        print(f"\nInput: {desc}")
        requirements = parser.parse(desc)
        parser.print_summary(requirements)
