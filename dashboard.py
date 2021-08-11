import pandas as pd
from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource, DataTable, TableColumn, PreText
from bokeh.transform import factor_cmap, cumsum
from bokeh.plotting import figure
from bokeh.palettes import Spectral6, Category20c
from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.core.properties import Seq, String
from math import pi


data = pd.read_excel('db.xls')

#INFORMACIÓN DE VACANTES ORDENADOS POR UBICACIÓN
vacante = data.loc[data['Vacante'] == True].groupby('Ubicación')\
    .count()[['Usuario']].sort_values('Usuario', ascending = False).reset_index()

source = ColumnDataSource(data = vacante.head(5))
fill_color=factor_cmap('Ubicación', palette = Spectral6, factors = sorted(vacante['Ubicación'].unique()))
figure1 = figure(x_range = vacante['Ubicación'], plot_height=350, plot_width=900, title="Vacantes ordenados por ubicación")
figure1.vbar(x='Ubicación', top='Usuario', width=0.9, source=source, legend_field="Ubicación",
       line_color='white', fill_color=fill_color)

#CONTRATACIONES POR AÑOS
data['Ultima contratación'] = data['Fecha de Última Contratación'].apply(lambda x: x.year)
contrataciones = data.groupby('Ultima contratación')\
    .count()[['Usuario']]\
    .sort_values('Ultima contratación')\
    .reset_index()

figure2 = figure(title="Contrataciones por años", plot_height=350, plot_width=1000, x_axis_label="Año", y_axis_label="Contrataciones")
figure2.line(contrataciones['Ultima contratación'], contrataciones['Usuario'], line_width=2)

#PERSONAS QUE SÍ PERTENECEN AL SINDICATO
sindicato = data.loc[(data['Pertenece a Sindicato'] == 'Si') & (data['Vacante'] == False)]\
    .groupby('Ubicación').count()[['Usuario']].sort_values('Usuario', ascending = False).reset_index()

source = ColumnDataSource(data=sindicato)
fill_color=factor_cmap('Ubicación', palette=Spectral6, factors = sorted(sindicato['Ubicación'].unique()))
figure3 = figure(x_range = sindicato['Ubicación'], plot_height=350, plot_width=900, title="Colaboradores que pertenecen al sindicato agrupados por ubicación")
figure3.vbar(x='Ubicación', top='Usuario', width=0.9, source=source, legend_field="Ubicación",
       line_color='white', fill_color=fill_color)

#TIPOS DE CONTRATOS
jornada = data.groupby('Tipo de contrato').count()[['Usuario']]\
    .sort_values('Usuario', ascending = False).reset_index()

source = ColumnDataSource(data = jornada)
fill_color = factor_cmap('Tipo de contrato', palette=Spectral6, factors=sorted(jornada['Tipo de contrato'].unique()))
figure4 = figure(x_range = jornada['Tipo de contrato'], plot_height=350, plot_width=700, title="Tipos de contrato")
figure4.vbar(x='Tipo de contrato', top='Estado del Empleado', width=0.9, source=source, legend_field="Tipo de contrato",
       line_color='white', fill_color=fill_color)

#PERSONAS CONTRATADOS POR DEPARTAMENTOS
departamentos = data.loc[data['Vacante'] == True]
departamentos = departamentos.groupby('Nombre Departamento')\
    .count()[['Usuario']].sort_values('Usuario', ascending = False).reset_index().head(10)

departamentos['angle'] = departamentos['Usuario']/departamentos['Usuario'].sum() * 2*pi
departamentos['color'] = Category20c[len(departamentos)]
departamentos['Departamento'] = departamentos['Nombre Departamento']
figure5 = figure(plot_height=720, plot_width=900, title="Los 10 departamentos com más empleados", tools="hover", tooltips="@Departamento: @Usuario", x_range=(-0.5, 1.0))
figure5.wedge(x=0, y=1, radius=0.4, start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", fill_color='color', legend_field='Departamento', source=departamentos)

col0 = column(figure1, figure2)
col1 = column(figure3,figure4)

row1 = row(col0, col1)
row2 = row(figure5)

layout = column(row1, row2)

output_file("index.html")
show(layout)