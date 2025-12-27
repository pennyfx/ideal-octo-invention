/**
 * House Renderer
 * Creates 3D house models using Three.js
 */

class HouseRenderer {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.container = this.canvas.parentElement;

        // Three.js components
        this.scene = null;
        this.camera = null;
        this.renderer = null;
        this.controls = null;

        // House objects
        this.houseGroup = null;
        this.roofGroup = null;
        this.rooms = [];

        // Settings
        this.showRoof = true;
        this.wireframeMode = false;
        this.wallHeight = 2.7;  // meters
        this.wallThickness = 0.15;  // meters
        this.floorThickness = 0.1;  // meters

        // Scale factor (mm to scene units)
        this.scale = 0.001;  // 1mm = 0.001 units (so 1m = 1 unit)

        this._init();
    }

    _init() {
        // Create scene
        this.scene = new THREE.Scene();
        this.scene.background = new THREE.Color(0x1a1a2e);

        // Create camera
        const aspect = this.container.clientWidth / this.container.clientHeight;
        this.camera = new THREE.PerspectiveCamera(45, aspect, 0.1, 1000);
        this.camera.position.set(30, 25, 30);
        this.camera.lookAt(0, 0, 0);

        // Create renderer
        this.renderer = new THREE.WebGLRenderer({
            canvas: this.canvas,
            antialias: true
        });
        this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
        this.renderer.setPixelRatio(window.devicePixelRatio);
        this.renderer.shadowMap.enabled = true;
        this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;

        // Create controls
        this.controls = new THREE.OrbitControls(this.camera, this.renderer.domElement);
        this.controls.enableDamping = true;
        this.controls.dampingFactor = 0.05;
        this.controls.maxPolarAngle = Math.PI / 2;

        // Add lights
        this._addLights();

        // Add ground plane
        this._addGround();

        // Add grid helper
        const gridHelper = new THREE.GridHelper(50, 50, 0x333333, 0x222222);
        this.scene.add(gridHelper);

        // Handle window resize
        window.addEventListener('resize', () => this._onResize());

        // Start animation loop
        this._animate();
    }

    _addLights() {
        // Ambient light
        const ambient = new THREE.AmbientLight(0xffffff, 0.4);
        this.scene.add(ambient);

        // Directional light (sun)
        const sun = new THREE.DirectionalLight(0xffffff, 0.8);
        sun.position.set(20, 30, 20);
        sun.castShadow = true;
        sun.shadow.mapSize.width = 2048;
        sun.shadow.mapSize.height = 2048;
        sun.shadow.camera.near = 0.5;
        sun.shadow.camera.far = 100;
        sun.shadow.camera.left = -30;
        sun.shadow.camera.right = 30;
        sun.shadow.camera.top = 30;
        sun.shadow.camera.bottom = -30;
        this.scene.add(sun);

        // Fill light
        const fill = new THREE.DirectionalLight(0x88ccff, 0.3);
        fill.position.set(-10, 15, -10);
        this.scene.add(fill);
    }

    _addGround() {
        const groundGeometry = new THREE.PlaneGeometry(100, 100);
        const groundMaterial = new THREE.MeshStandardMaterial({
            color: 0x1a472a,
            roughness: 0.9,
        });
        const ground = new THREE.Mesh(groundGeometry, groundMaterial);
        ground.rotation.x = -Math.PI / 2;
        ground.position.y = -0.01;
        ground.receiveShadow = true;
        this.scene.add(ground);
    }

    _onResize() {
        const width = this.container.clientWidth;
        const height = this.container.clientHeight;

        this.camera.aspect = width / height;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(width, height);
    }

    _animate() {
        requestAnimationFrame(() => this._animate());
        this.controls.update();
        this.renderer.render(this.scene, this.camera);
    }

    /**
     * Clear the current house model
     */
    clearHouse() {
        if (this.houseGroup) {
            this.scene.remove(this.houseGroup);
            this.houseGroup = null;
        }
        if (this.roofGroup) {
            this.scene.remove(this.roofGroup);
            this.roofGroup = null;
        }
        this.rooms = [];
    }

    /**
     * Build a 3D house from rooms
     * @param {Room[]} rooms - Array of Room objects
     * @param {Object} houseDimensions - {length, width} in mm
     */
    buildHouse(rooms, houseDimensions) {
        this.clearHouse();
        this.rooms = rooms;

        // Create house group
        this.houseGroup = new THREE.Group();
        this.roofGroup = new THREE.Group();

        // Calculate center offset
        const centerX = (houseDimensions.length * this.scale) / 2;
        const centerZ = (houseDimensions.width * this.scale) / 2;

        // Create foundation
        this._createFoundation(houseDimensions, centerX, centerZ);

        // Create rooms
        for (const room of rooms) {
            this._createRoom(room, centerX, centerZ);
        }

        // Create roof
        this._createRoof(houseDimensions, centerX, centerZ);

        // Add to scene
        this.scene.add(this.houseGroup);
        this.scene.add(this.roofGroup);

        // Set roof visibility
        this.roofGroup.visible = this.showRoof;

        // Center camera on house
        this._focusOnHouse(houseDimensions);
    }

    _createFoundation(dimensions, centerX, centerZ) {
        const length = dimensions.length * this.scale;
        const width = dimensions.width * this.scale;

        const geometry = new THREE.BoxGeometry(length, this.floorThickness, width);
        const material = new THREE.MeshStandardMaterial({
            color: 0x4a4a4a,
            roughness: 0.8,
            wireframe: this.wireframeMode,
        });

        const foundation = new THREE.Mesh(geometry, material);
        foundation.position.set(length / 2 - centerX, this.floorThickness / 2, width / 2 - centerZ);
        foundation.castShadow = true;
        foundation.receiveShadow = true;

        this.houseGroup.add(foundation);
    }

    _createRoom(room, centerX, centerZ) {
        const x = room.x * this.scale;
        const z = room.y * this.scale;
        const length = room.length * this.scale;
        const width = room.width * this.scale;

        // Room floor
        const floorGeometry = new THREE.BoxGeometry(length, 0.02, width);
        const floorMaterial = new THREE.MeshStandardMaterial({
            color: room.color,
            roughness: 0.7,
            wireframe: this.wireframeMode,
        });
        const floor = new THREE.Mesh(floorGeometry, floorMaterial);
        floor.position.set(
            x + length / 2 - centerX,
            this.floorThickness + 0.01,
            z + width / 2 - centerZ
        );
        floor.receiveShadow = true;
        this.houseGroup.add(floor);

        // Create walls
        const wallMaterial = new THREE.MeshStandardMaterial({
            color: 0xf5f5dc,  // Beige
            roughness: 0.6,
            wireframe: this.wireframeMode,
        });

        // Wall positions: front, back, left, right
        const walls = [
            { pos: [x + length / 2 - centerX, this.floorThickness + this.wallHeight / 2, z - centerZ], size: [length, this.wallHeight, this.wallThickness] },
            { pos: [x + length / 2 - centerX, this.floorThickness + this.wallHeight / 2, z + width - centerZ], size: [length, this.wallHeight, this.wallThickness] },
            { pos: [x - centerX, this.floorThickness + this.wallHeight / 2, z + width / 2 - centerZ], size: [this.wallThickness, this.wallHeight, width] },
            { pos: [x + length - centerX, this.floorThickness + this.wallHeight / 2, z + width / 2 - centerZ], size: [this.wallThickness, this.wallHeight, width] },
        ];

        for (const wall of walls) {
            const wallGeometry = new THREE.BoxGeometry(...wall.size);
            const wallMesh = new THREE.Mesh(wallGeometry, wallMaterial.clone());
            wallMesh.position.set(...wall.pos);
            wallMesh.castShadow = true;
            wallMesh.receiveShadow = true;
            this.houseGroup.add(wallMesh);
        }

        // Add windows
        if (room.windows > 0) {
            this._addWindows(room, centerX, centerZ);
        }
    }

    _addWindows(room, centerX, centerZ) {
        const windowWidth = 1.2;
        const windowHeight = 1.2;
        const windowSill = 0.9;

        const x = room.x * this.scale;
        const z = room.y * this.scale;
        const length = room.length * this.scale;
        const width = room.width * this.scale;

        const windowMaterial = new THREE.MeshStandardMaterial({
            color: 0x87ceeb,
            transparent: true,
            opacity: 0.5,
            wireframe: this.wireframeMode,
        });

        // Add windows on back wall
        for (let i = 0; i < Math.min(room.windows, 3); i++) {
            const windowGeometry = new THREE.BoxGeometry(windowWidth, windowHeight, 0.1);
            const windowMesh = new THREE.Mesh(windowGeometry, windowMaterial);

            const spacing = length / (room.windows + 1);
            windowMesh.position.set(
                x + spacing * (i + 1) - centerX,
                this.floorThickness + windowSill + windowHeight / 2,
                z + width - centerZ + 0.1
            );

            this.houseGroup.add(windowMesh);
        }
    }

    _createRoof(dimensions, centerX, centerZ) {
        const length = dimensions.length * this.scale + 1;  // Overhang
        const width = dimensions.width * this.scale + 1;
        const roofHeight = 2;

        const roofMaterial = new THREE.MeshStandardMaterial({
            color: 0x8b4513,
            roughness: 0.7,
            side: THREE.DoubleSide,
            wireframe: this.wireframeMode,
        });

        // Create pitched roof using BufferGeometry
        const halfWidth = width / 2;
        const roofSlope = Math.sqrt(halfWidth * halfWidth + roofHeight * roofHeight);

        // Left roof plane
        const leftRoofGeometry = new THREE.PlaneGeometry(length, roofSlope);
        const leftRoof = new THREE.Mesh(leftRoofGeometry, roofMaterial);
        leftRoof.rotation.x = Math.atan2(roofHeight, halfWidth);
        leftRoof.position.set(
            0,
            this.floorThickness + this.wallHeight + roofHeight / 2,
            -halfWidth / 2
        );
        leftRoof.castShadow = true;
        this.roofGroup.add(leftRoof);

        // Right roof plane
        const rightRoofGeometry = new THREE.PlaneGeometry(length, roofSlope);
        const rightRoof = new THREE.Mesh(rightRoofGeometry, roofMaterial);
        rightRoof.rotation.x = -Math.atan2(roofHeight, halfWidth) + Math.PI;
        rightRoof.position.set(
            0,
            this.floorThickness + this.wallHeight + roofHeight / 2,
            halfWidth / 2
        );
        rightRoof.castShadow = true;
        this.roofGroup.add(rightRoof);

        // Roof ridge
        const ridgeMaterial = new THREE.MeshStandardMaterial({
            color: 0x654321,
            wireframe: this.wireframeMode,
        });
        const ridgeGeometry = new THREE.BoxGeometry(length, 0.1, 0.3);
        const ridge = new THREE.Mesh(ridgeGeometry, ridgeMaterial);
        ridge.position.set(0, this.floorThickness + this.wallHeight + roofHeight, 0);
        this.roofGroup.add(ridge);
    }

    _focusOnHouse(dimensions) {
        const length = dimensions.length * this.scale;
        const width = dimensions.width * this.scale;
        const maxDim = Math.max(length, width);

        const distance = maxDim * 1.5;
        this.camera.position.set(distance, distance * 0.7, distance);
        this.camera.lookAt(0, 2, 0);
        this.controls.target.set(0, 2, 0);
    }

    /**
     * Set camera to specific view
     * @param {string} view - 'top', 'front', 'side', 'iso'
     */
    setView(view) {
        const distance = 25;

        switch (view) {
            case 'top':
                this.camera.position.set(0, distance * 1.5, 0.01);
                break;
            case 'front':
                this.camera.position.set(0, distance * 0.4, distance);
                break;
            case 'side':
                this.camera.position.set(distance, distance * 0.4, 0);
                break;
            case 'iso':
            default:
                this.camera.position.set(distance, distance * 0.7, distance);
                break;
        }

        this.camera.lookAt(0, 2, 0);
        this.controls.target.set(0, 2, 0);
    }

    /**
     * Toggle roof visibility
     */
    toggleRoof() {
        this.showRoof = !this.showRoof;
        if (this.roofGroup) {
            this.roofGroup.visible = this.showRoof;
        }
        return this.showRoof;
    }

    /**
     * Toggle wireframe mode
     */
    toggleWireframe() {
        this.wireframeMode = !this.wireframeMode;

        // Update all materials in the scene
        this.houseGroup?.traverse((child) => {
            if (child.isMesh && child.material) {
                child.material.wireframe = this.wireframeMode;
            }
        });

        this.roofGroup?.traverse((child) => {
            if (child.isMesh && child.material) {
                child.material.wireframe = this.wireframeMode;
            }
        });

        return this.wireframeMode;
    }
}

/**
 * Floor Plan Renderer
 * Draws 2D floor plan on canvas
 */
class FloorPlanRenderer {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        this.padding = 20;
    }

    /**
     * Draw floor plan
     * @param {Room[]} rooms
     * @param {Object} dimensions - {length, width} in mm
     */
    draw(rooms, dimensions) {
        // Set canvas size
        this.canvas.width = this.canvas.parentElement.clientWidth - 40;
        this.canvas.height = 180;

        const ctx = this.ctx;
        const width = this.canvas.width;
        const height = this.canvas.height;

        // Clear canvas
        ctx.fillStyle = '#0f172a';
        ctx.fillRect(0, 0, width, height);

        if (rooms.length === 0) return;

        // Calculate scale
        const houseLength = dimensions.length;
        const houseWidth = dimensions.width;
        const scaleX = (width - 2 * this.padding) / houseLength;
        const scaleY = (height - 2 * this.padding) / houseWidth;
        const scale = Math.min(scaleX, scaleY);

        // Calculate offset to center
        const offsetX = (width - houseLength * scale) / 2;
        const offsetY = (height - houseWidth * scale) / 2;

        // Draw rooms
        for (const room of rooms) {
            const x = room.x * scale + offsetX;
            const y = room.y * scale + offsetY;
            const w = room.length * scale;
            const h = room.width * scale;

            // Room fill
            ctx.fillStyle = `#${room.color.toString(16).padStart(6, '0')}`;
            ctx.globalAlpha = 0.6;
            ctx.fillRect(x, y, w, h);
            ctx.globalAlpha = 1;

            // Room border
            ctx.strokeStyle = '#ffffff';
            ctx.lineWidth = 1;
            ctx.strokeRect(x, y, w, h);

            // Room label
            if (w > 30 && h > 20) {
                ctx.fillStyle = '#ffffff';
                ctx.font = '10px sans-serif';
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';

                // Truncate name if needed
                let name = room.name;
                if (name.length > 12 && w < 80) {
                    name = name.substring(0, 10) + '...';
                }
                ctx.fillText(name, x + w / 2, y + h / 2);
            }
        }

        // Draw scale indicator
        this._drawScaleBar(dimensions);
    }

    _drawScaleBar(dimensions) {
        const ctx = this.ctx;
        const width = this.canvas.width;
        const height = this.canvas.height;

        // Calculate 5m in screen units
        const houseLength = dimensions.length;
        const scaleX = (width - 2 * this.padding) / houseLength;
        const scaleY = (height - 2 * this.padding) / dimensions.width;
        const scale = Math.min(scaleX, scaleY);

        const fiveMeters = 5000 * scale;  // 5m = 5000mm

        // Draw scale bar
        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(10, height - 15);
        ctx.lineTo(10 + fiveMeters, height - 15);
        ctx.stroke();

        // End caps
        ctx.beginPath();
        ctx.moveTo(10, height - 20);
        ctx.lineTo(10, height - 10);
        ctx.moveTo(10 + fiveMeters, height - 20);
        ctx.lineTo(10 + fiveMeters, height - 10);
        ctx.stroke();

        // Label
        ctx.fillStyle = '#ffffff';
        ctx.font = '10px sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText('5m', 10 + fiveMeters / 2, height - 3);
    }
}

// Export
window.HouseRenderer = HouseRenderer;
window.FloorPlanRenderer = FloorPlanRenderer;
