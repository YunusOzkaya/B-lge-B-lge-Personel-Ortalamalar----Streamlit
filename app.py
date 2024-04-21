import streamlit as st
import pandas as pd
import plotly.graph_objs as go


st.set_page_config(page_title="2023 Yılı Birim Bazında Personel ve Evrak Ortalamaları")

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            .stDeployButton {display:none;}

            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

unvan = st.selectbox(
    label="Lütfen Görmek İstediğiniz Unvanı Seçiniz : ",
    options=["Zabıt Katibi", "Mübaşir", "YİM"],
)

personelOrtalamalariMahkeme = pd.read_excel(
    io="PersonelOrtalamaları.xlsx", engine="openpyxl", sheet_name=unvan
)

evrakOrtalamalariMahkeme = pd.read_excel(
    io="EvrakOrtalamaları.xlsx",
    engine="openpyxl",
    sheet_name="Bölgesel Evrak Ortalamaları",
)

personelOrtalamalariSavcilik = pd.read_excel(
    io="PersonelOrtalamalarıSavcılık.xlsx",
    engine="openpyxl",
    sheet_name="Zabıt Katibi",
)

evrakOrtalamalariSavcilik = pd.read_excel(
    io="EvrakOrtalamalarıSavcılık.xlsx",
    engine="openpyxl",
    sheet_name="2023 Savcılık",
)

st.sidebar.header("Filtrele")
bolgeSelect = st.sidebar.multiselect(
    "Bölge Seçin: ",
    placeholder="Bölgeler",
    options=personelOrtalamalariMahkeme["Bölgeler"].unique(),
)

birim = st.sidebar.multiselect(
    "Birim Seçin:", placeholder="Birimler", options=personelOrtalamalariMahkeme.columns
)

filtered_dfPersonelMahkeme = round(
    personelOrtalamalariMahkeme[
        personelOrtalamalariMahkeme["Bölgeler"].isin(bolgeSelect)
    ],
    2,
)
filtered_dfEvrakMahkeme = round(
    evrakOrtalamalariMahkeme[evrakOrtalamalariMahkeme["Bölgeler"].isin(bolgeSelect)]
)

selected_columns = ["Bölgeler"] + birim
df_selectedMahkemePersonel = filtered_dfPersonelMahkeme[selected_columns]
df_selectedMahkemeEvrak = filtered_dfEvrakMahkeme[selected_columns]
st.markdown(f"## 2023 Yıl Bölgesel Ortalama {unvan} Verileri")
st.subheader("Unvan Bazlı Ortalama Tablosu")
st.dataframe(df_selectedMahkemePersonel)
st.subheader("Oluşturulan Evrak Bazlı Ortalama Tablosu")
st.dataframe(df_selectedMahkemeEvrak)


df_selectedMahkemePersonel["Ortalama Personel"] = df_selectedMahkemePersonel[
    birim
].mean(axis=1)
df_selectedMahkemeEvrak["Ortalama Evrak"] = df_selectedMahkemeEvrak[birim].mean(axis=1)
st.markdown("## grafikMahkeme Seçenekleri")
show_avg_personel = st.checkbox("Seçili Personelde Ortalama Personel Sayısı")
show_avg_evrak = st.checkbox("Seçili Bölgedeki Birimin Ortalama Evrak Sayısı")
show_ratio = st.checkbox("Seçili Bölge ve Birimdeki Personel Başına Düşen Evrak Sayısı")

grafikMahkeme = go.Figure()

if show_avg_personel:
    grafikMahkeme.add_trace(
        go.Bar(
            x=df_selectedMahkemePersonel["Bölgeler"],
            y=df_selectedMahkemePersonel["Ortalama Personel"],
            name="Ortalama Personel",
            marker_color="indianred",
        )
    )

if show_avg_evrak:
    grafikMahkeme.add_trace(
        go.Bar(
            x=df_selectedMahkemeEvrak["Bölgeler"],
            y=df_selectedMahkemeEvrak["Ortalama Evrak"],
            name="Ortalama Evrak",
            marker_color="lightsalmon",
        )
    )

if show_ratio:
    ratio = (
        df_selectedMahkemeEvrak["Ortalama Evrak"]
        / df_selectedMahkemePersonel["Ortalama Personel"]
    )
    grafikMahkeme.add_trace(
        go.Bar(
            x=df_selectedMahkemeEvrak["Bölgeler"],
            y=ratio,
            name="Personel Başına Evrak",
            marker_color="royalblue",
        )
    )

grafikMahkeme.update_layout(
    title="Bölgelere Göre Göstergeler",
    xaxis=dict(
        title="Bölgeler",
        tickfont_size=14,
        titlefont_size=25,
    ),
    yaxis=dict(
        title="Ortalama Evrak Sayıları",
        titlefont_size=25,
        tickfont_size=14,
    ),
    legend=dict(
        x=0,
        y=1.0,
        bgcolor="rgba(255, 255, 255, 0)",
        bordercolor="rgba(255, 255, 255, 0)",
    ),
    barmode="group",
    bargap=0.15,
    bargroupgap=0.1,
)
savcilikBtn = st.button("Savcılık Verilerini Görüntüle")
if savcilikBtn:
    ratio = round(
        (
            evrakOrtalamalariSavcilik["Toplam Evrak Sayısı"]
            / personelOrtalamalariSavcilik["Ortalama Zabıt Katibi"]
        ),
        2,
    )
    grafikSavcilik = go.Figure()
    grafikSavcilik.add_trace(
        go.Bar(
            x=evrakOrtalamalariSavcilik["Bölgeler"],
            y=ratio,
            name="Personel Başına Evrak",
            marker_color="royalblue",
        )
    )

    st.plotly_chart(grafikSavcilik)
st.plotly_chart(grafikMahkeme)
