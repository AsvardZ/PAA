
import streamlit as st
import pandas as pd
import requests
from io import BytesIO

st.set_page_config(page_title="Albion Online - Precios del Marketplace")

st.title("📊 Precios del Marketplace - Albion Online")
st.markdown("Genera precios actualizados de ítems por ciudad y analiza ganancias.")

# Ciudades e ítems a consultar
cities = ["Bridgewatch", "Martlock", "Thetford", "Fort Sterling", "Lymhurst", "Caerleon"]
items = [
    "T4_BAG", "T5_BAG", "T6_BAG",
    "T4_CAPE", "T5_CAPE", "T6_CAPE",
    "T4_MAIN_SWORD", "T5_MAIN_SWORD", "T6_MAIN_SWORD",
    "T4_ARMOR_PLATE_SET1", "T5_ARMOR_PLATE_SET1", "T6_ARMOR_PLATE_SET1",
    "T4_SHOES_PLATE_SET1", "T5_SHOES_PLATE_SET1", "T6_SHOES_PLATE_SET1"
]

# Botón para generar precios
if st.button("🔄 Generar precios actualizados"):
    base_url = "https://www.albion-online-data.com/api/v2/stats/prices/"
    results = []

    with st.spinner("Consultando la API de Albion..."):
        for item_id in items:
            url = f"{base_url}{item_id}?locations={','.join(cities)}"
            try:
                res = requests.get(url)
                if res.status_code == 200:
                    for entry in res.json():
                        sell = entry.get("sell_price_min", 0)
                        buy = entry.get("buy_price_max", 0)
                        if sell > 0 and buy > 0:
                            results.append({
                                "Ciudad": entry["city"],
                                "Item": item_id,
                                "Precio Venta (jugadores)": sell,
                                "Precio Compra (jugadores)": buy,
                                "Ganancia Potencial": sell - buy
                            })
            except Exception as e:
                st.warning(f"Error con {item_id}: {e}")

    if results:
        df = pd.DataFrame(results)
        st.success("✅ Precios generados correctamente")
        st.dataframe(df.sort_values("Ganancia Potencial", ascending=False))

        # Filtro por ciudad
        ciudad_filtrada = st.selectbox("Filtrar por ciudad", ["Todas"] + cities)
        if ciudad_filtrada != "Todas":
            df = df[df["Ciudad"] == ciudad_filtrada]

        # Descargar Excel
        output = BytesIO()
        df.to_excel(output, index=False)
        st.download_button(
            label="📥 Descargar Excel",
            data=output.getvalue(),
            file_name="precios_albion.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.error("No se encontraron datos para mostrar.")
