# FreeCAD House Designer

A Python application that uses the FreeCAD API to design a simple house with walls, roof, floor, doors, and windows.

## Features

- **Automated House Design**: Creates a complete house structure programmatically
- **Parametric Design**: Easily customizable dimensions for walls, doors, and windows
- **Complete Structure**: Includes floor, walls, doors, windows, and pitched roof
- **Export Support**: Save designs in FreeCAD format (.FCStd) and STEP format (.step)
- **Well-documented Code**: Clear class structure with detailed comments

## House Components

The generated house includes:
- **Floor**: Solid foundation base (100mm thick)
- **Walls**: Four walls with customizable thickness (default 200mm) and height (3000mm)
- **Doors**: Front entrance door (900mm × 2100mm)
- **Windows**: Three windows - back, left, and right walls (1200mm × 1500mm each)
- **Roof**: Pitched roof with overhang (2000mm peak height)

## Requirements

- **FreeCAD**: Version 0.19 or later
- **Python**: 3.6 or later (included with FreeCAD)

### Installing FreeCAD

FreeCAD must be installed on your system:

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

## Usage

### Method 1: Run in FreeCAD (Recommended)

1. Open FreeCAD application
2. Go to **Macro → Macros...**
3. Click **Create** and name it (e.g., "house_designer")
4. Copy the contents of `house_designer.py` into the macro editor
5. Click **Execute** to run

### Method 2: Run from Command Line

If FreeCAD is in your PATH:

```bash
freecadcmd house_designer.py
```

Or with Python if FreeCAD Python module is accessible:

```bash
python3 house_designer.py
```

### Method 3: Run within FreeCAD Python Console

1. Open FreeCAD
2. Open the Python console: **View → Panels → Python console**
3. Execute:
```python
exec(open('house_designer.py').read())
```

## Output Files

The script generates:
- **house_design.FCStd**: FreeCAD native format (can be opened and edited in FreeCAD)
- **house_design.step**: STEP format for CAD interoperability

## Customization

You can modify the house dimensions by editing the class parameters in `house_designer.py`:

```python
class HouseDesigner:
    def __init__(self, doc_name="House"):
        self.wall_thickness = 200   # mm - Wall thickness
        self.wall_height = 3000     # mm - Wall height
        self.house_width = 8000     # mm - House width
        self.house_length = 10000   # mm - House length
        self.door_width = 900       # mm - Door width
        self.door_height = 2100     # mm - Door height
        self.window_width = 1200    # mm - Window width
        self.window_height = 1500   # mm - Window height
```

## Code Structure

- `HouseDesigner`: Main class that handles house creation
  - `create_floor()`: Creates the foundation floor
  - `create_wall()`: Creates individual walls
  - `create_door()`: Creates door openings
  - `create_window()`: Creates window openings
  - `create_roof()`: Creates pitched roof
  - `create_walls_with_openings()`: Assembles walls with doors and windows
  - `build_house()`: Main method to build complete house
  - `save_design()`: Saves to FreeCAD format
  - `export_step()`: Exports to STEP format

## Example

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

## License

This project is open source and available for educational and commercial use.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## Resources

- [FreeCAD Official Website](https://www.freecad.org/)
- [FreeCAD Python Scripting Documentation](https://wiki.freecad.org/Python_scripting_tutorial)
- [FreeCAD API Documentation](https://freecad.github.io/SourceDoc/)
