import requests
import pandas as pd
import plotly.express as px
import plotly.io as pio
from django.shortcuts import render

def dashboard_view(request):

    url = "https://www.datos.gov.co/resource/wgj6-cvyj.json"
    data = requests.get(url).json()

    df = pd.DataFrame(data)

    numeric_cols = [
        "indice_total",
        "indice_acu_cultura",
        "indice_avicultura",
        "indice_bovinos",
        "indice_porcicultura",
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")
    df = df.dropna(subset=["fecha"]).sort_values("fecha")

    year = request.GET.get("year")
    years_available = sorted(df["fecha"].dt.year.unique())

    if year:
        year = int(year)
        df = df[df["fecha"].dt.year == year]

    fig_line_total = px.line(
        df, x="fecha", y="indice_total",
        title="Índice Total a lo largo del tiempo", markers=True
    )

    fig_area_avicultura = px.area(
        df, x="fecha", y="indice_avicultura",
        title="Índice de Avicultura"
    )

    fig_bar_comparacion = px.bar(
        df,
        x="fecha",
        y=["indice_acu_cultura", "indice_bovinos", "indice_porcicultura"],
        title="Comparación de sectores por fecha"
    )

    fig_heatmap = px.imshow(
        df[numeric_cols].corr(),
        text_auto=True,
        title="Mapa de Calor - Correlación entre índices"
    )

    promedios = df[numeric_cols].mean()

    fig_dona = px.pie(
        values=promedios.values,
        names=promedios.index,
        hole=0.5,
        title="Distribución Promedio"
    )

    context = {
        "fig_line_total": pio.to_html(fig_line_total, full_html=False),
        "fig_area_avicultura": pio.to_html(fig_area_avicultura, full_html=False),
        "fig_bar_comparacion": pio.to_html(fig_bar_comparacion, full_html=False),
        "fig_heatmap": pio.to_html(fig_heatmap, full_html=False),
        "fig_dona": pio.to_html(fig_dona, full_html=False),
        "years": years_available,
        "selected_year": year,
    }

    return render(request, "dashboard/dashboard.html", context)
