/**
 * Floor Plan Generator
 * Generates room layouts based on house requirements
 * JavaScript port of the Python version
 */

class Room {
    constructor(name, sqft, roomType) {
        this.name = name;
        this.sqft = sqft;
        this.roomType = roomType;
        this.x = 0;          // Position in floor plan (mm)
        this.y = 0;
        this.width = 0;      // Dimensions (mm)
        this.length = 0;
        this.doors = [];     // Connected rooms
        this.windows = 0;    // Number of windows
        this.color = this.getColorForType(roomType);
    }

    getColorForType(roomType) {
        const colors = {
            'master_bedroom': 0x6366f1,  // Indigo
            'bedroom': 0x8b5cf6,          // Purple
            'bathroom': 0x06b6d4,         // Cyan
            'master_bathroom': 0x0891b2,  // Dark Cyan
            'jack_and_jill_bathroom': 0x14b8a6, // Teal
            'half_bathroom': 0x22d3ee,    // Light Cyan
            'kitchen': 0xf59e0b,           // Amber
            'dining_room': 0xfbbf24,       // Yellow
            'living_room': 0x22c55e,       // Green
            'garage': 0x64748b,            // Gray
            'gameroom': 0xec4899,          // Pink
            'den': 0xf472b6,               // Light Pink
            'office': 0x3b82f6,            // Blue
            'study': 0x60a5fa,             // Light Blue
            'library': 0x92400e,           // Brown
            'media_room': 0xa855f7,        // Purple
            'home_theater': 0x7c3aed,      // Violet
            'gym': 0xef4444,               // Red
            'mudroom': 0x78716c,           // Stone
            'laundry': 0xa8a29e,           // Light Stone
            'pantry': 0xd97706,            // Dark Amber
            'foyer': 0x4ade80,             // Light Green
            'hallway': 0x9ca3af,           // Gray
        };
        return colors[roomType] || 0x94a3b8;
    }

    toString() {
        return `Room(${this.name}, ${this.sqft}sqft, ${this.width}x${this.length}mm)`;
    }
}

class FloorPlanGenerator {
    constructor(requirements) {
        this.requirements = requirements;
        this.rooms = [];

        // Room size guidelines (in square feet)
        this.roomSizes = {
            'master_bedroom': 300,
            'bedroom': 150,
            'bathroom': 40,
            'jack_and_jill_bathroom': 80,
            'master_bathroom': 100,
            'half_bathroom': 25,
            'kitchen': 200,
            'living_room': 300,
            'dining_room': 150,
            'garage': 250,  // per car
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
        };
    }

    /**
     * Generate a complete floor plan
     * @returns {Room[]} - Array of Room objects
     */
    generateFloorPlan() {
        this.rooms = [];

        // Add essential rooms
        this._addBedrooms();
        this._addBathrooms();
        this._addKitchen();
        this._addLivingAreas();
        this._addGarage();
        this._addSpecialRooms();
        this._addCirculationSpaces();

        // Calculate room dimensions
        this._calculateRoomDimensions();

        // Arrange rooms in floor plan
        this._arrangeRooms();

        return this.rooms;
    }

    _addBedrooms() {
        // Master bedroom
        const master = new Room('Master Bedroom', this.roomSizes['master_bedroom'], 'master_bedroom');
        master.windows = 2;
        this.rooms.push(master);

        // Additional bedrooms
        for (let i = 0; i < this.requirements.bedrooms - 1; i++) {
            const bedroom = new Room(`Bedroom ${i + 2}`, this.roomSizes['bedroom'], 'bedroom');
            bedroom.windows = 1;
            this.rooms.push(bedroom);
        }
    }

    _addBathrooms() {
        let bathroomCount = Math.floor(this.requirements.bathrooms);
        const halfBathCount = (this.requirements.bathrooms % 1 >= 0.5) ? 1 : 0;

        // Master bathroom
        const masterBath = new Room('Master Bathroom', this.roomSizes['master_bathroom'], 'master_bathroom');
        masterBath.windows = 1;
        this.rooms.push(masterBath);
        bathroomCount--;

        // Jack and Jill bathroom if specified
        if (this.requirements.bathroomTypes.includes('jack_and_jill') && bathroomCount > 0) {
            const jnjBath = new Room('Jack and Jill Bathroom', this.roomSizes['jack_and_jill_bathroom'], 'jack_and_jill_bathroom');
            jnjBath.windows = 1;
            this.rooms.push(jnjBath);
            bathroomCount--;
        }

        // Additional full bathrooms
        for (let i = 0; i < bathroomCount; i++) {
            const bathroom = new Room(`Bathroom ${i + 2}`, this.roomSizes['bathroom'], 'bathroom');
            bathroom.windows = 1;
            this.rooms.push(bathroom);
        }

        // Half bathrooms
        for (let i = 0; i < halfBathCount; i++) {
            const halfBath = new Room('Powder Room', this.roomSizes['half_bathroom'], 'half_bathroom');
            halfBath.windows = 0;
            this.rooms.push(halfBath);
        }
    }

    _addKitchen() {
        const kitchen = new Room('Kitchen', this.roomSizes['kitchen'], 'kitchen');
        kitchen.windows = 2;
        this.rooms.push(kitchen);

        const dining = new Room('Dining Room', this.roomSizes['dining_room'], 'dining_room');
        dining.windows = 1;
        this.rooms.push(dining);
    }

    _addLivingAreas() {
        const living = new Room('Living Room', this.roomSizes['living_room'], 'living_room');
        living.windows = 3;
        this.rooms.push(living);
    }

    _addGarage() {
        if (this.requirements.garageCars > 0) {
            const garageSize = this.roomSizes['garage'] * this.requirements.garageCars;
            const garage = new Room(`${this.requirements.garageCars} Car Garage`, garageSize, 'garage');
            garage.windows = 0;
            this.rooms.push(garage);
        }
    }

    _addSpecialRooms() {
        for (const roomType of this.requirements.specialRooms) {
            if (this.roomSizes[roomType]) {
                const roomName = roomType.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
                const room = new Room(roomName, this.roomSizes[roomType], roomType);
                room.windows = 1;
                this.rooms.push(room);
            }
        }
    }

    _addCirculationSpaces() {
        const foyer = new Room('Foyer', this.roomSizes['foyer'], 'foyer');
        foyer.windows = 0;
        this.rooms.push(foyer);

        // Add hallways if needed
        if (this.requirements.bedrooms >= 3) {
            const hallway = new Room('Hallway', this.roomSizes['hallway'], 'hallway');
            hallway.windows = 0;
            this.rooms.push(hallway);
        }
    }

    _calculateRoomDimensions() {
        const SQFT_TO_MM2 = 92903.04;  // 1 sqft = 92903.04 mm²

        for (const room of this.rooms) {
            // Use reasonable aspect ratios for different room types
            let aspectRatio;
            if (room.roomType === 'garage') {
                aspectRatio = 1.5;  // Garages are deeper than wide
            } else if (['hallway', 'mudroom'].includes(room.roomType)) {
                aspectRatio = 3.0;  // Long and narrow
            } else if (['master_bedroom', 'living_room'].includes(room.roomType)) {
                aspectRatio = 1.2;  // More square
            } else {
                aspectRatio = 1.3;  // Default
            }

            // Calculate dimensions
            const areaMm2 = room.sqft * SQFT_TO_MM2;
            room.width = Math.floor(Math.sqrt(areaMm2 / aspectRatio));
            room.length = Math.floor(areaMm2 / room.width);
        }
    }

    _arrangeRooms() {
        if (this.rooms.length === 0) return;

        // Sort rooms by size (largest first)
        const sortedRooms = [...this.rooms].sort((a, b) => b.sqft - a.sqft);

        // Calculate total area
        const totalArea = this.rooms.reduce((sum, r) => sum + r.sqft, 0);

        // Scale if specified square footage is larger
        if (this.requirements.totalSqft > totalArea) {
            const scaleFactor = Math.sqrt(this.requirements.totalSqft / totalArea);
            for (const room of this.rooms) {
                room.width = Math.floor(room.width * scaleFactor);
                room.length = Math.floor(room.length * scaleFactor);
            }
        }

        // Simple row-based layout
        const SQFT_TO_MM2 = 92903.04;
        let currentX = 0;
        let currentY = 0;
        let rowHeight = 0;
        const maxWidth = Math.floor(Math.sqrt(this.requirements.totalSqft * SQFT_TO_MM2) * 1.3);

        for (const room of sortedRooms) {
            if (currentX + room.length > maxWidth && currentX > 0) {
                // Start new row
                currentX = 0;
                currentY += rowHeight + 200;  // 200mm gap for walls
                rowHeight = 0;
            }

            room.x = currentX;
            room.y = currentY;

            currentX += room.length + 200;  // 200mm gap for walls
            rowHeight = Math.max(rowHeight, room.width);
        }
    }

    /**
     * Get overall house dimensions
     * @returns {Object} - {length, width} in mm
     */
    getHouseDimensions() {
        if (this.rooms.length === 0) {
            return { length: 10000, width: 8000 };
        }

        const maxX = Math.max(...this.rooms.map(r => r.x + r.length));
        const maxY = Math.max(...this.rooms.map(r => r.y + r.width));

        return {
            length: maxX + 1000,  // Add margin
            width: maxY + 1000
        };
    }

    /**
     * Get summary statistics
     * @returns {Object}
     */
    getSummary() {
        const totalSqft = this.rooms.reduce((sum, r) => sum + r.sqft, 0);
        const dims = this.getHouseDimensions();

        return {
            totalRooms: this.rooms.length,
            totalArea: Math.round(totalSqft),
            dimensions: `${(dims.length / 1000).toFixed(1)}m x ${(dims.width / 1000).toFixed(1)}m`,
        };
    }
}

// Export for use in other modules
window.Room = Room;
window.FloorPlanGenerator = FloorPlanGenerator;
