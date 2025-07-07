# 🏗️ Hotel Dashboard Project Structure

## 📁 Directory Organization

```
hotel-dashboard/
├── 📄 app.py                    # Main entry point for Streamlit
├── 📄 requirements.txt          # Python dependencies
├── 📄 README.md                # Project documentation
├── 📄 PROJECT_STRUCTURE.md     # This file
├── 📁 src/                     # Source code
│   └── 📄 hotel_dashboard.py   # Main dashboard application
├── 📁 data/                    # Data files
│   └── 📄 hotel_bookings.csv   # Hotel booking dataset (119,390 rows)
├── 📁 config/                  # Configuration files
│   └── 📄 config.py           # Dashboard settings and styling
├── 📁 scripts/                 # Utility scripts
│   └── 📄 deploy.py           # Deployment automation script
├── 📁 docs/                    # Documentation and analysis
│   ├── 📄 file.ipynb          # Comprehensive EDA notebook
│   ├── 📄 explaination.ipynb  # Educational analysis notebook
│   └── 📄 new.ipynb           # Machine learning experiments
└── 📁 assets/                  # Generated visualizations
    ├── 📄 adr_distribution.png
    ├── 📄 lead_time_distribution.png
    ├── 📄 special_requests.png
    └── 📄 total_guests.png
```

## 🎯 Purpose of Each Directory

### **📁 src/**
Contains the main application code:
- **hotel_dashboard.py**: Core dashboard functionality with 6 main sections
  - Overview dashboard with KPIs
  - Booking trends analysis
  - Revenue analytics
  - Guest demographics
  - Operational insights
  - Predictive analytics

### **📁 data/**
Stores all data files:
- **hotel_bookings.csv**: Main dataset with 32 columns and 119,390 rows
- Future data files can be added here

### **📁 config/**
Configuration and settings:
- **config.py**: Centralized configuration for colors, settings, and styling
- Easy to customize dashboard appearance and behavior

### **📁 scripts/**
Utility and automation scripts:
- **deploy.py**: Automated deployment preparation and testing
- Future automation scripts can be added here

### **📁 docs/**
Documentation and analysis notebooks:
- **file.ipynb**: Complete exploratory data analysis
- **explaination.ipynb**: Educational step-by-step analysis
- **new.ipynb**: Machine learning experiments

### **📁 assets/**
Generated visualizations and static files:
- PNG files from the analysis
- Future static assets (CSS, images, etc.)

## 🚀 How to Run

### **Local Development**
```bash
cd hotel-dashboard
streamlit run app.py
```

### **Production Deployment**
```bash
cd hotel-dashboard
python scripts/deploy.py
```

## 🔧 Key Features

### **Dashboard Sections**
1. **📊 Overview**: Key metrics and KPIs
2. **📈 Booking Trends**: Time series analysis
3. **💰 Revenue Analytics**: ADR and revenue insights
4. **🌍 Guest Demographics**: Geographic and demographic analysis
5. **🎯 Operational Insights**: Cancellation and operational metrics
6. **🤖 Predictive Analytics**: ML-based predictions

### **Interactive Features**
- Real-time data filtering
- Interactive charts with Plotly
- Machine learning predictions
- Responsive design
- Professional styling

### **Technical Stack**
- **Frontend**: Streamlit
- **Visualization**: Plotly
- **Data Processing**: Pandas, NumPy
- **Machine Learning**: Scikit-learn
- **Styling**: Custom CSS

## 📊 Data Insights

### **Key Metrics**
- **Total Bookings**: 119,390
- **Average ADR**: $101.83
- **Cancellation Rate**: 37%
- **Room Match Rate**: 85%
- **Average Lead Time**: 79 days

### **Top Insights**
- Online TA generates highest ADR ($118.17)
- Portugal is the top booking country (27,451 bookings)
- Most common group size is 2 guests
- Transient guests dominate revenue

## 🎨 Customization

### **Styling**
- Modify `config/config.py` for colors and themes
- Update CSS in `src/hotel_dashboard.py`
- Add custom components as needed

### **Data**
- Replace `data/hotel_bookings.csv` with your dataset
- Update data loading in `src/hotel_dashboard.py`
- Modify feature engineering as needed

### **Features**
- Add new pages in `src/hotel_dashboard.py`
- Create new analysis functions
- Extend ML models in predictive analytics

## 🔄 Version Control

### **Git Setup**
```bash
cd hotel-dashboard
git init
git add .
git commit -m "Initial hotel dashboard commit"
```

### **Deployment**
1. Push to GitHub
2. Connect to Streamlit Cloud
3. Deploy with path: `app.py`

## 📈 Future Enhancements

### **Planned Features**
- Real-time data integration
- Advanced ML models
- User authentication
- Custom reporting
- API endpoints

### **Scalability**
- Modular code structure
- Configuration-driven design
- Easy to extend and maintain
- Professional documentation

---

**🏨 Hotel Analytics Dashboard - Professional Data Science Project** 