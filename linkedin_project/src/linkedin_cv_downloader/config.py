"""
Configuration settings for LinkedIn CV Downloader
"""

# Browser settings
BROWSER_CONFIG = {
    'headless': False,
    'viewport': {'width': 1920, 'height': 1080},
    'user_agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'locale': 'es-ES',
    'timezone': 'America/Argentina/Buenos_Aires',
}

# Browser launch arguments
BROWSER_ARGS = [
    '--disable-blink-features=AutomationControlled',
    '--disable-dev-shm-usage',
    '--no-sandbox',
    '--disable-web-security',
    '--disable-features=IsolateOrigins,site-per-process'
]

# Anti-detection script
ANTI_DETECTION_SCRIPT = """
    // Remove webdriver property
    Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined
    });
    
    // Add chrome object
    window.chrome = {
        runtime: {},
        loadTimes: function() {},
        csi: function() {},
        app: {}
    };
    
    // Permissions
    const originalQuery = window.navigator.permissions.query;
    window.navigator.permissions.query = (parameters) => (
        parameters.name === 'notifications' ?
            Promise.resolve({ state: Notification.permission }) :
            originalQuery(parameters)
    );
    
    // Plugins
    Object.defineProperty(navigator, 'plugins', {
        get: () => [1, 2, 3, 4, 5]
    });
    
    // Languages
    Object.defineProperty(navigator, 'languages', {
        get: () => ['es-ES', 'es', 'en-US', 'en']
    });
"""

# Selectors for LinkedIn elements
SELECTORS = {
    'more_button': [
        'button[aria-label="More actions"]',
        'button[aria-label="Más acciones"]',
        'button:has-text("More")',
        'button:has-text("Más")'
    ],
    'save_to_pdf': [
        'div[aria-label="Save to PDF"]',
        'div[aria-label="Guardar como PDF"]',
        'text="Save to PDF"',
        'text="Guardar como PDF"',
        '.artdeco-dropdown__item:has-text("Save to PDF")',
        '.artdeco-dropdown__item:has-text("Guardar como PDF")'
    ],
    'navigation': 'nav[aria-label="Primary Navigation"]'
}

# Timing configuration (in milliseconds)
TIMING = {
    'page_load': (2000, 3500),
    'reading': (1500, 3000),
    'thinking': (500, 1200),
    'click_delay': (200, 500),
    'hover': (100, 300),
    'menu_open': (800, 1500),
    'pdf_generation': (4000, 7000),
    'between_profiles': (8000, 15000)
}

# Download settings
DOWNLOAD_DIR = "downloads/cvs"
DEBUG_SCREENSHOT_DIR = "downloads/debug"
