import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go


# Load data 
def load_data(file):
    df = pd.read_csv(file)  
    return df

    

df_feb = load_data(r"february_sales.csv")
df_jan =load_data(r"january_sales.csv")


# Filter sold items
sold_items = df_feb[df_feb["Sold"] == True]
unsold_items = df_feb[df_feb["Sold"] == False]
unsold_items["Profit / Loss"] = -440 

jan_sold_items = df_jan[df_jan["Sold"] == True]
jan_unsold_items = df_jan[df_jan["Sold"] == False]
jan_unsold_items["Profit / Loss"] = -440 




# Key metrics
total_profit = sold_items["Profit / Loss"].sum()
total_fee =  unsold_items["Profit / Loss"].sum()
total_revenue = total_profit + total_fee + 880 #two gray items so we did not pay the fee
total_sold = sold_items.shape[0]
total_unsold = df_feb.shape[0] - total_sold 

jan_total_profit = jan_sold_items["Profit / Loss"].sum()
jan_total_fee =  jan_unsold_items["Profit / Loss"].sum()
jan_total_revenue = jan_total_profit + jan_total_fee


# Brand performance summary
brand_sales = sold_items.groupby("Brand Name")["Profit / Loss"].sum().reset_index()
brand_sales = brand_sales.sort_values(by="Profit / Loss", ascending=False)

# Streamlit app layout
st.title("February 2025 Ecoring Auction Sales Report")


# Calculate percentage increase
if jan_total_revenue > 0:
    revenue_increase = ((total_revenue - jan_total_revenue) / jan_total_revenue) * 100
elif jan_total_revenue < 0:
    revenue_increase = ((total_revenue - jan_total_revenue) / abs(jan_total_revenue)) * 100
else:  # If jan_total_revenue is exactly 0
    revenue_increase = float("inf") if total_revenue > 0 else 0


# Define color and arrow
increase_color = "green" if revenue_increase >= 0 else "red"
arrow = "⬆️" if revenue_increase >= 0 else "⬇️"

# Create columns
# Create columns with better spacing
col1, col2, col3 = st.columns([2, 0.5, 1])  # Adjust column widths (col2 acts as a small spacer)

with col1:
    st.markdown(f"""
        <div style="font-size:24px; font-weight:bold;">Total Sales Revenue</div>
        <div style="font-size:36px; font-weight:bold;">¥{total_revenue:,.0f}</div>
        <div style="font-size:18px; color:gray;">(Jan: ¥{jan_total_revenue:,.0f})</div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div style="text-align:right;">
            <div style="font-size:16px; color:gray;">Increase from last month</div>
            <div style="font-size:24px; font-weight:bold; color:{increase_color};">
                {arrow} {revenue_increase:.1f}%
            </div>
        </div>
    """, unsafe_allow_html=True)



# Key Stats
#st.metric(label="Total Sales Revenue", value=f"¥{total_revenue:,.0f}")

# st.metric(label="Total Sales Revenue_jan", value=f"¥{jan_total_revenue:,.0f}")

st.metric(label="Number of Items Sold", value=f"{total_sold}/{df_feb.shape[0]}" )



#st.metric(label="Number of Items Unsold", value=total_unsold)

# Brand Performance
st.subheader("Top Selling Brands for Feburary 2025")
# Create columns for layout
# Create columns for layout with 25% / 75% split
col1, col2 = st.columns([1.5, 2.5])  # 1:3 ratio for 25% and 75% width split

# Place the dataframe in the first column (col1)
with col1:
    st.dataframe(brand_sales, hide_index=True)

# Plotly Pie Chart in the second column (col2)
with col2:
    fig = px.pie(brand_sales, 
                 names='Brand Name', 
                 values='Profit / Loss', 
                 title='Brand Performance', 
                 hole=0.001)  # Create a donut chart for better visualization
    fig.update_traces(textinfo='percent+label', pull=[0.05] * len(brand_sales))  # Pull each slice slightly for emphasis
    st.plotly_chart(fig, use_container_width=True, width=800, height=600)  # Adjusted size


# Assuming sold_items is already prepared and contains the relevant data
# Sort by earnings (assuming 'Profit / Loss' column is available)
top_items = sold_items[['Ctag', 'Profit / Loss', 'Cost(price after Tax)']].sort_values(by='Profit / Loss', ascending=False).head(3)

# Streamlit layout
st.title("Top Earning Items for This Month")

# Create a podium layout
st.markdown("### Podium for Top 3 Earning Items:")

# Loop through the top 3 items
podium_colors = ["gold", "silver", "#cd7f32"]  # Colors for 1st, 2nd, and 3rd place
podium_positions = ["1st", "2nd", "3rd"]

for i in range(3):
    ctag = top_items.iloc[i]['Ctag']
    profit = top_items.iloc[i]['Profit / Loss']
    cost = pd.to_numeric(str(top_items.iloc[i]['Cost(price after Tax)']).replace('¥', '').replace(',', ''), errors='coerce')
    img_url = f"https://s3.amazonaws.com/storage.j-ports/photographs/{ctag}/thumbnail/1.jpg"

        # Calculate revenue percentage
    if cost > 0:
        revenue_percent = ((profit - cost) / cost) * 100
    else:
        revenue_percent = 0

    col1, col2 = st.columns([1, 4])  # Image on the left, text on the right

    with col1:
        st.image(img_url, width=100)  # Display item image

    with col2:
        st.markdown(f"""
            <div style="display: flex; align-items: center;">
                <div style="background-color: {podium_colors[i]}; width: {100 - (i * 20)}px; height: {100 - (i * 20)}px; 
                            border-radius: 50%; margin-right: 20px; display: flex; justify-content: center; align-items: center;">
                    <div style="font-size: 24px; color: white; text-align: center;">
                        {podium_positions[i]}
                    </div>
                </div>
                <div>
                    <h3>{ctag}</h3>
                    <p style="font-size: 18px; color: green;">¥{profit:,.0f}</p>
                    <p style="font-size: 14px; color: gray;">Revenue: {revenue_percent:.1f}%</p>
                </div>
            </div>
        """, unsafe_allow_html=True)

# You can add more items in the same way or display additional information.





# Prepping legacy sale data from 2024
input_folder = r"C:\Users\Jens\JPorts_al\Ecoring\Eco_sale_data\Ecoring_2024_yuko"

monthly_revenue_24 = {}

# Loop through all files in the folder
for file_name in os.listdir(input_folder):
    if file_name.endswith(".csv"):
        # Extract month name from the file name
        month = file_name.split('_')[1].capitalize()
        
        # Load the data
        df_24 = pd.read_csv(f"{input_folder}/{file_name}")
        
        # Filter sold and unsold items
        sold_items_24 = df_24[df_24["Sold"] == True]
        unsold_items_24 = df_24[df_24["Sold"] == False]
        
        # Adding the unsold fee to unsold items
        unsold_items_24["Profit / Loss"] = -440 
        
        # Calculate total profit from sold items and total fee from unsold items
        total_profit_24 = sold_items_24["Profit / Loss"].sum()
        total_fee_24 = unsold_items_24["Profit / Loss"].sum()
        
        # Total revenue for the month
        total_revenue_24 = total_profit_24 + total_fee_24
        
        # Store the total revenue in the dictionary
        monthly_revenue_24[month] = total_revenue_24

# Adding January and February revenue manually
monthly_revenue_24["January_25"] = jan_total_revenue
monthly_revenue_24["February_25"] = total_revenue

# Define all months in 2024, adding a 0 value for missing months
all_months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

# Ensure every month is represented, even if no data is found for it (set to 0 if missing)
for month in all_months:
    if month not in monthly_revenue_24:
        monthly_revenue_24[month] = 0  # Set missing months to 0

# Sort months for plotting
# Create a list of month names in the correct order
month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

# Sort the dictionary keys based on the order of months and handle the "_25" entries
def custom_sort(month):
    # Check if "_25" is in the month string and treat it as a separate "month_25" category
    if "_25" in month:
        return (12, 99)  # Put "_25" entries at the end (99th month, after December)
    else:
        # Otherwise, use the month order and return the tuple (month_index, year)
        month_name = month.split('_')[0]  # e.g., "January" from "January_25"
        return (month_order.index(month_name), 2024)

# Sort the months based on the custom sort function
sorted_months = sorted(monthly_revenue_24.keys(), key=custom_sort)

# Streamlit app layout
st.title("Ecoring 2024-2025 Total Revenue Plot")

# Convert the dictionary to a pandas DataFrame
revenue_df_24 = pd.DataFrame(list(monthly_revenue_24.items()), columns=['Month', 'Total Revenue'])

# Sort the DataFrame by the 'Month' column based on the sorted months
revenue_df_24['Month'] = pd.Categorical(revenue_df_24['Month'], categories=sorted_months, ordered=True)
revenue_df_24 = revenue_df_24.sort_values('Month')

# Plot the total revenue as a line chart using Streamlit
#st.line_chart(revenue_df_24.set_index('Month')['Total Revenue'])

import plotly.graph_objects as go

# Convert the dictionary to a pandas DataFrame
revenue_df_24 = pd.DataFrame(list(monthly_revenue_24.items()), columns=['Month', 'Total Revenue'])

# Sort the DataFrame by the 'Month' column based on the sorted months
revenue_df_24['Month'] = pd.Categorical(revenue_df_24['Month'], categories=sorted_months, ordered=True)
revenue_df_24 = revenue_df_24.sort_values('Month')

months_2024 = [month for month in sorted_months if not month.endswith("_25")]


# Create a line plot using Plotly
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=revenue_df_24['Month'], 
    y=revenue_df_24['Total Revenue'], 
    mode='lines+markers',
    name='Total Revenue'
))


fig.add_shape(
    type="rect",
    x0=months_2024[0],  # First 2024 month
    x1=months_2024[-1],  # Last 2024 month
    y0=-1e6,  # Extend below zero
    y1=max(revenue_df_24['Total Revenue']),  
    fillcolor="rgba(255, 0, 0, 0.1)",  # Light red with transparency
    layer="below",  
    line=dict(width=0)  
)
# Add a zero line for better visualization
fig.add_hline(y=0, line_dash="dash", line_color="black", annotation_text="", annotation_position="bottom right")

# Layout settings
fig.update_layout(
    title="Ecoring 2024-2025 Total Revenue",
    xaxis_title="Month",
    yaxis_title="Total Revenue",
    xaxis=dict(type='category'),
    template="plotly_white"
)

# Display the plot in Streamlit
st.plotly_chart(fig, use_container_width=True)

# Add heading and hyperlink
st.markdown("### For more information about all items sold, click the link below:")
st.markdown("<a href='https://docs.google.com/spreadsheets/d/1I79no2diVE6wWwJlVm35XE6J_KcWQDoHsERErcT2Pok/edit?gid=0#gid=0' style='font-size:20px; color:#4CAF50;'>Click here to view the Google Sheet</a>", unsafe_allow_html=True)
