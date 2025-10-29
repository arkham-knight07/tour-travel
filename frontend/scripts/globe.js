// 🌍 Globe.js - Interactive 3D Globe with Backend Integration

// API Configuration
const API_BASE_URL = 'http://localhost:5002';

// Place data will be loaded from backend
let PLACES = [];

// Color scheme for place types
const MARKER_COLORS = {
    destination: '#ff6b6b',    // Red
    trek: '#4ecdc4',           // Cyan
    international: '#ffd93d',  // Yellow
};

// Globe instance
let globeInstance;
let currentPlace = null;

// Initialize globe on page load
window.addEventListener('DOMContentLoaded', async () => {
    console.log('🚀 Globe initializing...');
    await loadPlacesFromAPI();
    initGlobe();
});

/**
 * Fetch places from backend API
 */
async function loadPlacesFromAPI() {
    try {
        console.log('📡 Fetching places from API...');
        const response = await fetch(`${API_BASE_URL}/api/places?limit=100`);
        
        if (!response.ok) {
            throw new Error(`API Error: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.places && Array.isArray(data.places)) {
            PLACES = data.places.map(place => ({
                id: place.id,
                name: place.name,
                type: place.category,
                lat: place.latitude,
                lng: place.longitude,
                description: place.description,
                image: place.image_url || '../assets/images/destinations/bali.jpg',
                price: place.price,
                rating: place.rating,
                review_count: place.review_count,
            }));
            console.log(`✅ Loaded ${PLACES.length} places from API`);
        } else {
            throw new Error('Invalid API response format');
        }
    } catch (error) {
        console.error('❌ Failed to load places from API:', error);
        console.warn('⚠️  Using fallback data...');
        loadFallbackPlaces();
    }
}

/**
 * Fallback places (in case API is not available)
 */
function loadFallbackPlaces() {
    PLACES = [
        // Domestic Destinations
        {
            id: 'goa',
            name: 'Goa, India',
            type: 'destination',
            lat: 15.2993,
            lng: 73.8243,
            description: 'Beautiful beaches, vibrant nightlife, and Portuguese heritage.',
            image: '../assets/images/destinations/goa.jpg',
            price: '₹8,999',
            rating: 4.5,
            review_count: 128,
        },
        {
            id: 'manali',
            name: 'Manali, India',
            type: 'destination',
            lat: 32.2396,
            lng: 77.1887,
            description: 'Snow-capped mountains, adventure sports, and hill station charm.',
            image: '../assets/images/destinations/manali.jpg',
            price: '₹12,999',
            rating: 4.7,
            review_count: 95,
        },
        {
            id: 'kerala',
            name: 'Kerala, India',
            type: 'destination',
            lat: 10.8505,
            lng: 76.2711,
            description: 'Backwaters, houseboats, spices, and God\'s own country.',
            image: '../assets/images/destinations/kerala.jpg',
            price: '₹15,999',
            rating: 4.6,
            review_count: 142,
        },
        {
            id: 'ladakh',
            name: 'Ladakh, India',
            type: 'destination',
            lat: 34.1526,
            lng: 77.5771,
            description: 'High altitude desert, monasteries, and breathtaking landscapes.',
            image: '../assets/images/destinations/ladakh.jpg',
            price: '₹25,999',
            rating: 4.8,
            review_count: 67,
        },
        {
            id: 'jaipur',
            name: 'Jaipur, India',
            type: 'destination',
            lat: 26.9124,
            lng: 75.7873,
            description: 'Pink city, royal palaces, and rich Rajasthani culture.',
            image: '../assets/images/destinations/jaipur.jpg',
            price: '₹10,999',
            rating: 4.4,
            review_count: 110,
        },
        // Treks
        {
            id: 'everest',
            name: 'Everest Base Camp Trek',
            type: 'trek',
            lat: 28.0,
            lng: 86.85,
            description: 'The iconic trek to Mount Everest Base Camp in Nepal.',
            image: '../assets/images/treks/everest.jpg',
            price: '₹45,999',
            rating: 4.9,
            review_count: 203,
        },
        {
            id: 'hampta',
            name: 'Hampta Pass Trek',
            type: 'trek',
            lat: 32.2,
            lng: 77.3,
            description: 'A scenic trek through the Himalayas connecting Himachal Pradesh.',
            image: '../assets/images/treks/hampta.jpg',
            price: '₹12,999',
            rating: 4.6,
            review_count: 85,
        },
        {
            id: 'sandakphu',
            name: 'Sandakphu Trek',
            type: 'trek',
            lat: 27.33,
            lng: 88.15,
            description: 'Trek to the highest peak in West Bengal with stunning mountain views.',
            image: '../assets/images/treks/sandakphu.jpg',
            price: '₹15,999',
            rating: 4.5,
            review_count: 72,
        },
        // International Destinations
        {
            id: 'bali',
            name: 'Bali, Indonesia',
            type: 'international',
            lat: -8.6705,
            lng: 115.2126,
            description: 'Tropical paradise, temples, rice terraces, and beach resorts.',
            image: '../assets/images/destinations/bali.jpg',
            price: '₹45,999',
            rating: 4.7,
            review_count: 256,
        },
        {
            id: 'paris',
            name: 'Paris, France',
            type: 'international',
            lat: 48.8566,
            lng: 2.3522,
            description: 'The City of Light. Iconic landmarks, world-class museums, and romantic charm.',
            image: '../assets/images/destinations/paris.jpg',
            price: '₹85,999',
            rating: 4.8,
            review_count: 312,
        },
        {
            id: 'newyork',
            name: 'New York, USA',
            type: 'international',
            lat: 40.7128,
            lng: -74.0060,
            description: 'The city that never sleeps. Skyscrapers, Broadway shows, and world-famous attractions.',
            image: '../assets/images/destinations/newyork.jpg',
            price: '₹95,999',
            rating: 4.6,
            review_count: 289,
        },
    ];
    console.log(`✅ Loaded ${PLACES.length} fallback places`);
}

/**
 * Initialize 3D Globe
 */
function initGlobe() {
    try {
        if (PLACES.length === 0) {
            console.error('❌ No places to display on globe');
            return;
        }

        // Get canvas element
        const canvas = document.getElementById('globeViz');
        if (!canvas) {
            console.error('❌ Canvas element not found!');
            return;
        }

        console.log('🌐 Creating globe with Three.js...');

        // Initialize Globe.gl
        globeInstance = Globe()
            .globeImageUrl('../assets/images/hero.jpg')
            .bumpImageUrl('https://unpkg.com/three-globe/examples/img/earth_bump.200401.tif')
            .backgroundColor('rgba(26, 26, 46, 0)')
            (canvas);

        // Prepare points data
        const pointsData = PLACES.map(place => ({
            lat: place.lat,
            lng: place.lng,
            size: 0.8,
            color: MARKER_COLORS[place.type] || '#ffffff',
            place: place,
        }));

        // Add points to globe
        globeInstance
            .pointsData(pointsData)
            .pointAltitude(0.01)
            .pointColor('color')
            .pointSize('size')
            .pointLabel(d => `<div style="background: rgba(26,26,46,0.95); padding:10px 14px; border-radius:8px; font-size:13px; color:#eaeaea; font-weight:500; border: 1px solid rgba(255,255,255,0.2);">${d.place.name}</div>`)
            .onPointHover(d => {
                if (d) {
                    showPlaceDetails(d.place);
                    globeInstance.pointOfView({ lat: d.lat, lng: d.lng, altitude: 1.5 }, 300);
                } else {
                    document.getElementById('placeDetails').classList.remove('active');
                }
            })
            .onPointClick(d => {
                if (d) {
                    showPlaceDetails(d.place);
                    currentPlace = d.place;
                }
            });

        // Auto-rotate globe
        globeInstance.controls().autoRotate = true;
        globeInstance.controls().autoRotateSpeed = 0.5;

        // Handle window resize
        window.addEventListener('resize', () => {
            globeInstance.width(window.innerWidth).height(window.innerHeight);
        });

        console.log(`✅ Globe initialized with ${pointsData.length} markers`);

    } catch (error) {
        console.error('❌ Globe initialization error:', error);
    }
}

/**
 * Display place details in the panel
 */
function showPlaceDetails(place) {
    try {
        const detailsPanel = document.getElementById('placeDetails');
        const bgColor = MARKER_COLORS[place.type] || '#ffffff';

        document.getElementById('placeName').textContent = place.name;
        document.getElementById('placeCategory').textContent = place.type?.toUpperCase() || 'UNKNOWN';
        document.getElementById('placeCategory').style.background = `${bgColor}33`;
        document.getElementById('placeCategory').style.color = bgColor;
        
        // Handle image fallback
        const img = document.getElementById('placeImage');
        img.src = place.image || '../assets/images/destinations/bali.jpg';
        img.onerror = () => {
            img.src = '../assets/images/destinations/bali.jpg';
        };

        document.getElementById('placeDescription').textContent = place.description || 'No description available';
        document.getElementById('placeCoords').textContent = `📍 ${place.lat.toFixed(4)}°N, ${place.lng.toFixed(4)}°E`;
        
        // Show rating if available
        const ratingEl = document.getElementById('placeRating');
        if (ratingEl && place.rating) {
            ratingEl.textContent = `⭐ ${place.rating} (${place.review_count} reviews)`;
        }

        detailsPanel.classList.add('active');
        currentPlace = place;

    } catch (error) {
        console.error('❌ Error showing place details:', error);
    }
}

/**
 * Search for a place
 */
function searchPlace() {
    try {
        const query = document.getElementById('placeSearch').value.toLowerCase().trim();
        
        if (!query) {
            console.warn('⚠️  Search query is empty');
            return;
        }

        const found = PLACES.find(p => 
            p.name.toLowerCase().includes(query) || 
            p.description.toLowerCase().includes(query)
        );

        if (found) {
            showPlaceDetails(found);
            globeInstance.pointOfView({ lat: found.lat, lng: found.lng, altitude: 1.5 }, 800);
            document.getElementById('placeSearch').value = '';
        } else {
            alert(`❌ Place not found: "${query}"\n\n💡 Try searching for: Goa, Manali, Kerala, Bali, Paris, etc.`);
        }
    } catch (error) {
        console.error('❌ Search error:', error);
    }
}

/**
 * Zoom in
 */
function zoomIn() {
    try {
        const pov = globeInstance.pointOfView();
        globeInstance.pointOfView(
            { ...pov, altitude: Math.max(0.5, pov.altitude - 0.5) },
            300
        );
    } catch (error) {
        console.error('❌ Zoom in error:', error);
    }
}

/**
 * Zoom out
 */
function zoomOut() {
    try {
        const pov = globeInstance.pointOfView();
        globeInstance.pointOfView(
            { ...pov, altitude: pov.altitude + 0.5 },
            300
        );
    } catch (error) {
        console.error('❌ Zoom out error:', error);
    }
}

/**
 * Reset globe to initial state
 */
function resetGlobe() {
    try {
        globeInstance.pointOfView({ lat: 0, lng: 0, altitude: 3 }, 1000);
        document.getElementById('placeDetails').classList.remove('active');
        globeInstance.controls().autoRotate = true;
    } catch (error) {
        console.error('❌ Reset error:', error);
    }
}

/**
 * Explore selected place (go to destination page)
 */
function goToDestination() {
    if (currentPlace) {
        window.location.href = `destinations.html?place=${currentPlace.id}`;
    }
}

// Log initialization
console.log('✅ Globe.js loaded and ready\n🌐 Connecting to API at ' + API_BASE_URL);
