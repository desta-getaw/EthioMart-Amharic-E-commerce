import pandas as pd

def extract_price(text):
    """Helper function to extract price from text"""
    try:
        price_part = text.split('ዋጋ፦')[1].split('ብር')[0].strip()
        price = ''.join(c for c in price_part if c.isdigit())
        return int(price) if price else None
    except:
        return None

def calculate_vendor_scorecard(vendor_df):
    """Calculate metrics for a single vendor's DataFrame"""
    # Convert timestamp to datetime
    vendor_df = vendor_df.copy()
    vendor_df['timestamp'] = pd.to_datetime(vendor_df['timestamp'])
    vendor_df['date'] = vendor_df['timestamp'].dt.date
    
    # Extract price information
    vendor_df['price'] = vendor_df['text_original'].apply(extract_price)
    
    # Calculate time metrics
    start_date = vendor_df['timestamp'].min()
    end_date = vendor_df['timestamp'].max()
    total_days = (end_date - start_date).days
    total_weeks = max(total_days / 7, 1)
    
    # Calculate metrics
    metrics = {
        'Vendor': vendor_df['channel_name'].iloc[0],
        'Total Posts': len(vendor_df),
        'Posts/Week': len(vendor_df) / total_weeks,
        'Avg Views/Post': vendor_df['views'].mean(),
        'Median Views': vendor_df['views'].median(),
        'Max Views': vendor_df['views'].max(),
        'Top Product': vendor_df.loc[vendor_df['views'].idxmax(), 'text_original'][:50] + '...',
        'Top Product Price': vendor_df.loc[vendor_df['views'].idxmax(), 'price'],
        'Avg Price (ETB)': vendor_df['price'].mean(),
        'Median Price': vendor_df['price'].median(),
        'Image Posts %': vendor_df['has_image'].mean() * 100,
        'Date Range': f"{start_date.date()} to {end_date.date()}",
        'Days Active': total_days
    }
    
    return metrics

def generate_scorecard(all_vendors_df):
    """Generate scorecard for all vendors"""
    # Group by vendor and calculate metrics for each
    vendors = all_vendors_df['channel_name'].unique()
    scorecards = []
    
    for vendor in vendors:
        vendor_df = all_vendors_df[all_vendors_df['channel_name'] == vendor]
        scorecard = calculate_vendor_scorecard(vendor_df)
        scorecards.append(scorecard)
    
    # Convert to DataFrame
    scorecard_df = pd.DataFrame(scorecards)
    
    # Calculate lending score (custom formula)
    max_views = scorecard_df['Avg Views/Post'].max()
    max_freq = scorecard_df['Posts/Week'].max() * 1.5
    max_price = scorecard_df['Avg Price (ETB)'].max()
    
    scorecard_df['Lending Score'] = (
        (scorecard_df['Avg Views/Post'] / max_views * 50) +
        (scorecard_df['Posts/Week'] / max_freq * 30) +
        (scorecard_df['Avg Price (ETB)'] / max_price * 20)
    ).round(1)
    
    # Sort by Lending Score
    scorecard_df = scorecard_df.sort_values('Lending Score', ascending=False)
    
    # Select and order columns for final display
    display_columns = [
        'Vendor',
        'Posts/Week',
        'Avg Views/Post', 
        'Avg Price (ETB)',
        'Lending Score',
        'Total Posts',
        'Days Active',
        'Image Posts %'
    ]
    
    return scorecard_df[display_columns]