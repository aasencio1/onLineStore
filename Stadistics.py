import json
import pandas as pd
from bokeh.plotting import figure, show
from bokeh.layouts import column

# Cargar datos desde el archivo JSON
with open("Payments.json", "r") as file:
    data = json.load(file)

# Convertir los datos en un DataFrame
df = pd.DataFrame(data)

# Asegurarse de que las fechas estén en formato de datetime
df['fecha'] = pd.to_datetime(df['fecha'])

# Crear un gráfico para pagos por día
p_day = figure(x_axis_type="datetime", title="Pagos por Día", width=800, height=300)
p_day.line(df['fecha'], df['pago_diario'], line_width=2, legend_label="Pagos Diarios")
p_day.circle(df['fecha'], df['pago_diario'], size=6, color="red", legend_label="Pagos Diarios")
p_day.legend.location = "top_left"

# Crear un gráfico para pagos por semana
p_week = figure(x_axis_type="datetime", title="Pagos por Semana", width=800, height=300)
p_week.line(df['fecha'], df['pago_semanal'], line_width=2, color="green", legend_label="Pagos Semanales")
p_week.circle(df['fecha'], df['pago_semanal'], size=6, color="blue", legend_label="Pagos Semanales")
p_week.legend.location = "top_left"

# Crear un gráfico para pagos por año
p_year = figure(x_axis_type="datetime", title="Pagos por Año", width=800, height=300)
p_year.line(df['fecha'], df['pago_anual'], line_width=2, color="orange", legend_label="Pagos Anuales")
p_year.circle(df['fecha'], df['pago_anual'], size=6, color="purple", legend_label="Pagos Anuales")
p_year.legend.location = "top_left"

# Mostrar los gráficos en una sola columna
layout = column(p_day, p_week, p_year)
show(layout)
