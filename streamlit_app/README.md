# 🏨 Hotel Analytics Dashboard

A comprehensive, interactive dashboard for hotel booking data analysis built with Streamlit and Plotly.

## 📊 Features

### **Overview Dashboard**
- Key performance indicators (KPIs)
- Revenue metrics and booking statistics
- Market segment analysis
- ADR and lead time distributions

### **Booking Trends**
- Monthly booking patterns
- Time series analysis
- Lead time analysis by customer type and distribution channel
- Interactive year and metric selection

### **Revenue Analytics**
- ADR analysis by hotel type and market segment
- Revenue correlation analysis
- Top countries by average ADR
- Revenue per booking metrics

### **Guest Demographics**
- Guest count distribution
- Customer type analysis
- Geographic analysis with country breakdowns
- Family booking statistics

### **Operational Insights**
- Cancellation analysis
- Room upgrade and match rates
- Special requests analysis
- Booking changes patterns

### **Predictive Analytics**
- Machine learning-based cancellation prediction
- Feature importance analysis
- Interactive prediction tool
- Model performance metrics

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip package manager

### Installation

1. **Clone or download the project files**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the dashboard:**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser** and navigate to `http://localhost:8501`

## 📁 Project Structure

```
hotel-dashboard/
├── app.py                 # Main entry point
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── src/                  # Source code
│   └── hotel_dashboard.py # Main dashboard application
├── data/                 # Data files
│   └── hotel_bookings.csv # Hotel booking dataset
├── config/               # Configuration files
│   └── config.py         # Dashboard configuration
├── scripts/              # Utility scripts
│   └── deploy.py         # Deployment script
├── docs/                 # Documentation and notebooks
│   ├── file.ipynb        # Original analysis notebook
│   ├── explaination.ipynb # Educational notebook
│   └── new.ipynb         # ML experiments
└── assets/               # Generated visualizations
    ├── adr_distribution.png
    ├── lead_time_distribution.png
    ├── special_requests.png
    └── total_guests.png
```

## 🎯 Key Insights

### **Revenue Optimization**
- Online TA generates highest ADR ($118.17)
- Direct bookings are second highest ($116.58)
- Top revenue countries: DJI ($273), AIA ($265), AND ($202.65)

### **Operational Efficiency**
- Room match rate: 85%
- Room upgrade rate: 15%
- Average lead time: 79 days
- Cancellation rate: 37%

### **Guest Behavior**
- Most common group size: 2 guests (57,055 bookings)
- Top countries: Portugal (27,451), UK (10,433), France (8,837)
- Transient guests dominate revenue (7.9M vs 1M for Transient-Party)

## 🛠️ Technical Stack

- **Frontend**: Streamlit
- **Visualization**: Plotly
- **Data Processing**: Pandas, NumPy
- **Machine Learning**: Scikit-learn
- **Styling**: Custom CSS

## 📈 Dashboard Sections

### 1. **Overview** 📊
- Key metrics cards
- ADR and lead time distributions
- Market segment performance

### 2. **Booking Trends** 📈
- Monthly booking patterns
- Lead time analysis
- Interactive time series

### 3. **Revenue Analytics** 💰
- ADR analysis by factors
- Revenue correlation matrix
- Country-based revenue analysis

### 4. **Guest Demographics** 🌍
- Guest count distribution
- Customer type analysis
- Geographic breakdown

### 5. **Operational Insights** 🎯
- Cancellation analysis
- Special requests patterns
- Booking changes analysis

### 6. **Predictive Analytics** 🤖
- ML-based cancellation prediction
- Feature importance
- Interactive prediction tool

## 🔧 Customization

### Adding New Features
1. Create new functions in `hotel_dashboard.py`
2. Add navigation options in the sidebar
3. Update the main routing logic

### Styling
- Modify the CSS in the `st.markdown()` section
- Add custom themes or color schemes
- Implement responsive design elements

### Data Sources
- Replace `hotel_bookings.csv` with your own dataset
- Update the `load_data()` function to match your data structure
- Modify feature engineering as needed

## 📊 Data Dictionary

| Column | Description | Type |
|--------|-------------|------|
| hotel | Hotel type (Resort/City) | Categorical |
| is_canceled | Booking cancellation status | Binary |
| lead_time | Days between booking and arrival | Numeric |
| arrival_date_year | Year of arrival | Numeric |
| arrival_date_month | Month of arrival | Categorical |
| adults | Number of adults | Numeric |
| children | Number of children | Numeric |
| babies | Number of babies | Numeric |
| country | Guest country | Categorical |
| adr | Average Daily Rate | Numeric |
| market_segment | Market segment | Categorical |
| customer_type | Type of customer | Categorical |

## 🚀 Deployment

### Local Development
```bash
streamlit run app.py
```

### Streamlit Cloud Deployment
1. Push code to GitHub
2. Connect repository to Streamlit Cloud
3. Deploy automatically

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "hotel_dashboard.py"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is open source and available under the MIT License.

## 🆘 Support

For issues or questions:
1. Check the existing documentation
2. Review the code comments
3. Create an issue on GitHub

---

**Built with ❤️ using Streamlit and Plotly** 