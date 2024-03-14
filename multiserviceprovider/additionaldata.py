import pandas as pd
import numpy as np

# Load the existing dataset
existing_df = pd.read_csv("sampledata.csv")

# Generate additional data
additional_data = pd.DataFrame({
    'branch_id': np.arange(51, 501),  # Generate 450 additional branch_ids
    'expense': np.random.randint(1000, 1000000, size=450),      # Random expense values
    'income': 0,  # Placeholder for income
    'num_booking': np.random.randint(45, 160, size=450),
    'avg_cost': np.random.randint(480, 1000, size=450),
})

# Calculate income based on expense
additional_data['income'] = np.where(additional_data['expense'] < 100000, 
                                     np.random.randint(80000, 120000, size=450),
                                     np.random.randint(50000, 80000, size=450))

# Identify high income and expense entries
high_income_mask = additional_data['income'] > 110000
high_expense_mask = additional_data['expense'] > 1500

# Increase num_booking for high income and high expense entries
additional_data.loc[high_income_mask, 'num_booking'] += 50
additional_data.loc[high_expense_mask, 'num_booking'] += 30

# Calculate is_profitable based on income and expense
additional_data['is_profitable'] = np.where(additional_data['income'] > additional_data['expense'], 1, 0)

# Concatenate the existing and synthetic data
combined_df = pd.concat([existing_df, additional_data], ignore_index=True)

# Save the combined dataset to a new CSV file
combined_df.to_csv("combined_data.csv", index=False)
