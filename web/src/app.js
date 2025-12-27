/**
 * AI House Designer - Main Application
 * Orchestrates the parser, floor plan generator, and 3D renderer
 */

class AIHouseDesignerApp {
    constructor() {
        // Initialize components
        this.parser = new AIHouseParser();
        this.houseRenderer = new HouseRenderer('house-canvas');
        this.floorPlanRenderer = new FloorPlanRenderer('floor-plan-canvas');

        // State
        this.requirements = null;
        this.rooms = [];
        this.houseDimensions = null;

        // Bind event handlers
        this._bindEvents();

        // Show initial state
        console.log('AI House Designer initialized');
    }

    _bindEvents() {
        // Generate button
        document.getElementById('generate-btn').addEventListener('click', () => {
            this._handleGenerate();
        });

        // Example buttons
        document.querySelectorAll('.btn-example').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const description = e.target.dataset.desc;
                document.getElementById('description').value = description;
                this._handleGenerate();
            });
        });

        // View controls
        document.getElementById('view-top').addEventListener('click', () => this._setView('top'));
        document.getElementById('view-front').addEventListener('click', () => this._setView('front'));
        document.getElementById('view-side').addEventListener('click', () => this._setView('side'));
        document.getElementById('view-iso').addEventListener('click', () => this._setView('iso'));

        // Toggle controls
        document.getElementById('toggle-roof').addEventListener('click', (e) => {
            const isVisible = this.houseRenderer.toggleRoof();
            e.target.classList.toggle('active', isVisible);
        });

        document.getElementById('toggle-wireframe').addEventListener('click', (e) => {
            const isWireframe = this.houseRenderer.toggleWireframe();
            e.target.classList.toggle('active', isWireframe);
        });

        // Textarea enter key
        document.getElementById('description').addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this._handleGenerate();
            }
        });

        // Window resize for floor plan
        window.addEventListener('resize', () => {
            if (this.rooms.length > 0) {
                this.floorPlanRenderer.draw(this.rooms, this.houseDimensions);
            }
        });
    }

    _handleGenerate() {
        const description = document.getElementById('description').value.trim();

        if (!description) {
            alert('Please enter a house description');
            return;
        }

        console.log('Generating house from:', description);

        // Step 1: Parse the description
        this.requirements = this.parser.parse(description);
        console.log('Parsed requirements:', this.requirements);

        // Update requirements display
        this._updateRequirementsDisplay();

        // Step 2: Generate floor plan
        const generator = new FloorPlanGenerator(this.requirements);
        this.rooms = generator.generateFloorPlan();
        this.houseDimensions = generator.getHouseDimensions();
        console.log('Generated rooms:', this.rooms);
        console.log('House dimensions:', this.houseDimensions);

        // Update rooms display
        this._updateRoomsDisplay();

        // Step 3: Build 3D model
        this.houseRenderer.buildHouse(this.rooms, this.houseDimensions);

        // Step 4: Draw 2D floor plan
        this.floorPlanRenderer.draw(this.rooms, this.houseDimensions);

        // Reset view to isometric
        this._setView('iso');
    }

    _updateRequirementsDisplay() {
        const container = document.getElementById('requirements-content');
        const summary = this.parser.getSummary(this.requirements);

        let html = '';
        for (const [label, value] of Object.entries(summary)) {
            html += `
                <div class="requirement-item">
                    <span class="requirement-label">${label}:</span>
                    <span class="requirement-value">${value}</span>
                </div>
            `;
        }

        container.innerHTML = html;
    }

    _updateRoomsDisplay() {
        const container = document.getElementById('rooms-content');

        let html = `<div class="room-item" style="font-weight: bold; border-bottom: 2px solid var(--surface-light);">
            <span class="room-name">Total Rooms: ${this.rooms.length}</span>
            <span class="room-size">${Math.round(this.rooms.reduce((sum, r) => sum + r.sqft, 0))} sq ft</span>
        </div>`;

        for (const room of this.rooms) {
            const colorHex = room.color.toString(16).padStart(6, '0');
            html += `
                <div class="room-item">
                    <span class="room-name">
                        <span class="room-color" style="background-color: #${colorHex}"></span>
                        ${room.name}
                    </span>
                    <span class="room-size">${Math.round(room.sqft)} sq ft</span>
                </div>
            `;
        }

        container.innerHTML = html;
    }

    _setView(view) {
        // Update button states
        document.querySelectorAll('.btn-view').forEach(btn => {
            btn.classList.remove('active');
        });
        document.getElementById(`view-${view}`).classList.add('active');

        // Set camera view
        this.houseRenderer.setView(view);
    }
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.app = new AIHouseDesignerApp();

    // Generate a default house on load
    setTimeout(() => {
        document.getElementById('description').value = '2500 sqft Ranch style, 3 bedrooms, 2 bathrooms, 2 car garage';
        document.getElementById('generate-btn').click();
    }, 500);
});
