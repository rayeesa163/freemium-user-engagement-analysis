#import required libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

data = pd.read_csv(r"C:\Users\sraye\OneDrive\Desktop\freemium_app_user_data.csv")

data.head()


print(data.head())

data['signup_date'] = pd.to_datetime(data['signup_date'], errors='coerce')
data['last_active_date'] = pd.to_datetime(data['last_active_date'], errors='coerce')

# Check for rows with invalid or missing dates
invalid_dates = data[data['signup_date'].isna() | data['last_active_date'].isna()]
print(f"Number of rows with invalid or missing dates: {len(invalid_dates)}")
print("Rows with invalid or missing dates:")
print(invalid_dates)



# Calculate days_active for each user
data['days_active'] = (data['last_active_date'] - data['signup_date']).dt.days

print(data[['user_id', 'days_active']].head())

latest_date = data['last_active_date'].max()
data['churned'] = (latest_date - data['last_active_date']).dt.days > 30

retention_curve = data.groupby('days_active').size().reset_index(name='users')
sns.lineplot(data=retention_curve, x='days_active', y='users')
plt.title('User Retention Over Time')
plt.xlabel('Days Active')
plt.ylabel('Number of Users')
plt.grid(True)
plt.show()

#Correlation Analysis
corr_features = ['session_duration', 'in_app_purchases', 'days_active']
correlation_df = data[corr_features + ['churned']]
correlation_df['churned'] = correlation_df['churned'].astype(int)
sns.heatmap(correlation_df.corr(), annot=True, cmap='coolwarm')
plt.title('Feature Correlation with Churn')
plt.tight_layout()
plt.show()

data.to_csv('processed_freemium_app_data.csv', index=False)






