/**
 * AI House Parser
 * Parses natural language house descriptions and extracts structured requirements
 * JavaScript port of the Python version
 */

class HouseRequirements {
    constructor() {
        this.totalSqft = 2000;
        this.style = 'Ranch';
        this.bedrooms = 3;
        this.bathrooms = 2;
        this.garageCars = 2;
        this.hasAttic = false;
        this.hasBasement = false;
        this.specialRooms = [];
        this.bathroomTypes = [];
        this.stories = 1;
    }

    toString() {
        return `HouseRequirements(sqft=${this.totalSqft}, style=${this.style}, bedrooms=${this.bedrooms}, bathrooms=${this.bathrooms})`;
    }
}

class AIHouseParser {
    constructor() {
        this.styleKeywords = {
            'ranch': 'Ranch',
            'colonial': 'Colonial',
            'victorian': 'Victorian',
            'modern': 'Modern',
            'contemporary': 'Contemporary',
            'craftsman': 'Craftsman',
            'cape cod': 'Cape Cod',
            'mediterranean': 'Mediterranean',
            'tudor': 'Tudor',
        };

        this.specialRoomKeywords = {
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
        };

        this.bathroomTypeKeywords = {
            'jack and jill': 'jack_and_jill',
            'ensuite': 'ensuite',
            'master bath': 'master',
            'half bath': 'half',
            'powder room': 'powder',
        };
    }

    /**
     * Parse a natural language house description
     * @param {string} description - Natural language description of the house
     * @returns {HouseRequirements} - Structured requirements object
     */
    parse(description) {
        const requirements = new HouseRequirements();
        const descLower = description.toLowerCase();

        // Parse square footage
        const sqftMatch = descLower.match(/(\d+)\s*(?:sq\s*ft|sqft|square\s*feet)/);
        if (sqftMatch) {
            requirements.totalSqft = parseInt(sqftMatch[1], 10);
        }

        // Parse style
        for (const [keyword, style] of Object.entries(this.styleKeywords)) {
            if (descLower.includes(keyword)) {
                requirements.style = style;
                break;
            }
        }

        // Parse bedrooms
        const bedroomMatch = descLower.match(/(\d+)\s*(?:bed|bedroom|br)/);
        if (bedroomMatch) {
            requirements.bedrooms = parseInt(bedroomMatch[1], 10);
        }

        // Parse bathrooms
        const bathroomMatch = descLower.match(/(\d+(?:\.\d+)?)\s*(?:bath|bathroom|ba)/);
        if (bathroomMatch) {
            requirements.bathrooms = parseFloat(bathroomMatch[1]);
        }

        // Parse garage
        const garageMatch = descLower.match(/(\d+)\s*(?:-?\s*)?car\s*garage/);
        if (garageMatch) {
            requirements.garageCars = parseInt(garageMatch[1], 10);
        }

        // Check for attic
        if (descLower.includes('attic')) {
            requirements.hasAttic = true;
        }

        // Check for basement
        if (descLower.includes('basement')) {
            requirements.hasBasement = true;
        }

        // Parse special rooms
        for (const [keyword, roomType] of Object.entries(this.specialRoomKeywords)) {
            if (descLower.includes(keyword)) {
                if (!requirements.specialRooms.includes(roomType)) {
                    requirements.specialRooms.push(roomType);
                }
            }
        }

        // Parse bathroom types
        for (const [keyword, bathType] of Object.entries(this.bathroomTypeKeywords)) {
            if (descLower.includes(keyword)) {
                if (!requirements.bathroomTypes.includes(bathType)) {
                    requirements.bathroomTypes.push(bathType);
                }
            }
        }

        // Parse stories
        if (descLower.includes('two story') || descLower.includes('2 story') || descLower.includes('2-story')) {
            requirements.stories = 2;
        } else if (descLower.includes('three story') || descLower.includes('3 story') || descLower.includes('3-story')) {
            requirements.stories = 3;
        } else if (descLower.includes('ranch') || descLower.includes('single story')) {
            requirements.stories = 1;
        }

        return requirements;
    }

    /**
     * Get a formatted summary of the requirements
     * @param {HouseRequirements} requirements
     * @returns {Object} - Formatted summary for display
     */
    getSummary(requirements) {
        const summary = {
            'Style': requirements.style,
            'Total Size': `${requirements.totalSqft.toLocaleString()} sq ft`,
            'Stories': requirements.stories,
            'Bedrooms': requirements.bedrooms,
            'Bathrooms': requirements.bathrooms,
            'Garage': `${requirements.garageCars} car(s)`,
        };

        if (requirements.specialRooms.length > 0) {
            summary['Special Rooms'] = requirements.specialRooms.map(r => r.replace('_', ' ')).join(', ');
        }

        if (requirements.bathroomTypes.length > 0) {
            summary['Bathroom Types'] = requirements.bathroomTypes.map(t => t.replace('_', ' ')).join(', ');
        }

        if (requirements.hasAttic) {
            summary['Attic'] = 'Yes';
        }

        if (requirements.hasBasement) {
            summary['Basement'] = 'Yes';
        }

        return summary;
    }
}

// Export for use in other modules
window.HouseRequirements = HouseRequirements;
window.AIHouseParser = AIHouseParser;
