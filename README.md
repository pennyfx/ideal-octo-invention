# AI House Designer

A multi-platform application that uses AI to design houses from natural language descriptions. Simply describe your dream house in plain English, and the AI will generate a complete 3D model with floor plan, rooms, and structure.

## Platforms

This project includes two implementations:

| Platform | Technology | 3D Rendering | Requirements |
|----------|------------|--------------|--------------|
| **Web** | JavaScript, Three.js | WebGL Canvas | Modern browser |
| **Python** | Python 3.6+, FreeCAD | FreeCAD API | FreeCAD installed |

## Quick Start

### Web Version (Recommended)

The easiest way to use the AI House Designer:

```bash
# Navigate to web directory
cd web

# Serve with any static file server
python3 -m http.server 8080

# Open in browser
# http://localhost:8080
```

Or simply open `web/index.html` directly in your browser.

### Python Version

For CAD-quality output with FreeCAD:

```bash
cd python

# Run with Python (generates floor plan + summary)
python3 ai_house_designer.py

# Or run within FreeCAD for full 3D modeling
freecadcmd ai_house_designer.py
```

## Features

### AI-Powered Natural Language Design

Describe your house in plain English:
- "3000 sqft Ranch style house, 4 bedrooms, 4 bathrooms, gameroom, 3 car garage"
- "2500 sq ft Colonial, 3 bed, 2.5 bath, 2 car garage, office, mudroom"
- "Modern 1800 sqft home with 3 bedrooms, 2 bathrooms, 2 car garage"

### What the AI Understands

| Category | Examples |
|----------|----------|
| **Size** | "3000 sqft", "2500 sq ft", "1800 square feet" |
| **Style** | Ranch, Colonial, Victorian, Modern, Contemporary, Craftsman, Cape Cod, Mediterranean, Tudor |
| **Bedrooms** | "4 bedrooms", "3 bed", "5 BR" |
| **Bathrooms** | "3 bathrooms", "2.5 bath", "4 BA" |
| **Special Rooms** | gameroom, den, office, study, library, media room, home theater, gym, mudroom, laundry, pantry |
| **Features** | Jack and Jill bathroom, ensuite, half bath, attic, basement |
| **Garage** | "3 car garage", "2-car garage" |

## Project Structure

```
ideal-octo-invention/
├── README.md                    # This file
├── CODE_REVIEW.md               # Code review document
├── web/                         # Three.js Web Application
│   ├── index.html              # Main HTML entry point
│   ├── styles/
│   │   └── main.css            # Application styles
│   └── src/
│       ├── parser.js           # Natural language parser
│       ├── floorPlan.js        # Floor plan generator
│       ├── houseRenderer.js    # Three.js 3D renderer
│       └── app.js              # Main application logic
│
└── python/                      # Python/FreeCAD Application
    ├── ai_house_designer.py    # Main AI-powered designer
    ├── ai_house_parser.py      # Natural language parser
    ├── floor_plan_generator.py # Room layout generator
    ├── house_designer.py       # FreeCAD 3D modeling
    ├── examples.py             # Example house designs
    ├── test_ai_designer.py     # Test suite
    └── requirements.txt        # Dependencies info
```

## Web Version Details

### Features
- Real-time 3D visualization with Three.js
- Interactive camera controls (orbit, zoom, pan)
- Multiple view modes (Top, Front, Side, 3D Isometric)
- Toggle roof visibility
- Wireframe mode
- 2D floor plan view
- Room color coding
- Responsive design

### Browser Requirements
- Modern browser with WebGL support
- Chrome, Firefox, Safari, or Edge recommended

### Usage

1. Open `web/index.html` in your browser
2. Enter a house description or click an example
3. Click "Generate House" to create the 3D model
4. Use view controls to explore the design
5. Toggle roof or wireframe mode as needed

## Python Version Details

### Features
- CAD-quality 3D model generation
- Export to FreeCAD (.FCStd) and STEP formats
- Detailed floor plan with room dimensions
- Works with or without FreeCAD installed

### Requirements
- Python 3.6+
- FreeCAD (optional, for 3D modeling)

### Installing FreeCAD

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
Download from [FreeCAD Downloads](https://www.freecad.org/downloads.php)

### Usage

```python
from ai_house_designer import AIHouseDesigner

# Create designer
designer = AIHouseDesigner()

# Design from natural language
description = "3000 sqft Ranch, 4 bed, 3 bath, 2 car garage, office"
requirements, rooms, doc = designer.design_from_description(description)

# Save outputs
designer.save_design("my_house.FCStd")
designer.export_summary("my_house_summary.txt")
```

## Architecture

Both platforms share the same 3-layer architecture:

```
┌─────────────────────────────────────────────────────────────┐
│                      USER INTERFACE                          │
│  Web: HTML/CSS/JS Canvas    |    Python: CLI/FreeCAD GUI    │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│                   AI HOUSE DESIGNER                          │
│  Orchestrates parsing, floor planning, and 3D modeling      │
└────────────────────────┬────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
┌───────▼────────┐ ┌────▼──────────┐ ┌──▼────────────────┐
│ AI PARSER      │ │ FLOOR PLAN    │ │ 3D RENDERER       │
│                │ │ GENERATOR     │ │                   │
│ • Parse NL     │ │ • Room sizes  │ │ Web: Three.js     │
│ • Extract reqs │ │ • Arrangement │ │ Python: FreeCAD   │
└────────────────┘ └───────────────┘ └───────────────────┘
```

## Testing

### Web
Open `web/index.html` and try different house descriptions.

### Python
```bash
cd python
python3 test_ai_designer.py
```

## Output Examples

### Web Version
- Interactive 3D model in browser
- 2D floor plan visualization
- Room list with color coding

### Python Version
- `[style]_house_[size]sqft.FCStd` - FreeCAD 3D model
- `house_design_summary.txt` - Detailed text summary
- `house_design.step` - STEP format for CAD interoperability

## License

This project is open source and available for educational and commercial use.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## Resources

- [Three.js Documentation](https://threejs.org/docs/)
- [FreeCAD Official Website](https://www.freecad.org/)
- [FreeCAD Python Scripting](https://wiki.freecad.org/Python_scripting_tutorial)
