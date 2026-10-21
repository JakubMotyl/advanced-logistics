import pandas as pd

df = pd.read_csv('data.csv')

# Clean column names (replace dots for SQL/database compatibility)
df = df.rename(columns={"Reached.on.Time_Y.N": "Reached_on_Time_Y_N"})

penalty_rates = pd.DataFrame({
    "Product_importance": ['low', 'medium', 'high'],
    "Delay_Penalty_Cost": [15.0, 30.0, 50.0]
})

# Perform LEFT JOIN to enrich shipment records with penalty benchmark rates
df_merged = pd.merge(df, penalty_rates, on="Product_importance", how="left")

# Condition (x == 0) evaluates to True (1) for delayed shipments and False (0) for on-time deliveries,
# multiplying directly by the rate to zero out costs for compliant shipments.
df_merged['Total_Delay_Penalty'] = (df_merged['Reached_on_Time_Y_N'] == 0) * df_merged['Delay_Penalty_Cost']

# Export clean datasets to multi-tab Excel report
with pd.ExcelWriter('Advanced_Logistics_Operations.xlsx') as writer:
    df_merged.to_excel(writer, sheet_name="Operations_Data", index=False)
    penalty_rates.to_excel(writer, sheet_name="Penalty_Lookup", index=False)