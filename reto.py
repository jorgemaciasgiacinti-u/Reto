import pandas as pd
import streamlit as st

df = pd.read_csv("Employee_data.csv")
print(df)

# Al realizar el código decidí elegir en la mayoría de los casos "multiselect", 
# ya que ayuda a que se puedan elegir diferentes combinaciones de parámetros y será de mayor utilidad para los usuarios.

#Código que contenga las instrucciones para el despliegue de 
# un título y una breve descripción de la aplicación web.

st.title("Indicadores de Desempeño de empleados")
st.write("Esta aplicación Web muestra gráficas referentes " \
"al desempeño de los empleados dentro de la empresa. La página permite seleccionar al usuario " \
"las características de los empleados que se requiera analizar (género,rango de puntajes de desempeño y estado civil).")

st.image("S_N_logo.png",use_container_width=True)

# elegir el género de los empleados
df["gender"] = df["gender"].str.strip()
genero = st.multiselect("Seleccione el género del empleado:", df["gender"].unique(),default=["M","F"])

datos_filtrados = df[df["gender"].isin(genero)]


#seleccionar un rango de desempeño del empleado:

valor = st.slider("Selecciona el nivel de desempeño del empleado:", df["performance_score"].min(), df["performance_score"].max(), (1,4))
st.write("Nivel seleccionado:", valor)

datos_filtrados = datos_filtrados[
    (datos_filtrados["performance_score"] >= valor[0]) & 
    (datos_filtrados["performance_score"] <= valor[1])
]
#seleccionar el estado civil del empleado:

m_status= st.multiselect("Seleccione el estado civil del empleado", df["marital_status"].unique(),default=['Single', 'Married', 'Divorced', 'Separated', 'Widowed'])

datos_filtrados = datos_filtrados[datos_filtrados["marital_status"].isin(m_status)]


# •	Código que permita mostrar un gráfico en
#  donde se visualice la distribución de los puntajes de desempeño.

import altair as alt


barras = alt.Chart(datos_filtrados).mark_bar(color="steelblue").encode(
    x=alt.X("performance_score:O", title="Nivel de desempeño",axis=alt.Axis(labelAngle=0)), 
    y=alt.Y("count()", title="Frecuencia"),
).properties(
    title="Distribución de Desempeño"
)

st.altair_chart(barras, use_container_width=True)

#•	Código que permita mostrar un gráfico en donde se visualice el promedio 
# de horas trabajadas por el género del empleado.

boxplot = alt.Chart(datos_filtrados).mark_boxplot().encode(
    x=alt.X("gender:N", title="Género",axis=alt.Axis(labelAngle=0)),
    y=alt.Y("average_work_hours:Q", title="Horas de Trabajo promedio",
    scale=alt.Scale(domain=[datos_filtrados["average_work_hours"].min()-200,datos_filtrados["average_work_hours"].max()+200])),
    color="gender:N"
).properties(
    title="Distribución de horas de trabajo por género"
)

st.altair_chart(boxplot)

#Código que permita mostrar un gráfico en donde se visualice la edad de 
# los empleados con respecto al salario de los mismo.


scatter = alt.Chart(datos_filtrados).mark_point(size=80, opacity=0.7, color="steelblue").encode(
    x=alt.X("salary:Q", title="Salario"),
    y=alt.Y("age:Q", title="Edad"),
).properties(
    title="Relación entre edad de los empleados y su salario"
)

st.altair_chart(scatter)


#•	Código que permita mostrar un gráfico en donde se visualice la relación 
# del promedio de horas trabajadas versus el puntaje de desempeño.

boxplot2 = alt.Chart(datos_filtrados).mark_boxplot(size=80).encode(
    x=alt.Y("performance_score:O", title="Puntaje de desempeño",axis=alt.Axis(labelAngle=0)),
    y=alt.X("average_work_hours:Q", title="Promedio de horas trabajadas"),
    color=alt.value("steelblue"),  
    opacity=alt.value(0.7)  
).properties(
    title="Relación del promedio de horas trabajadas versus el puntaje de desempeño"
)

st.altair_chart(boxplot2, use_container_width=True)


st.subheader("Conclusiones")
st.write("Del análisis se puede concluir que aproximadamente el 78% de los empleados están en el nivel 3 de desempeño y el grupo más pequeño es el que tiene un desempeño de 1." \
"También se observa que la mediana de las horas promedio de trabajo es mayor para las mujeres que para los hombres." \
"No se observa una relación clara entre la edad y el salario, lo que puede indicar que la empresa tiene variedad en los puestos y empleados que tiene." \
"Es interesante analizar que la mediana de las horas promedio de trabajo es mayor para los de nivel de desempeño 2, se esperaría" \
"que los de un mayor desepeño tuvieran mayores horas de trabajo promedio.")