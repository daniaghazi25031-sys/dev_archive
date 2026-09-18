import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider


path = r"C:\Users\shamama\Downloads\archive (7)\Life Expectancy Data.csv"
df = pd.read_csv(path)
df.columns = [col.strip() for col in df.columns] 


years_list = sorted(df['Year'].unique())


fig, ax = plt.subplots(figsize=(12, 7))
plt.subplots_adjust(bottom=0.25) 


def get_data(year):
   
    return df[df['Year'] == year].sort_values("Alcohol", ascending=False).head(15)


initial_year = years_list[0]
top_data = get_data(initial_year)
bars = ax.bar(top_data['Country'], top_data['Alcohol'], color='#e67e22') 

ax.set_title(f"Top 15 Countries by Alcohol Consumption - Year: {initial_year}", fontsize=14)
ax.set_ylabel("Alcohol (Litres per capita)")
plt.xticks(rotation=45, ha='right')


ax_slider = plt.axes([0.2, 0.05, 0.6, 0.03], facecolor='#f0f0f0')
slider = Slider(                  # [المسافة من اليسار، المسافة من الأسفل، العرض، الارتفاع]                              
    ax_slider, 'Select Year  ', 
    0, len(years_list) - 1, 
    valinit=0, 
    valstep=1
)


def update(val):
    year_idx = int(slider.val)
    current_year = years_list[year_idx]
    
   
    new_data = get_data(current_year)
    
    
    ax.clear()
    ax.bar(new_data['Country'], new_data['Alcohol'], color='#e67e22')
    
   
    ax.set_title(f"Top 15 Countries by Alcohol Consumption - Year: {current_year}", fontsize=14)
    ax.set_ylabel("Alcohol (Litres per capita)")
    ax.set_ylim(0, 25) 
    
    plt.sca(ax)
    plt.xticks(rotation=45, ha='right')
    
    fig.canvas.draw_idle()


slider.on_changed(update)

plt.show()