# FreeCAD AI House Designer

A Python application that uses AI and the FreeCAD API to design houses from natural language descriptions. Simply describe your dream house in plain English, and the AI will generate a complete 3D model with floor plan, rooms, and structure.

## ✨ Key Features

### 🤖 AI-Powered Natural Language Design
- **Describe your house in plain English**: "3000 sqft Ranch style house, 4 bedrooms, 4 bathrooms, gameroom, 3 car garage"
- **Automatic parsing**: Extracts style, size, room count, and special features
- **Smart floor plan generation**: Creates realistic room layouts with proper dimensions
- **3D model creation**: Builds complete FreeCAD 3D models automatically

### 🏗️ Comprehensive House Components
- **Automated House Design**: Creates complete house structure programmatically
- **Parametric Design**: Easily customizable dimensions for walls, doors, and windows
- **Complete Structure**: Includes floor, walls, doors, windows, and pitched roof
- **Room-by-room modeling**: Individual rooms with proper dimensions and windows
- **Export Support**: Save designs in FreeCAD format (.FCStd) and STEP format (.step)
- **Well-documented Code**: Clear class structure with detailed comments

## 🏠 What the AI Can Understand

The AI house designer can parse and understand:

### House Specifications
- **Size**: "3000 sqft", "2500 sq ft", "1800 square feet"
- **Style**: Ranch, Colonial, Victorian, Modern, Contemporary, Craftsman, Cape Cod, Mediterranean, Tudor
- **Stories**: Single story, two story, three story

### Rooms
- **Bedrooms**: "4 bedrooms", "3 bed", "5 BR"
- **Bathrooms**: "3 bathrooms", "2.5 bath", "4 BA"
- **Special rooms**: gameroom, den, office, study, library, media room, home theater, gym, mudroom, laundry, pantry

### Special Features
- **Bathroom types**: Jack and Jill, ensuite, master bath, half bath, powder room
- **Garage**: "3 car garage", "2-car garage"
- **Additional spaces**: Attic, basement

## 🚀 Quick Start - AI Designer

The easiest way to design a house is using natural language:

```bash
python3 ai_house_designer.py
```

Then simply describe your house when prompted:
```
"3000 sqft Ranch style house, 4 bedrooms, 4 bathrooms. 
Jack and Jill bathroom. Gameroom. 3 car garage. Attic man den."
```

The AI will:
1. ✅ Parse your requirements
2. ✅ Generate a complete floor plan with all rooms
3. ✅ Create a 3D model in FreeCAD (if installed)
4. ✅ Export summary and design files

### Example Output

```
AI-POWERED HOUSE DESIGNER
======================================================================

Input Description:
  "3000 sqft Ranch style house, 4 bedrooms, 4 bathrooms. 
   Jack and Jill bathroom. Gameroom. 3 car garage."

Step 1: Parsing house requirements...
  ✓ Style: Ranch
  ✓ Size: 3000 sq ft
  ✓ Bedrooms: 4
  ✓ Bathrooms: 4
  ✓ Special rooms: gameroom, den
  ✓ Garage: 3 cars

Step 2: Generating floor plan...
  ✓ Created 16 rooms
  ✓ Total area: 2940 sq ft
  ✓ Rooms: Master Bedroom, 3 Bedrooms, Master Bath, 
          Jack and Jill Bath, 2 Bathrooms, Kitchen, 
          Dining Room, Living Room, Gameroom, Den, 
          3 Car Garage, Foyer, Hallway

Step 3: Creating 3D model in FreeCAD...
  ✓ Foundation: 22.5m x 19.1m
  ✓ 16 rooms with walls
  ✓ Pitched roof

HOUSE DESIGN COMPLETED
```

## House Components

The generated house includes:
- **Floor**: Solid foundation base (100mm thick)
- **Walls**: Four walls with customizable thickness (default 200mm) and height (3000mm)
- **Doors**: Front entrance door (900mm × 2100mm)
- **Windows**: Three windows - back, left, and right walls (1200mm × 1500mm each)
- **Roof**: Pitched roof with overhang (2000mm peak height)

## Requirements

- **FreeCAD**: Version 0.19 or later (for 3D modeling)
- **Python**: 3.6 or later
- **No external dependencies**: Works with just Python standard library and FreeCAD

### Installing FreeCAD

FreeCAD must be installed on your system for 3D model generation:

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install freecad
```

**macOS:**
```bash
brew install freecad
```

**Windows:**
- Download the installer from [FreeCAD Downloads](https://www.freecad.org/downloads.php)
- Run the installer and follow the instructions

**Note**: The AI parser and floor plan generator work without FreeCAD. You'll get a complete room list and floor plan summary even without FreeCAD installed.

## 📖 Usage

### Method 1: AI-Powered Design (Recommended) 🌟

Use natural language to describe your house:

```bash
python3 ai_house_designer.py
```

Or run directly in FreeCAD for full 3D modeling:
```bash
freecadcmd ai_house_designer.py
```

**Example descriptions you can use:**
- "3000 sqft Ranch style house, 4 bedrooms, 4 bathrooms. Jack and Jill bathroom. Gameroom. 3 car garage. Attic man den."
- "2500 sq ft Colonial, 3 bed, 2.5 bath, 2 car garage, office, mudroom"
- "Modern 1800 sqft home with 3 bedrooms, 2 bathrooms, 2 car garage"
- "4000 sqft Contemporary with 5 bedrooms, 3.5 bathrooms, home theater, gym, wine cellar, 3 car garage"

### Method 2: Programmatic API

Use the AI designer programmatically in your own code:

```python
from ai_house_designer import AIHouseDesigner

# Create designer
designer = AIHouseDesigner()

# Design from natural language
description = "3000 sqft Ranch, 4 bed, 3 bath, 2 car garage, office"
requirements, rooms, doc = designer.design_from_description(description)

# Save the design
if doc:  # If FreeCAD is available
    designer.save_design("my_house.FCStd")

# Export summary
designer.export_summary("my_house_summary.txt")
```

### Method 3: Manual House Design

Use the basic house designer for simple predefined houses:

```bash
python3 house_designer.py
```

Or run examples:
```bash
python3 examples.py
```

### Method 4: Run in FreeCAD GUI

1. Open FreeCAD application
2. Go to **Macro → Macros...**
3. Click **Create** and name it (e.g., "ai_house_designer")
4. Copy the contents of `ai_house_designer.py` into the macro editor
5. Click **Execute** to run


## 📁 Project Structure

```
ideal-octo-invention/
├── ai_house_designer.py      # Main AI-powered house designer
├── ai_house_parser.py         # Natural language parser
├── floor_plan_generator.py    # Room layout generator
├── house_designer.py          # Basic FreeCAD house builder
├── examples.py                # Example house designs
├── requirements.txt           # Dependencies info
├── .gitignore                 # Git ignore file
└── README.md                  # This file
```

## Output Files

The AI house designer generates:
- **[style]_house_[size]sqft.FCStd**: FreeCAD 3D model (can be opened and edited in FreeCAD)
- **house_design_summary.txt**: Detailed text summary with room list and dimensions
- **house_design.step**: STEP format for CAD interoperability (optional)

## 🎨 Customization

### AI-Based Customization

Simply modify your natural language description:
- "5000 sqft luxury modern estate with 6 bedrooms, 5 bathrooms, wine cellar, home theater"
- "Cozy 1500 sqft cottage with 2 bedrooms, 1.5 bathrooms, fireplace, sunroom"

### Programmatic Customization

For the basic house designer, modify parameters:

```python
from house_designer import HouseDesigner

# Create a custom house
designer = HouseDesigner(doc_name="MyCustomHouse")

# Customize dimensions
designer.house_length = 12000  # 12 meters
designer.house_width = 10000   # 10 meters
designer.wall_height = 3500    # 3.5 meters

# Build the house
doc = designer.build_house()

# Save the design
designer.save_design("my_custom_house.FCStd")
```

## 🏗️ Architecture

### AI House Designer Components

1. **AIHouseParser** (`ai_house_parser.py`)
   - Parses natural language descriptions
   - Extracts: size, style, rooms, features
   - Supports various input formats

2. **FloorPlanGenerator** (`floor_plan_generator.py`)
   - Generates room layouts
   - Calculates room dimensions
   - Arranges rooms in floor plan
   - Handles special room types

3. **AIHouseDesigner** (`ai_house_designer.py`)
   - Orchestrates the entire process
   - Integrates parser + floor plan + 3D model
   - Creates FreeCAD 3D models
   - Exports results

4. **HouseDesigner** (`house_designer.py`)
   - Core FreeCAD 3D modeling
   - Creates walls, floors, roofs
   - Adds doors and windows
   - Exports to various formats

## 📝 More Examples

```python
from ai_house_designer import AIHouseDesigner

designer = AIHouseDesigner()

# Example 1: Luxury home
designer.design_from_description(
    "5000 sqft Mediterranean villa, 5 bedrooms, 4.5 bathrooms, "
    "home theater, wine cellar, gym, 3 car garage"
)

# Example 2: Starter home
designer.design_from_description(
    "1500 sqft Ranch, 3 bed, 2 bath, 2 car garage"
)

# Example 3: Family home
designer.design_from_description(
    "3200 sqft Colonial, 4 bedrooms, 3 bathrooms, "
    "Jack and Jill bathroom, office, mudroom, 2 car garage"
)
```

## 🧪 Testing

Test the AI parser:
```bash
python3 ai_house_parser.py
```

Test floor plan generation:
```bash
python3 floor_plan_generator.py
```

Test basic house designer:
```bash
python3 house_designer.py
```

Test with examples:
```bash
python3 examples.py
```

## License

This project is open source and available for educational and commercial use.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## Resources

- [FreeCAD Official Website](https://www.freecad.org/)
- [FreeCAD Python Scripting Documentation](https://wiki.freecad.org/Python_scripting_tutorial)
- [FreeCAD API Documentation](https://freecad.github.io/SourceDoc/)
