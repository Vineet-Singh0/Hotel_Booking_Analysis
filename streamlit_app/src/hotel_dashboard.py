import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
from datetime import datetime, timedelta
import warnings
import os
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Hotel Dashboard",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling (commented out for alignment fix)
# st.markdown("""
# <style>
#     .main-header {
#         font-size: 2.5rem;
#         font-weight: bold;
#         color: #1f77b4;
#         text-align: center;
#         margin-bottom: 2rem;
#     }
#     .metric-card {
#         background-color: #f0f2f6;
#         padding: 1rem;
#         border-radius: 0.5rem;
#         border-left: 4px solid #1f77b4;
#     }
#     .metric-value {
#         font-size: 1.7rem;
#         font-weight: bold;
#         color: #1f77b4;
#     }
#     .metric-label {
#         font-size: 0.9rem;
#         color: #666;
#         text-transform: uppercase;
#     }
#     .sidebar .sidebar-content {
#         background-color: #f8f9fa;
#     }
# </style>
# """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and preprocess hotel booking data"""
    try:
        # Get the correct path to data file
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        data_path = os.path.join(project_root, 'data', 'hotel_bookings.csv')
        df = pd.read_csv(data_path)
        
        # Data cleaning
        df['children'].fillna(0, inplace=True)
        df['country'].fillna('Unknown', inplace=True)
        df['agent'].fillna(0, inplace=True)
        df['company'].fillna(0, inplace=True)
        
        # Convert data types
        df['children'] = df['children'].astype(int)
        df['agent'] = df['agent'].astype(int)
        df['company'] = df['company'].astype(int)
        
        # Create derived features
        df['total_guests'] = df['adults'] + df['children'] + df['babies']
        df['total_stay'] = df['stays_in_weekend_nights'] + df['stays_in_week_nights']
        df['booking_success'] = np.where(df['is_canceled'] == 0, 1, 0)
        df['room_mismatch'] = np.where(df['reserved_room_type'] != df['assigned_room_type'], 1, 0)
        
        # Convert date columns
        df['reservation_status_date'] = pd.to_datetime(df['reservation_status_date'])
        
        # Month mapping
        month_map = {
            'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
            'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12
        }
        df['arrival_month'] = df['arrival_date_month'].map(month_map)
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

def main():
    """Main dashboard application"""
    
    # Load data
    df = load_data()
    if df is None:
        st.error("Failed to load data. Please check if 'hotel_bookings.csv' exists.")
        return
    
    # Sidebar navigation with all options visible
    st.sidebar.image('https://img.icons8.com/ios-filled/100/1f77b4/hotel.png', width=60)
    st.sidebar.title("🏨 Hotel Dashboard")
    st.sidebar.info("""
**About:**
- Author: Vineet Singh
- Data: hotel_bookings.csv

""")
    # --- Clean Sidebar Navigation: Only Streamlit Buttons with Icons ---
    st.sidebar.markdown("### Navigation")

    if "page" not in st.session_state:
        st.session_state.page = "Summary"

    def nav_button(label, key, icon):
        active = st.session_state.page == key
        btn_label = f"{icon} **{label}**" if active else f"{icon} {label}"
        if st.sidebar.button(btn_label, key=f"btn_{key}"):
            st.session_state.page = key

    nav_button("Summary", "Summary", "🏠")
    nav_button("Booking Patterns", "Booking Patterns", "📈")
    nav_button("Revenue", "Revenue", "💰")
    nav_button("Guest Profiles", "Guest Profiles", "👤")
    nav_button("Operations", "Operations", "⚙️")
    nav_button("Cancellation Prediction", "Cancellation Prediction", "❓")

    # Page routing
    page = st.session_state.page
    if page == "Summary":
        show_summary(df)
    elif page == "Booking Patterns":
        show_booking_patterns(df)
    elif page == "Revenue":
        show_revenue(df)
    elif page == "Guest Profiles":
        show_guest_profiles(df)
    elif page == "Operations":
        show_operations(df)
    elif page == "Cancellation Prediction":
        show_cancellation_prediction(df)

def show_summary(df):
    """Overview dashboard with key metrics (robust alignment, card design)"""
    with st.container():
        st.markdown('<h1 style="font-size:2.5rem;font-weight:bold;color:#1f77b4;text-align:center;margin-bottom:2rem;">Hotel Booking Summary</h1>', unsafe_allow_html=True)
        st.markdown("""
**Summary:** A quick look at the most important numbers for your hotel bookings.
""")
        # Expander for explanations (full width)
        with st.expander("What do these numbers mean?"):
            st.write("""
- **Total Bookings:** How many bookings are in the data.
- **Average Room Price:** The average price paid per room (ADR).
- **Cancellation Rate:** What percent of bookings were cancelled.
- **Days Booked in Advance:** How far ahead people book on average.
            """)

        # Key metrics as attractive cards (single row)
        total_bookings = len(df)
        avg_adr = df['adr'].mean()
        cancellation_rate = (df['is_canceled'].sum() / len(df)) * 100
        avg_lead_time = df['lead_time'].mean()
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f'''
                <div style="background-color:#e3f2fd;padding:20px 10px 10px 10px;border-radius:12px;box-shadow:0 2px 8px #e3f2fd;text-align:center;">
                    <div style="font-size:1.1rem;color:#1565c0;font-weight:600;margin-bottom:8px;">Total Bookings</div>
                    <div style="font-size:2.2rem;font-weight:bold;color:#1565c0;">{total_bookings:,}</div>
                </div>
            ''', unsafe_allow_html=True)
        with col2:
            st.markdown(f'''
                <div style="background-color:#e3f2fd;padding:20px 10px 10px 10px;border-radius:12px;box-shadow:0 2px 8px #e3f2fd;text-align:center;">
                    <div style="font-size:1.1rem;color:#1565c0;font-weight:600;margin-bottom:8px;">Average Room Price</div>
                    <div style="font-size:2.2rem;font-weight:bold;color:#1565c0;">${avg_adr:.0f}</div>
                </div>
            ''', unsafe_allow_html=True)
        with col3:
            st.markdown(f'''
                <div style="background-color:#e3f2fd;padding:20px 10px 10px 10px;border-radius:12px;box-shadow:0 2px 8px #e3f2fd;text-align:center;">
                    <div style="font-size:1.1rem;color:#1565c0;font-weight:600;margin-bottom:8px;">Cancellation Rate</div>
                    <div style="font-size:2.2rem;font-weight:bold;color:#1565c0;">{cancellation_rate:.1f}%</div>
                </div>
            ''', unsafe_allow_html=True)
        with col4:
            st.markdown(f'''
                <div style="background-color:#e3f2fd;padding:20px 10px 10px 10px;border-radius:12px;box-shadow:0 2px 8px #e3f2fd;text-align:center;">
                    <div style="font-size:1.1rem;color:#1565c0;font-weight:600;margin-bottom:8px;">Days Booked in Advance</div>
                    <div style="font-size:2.2rem;font-weight:bold;color:#1565c0;">{avg_lead_time:.0f} days</div>
                </div>
            ''', unsafe_allow_html=True)

        st.write("")  # Add vertical space between metric cards and info box

        # Info box (full width, below metrics)
        st.info("Average Room Price is the average paid per room. Days Booked in Advance is how far ahead people book.")

        # Charts row (new, balanced columns)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Room Price Distribution:** How much do guests pay per room?")
            fig_adr = px.histogram(df, x='adr', nbins=50, 
                                  title="Room Price Distribution",
                                  labels={'adr': 'Room Price ($)', 'count': 'Number of Bookings'})
            fig_adr.update_layout(height=400)
            st.plotly_chart(fig_adr, use_container_width=True)
            with st.expander("What is Average Room Price?"):
                st.write("""
This is the average price paid per room (ADR). Higher values mean higher pricing or premium bookings.
                """)
        with col2:
            st.markdown("**How far ahead do guests book?**")
            fig_lead = px.histogram(df, x='lead_time', nbins=50,
                                   title="Days Booked in Advance",
                                   labels={'lead_time': 'Days in Advance', 'count': 'Number of Bookings'})
            fig_lead.update_layout(height=400)
            st.plotly_chart(fig_lead, use_container_width=True)
            with st.expander("What is Days Booked in Advance?"):
                st.write("""
This is the number of days between when a booking is made and the guest's arrival date.
                """)

        # Market Segment Analysis (unchanged, but outside the above containers)
        st.subheader("Booking Source Comparison")
        st.markdown("**Average Room Price by Booking Source:** See which sources bring in the most revenue.")
        segment_stats = df.groupby('market_segment').agg({
            'adr': 'mean',
            'is_canceled': 'mean',
            'lead_time': 'mean'
        }).round(2)
        fig_segment = px.bar(segment_stats, y='adr', 
                             title="Average Room Price by Booking Source",
                             labels={'adr': 'Room Price ($)', 'market_segment': 'Booking Source'})
        fig_segment.update_layout(height=400)
        st.plotly_chart(fig_segment, use_container_width=True)
        with st.expander("What is a Booking Source?"):
            st.write("""
A booking source is how the guest made the booking (e.g., Online Travel Agent, Direct, Corporate).
            """)

        st.markdown("---")
        st.subheader("Business Intelligence Highlights")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Top 10 Countries by Revenue**")
            country_revenue = df.groupby('country').apply(lambda x: (x['adr'] * (x['stays_in_weekend_nights'] + x['stays_in_week_nights'])).sum()).sort_values(ascending=False).head(10).reset_index(name='revenue')
            fig_country_rev = px.bar(country_revenue, x='revenue', y='country', orientation='h',
                                    title='Top 10 Countries by Revenue', labels={'revenue': 'Revenue', 'country': 'Country'})
            st.plotly_chart(fig_country_rev, use_container_width=True)
            with st.expander("What does this chart show?"):
                st.write("Shows the countries that bring in the most revenue.")
        with col2:
            st.markdown("**Top 10 Market Segments by Revenue**")
            segment_revenue = df.groupby('market_segment').apply(lambda x: (x['adr'] * (x['stays_in_weekend_nights'] + x['stays_in_week_nights'])).sum()).sort_values(ascending=False).head(10).reset_index(name='revenue')
            fig_segment_rev = px.bar(segment_revenue, x='revenue', y='market_segment', orientation='h',
                                     title='Top 10 Market Segments by Revenue', labels={'revenue': 'Revenue', 'market_segment': 'Market Segment'})
            st.plotly_chart(fig_segment_rev, use_container_width=True)
            with st.expander("What does this chart show?"):
                st.write("Shows which booking sources/segments are most profitable.")
        st.info("Use these charts to target your best markets and segments.")

        st.markdown("---")
        st.subheader("Cohort & Retention Analysis")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Monthly Bookings by Guest Type**")
            df['month'] = df['reservation_status_date'].dt.to_period('M').astype(str)
            cohort = df.groupby(['month', 'customer_type']).size().reset_index(name='bookings')
            fig_cohort = px.line(cohort, x='month', y='bookings', color='customer_type',
                                 title='Monthly Bookings by Guest Type')
            st.plotly_chart(fig_cohort, use_container_width=True)
            with st.expander("What does this chart show?"):
                st.write("Shows how different guest types book over time.")
        with col2:
            st.markdown("**Repeat Guest Analysis**")
            repeat_pct = df['is_repeated_guest'].mean() * 100
            repeat_counts = df['is_repeated_guest'].value_counts().rename({0: 'Non-Repeat', 1: 'Repeat'})
            fig_repeat = px.pie(values=repeat_counts.values, names=repeat_counts.index,
                                title='Repeat vs. Non-Repeat Guests')
            st.plotly_chart(fig_repeat, use_container_width=True)
            st.metric("% Repeat Guests", f"{repeat_pct:.1f}%")
            with st.expander("What does this chart show?"):
                st.write("Shows the proportion of repeat vs. new guests.")
        st.info("Repeat guests are valuable for long-term business.")

        st.markdown("---")
        st.subheader("Geographical & Time Series Analysis")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Bookings by Country (Map)**")
            country_counts = df['country'].value_counts().reset_index()
            country_counts.columns = ['country', 'bookings']
            fig_map = px.choropleth(country_counts, locations='country', color='bookings',
                locationmode='country names', color_continuous_scale='Blues', title='Bookings by Country')
            st.plotly_chart(fig_map, use_container_width=True)
            with st.expander("What does this map show?"):
                st.write("Shows the number of bookings by country. Darker colors mean more bookings.")
        with col2:
            st.markdown("**Monthly Bookings, Revenue, and Cancellations**")
            df['month'] = df['reservation_status_date'].dt.to_period('M').astype(str)
            ts = df.groupby('month').agg({
                'is_canceled': 'sum',
                'adr': 'mean',
                'booking_changes': 'count'
            }).rename(columns={'is_canceled': 'Cancellations', 'adr': 'Avg Room Price', 'booking_changes': 'Bookings'}).reset_index()
            ts['Revenue'] = df.groupby('month').apply(lambda x: (x['adr'] * (x['stays_in_weekend_nights'] + x['stays_in_week_nights'])).sum()).values
            fig_ts = px.line(ts, x='month', y=['Bookings', 'Revenue', 'Cancellations'],
                             title='Monthly Bookings, Revenue, and Cancellations')
            st.plotly_chart(fig_ts, use_container_width=True)
            with st.expander("How to use this chart?"):
                st.write("Shows monthly trends for bookings, revenue, and cancellations.")
        st.success("All charts and metrics update instantly with your filters!")

def show_booking_patterns(df):
    """Booking trends and time series analysis (robust alignment)"""
    with st.container():
        st.title("Booking Patterns")
        st.markdown("""
**Booking Patterns:**
See how bookings, prices, and cancellations change over the year.
""")
        with st.expander("Why look at booking patterns?"):
            st.write("""
Booking patterns help you spot busy and slow times, plan staff, and adjust prices.
            """)

        # Time period selector (single row)
        col1, col2 = st.columns(2)
        with col1:
            year_filter = st.selectbox("Pick a year:", sorted(df['arrival_date_year'].unique()))
        with col2:
            metric = st.selectbox("Pick what to see:", ["Bookings", "Average Room Price", "Cancellations"])

        # Filter data
        df_filtered = df[df['arrival_date_year'] == year_filter]
        monthly_data = df_filtered.groupby('arrival_month').agg({
            'booking_success': 'count',
            'adr': 'mean',
            'is_canceled': 'sum'
        }).reset_index()
        monthly_data['month_name'] = monthly_data['arrival_month'].map({
            1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
            7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
        })
        if metric == "Bookings":
            y_col = 'booking_success'
            title = f"Monthly Bookings - {year_filter}"
        elif metric == "Average Room Price":
            y_col = 'adr'
            title = f"Monthly Average Room Price - {year_filter}"
        else:
            y_col = 'is_canceled'
            title = f"Monthly Cancellations - {year_filter}"
        st.markdown(f"**{title}:** How does this change month by month?")
        fig_trend = px.line(monthly_data, x='month_name', y=y_col,
                            title=title,
                            labels={'booking_success': 'Bookings', 'adr': 'Room Price ($)', 
                                   'is_canceled': 'Cancellations', 'month_name': 'Month'})
        fig_trend.update_layout(height=500)
        st.plotly_chart(fig_trend, use_container_width=True)
        with st.expander("How to use this chart?"):
            st.write("""
Pick a year and what you want to see. Peaks show busy times, dips show slow times. Use this to plan ahead.
            """)

        # Lead time analysis (balanced columns)
        st.subheader("How far ahead do different guests book?")
        st.markdown("**See how early different guest types and booking sources make their bookings.**")
        col1, col2 = st.columns(2)
        with col1:
            lead_by_customer = df.groupby('customer_type')['lead_time'].mean().reset_index()
            fig_lead_customer = px.bar(lead_by_customer, x='customer_type', y='lead_time',
                                      title="Days Booked in Advance by Guest Type",
                                      labels={'lead_time': 'Days in Advance', 'customer_type': 'Guest Type'})
            st.plotly_chart(fig_lead_customer, use_container_width=True)
            with st.expander("Why does this matter?"):
                st.write("""
Some guests (like groups or business travelers) book earlier than others. This helps you plan for them.
                """)
        with col2:
            lead_by_channel = df.groupby('distribution_channel')['lead_time'].mean().reset_index()
            fig_lead_channel = px.bar(lead_by_channel, x='distribution_channel', y='lead_time',
                                     title="Days Booked in Advance by Booking Source",
                                     labels={'lead_time': 'Days in Advance', 'distribution_channel': 'Booking Source'})
            st.plotly_chart(fig_lead_channel, use_container_width=True)
            with st.expander("What is a booking source?"):
                st.write("""
A booking source is how the guest made the booking (e.g., Direct, Online Travel Agent, Corporate).
                """)

def show_revenue(df):
    """Revenue analysis and ADR insights (robust alignment, card design)"""
    with st.container():
        st.title("Revenue")
        st.markdown("""
**Revenue:**
See what brings in the most money for your hotel.
""")
        with st.expander("What is Average Room Price?"):
            st.write("""
Average Room Price (ADR) is the average price paid per room. It's a key number for hotel revenue.
            """)

        # Revenue metrics as attractive cards (single row)
        total_revenue = (df['adr'] * df['total_stay']).sum()
        avg_adr = df['adr'].mean()
        revenue_per_booking = total_revenue / len(df)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f'''
                <div style="background-color:#e3f2fd;padding:20px 10px 10px 10px;border-radius:12px;box-shadow:0 2px 8px #e3f2fd;text-align:center;">
                    <div style="font-size:1.1rem;color:#1565c0;font-weight:600;margin-bottom:8px;">Total Revenue</div>
                    <div style="font-size:2.2rem;font-weight:bold;color:#1565c0;">${total_revenue:,.0f}</div>
                </div>
            ''', unsafe_allow_html=True)
        with col2:
            st.markdown(f'''
                <div style="background-color:#e3f2fd;padding:20px 10px 10px 10px;border-radius:12px;box-shadow:0 2px 8px #e3f2fd;text-align:center;">
                    <div style="font-size:1.1rem;color:#1565c0;font-weight:600;margin-bottom:8px;">Average Room Price</div>
                    <div style="font-size:2.2rem;font-weight:bold;color:#1565c0;">${avg_adr:.2f}</div>
                </div>
            ''', unsafe_allow_html=True)
        with col3:
            st.markdown(f'''
                <div style="background-color:#e3f2fd;padding:20px 10px 10px 10px;border-radius:12px;box-shadow:0 2px 8px #e3f2fd;text-align:center;">
                    <div style="font-size:1.1rem;color:#1565c0;font-weight:600;margin-bottom:8px;">Revenue per Booking</div>
                    <div style="font-size:2.2rem;font-weight:bold;color:#1565c0;">${revenue_per_booking:.2f}</div>
                </div>
            ''', unsafe_allow_html=True)

        # ADR Analysis (balanced columns)
        st.subheader("Compare by Hotel and Source")
        st.markdown("**See which hotel types and booking sources bring in the most revenue.**")
        col1, col2 = st.columns(2)
        with col1:
            adr_by_hotel = df.groupby('hotel')['adr'].mean().reset_index()
            fig_adr_hotel = px.bar(adr_by_hotel, x='hotel', y='adr',
                                   title="Average Room Price by Hotel Type",
                                   labels={'adr': 'Room Price ($)', 'hotel': 'Hotel Type'})
            st.plotly_chart(fig_adr_hotel, use_container_width=True)
            with st.expander("What are hotel types?"):
                st.write("""
Hotel types in this data are Resort and City hotels. Comparing them shows which is more profitable.
                """)
        with col2:
            adr_by_segment = df.groupby('market_segment')['adr'].mean().reset_index()
            fig_adr_segment = px.bar(adr_by_segment, x='market_segment', y='adr',
                                    title="Average Room Price by Booking Source",
                                    labels={'adr': 'Room Price ($)', 'market_segment': 'Booking Source'})
            st.plotly_chart(fig_adr_segment, use_container_width=True)
            with st.expander("What is a booking source?"):
                st.write("""
A booking source is how the guest made the booking (e.g., Online Travel Agent, Direct, Corporate).
                """)

        # ADR correlation analysis (full width)
        st.subheader("What affects room price?")
        st.markdown("**See how room price relates to other numbers like days booked in advance, group size, and special requests.**")
        numeric_cols = ['adr', 'lead_time', 'total_guests', 'total_stay', 
                       'total_of_special_requests', 'booking_changes']
        corr_matrix = df[numeric_cols].corr()
        fig_corr = px.imshow(corr_matrix, 
                             title="Room Price Correlation Matrix",
                             color_continuous_scale='RdBu',
                             aspect="auto")
        fig_corr.update_layout(height=500)
        st.plotly_chart(fig_corr, use_container_width=True)
        with st.expander("How to read this?"):
            st.write("""
Numbers close to 1 or -1 mean a strong relationship. Use this to spot what drives revenue.
            """)

        # Top countries by ADR (full width)
        st.subheader("Top Countries by Room Price")
        st.markdown("**Which countries pay the most per booking?**")
        country_adr = df.groupby('country')['adr'].mean().sort_values(ascending=False).head(10).reset_index()
        fig_country_adr = px.bar(country_adr, x='adr', y='country',
                                 title="Top 10 Countries by Room Price",
                                 labels={'adr': 'Room Price ($)', 'country': 'Country'},
                                 orientation='h')
        st.plotly_chart(fig_country_adr, use_container_width=True)
        with st.expander("Why look at countries?"):
            st.write("""
Knowing which countries pay more helps you target marketing and offers.
            """)

def show_guest_profiles(df):
    """Guest demographics and country analysis (robust alignment, card design)"""
    with st.container():
        st.title("Guest Profiles")
        st.markdown("""
**Guest Profiles:**
See who your guests are and where they come from.
""")
        with st.expander("Why look at guest profiles?"):
            st.write("""
Knowing your guests helps you make better offers and improve their experience.
            """)

        # Guest statistics as attractive cards (single row)
        avg_guests = df['total_guests'].mean()
        most_common_size = df['total_guests'].mode().iloc[0]
        family_bookings = ((df['children'] > 0) | (df['babies'] > 0)).sum()
        family_percentage = (family_bookings / len(df)) * 100
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f'''
                <div style="background-color:#e3f2fd;padding:20px 10px 10px 10px;border-radius:12px;box-shadow:0 2px 8px #e3f2fd;text-align:center;">
                    <div style="font-size:1.1rem;color:#1565c0;font-weight:600;margin-bottom:8px;">Average Group Size</div>
                    <div style="font-size:2.2rem;font-weight:bold;color:#1565c0;">{avg_guests:.1f}</div>
                </div>
            ''', unsafe_allow_html=True)
        with col2:
            st.markdown(f'''
                <div style="background-color:#e3f2fd;padding:20px 10px 10px 10px;border-radius:12px;box-shadow:0 2px 8px #e3f2fd;text-align:center;">
                    <div style="font-size:1.1rem;color:#1565c0;font-weight:600;margin-bottom:8px;">Most Common Group Size</div>
                    <div style="font-size:2.2rem;font-weight:bold;color:#1565c0;">{most_common_size}</div>
                </div>
            ''', unsafe_allow_html=True)
        with col3:
            st.markdown(f'''
                <div style="background-color:#e3f2fd;padding:20px 10px 10px 10px;border-radius:12px;box-shadow:0 2px 8px #e3f2fd;text-align:center;">
                    <div style="font-size:1.1rem;color:#1565c0;font-weight:600;margin-bottom:8px;">Family Bookings</div>
                    <div style="font-size:2.2rem;font-weight:bold;color:#1565c0;">{family_percentage:.1f}%</div>
                </div>
            ''', unsafe_allow_html=True)

        # Guest distribution (balanced columns)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Group Size Distribution:** How many people are in each booking?")
            guest_dist = df['total_guests'].value_counts().sort_index()
            fig_guests = px.bar(x=guest_dist.index, y=guest_dist.values,
                               title="Group Size Distribution",
                               labels={'x': 'Group Size', 'y': 'Number of Bookings'})
            st.plotly_chart(fig_guests, use_container_width=True)
            with st.expander("Why does group size matter?"):
                st.write("""
Group size affects room needs and pricing. Bigger groups may want special deals.
                """)
        with col2:
            st.markdown("**Guest Type Distribution:** Shows the breakdown of guest types.")
            customer_dist = df['customer_type'].value_counts()
            fig_customer = px.pie(values=customer_dist.values, names=customer_dist.index,
                                 title="Guest Type Distribution")
            st.plotly_chart(fig_customer, use_container_width=True)
            with st.expander("What are guest types?"):
                st.write("""
Guest types include Transient (individual), Group, Contract, and Transient-Party.
                """)

        # Country analysis (full width)
        st.subheader("Where do guests come from?")
        st.markdown("**Top 10 Countries by Number of Bookings:** See where your guests are from.")
        top_countries = df['country'].value_counts().head(10)
        fig_countries = px.bar(x=top_countries.values, y=top_countries.index,
                              title="Top 10 Countries by Number of Bookings",
                              labels={'x': 'Number of Bookings', 'y': 'Country'},
                              orientation='h')
        st.plotly_chart(fig_countries, use_container_width=True)
        with st.expander("Why look at countries?"):
            st.write("""
Country analysis helps you find your best markets and plan marketing.
            """)

        # Country selector for detailed analysis (balanced columns)
        st.subheader("Country Details")
        selected_country = st.selectbox("Pick a country:", sorted(df['country'].unique()))
        country_data = df[df['country'] == selected_country]
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Room Price Distribution for {selected_country}:**")
            fig_country_adr = px.histogram(country_data, x='adr',
                                          title=f"Room Price Distribution - {selected_country}",
                                          labels={'adr': 'Room Price ($)', 'count': 'Number of Bookings'})
            st.plotly_chart(fig_country_adr, use_container_width=True)
        with col2:
            st.markdown(f"**Guest Type Distribution for {selected_country}:**")
            customer_country = country_data['customer_type'].value_counts()
            fig_customer_country = px.pie(values=customer_country.values, 
                                         names=customer_country.index,
                                         title=f"Guest Types - {selected_country}")
            st.plotly_chart(fig_customer_country, use_container_width=True)

def show_operations(df):
    """Operational insights and performance metrics (robust alignment, card design)"""
    with st.container():
        st.title("Operations")
        st.markdown("""
**Operations:**
See how often bookings are changed, cancelled, or upgraded, and how many special requests guests make.
""")
        with st.expander("Why look at operations?"):
            st.write("""
Operational numbers help you manage staff, reduce cancellations, and improve guest experience.
            """)

        # Key operational metrics as attractive cards (single row)
        room_match_rate = (df['reserved_room_type'] == df['assigned_room_type']).mean() * 100
        upgrade_rate = (df['reserved_room_type'] != df['assigned_room_type']).mean() * 100
        avg_special_requests = df['total_of_special_requests'].mean()
        avg_booking_changes = df['booking_changes'].mean()
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f'''
                <div style="background-color:#e3f2fd;padding:20px 10px 10px 10px;border-radius:12px;box-shadow:0 2px 8px #e3f2fd;text-align:center;">
                    <div style="font-size:1.1rem;color:#1565c0;font-weight:600;margin-bottom:8px;">Room Match Rate</div>
                    <div style="font-size:2.2rem;font-weight:bold;color:#1565c0;">{room_match_rate:.1f}%</div>
                </div>
            ''', unsafe_allow_html=True)
        with col2:
            st.markdown(f'''
                <div style="background-color:#e3f2fd;padding:20px 10px 10px 10px;border-radius:12px;box-shadow:0 2px 8px #e3f2fd;text-align:center;">
                    <div style="font-size:1.1rem;color:#1565c0;font-weight:600;margin-bottom:8px;">Room Upgrade Rate</div>
                    <div style="font-size:2.2rem;font-weight:bold;color:#1565c0;">{upgrade_rate:.1f}%</div>
                </div>
            ''', unsafe_allow_html=True)
        with col3:
            st.markdown(f'''
                <div style="background-color:#e3f2fd;padding:20px 10px 10px 10px;border-radius:12px;box-shadow:0 2px 8px #e3f2fd;text-align:center;">
                    <div style="font-size:1.1rem;color:#1565c0;font-weight:600;margin-bottom:8px;">Avg Special Requests</div>
                    <div style="font-size:2.2rem;font-weight:bold;color:#1565c0;">{avg_special_requests:.1f}</div>
                </div>
            ''', unsafe_allow_html=True)
        with col4:
            st.markdown(f'''
                <div style="background-color:#e3f2fd;padding:20px 10px 10px 10px;border-radius:12px;box-shadow:0 2px 8px #e3f2fd;text-align:center;">
                    <div style="font-size:1.1rem;color:#1565c0;font-weight:600;margin-bottom:8px;">Avg Booking Changes</div>
                    <div style="font-size:2.2rem;font-weight:bold;color:#1565c0;">{avg_booking_changes:.1f}</div>
                </div>
            ''', unsafe_allow_html=True)

        # Cancellation analysis (balanced columns)
        st.subheader("Cancellations")
        st.markdown("**See when and why guests cancel their bookings.**")
        col1, col2 = st.columns(2)
        with col1:
            df['lead_time_bins'] = pd.cut(df['lead_time'], 
                                         bins=[0, 30, 90, 365, float('inf')],
                                         labels=['0-30 days', '31-90 days', '91-365 days', '365+ days'])
            cancel_by_lead = df.groupby('lead_time_bins')['is_canceled'].mean().reset_index()
            fig_cancel_lead = px.bar(cancel_by_lead, x='lead_time_bins', y='is_canceled',
                                    title="Cancellation Rate by Days Booked in Advance",
                                    labels={'is_canceled': 'Cancellation Rate', 'lead_time_bins': 'Days in Advance'})
            st.plotly_chart(fig_cancel_lead, use_container_width=True)
            with st.expander("Why does this matter?"):
                st.write("""
Longer lead times may mean more cancellations. Watching this helps you plan policies.
                """)
        with col2:
            cancel_by_segment = df.groupby('market_segment')['is_canceled'].mean().reset_index()
            fig_cancel_segment = px.bar(cancel_by_segment, x='market_segment', y='is_canceled',
                                       title="Cancellation Rate by Booking Source",
                                       labels={'is_canceled': 'Cancellation Rate', 'market_segment': 'Booking Source'})
            st.plotly_chart(fig_cancel_segment, use_container_width=True)
            with st.expander("Why look at booking source?"):
                st.write("""
Some sources (like OTAs or groups) may have more cancellations. This helps you target improvements.
                """)

        # Special requests analysis (balanced columns)
        st.subheader("Special Requests")
        st.markdown("**How many special requests do guests make, and does it affect revenue?**")
        col1, col2 = st.columns(2)
        with col1:
            requests_dist = df['total_of_special_requests'].value_counts().sort_index()
            fig_requests = px.bar(x=requests_dist.index, y=requests_dist.values,
                                 title="Special Requests Distribution",
                                 labels={'x': 'Number of Special Requests', 'y': 'Number of Bookings'})
            st.plotly_chart(fig_requests, use_container_width=True)
            with st.expander("Why track special requests?"):
                st.write("""
Special requests (like extra beds or late check-out) affect staff and guest happiness.
                """)
        with col2:
            adr_by_requests = df.groupby('total_of_special_requests')['adr'].mean().reset_index()
            fig_adr_requests = px.line(adr_by_requests, x='total_of_special_requests', y='adr',
                                      title="Room Price by Number of Special Requests",
                                      labels={'adr': 'Room Price ($)', 'total_of_special_requests': 'Special Requests'})
            st.plotly_chart(fig_adr_requests, use_container_width=True)
            with st.expander("Does it affect revenue?"):
                st.write("""
Guests with more requests may pay more or need more service. This helps you balance service and profit.
                """)

        # Booking changes analysis (balanced columns)
        st.subheader("Booking Changes")
        st.markdown("**How often do guests change their bookings, and does it affect cancellations?**")
        col1, col2 = st.columns(2)
        with col1:
            changes_dist = df['booking_changes'].value_counts().sort_index()
            fig_changes = px.bar(x=changes_dist.index, y=changes_dist.values,
                                title="Booking Changes Distribution",
                                labels={'x': 'Number of Changes', 'y': 'Number of Bookings'})
            st.plotly_chart(fig_changes, use_container_width=True)
            with st.expander("Why does this matter?"):
                st.write("""
Frequent changes may mean indecision or special needs. Watching this helps you improve flexibility and reduce cancellations.
                """)
        with col2:
            cancel_by_changes = df.groupby('booking_changes')['is_canceled'].mean().reset_index()
            fig_cancel_changes = px.line(cancel_by_changes, x='booking_changes', y='is_canceled',
                                        title="Cancellation Rate by Booking Changes",
                                        labels={'is_canceled': 'Cancellation Rate', 'booking_changes': 'Booking Changes'})
            st.plotly_chart(fig_cancel_changes, use_container_width=True)
            with st.expander("Does it affect cancellations?"):
                st.write("""
Bookings with more changes may be at higher risk of cancellation. Use this to target improvements.
                """)

def show_cancellation_prediction(df):
    """Predictive analytics and ML insights"""
    st.title("Cancellation Prediction")
    st.markdown("""
**Cancellation Prediction:**
See which bookings are most likely to be cancelled, and what factors matter most.
""")
    with st.expander("How does this work?"):
        st.write("""
A machine learning model looks at things like days booked in advance, group size, and booking changes to predict cancellations.
        """)
    
    # Feature engineering for ML
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import classification_report, confusion_matrix
    import plotly.figure_factory as ff
    
    # Prepare features for cancellation prediction
    ml_df = df.copy()
    
    # Create features
    ml_df['is_family'] = ((ml_df['children'] > 0) | (ml_df['babies'] > 0)).astype(int)
    ml_df['room_upgrade'] = (ml_df['reserved_room_type'] != ml_df['assigned_room_type']).astype(int)
    
    # Select features
    features = ['lead_time', 'total_guests', 'total_stay', 'adr', 
               'total_of_special_requests', 'booking_changes', 'is_family', 'room_upgrade']
    
    X = ml_df[features]
    y = ml_df['is_canceled']
    
    # Train model
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    
    # Model performance
    y_pred = rf_model.predict(X_test)
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': features,
        'importance': rf_model.feature_importances_
    }).sort_values('importance', ascending=True)
    
    # Display results
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("What matters most?")
        st.markdown("**See which things most affect cancellations.**")
        fig_importance = px.bar(feature_importance, x='importance', y='feature',
                               title="What Affects Cancellations Most?",
                               orientation='h')
        st.plotly_chart(fig_importance, use_container_width=True)
        with st.expander("How to use this?"):
            st.write("""
Focus on the most important things (like days booked in advance or booking changes) to reduce cancellations.
            """)
    
    with col2:
        st.subheader("How good is the prediction?")
        st.markdown("**See how well the model predicts cancellations.**")
        
        # Confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        fig_cm = ff.create_annotated_heatmap(
            cm, 
            x=['Not Cancelled', 'Cancelled'],
            y=['Not Cancelled', 'Cancelled'],
            colorscale='Blues'
        )
        fig_cm.update_layout(title="Prediction Accuracy")
        st.plotly_chart(fig_cm, use_container_width=True)
        with st.expander("What is this chart?"):
            st.write("""
This chart shows how many bookings were correctly or incorrectly predicted as cancelled or not cancelled.
            """)
    
    # Prediction interface
    st.subheader("Try it yourself!")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        lead_time = st.slider("Days Booked in Advance", 0, 400, 50, help="Days between booking and arrival.")
        total_guests = st.slider("Group Size", 1, 10, 2, help="Number of guests in the booking.")
        total_stay = st.slider("Nights Stayed", 1, 30, 3, help="Number of nights stayed.")
    
    with col2:
        adr = st.slider("Room Price ($)", 0, 500, 100, help="Average price for the booking.")
        special_requests = st.slider("Special Requests", 0, 5, 0, help="Number of special requests.")
        booking_changes = st.slider("Booking Changes", 0, 10, 0, help="Number of changes made to the booking.")
    
    with col3:
        is_family = st.checkbox("Family Booking", help="Check if the booking includes children or babies.")
        room_upgrade = st.checkbox("Room Upgrade", help="Check if the guest was upgraded.")
    
    # Make prediction
    if st.button("Predict Cancellation Chance"):
        input_data = np.array([[
            lead_time, total_guests, total_stay, adr,
            special_requests, booking_changes, 
            int(is_family), int(room_upgrade)
        ]])
        
        probability = rf_model.predict_proba(input_data)[0][1]
        
        st.success(f"**Cancellation Chance: {probability:.1%}**")
        
        if probability > 0.5:
            st.warning("⚠️ High cancellation risk detected!")
        elif probability > 0.3:
            st.info("⚠️ Moderate cancellation risk")
        else:
            st.success("✅ Low cancellation risk")

if __name__ == "__main__":
    main() 