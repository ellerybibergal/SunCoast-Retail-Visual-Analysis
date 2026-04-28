# Module 11 Assignment: Data Visualization with Matplotlib
# SunCoast Retail Visual Analysis

# Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Welcome message
print("=" * 60)
print("SUNCOAST RETAIL VISUAL ANALYSIS")
print("=" * 60)

# ----- USE THE FOLLOWING CODE TO CREATE SAMPLE DATA (DO NOT MODIFY) -----
# Create a seed for reproducibility
np.random.seed(42)

# Generate dates for 8 quarters (Q1 2022 - Q4 2023)
quarters = pd.date_range(start='2022-01-01', periods=8, freq='Q')
quarter_labels = ['Q1 2022', 'Q2 2022', 'Q3 2022', 'Q4 2022', 
                 'Q1 2023', 'Q2 2023', 'Q3 2023', 'Q4 2023']

# Store locations
locations = ['Tampa', 'Miami', 'Orlando', 'Jacksonville']

# Product categories
categories = ['Electronics', 'Clothing', 'Home Goods', 'Sporting Goods', 'Beauty']

# Generate quarterly sales data for each location and category
quarterly_data = []

for quarter_idx, quarter in enumerate(quarters):
    for location in locations:
        for category in categories:
            # Base sales with seasonal pattern (Q4 higher, Q1 lower)
            base_sales = np.random.normal(loc=100000, scale=20000)
            seasonal_factor = 1.0
            if quarter.quarter == 4:  # Q4 (holiday boost)
                seasonal_factor = 1.3
            elif quarter.quarter == 1:  # Q1 (post-holiday dip)
                seasonal_factor = 0.8
            
            # Location effect
            location_factor = {
                'Tampa': 1.0,
                'Miami': 1.2,
                'Orlando': 0.9,
                'Jacksonville': 0.8
            }[location]
            
            # Category effect
            category_factor = {
                'Electronics': 1.5,
                'Clothing': 1.0,
                'Home Goods': 0.8,
                'Sporting Goods': 0.7,
                'Beauty': 0.9
            }[category]
            
            # Growth trend over time (5% per year, quarterly compounded)
            growth_factor = (1 + 0.05/4) ** quarter_idx
            
            # Calculate sales with some randomness
            sales = base_sales * seasonal_factor * location_factor * category_factor * growth_factor
            sales = sales * np.random.normal(loc=1.0, scale=0.1)  # Add noise
            
            # Advertising spend (correlated with sales but with diminishing returns)
            ad_spend = (sales ** 0.7) * 0.05 * np.random.normal(loc=1.0, scale=0.2)
            
            # Record
            quarterly_data.append({
                'Quarter': quarter,
                'QuarterLabel': quarter_labels[quarter_idx],
                'Location': location,
                'Category': category,
                'Sales': round(sales, 2),
                'AdSpend': round(ad_spend, 2),
                'Year': quarter.year
            })

# Create customer data
customer_data = []
total_customers = 2000

# Age distribution parameters for each location
age_params = {
    'Tampa': (45, 15),      # Older demographic
    'Miami': (35, 12),      # Younger demographic
    'Orlando': (38, 14),    # Mixed demographic
    'Jacksonville': (42, 13)  # Middle-aged demographic
}

for location in locations:
    # Generate ages based on location demographics
    mean_age, std_age = age_params[location]
    customer_count = int(total_customers * {
        'Tampa': 0.3,
        'Miami': 0.35,
        'Orlando': 0.2,
        'Jacksonville': 0.15
    }[location])
    
    ages = np.random.normal(loc=mean_age, scale=std_age, size=customer_count)
    ages = np.clip(ages, 18, 80).astype(int)  # Ensure ages are between 18-80
    
    # Generate purchase amounts
    for age in ages:
        # Younger and older customers spend differently across categories
        if age < 30:
            category_preference = np.random.choice(categories, p=[0.3, 0.3, 0.1, 0.2, 0.1])
        elif age < 50:
            category_preference = np.random.choice(categories, p=[0.25, 0.2, 0.25, 0.15, 0.15])
        else:
            category_preference = np.random.choice(categories, p=[0.15, 0.1, 0.35, 0.1, 0.3])
        
        # Purchase amount based on age and category
        base_amount = np.random.gamma(shape=5, scale=20)
        
        # Product tier (budget, mid-range, premium)
        price_tier = np.random.choice(['Budget', 'Mid-range', 'Premium'], 
                                     p=[0.3, 0.5, 0.2])
        
        tier_factor = {'Budget': 0.7, 'Mid-range': 1.0, 'Premium': 1.8}[price_tier]
        
        purchase_amount = base_amount * tier_factor
        
        customer_data.append({
            'Location': location,
            'Age': age,
            'Category': category_preference,
            'PurchaseAmount': round(purchase_amount, 2),
            'PriceTier': price_tier
        })

# Create DataFrames
sales_df = pd.DataFrame(quarterly_data)
customer_df = pd.DataFrame(customer_data)

# Add some calculated columns
sales_df['Quarter_Num'] = sales_df['Quarter'].dt.quarter
sales_df['SalesPerDollarSpent'] = sales_df['Sales'] / sales_df['AdSpend']

# Print data info
print("\nSales Data Sample:")
print(sales_df.head())
print("\nCustomer Data Sample:")
print(customer_df.head())
print("\nDataFrames created successfully. Ready for visualization!")
# ----- END OF DATA CREATION -----


# TODO 1: Time Series Visualization - Sales Trends
# 1.1 Create a line chart showing overall quarterly sales trends
# REQUIRED: Function must create and return a matplotlib figure
def plot_quarterly_sales_trend():
    """
    Create a line chart showing total sales for each quarter.
    REQUIRED: Return the figure object
    """
    # Your code here
    quarterly_sales = sales_df.groupby('QuarterLabel')['Sales'].sum()

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(quarterly_sales.index, quarterly_sales.values,
            marker='o', linewidth=2.5, color='navy')

    ax.set_title('Overall Quarterly Sales Trend', fontsize=14, fontweight='bold')
    ax.set_xlabel('Quarter')
    ax.set_ylabel('Total Sales ($)')
    ax.grid(True, linestyle='--', alpha=0.6)
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig

# 1.2 Create a multi-line chart comparing sales trends across locations
# REQUIRED: Function must create and return a matplotlib figure
def plot_location_sales_comparison():
    """
    Create a multi-line chart comparing quarterly sales across different locations.
    REQUIRED: Return the figure object
    """
    # Your code here
    location_sales = sales_df.groupby(['QuarterLabel', 'Location'])['Sales'].sum().unstack()

    fig, ax = plt.subplots(figsize=(10, 5))

    markers = ['o', 's', '^', 'D']
    for i, location in enumerate(location_sales.columns):
        ax.plot(location_sales.index,
                location_sales[location],
                marker=markers[i],
                linewidth=2,
                label=location)

    ax.set_title('Quarterly Sales by Store Location', fontsize=14, fontweight='bold')
    ax.set_xlabel('Quarter')
    ax.set_ylabel('Sales ($)')
    ax.legend(title='Location')
    ax.grid(True, linestyle='--', alpha=0.5)
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig

# TODO 2: Categorical Comparison - Product Performance by Location
# 2.1 Create a grouped bar chart comparing category performance by location
# REQUIRED: Function must create and return a matplotlib figure
def plot_category_performance_by_location():
    """
    Create a grouped bar chart showing how each product category performs in different locations.
    REQUIRED: Return the figure object
    """
    # Your code here
    latest_quarter = sales_df['Quarter'].max()
    recent_data = sales_df[sales_df['Quarter'] == latest_quarter]

    grouped = recent_data.pivot_table(index='Category', columns='Location', values='Sales', aggfunc='sum')

    fig, ax = plt.subplots(figsize=(10, 6))
    grouped.plot(kind='bar', ax=ax)

    ax.set_title('Category Performance by Location (Q4 2023)', fontsize=14, fontweight='bold')
    ax.set_xlabel('Product Category')
    ax.set_ylabel('Sales ($)')
    ax.legend(title='Location')
    plt.xticks(rotation=20)
    plt.tight_layout()
    return fig

# 2.2 Create a stacked bar chart showing the composition of sales in each location
# REQUIRED: Function must create and return a matplotlib figure
def plot_sales_composition_by_location():
    """
    Create a stacked bar chart showing the composition of sales across categories for each location.
    REQUIRED: Return the figure object
    """
    # Your code here
    location_category = sales_df.groupby(['Location', 'Category'])['Sales'].sum().unstack()
    percent_data = location_category.div(location_category.sum(axis=1), axis=0) * 100

    fig, ax = plt.subplots(figsize=(10, 6))
    percent_data.plot(kind='bar', stacked=True, ax=ax)

    ax.set_title('Sales Composition by Location', fontsize=14, fontweight='bold')
    ax.set_xlabel('Location')
    ax.set_ylabel('Percentage of Total Sales')
    ax.legend(title='Category', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    return fig

# TODO 3: Relationship Analysis - Advertising and Sales
# 3.1 Create a scatter plot to examine the relationship between ad spend and sales
# REQUIRED: Function must create and return a matplotlib figure
def plot_ad_spend_vs_sales():
    """
    Create a scatter plot to visualize the relationship between advertising spend and sales.
    REQUIRED: Return the figure object
    """
    # Your code here
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.scatter(sales_df['AdSpend'], sales_df['Sales'], alpha=0.7)

    z = np.polyfit(sales_df['AdSpend'], sales_df['Sales'], 1)
    p = np.poly1d(z)
    ax.plot(sales_df['AdSpend'], p(sales_df['AdSpend']), linestyle='--', linewidth=2)

    outlier = sales_df.loc[sales_df['Sales'].idxmax()]
    ax.annotate(f"{outlier['Location']} - {outlier['Category']}",
                (outlier['AdSpend'], outlier['Sales']),
                textcoords='offset points', xytext=(10, 10))

    ax.set_title('Advertising Spend vs Sales', fontsize=14, fontweight='bold')
    ax.set_xlabel('Advertising Spend ($)')
    ax.set_ylabel('Sales ($)')
    ax.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    return fig

# 3.2 Create a line chart showing sales per dollar spent on advertising over time
# REQUIRED: Function must create and return a matplotlib figure
def plot_ad_efficiency_over_time():
    """
    Create a line chart showing how efficient advertising spend has been over time.
    REQUIRED: Return the figure object
    """
    # Your code here
    efficiency = sales_df.groupby('QuarterLabel')['SalesPerDollarSpent'].mean()

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(efficiency.index, efficiency.values, marker='o', linewidth=2)

    best_quarter = efficiency.idxmax()
    ax.annotate('Highest Efficiency',
                xy=(best_quarter, efficiency.max()),
                xytext=(0, 15),
                textcoords='offset points',
                ha='center')

    ax.set_title('Advertising Efficiency Over Time', fontsize=14, fontweight='bold')
    ax.set_xlabel('Quarter')
    ax.set_ylabel('Sales per Advertising Dollar')
    ax.grid(True, linestyle='--', alpha=0.5)
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig

# TODO 4: Distribution Analysis - Customer Demographics
# 4.1 Create histograms of customer age distribution
# REQUIRED: Function must create and return a matplotlib figure with subplots
def plot_customer_age_distribution():
    """
    Create histograms showing the age distribution of customers, both overall and by location.
    REQUIRED: Return the figure object
    """
    # Your code here
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()

    # Overall distribution
    axes[0].hist(customer_df['Age'], bins=15, edgecolor='black')
    axes[0].axvline(customer_df['Age'].mean(), color='red', linestyle='--', label='Mean')
    axes[0].axvline(customer_df['Age'].median(), color='green', linestyle=':', label='Median')
    axes[0].set_title('Overall Customer Age Distribution')
    axes[0].legend()

    for i, location in enumerate(locations):
        subset = customer_df[customer_df['Location'] == location]
        axes[i + 1].hist(subset['Age'], bins=12, edgecolor='black')
        axes[i + 1].axvline(subset['Age'].mean(), color='red', linestyle='--')
        axes[i + 1].axvline(subset['Age'].median(), color='green', linestyle=':')
        axes[i + 1].set_title(f'{location} Age Distribution')
        axes[i + 1].set_xlabel('Age')
        axes[i + 1].set_ylabel('Customers')

    axes[5].axis('off')

    plt.tight_layout()
    return fig

# 4.2 Create box plots comparing purchase amounts by age groups
# REQUIRED: Function must create and return a matplotlib figure
def plot_purchase_by_age_group():
    """
    Create box plots showing purchase amounts across different age groups.
    REQUIRED: Return the figure object
    """
    # Your code here
    age_groups = pd.cut(customer_df['Age'],
                        bins=[18, 30, 45, 60, 80],
                        labels=['18-30', '31-45', '46-60', '61+'])

    grouped_data = [customer_df[age_groups == label]['PurchaseAmount']
                    for label in ['18-30', '31-45', '46-60', '61+']]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.boxplot(grouped_data, labels=['18-30', '31-45', '46-60', '61+'])

    ax.set_title('Purchase Amount by Age Group', fontsize=14, fontweight='bold')
    ax.set_xlabel('Age Group')
    ax.set_ylabel('Purchase Amount ($)')
    ax.grid(True, linestyle='--', alpha=0.4)
    plt.tight_layout()
    return fig

# TODO 5: Sales Distribution - Pricing Tiers
# 5.1 Create a histogram of purchase amounts
# REQUIRED: Function must create and return a matplotlib figure
def plot_purchase_amount_distribution():
    """
    Create a histogram showing the distribution of purchase amounts.
    REQUIRED: Return the figure object
    """
    # Your code here
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(customer_df['PurchaseAmount'], bins=20, edgecolor='black')

    ax.set_title('Distribution of Purchase Amounts', fontsize=14, fontweight='bold')
    ax.set_xlabel('Purchase Amount ($)')
    ax.set_ylabel('Number of Purchases')
    plt.tight_layout()
    return fig

# 5.2 Create a pie chart showing sales breakdown by price tier
# REQUIRED: Function must create and return a matplotlib figure
def plot_sales_by_price_tier():
    """
    Create a pie chart showing the breakdown of sales by price tier.
    REQUIRED: Return the figure object
    """
    # Your code here
    tier_sales = customer_df.groupby('PriceTier')['PurchaseAmount'].sum()
    explode = [0.1 if value == tier_sales.max() else 0 for value in tier_sales]
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.pie(
        tier_sales,
        labels=tier_sales.index,
        autopct='%1.1f%%',
        startangle=90,
        explode=explode,
        shadow=True
    )
    ax.set_title('Sales Breakdown by Price Tier')
    return fig


# TODO 6: Market Share Analysis
# 6.1 Create a pie chart showing sales breakdown by category
# REQUIRED: Function must create and return a matplotlib figure
def plot_category_market_share():
    """
    Create a pie chart showing the market share of each product category.
    REQUIRED: Return the figure object
    """
    # Your code here
    category_sales = sales_df.groupby('Category')['Sales'].sum()
    explode = [0.1 if value == category_sales.max() else 0 for value in category_sales]
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.pie(
        category_sales,
        labels=category_sales.index,
        autopct='%1.1f%%',
        startangle=90,
        explode=explode,
        shadow=True
    )
    ax.set_title('Market Share by Product Category')
    return fig

# 6.2 Create a pie chart showing sales breakdown by location
# REQUIRED: Function must create and return a matplotlib figure
def plot_location_sales_distribution():
    """
    Create a pie chart showing the distribution of sales across different store locations.
    REQUIRED: Return the figure object
    """
    # Your code here
    location_sales = sales_df.groupby('Location')['Sales'].sum()
    explode = [0.1 if value == location_sales.max() else 0 for value in location_sales]
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.pie(
        location_sales,
        labels=location_sales.index,
        autopct='%1.1f%%',
        startangle=90,
        explode=explode,
        shadow=True
    )
    ax.set_title('Sales Distribution by Location')
    return fig

# TODO 7: Comprehensive Dashboard
# REQUIRED: Function must create and return a matplotlib figure with at least 4 subplots
def create_business_dashboard():
    """
    Create a comprehensive dashboard with multiple subplots highlighting key business insights.
    REQUIRED: Return the figure object with at least 4 subplots
    """
    # Your code here
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('SunCoast Retail Business Dashboard', fontsize=18, fontweight='bold')

    # Subplot 1: Quarterly Sales Trend (Line chart)
    quarterly_sales = sales_df.groupby('QuarterLabel')['Sales'].sum()
    axes[0, 0].plot(quarterly_sales.index, quarterly_sales.values, marker='o', linewidth=2, color='blue')
    axes[0, 0].set_title('Quarterly Sales Trend')
    axes[0, 0].set_xlabel('Quarter')
    axes[0, 0].set_ylabel('Sales ($)')
    axes[0, 0].grid(True, linestyle='--', alpha=0.5)
    axes[0, 0].tick_params(axis='x', rotation=45)

    # Subplot 2: Sales Distribution by Location (Pie chart)
    location_sales = sales_df.groupby('Location')['Sales'].sum()
    explode = [0.1 if value == location_sales.max() else 0 for value in location_sales]
    axes[0, 1].pie(
        location_sales,
        labels=location_sales.index,
        autopct='%1.1f%%',
        startangle=90,
        explode=explode,
        shadow=True
    )
    axes[0, 1].set_title('Sales Distribution by Location')

    # Subplot 3: Sales by Product Category (Bar chart)
    category_sales = sales_df.groupby('Category')['Sales'].sum()
    axes[1, 0].bar(category_sales.index, category_sales.values, color='green', alpha=0.7)
    axes[1, 0].set_title('Sales by Product Category')
    axes[1, 0].set_xlabel('Category')
    axes[1, 0].set_ylabel('Sales ($)')
    axes[1, 0].tick_params(axis='x', rotation=20)

    # Subplot 4: Advertising Spend vs Sales (Scatter with trend line)
    axes[1, 1].scatter(sales_df['AdSpend'], sales_df['Sales'], alpha=0.6, color='orange')
    z = np.polyfit(sales_df['AdSpend'], sales_df['Sales'], 1)
    p = np.poly1d(z)
    axes[1, 1].plot(sales_df['AdSpend'], p(sales_df['AdSpend']), linestyle='--', color='red', linewidth=2)
    axes[1, 1].set_title('Advertising Spend vs Sales')
    axes[1, 1].set_xlabel('Advertising Spend ($)')
    axes[1, 1].set_ylabel('Sales ($)')
    axes[1, 1].grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    return fig
# Main function to execute all visualizations
# REQUIRED: Do not modify this function name
def main():
    print("\n" + "=" * 60)
    print("SUNCOAST RETAIL VISUAL ANALYSIS RESULTS")
    print("=" * 60)
    
    # REQUIRED: Call all visualization functions and store figures
    # Store each figure in a variable for potential saving/display
    
    # Time Series Analysis
    fig1 = plot_quarterly_sales_trend()
    fig2 = plot_location_sales_comparison()
    
    # Categorical Comparison
    fig3 = plot_category_performance_by_location()
    fig4 = plot_sales_composition_by_location()
    
    # Relationship Analysis
    fig5 = plot_ad_spend_vs_sales()
    fig6 = plot_ad_efficiency_over_time()
    
    # Distribution Analysis
    fig7 = plot_customer_age_distribution()
    fig8 = plot_purchase_by_age_group()
    
    # Sales Distribution
    fig9 = plot_purchase_amount_distribution()
    fig10 = plot_sales_by_price_tier()
    
    # Market Share Analysis
    fig11 = plot_category_market_share()
    fig12 = plot_location_sales_distribution()
    
    # Comprehensive Dashboard
    fig13 = create_business_dashboard()
    
    # REQUIRED: Add business insights summary
    print("\nKEY BUSINESS INSIGHTS:")
    # Your insights here based on the visualizations
    print("-" * 60)
    print("1. Quarterly Sales Trends: Sales peak in Q4 (holidays) and dip in Q1, with a slight upward trend overall.")
    print("2. Location Performance: Miami leads in sales, followed by Tampa, Orlando, and Jacksonville.")
    print("3. Product Category Insights: Electronics dominate sales, while Sporting Goods and Home Goods lag.")
    print("4. Advertising Effectiveness: Positive correlation between ad spend and sales, highest ROI in Q2/Q3.")
    print("5. Customer Demographics: Younger in Miami, older in Tampa, mixed elsewhere; 31-45 age group drives most purchases.")
    print("6. Pricing Tier Insights: Mid-range products dominate, followed by Premium and Budget.")
    print("7. Market Share: Electronics are the top category; Miami has the largest location market share.")
    
    # Display all figures
    plt.show()

# Run the main function
if __name__ == "__main__":
    main()