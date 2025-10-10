import polars as pl
import matplotlib.pyplot as plt
import statsmodels.api as sm


# Read the CSV file into a Polars DataFrame
df = pl.read_csv('data.csv')

# Define the ranges where real values are expected
expected_ranges = [10,20,30, 80]

# List to store results
avg_precision = []
avg_accuracy = []

# Filter 'Ángulo' column based on expected ranges and then calculate stats
for angle in expected_ranges:
    print("-" * 10)
    filtered_df = df.filter((pl.col('Ángulo') == angle))
    # Calculate and print statistics
    ## Mean of measured values
    measured_mean = filtered_df['Medición'].mean()
    ## Add accuracy to df
    filtered_df = filtered_df.with_columns(
        (1 - (pl.col('Medición') - angle).abs() / angle).alias('Exactitud')
    )
    ## Add precision to df
    filtered_df = filtered_df.with_columns(
        (1 - (pl.col('Medición').std() / measured_mean)).alias('Precisión')
    )
    # Mostrar resultados
    print(f"\nÁngulo: {angle}")
    print("-" * 3)
    # Show only 3 decimal places
    print(f"Media de Medición: {measured_mean:.3f}")
    print(f"Exactitud promedio: {filtered_df['Exactitud'].mean()  * 100:.3f}")
    print(f"Precisión promedio: {filtered_df['Precisión'].mean()  * 100:.3f}")
    
    avg_accuracy.append(filtered_df['Exactitud'].mean())
    avg_precision.append(filtered_df['Precisión'].mean())
    
    
    
# Calculate overall statistics
print("-" * 10)
print("\nEstadísticas Generales:")
print(f"Exactitud promedio general: {sum(avg_accuracy) / len(avg_accuracy) * 100:.3f}")
print(f"Precisión promedio general: {sum(avg_precision) / len(avg_precision) * 100:.3f}")

# Create graph and get linear regression
df = df.to_pandas()
X = df['Ángulo']
y = df['Medición']
X = sm.add_constant(X)  # Añadir constante para el intercepto
model = sm.OLS(y, X).fit()
print(model.summary())
predictions = model.predict(X)
# Get R-squared value
plt.scatter(df['Ángulo'], df['Medición'], label='Datos', color='blue')
plt.plot(df['Ángulo'], predictions, color='red', label='Regresión Lineal')
plt.xlabel('Ángulo')
plt.ylabel('Medición')
# Show graph with legend
plt.legend()
plt.title('Regresión Lineal de Ángulo vs Medición')
plt.grid()
plt.show()
# Print m and b
m = model.params['Ángulo']
b = model.params['const']
print(f"y = {m:.3f}x + {b:.3f}")
print(f"R² = {model.rsquared:.3f}")