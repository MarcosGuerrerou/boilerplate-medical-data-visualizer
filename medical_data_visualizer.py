import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv(r"medical_examination.csv")

# Add 'overweight' column
ow_list = []

for patient in df.index:
    Body_Mass_Index = df['weight'][patient] / ((df['height'][patient]/100)*(df['height'][patient]/100))
    if Body_Mass_Index > 25:
        ow_list.append(1)
    else:
        ow_list.append(0)

df['overweight'] = ow_list
# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.

cholesterol_list = []
gluc_list = []

for patient in df.index:
    if df['cholesterol'][patient] == 1:
        cholesterol_list.append(0)
    else:
        cholesterol_list.append(1)
    
    if df['gluc'][patient] == 1:
        gluc_list.append(0)
    else:
        gluc_list.append(1)

df['cholesterol'] = cholesterol_list
df['gluc'] = gluc_list

# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_reduced = df[['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight', 'cardio']]

    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
    
    df_cat = pd.melt(df_reduced, id_vars = 'cardio', value_vars = ['active', 'alco', 'cholesterol', 'gluc', 'overweight', 'smoke'], value_name = 'values')

    # Draw the catplot with 'sns.catplot()'

    graph = sns.catplot(x = 'variable', col = 'cardio', hue = 'values', data = df_cat, kind = 'count')
    graph.set_axis_labels('variable', 'total')
    fig = graph.fig


    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    # Clean the data
    df_heat = df[(df['ap_lo'] <= df['ap_hi']) 
                & (df['height'] >= df['height'].quantile(0.025)) 
                & (df['height'] <= df['height'].quantile(0.975))
                & (df['weight'] >= df['weight'].quantile(0.025)) 
                & (df['weight'] <= df['weight'].quantile(0.975))]

    # Calculate the correlation matrix
    corr = df_heat.corr()

    # Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr, dtype = bool))


    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize = (16, 12))

    # Draw the heatmap with 'sns.heatmap()'
    ax = sns.heatmap(corr, mask = mask, annot = True, fmt='.1f', center = 0, linewidths = 1, vmax = 0.25, vmin =-0.1, square = True, cbar_kws = {'format': '%.2f', 'shrink': 0.45})
    ax.set_yticklabels(ax.get_yticklabels(), rotation = 0, fontsize = 15)
    ax.set_xticklabels(ax.get_xticklabels(), rotation = 90, fontsize = 15)

    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig

if __name__ == '__main__':
    draw_heat_map()