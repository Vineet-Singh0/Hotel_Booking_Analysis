# Hotel Dashboard Configuration

# Dashboard Settings
DASHBOARD_TITLE = "Hotel Analytics Dashboard"
DASHBOARD_ICON = "🏨"
PAGE_LAYOUT = "wide"
INITIAL_SIDEBAR_STATE = "expanded"

# Color Scheme
PRIMARY_COLOR = "#1f77b4"
SECONDARY_COLOR = "#ff7f0e"
SUCCESS_COLOR = "#2ca02c"
WARNING_COLOR = "#d62728"
INFO_COLOR = "#17a2b8"

# Chart Settings
CHART_HEIGHT = 400
CHART_WIDTH = None  # Use container width
CHART_TEMPLATE = "plotly_white"

# Data Settings
DATA_FILE = "hotel_bookings.csv"
CACHE_TTL = 3600  # Cache data for 1 hour

# ML Model Settings
RANDOM_STATE = 42
TEST_SIZE = 0.2
N_ESTIMATORS = 100

# Feature Engineering
NUMERIC_FEATURES = [
    'lead_time', 'total_guests', 'total_stay', 'adr',
    'total_of_special_requests', 'booking_changes'
]

CATEGORICAL_FEATURES = [
    'hotel', 'market_segment', 'distribution_channel', 
    'customer_type', 'country'
]

# Dashboard Pages
PAGES = [
    {"name": "📊 Overview", "icon": "📊"},
    {"name": "📈 Booking Trends", "icon": "📈"},
    {"name": "💰 Revenue Analytics", "icon": "💰"},
    {"name": "🌍 Guest Demographics", "icon": "🌍"},
    {"name": "🎯 Operational Insights", "icon": "🎯"},
    {"name": "🤖 Predictive Analytics", "icon": "🤖"}
]

# Custom CSS Styles
CUSTOM_CSS = """
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #1f77b4;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #666;
        text-transform: uppercase;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
    .stButton > button {
        background-color: #1f77b4;
        color: white;
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
    }
    .stButton > button:hover {
        background-color: #1565c0;
    }
</style>
"""

# Chart Colors
CHART_COLORS = {
    'primary': '#1f77b4',
    'secondary': '#ff7f0e',
    'success': '#2ca02c',
    'warning': '#d62728',
    'info': '#17a2b8',
    'light': '#f0f2f6',
    'dark': '#2c3e50'
}

# Month Mapping
MONTH_MAP = {
    'January': 1, 'February': 2, 'March': 3, 'April': 4, 
    'May': 5, 'June': 6, 'July': 7, 'August': 8, 
    'September': 9, 'October': 10, 'November': 11, 'December': 12
}

# Month Names
MONTH_NAMES = {
    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
    7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
}

# Lead Time Bins
LEAD_TIME_BINS = {
    'labels': ['0-30 days', '31-90 days', '91-365 days', '365+ days'],
    'bins': [0, 30, 90, 365, float('inf')]
}

# Default Filters
DEFAULT_FILTERS = {
    'year': None,  # All years
    'hotel': None,  # All hotels
    'market_segment': None,  # All segments
    'customer_type': None,  # All customer types
    'country': None  # All countries
} 