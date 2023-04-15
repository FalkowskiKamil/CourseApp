import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv("airline/medical_examination.csv")

# Add 'overweight' column
df['overweight'] = ((df['weight'] / ((df['height']/100)**2))>25).astype(int)
# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.   
normalize = lambda x: 0 if x == 1 else 1
df['cholesterol'] = df['cholesterol'].apply(normalize)
df['gluc'] = df['gluc'].apply(normalize)


# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
  
    columns = ["cholesterol", "gluc", "smoke", "alco", "active", "overweight"]
    df_cat = pd.melt(df, id_vars=["cardio"], value_vars=columns)


    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
    grouped = df_cat.groupby(["cardio", "variable", "value"]).size().reset_index(name="total")
    grouped = grouped.rename(columns={"value": "cat_value"})

    # Draw the catplot with 'sns.catplot()'

    cat_plot = sns.catplot(data=grouped, kind="bar", x="variable", y="total", hue="cat_value", col="cardio")

    # Get the figure for the output
    fig = cat_plot.fig


    # Do not modify the next two lines
    fig.savefig('airline/static/airline/catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    # Clean the data
    height_threshold_low = df['height'].quantile(0.025)
    height_threshold_high = df['height'].quantile(0.975)    
    weight_threshold_low = df['weight'].quantile(0.025)
    weight_threshold_high = df['weight'].quantile(0.975)

    mask_1 = (df['ap_lo'] <= df['ap_hi']) & \
        (df['height'] >= height_threshold_low) & \
        (df['height'] <= height_threshold_high) & \
        (df['weight'] >= weight_threshold_low) & \
        (df['weight'] <= weight_threshold_high)

    df_heat = df.loc[mask_1]

    # Calculate the correlation matrix
    corr = df_heat.corr()

    # Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))


    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(11, 9))

    # Draw the heatmap with 'sns.heatmap()'

    sns.heatmap(corr, mask=mask, cmap='coolwarm', annot=True, fmt='.1f', vmin=-1, vmax=1, square=True, ax=ax)
    plt.xticks(rotation=90)
    # Do not modify the next two lines
    fig.savefig('airline/static/airline/heatmap.png')
    return fig
