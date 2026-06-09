import os
import pandas as pd
import streamlit as st
import datetime
import altair as alt

TRANSLATIONS = {
    "es": {
        "page_title": "Informe Financiero: GABE - Barnabas Aid",
        "header_title": "Informe Financiero: GABE - Barnabas Aid",
        "intro_title": "📝 1. Introducción y Gestión Inicial de Fondos",
        "intro_p1": "El presente reporte detalla el uso y la administración de los recursos otorgados por <strong>Barnabas Aid</strong> para el desarrollo operativo de la Granja Alas de Bendición y Esperanza (GABE).",
        "intro_p2": "Antes de la recepción formal de estos fondos, la granja ya se encontraba en funcionamiento. Para mantener la continuidad operativa, fue necesario utilizar temporalmente recursos en calidad de préstamo provenientes de otros proyectos de la organización, bajo el compromiso de restituirlos una vez se recibiera el financiamiento de Barnabas Aid.",
        "intro_p3": "Por lo tanto, tras recibir el desembolso inicial:",
        "intro_li1": "<strong>USD 5,000</strong> se destinaron de inmediato a saldar dicho financiamiento puente.",
        "intro_li2": "<strong>USD 10,000</strong> quedaron disponibles netos para la ejecución directa de las operaciones de la granja (tal como se ilustra en la primera imagen adjunta).",
        "intro_img_caption": "Cheques y Soporte Financiero Inicial - Barnabas Aid",
        "context_title": "💱 2. Contexto Económico y Estrategia de Manejo Cambiario",
        "context_p1": "Operar en la economía venezolana representa un desafío financiero complejo. Aunque la mayoría de los bienes y servicios se pagan en Bolívares (VES), sus precios de referencia están anclados al Dólar (USD). La fluctuación diaria de la tasa de cambio genera una dinámica inflacionaria que dificulta la planificación financiera.",
        "context_p2": "A esto se suma la coexistencia de múltiples tipos de cambio en el mercado nacional:",
        "context_li1": "<strong>Tasa Oficial (BCV)</strong>: Regulada por el Banco Central de Venezuela.",
        "context_li2": "<strong>Tasa Euro</strong>: Utilizada en ciertos sectores comerciales.",
        "context_li3": "<strong>Tasa Binance (P2P)</strong>: Generalmente la más alta del mercado y de carácter variable.",
        "context_p3": "En este contexto, obtener divisas en efectivo a tasas razonables para la operación regular de una granja avícola es prácticamente imposible, ya que el efectivo suele transarse bajo la tasa Binance, más orientada a la especulación.",
        "context_h3": "Mecanismo de Ejecución Financiera",
        "context_p4": "Para mitigar estos riesgos y optimizar los recursos, se optó por movilizar los fondos desde una cuenta en USD bajo demanda, empleando dos metodologías de pago de acuerdo a la necesidad:",
        "context_p4_li1": "<strong>Pagos Directos</strong>: Transferencias directas a proveedores de bienes y servicios mediante la plataforma Zelle.",
        "context_p4_li2": "<strong>Conversión a Bolívares</strong>: Para los gastos locales que requerían moneda nacional, los fondos en USD se enviaban vía Zelle a dos operadores cambiarios de total confianza (identificados como Gabriel y Sierra). Estos operadores convertían las divisas a la tasa del día y transferían los Bolívares a la cuenta matriz de la Granja en el Banco Provincial. Se seleccionaron dos operadores para garantizar la disponibilidad inmediata de fondos y asegurar la continuidad operativa.",
        "context_note": "<strong>Nota aclaratoria:</strong> Aunque este procedimiento administrativo pueda parecer complejo, demostró ser la vía más rápida, eficiente y segura para ejecutar los fondos dadas las restricciones del entorno económico venezolano.",
        "structure_title": "📋 Estructura del Reporte",
        "structure_p1": "A continuación, el informe se desglosa en las siguientes secciones para su revisión:",
        "structure_li1": "<strong>Sección 1</strong>: Registro detallado de todas las transacciones de compra directa realizadas a proveedores vía Zelle.",
        "structure_li2": "<strong>Sección 2</strong>: Gráficos financieros que muestran el flujo, manejo y destino de los fondos ejecutados en Bolívares desde la cuenta del Banco Provincial.",
        "structure_li3": "<strong>Sección 3</strong>: Data administrativa completa en Bolívares, organizada en tres formatos para facilitar su análisis: Tabla general, Vista de Calendario y Cronograma de ejecución.",
        "zelle_title": "💳 Sección 1: Transacciones de compra directa de bienes y servicios via Zelle",
        "zelle_soporte_col": "Soporte",
        "zelle_soporte_help": "Soporte digital de la transacción",
        "zelle_monto_col": "Monto USD",
        "zelle_chart_header": "#### Compras Dierctas(pago via Zelle)",
        "zelle_chart_x": "Monto Total ($ USD)",
        "zelle_chart_y": "Descripción",
        "zelle_chart_tooltip_cat": "Descripción",
        "zelle_chart_tooltip_total": "Monto Total ($ USD)",
        "zelle_chart_tooltip_ops": "Nº Transacciones",
        "zelle_kpi_label": "Total Operaciones Directas",
        "zelle_kpi_sub": "operaciones registradas",
        "prov_title": "📊 Sección 2: Flujo de operaciones a través de la cuenta administrativa en Bs",
        "prov_kpi_saldo_label": "Saldo USD ($)",
        "prov_kpi_saldo_sub": "Neto acumulado en el rango",
        "prov_kpi_flow_label": "Flujo USD Detalle",
        "prov_kpi_flow_sub": "Ingresos y egresos en divisas",
        "prov_kpi_tx_label": "Transacciones",
        "prov_kpi_tx_sub": "Operaciones en la selección",
        "prov_kpi_fallback_rows_label": "Filas Cargadas",
        "prov_kpi_fallback_rows_sub": "Total de registros filtrados",
        "prov_kpi_fallback_cols_label": "Columnas Disponibles",
        "prov_kpi_fallback_cols_sub": "Estructura del conjunto de datos",
        "prov_data_expander": "Data de movimientos del Banco Provincial",
        "prov_no_records": "No hay registros que coincidan con los filtros aplicados.",
        "prov_col_fecha": "Fecha",
        "prov_col_desc": "Descripción",
        "prov_col_det": "Detalle",
        "prov_col_monto": "Monto$",
        "prov_records_caption": "Mostrando {len_display} de {len_raw} registros de la hoja '{sheet}'.",
        "download_csv_label": "📥 Descargar CSV",
        "viz_title": "### Visualización",
        "tab_flow": "Flujo de Fondos",
        "tab_income_detail": "Ingresos(Detalle)",
        "tab_income_summary": "Resumen de Ingresos",
        "tab_expense_detail": "Egresos(Detalle)",
        "tab_expense_summary": "Resumen de Egresos",
        "viz_flow_title": "#### Flujo de Fondos Diario ($ USD)",
        "viz_flow_x": "Fecha",
        "viz_flow_y": "Monto Neto ($ USD)",
        "viz_flow_tooltip_date": "Fecha",
        "viz_flow_tooltip_flow": "Monto ($ USD)",
        "viz_flow_tooltip_ops": "Nº Operaciones",
        "viz_flow_missing_info": "Se requiere información temporal para graficar la tendencia.",
        "viz_income_detail_title": "#### Distribución de Ingresos por Detalle ($ USD)",
        "viz_income_detail_x": "Monto Ingreso ($ USD)",
        "viz_income_detail_y": "Detalle (Agrupado)",
        "viz_income_detail_tooltip_concept": "Concepto",
        "viz_income_detail_tooltip_amount": "Monto ($ USD)",
        "viz_income_detail_tooltip_ops": "Nº Operaciones",
        "viz_income_detail_dialog_title": "Detalle de Operaciones",
        "viz_income_detail_dialog_header": "Operaciones de **{concepto}**",
        "viz_income_detail_dialog_total": "Total: **{len_df}** transacciones de ingresos.",
        "viz_income_detail_dialog_caption": "Nota: Haz clic fuera del popup o en la 'X' superior para cerrar.",
        "viz_income_detail_no_records": "No hay transacciones positivas (ingresos) registradas en esta selección.",
        "viz_desc_missing": "Columna de descripción no encontrada.",
        "viz_income_summary_title": "#### Distribución de Ingresos ($ USD) Agrupados por Grupo Principal",
        "viz_income_summary_donut_legend": "Grupos",
        "viz_income_summary_donut_tooltip_group": "Grupo Principal",
        "viz_income_summary_donut_tooltip_amount": "Monto USD",
        "viz_income_summary_no_records": "No se registraron ingresos (valores mayores a 0) en el conjunto filtrado.",
        "viz_expense_detail_title": "#### Distribución de Egresos por Detalle ($ USD)",
        "viz_expense_detail_x": "Monto Egreso ($ USD)",
        "viz_expense_detail_y": "Detalle (Agrupado)",
        "viz_expense_detail_tooltip_concept": "Concepto",
        "viz_expense_detail_tooltip_amount": "Monto Total ($ USD)",
        "viz_expense_detail_tooltip_ops": "Nº Operaciones",
        "viz_expense_detail_dialog_title": "Detalle de Egresos",
        "viz_expense_detail_dialog_header": "Egresos de **{concepto}**",
        "viz_expense_detail_dialog_total": "Total: **{len_df}** transacciones de egresos.",
        "viz_expense_detail_dialog_caption": "Nota: Haz clic fuera del popup o en la 'X' superior para cerrar.",
        "viz_expense_detail_no_records": "No hay transacciones de egreso (en $neg) registradas en esta selección.",
        "viz_expense_summary_title": "#### Distribución de Egresos ($ USD) Agrupados por Grupo Principal",
        "viz_expense_summary_donut_legend": "Grupos",
        "sec3_title": "Seccion 3: Consolidado Total de Egresos (directos + via cuenta nacional)",
        "sec3_table_title": "##### Resumen de Egresos Consolidados",
        "sec3_col_egreso": "Egreso",
        "sec3_col_monto": "Monto ($)",
        "sec3_total_label": "Total Consolidado",
        "sec3_legend_title": "Conceptos de Egreso",
        "footer_text": "Desarrollado para el <strong>Dashboard Administrativo GABE</strong> | ASIGLEH - Dirección de Finanzas. Todos los derechos reservados."
    },
    "en": {
        "page_title": "Financial Report: GABE - Barnabas Aid",
        "header_title": "Financial Report: GABE - Barnabas Aid",
        "intro_title": "📝 1. Introduction and Initial Fund Management",
        "intro_p1": "This report details the use and administration of the resources granted by <strong>Barnabas Aid</strong> for the operational development of the Alas de Bendición y Esperanza Farm (GABE).",
        "intro_p2": "Before the formal receipt of these funds, the farm was already in operation. To maintain operational continuity, it was necessary to temporarily use resources as a loan from other projects of the organization, under the commitment to return them once the financing from Barnabas Aid was received.",
        "intro_p3": "Therefore, after receiving the initial disbursement:",
        "intro_li1": "<strong>USD 5,000</strong> were immediately allocated to settle that bridge financing.",
        "intro_li2": "<strong>USD 10,000</strong> remained net available for the direct execution of the farm's operations (as illustrated in the first attached image).",
        "intro_img_caption": "Cheques and Initial Financial Support - Barnabas Aid",
        "context_title": "💱 2. Economic Context and Exchange Rate Management Strategy",
        "context_p1": "Operating in the Venezuelan economy represents a complex financial challenge. Although most goods and services are paid in Bolívares (VES), their reference prices are anchored to the US Dollar (USD). The daily fluctuation of the exchange rate generates an inflationary dynamic that makes financial planning difficult.",
        "context_p2": "To this is added the coexistence of multiple exchange rates in the national market:",
        "context_li1": "<strong>Official Rate (BCV)</strong>: Regulated by the Central Bank of Venezuela.",
        "context_li2": "<strong>Euro Rate</strong>: Used in certain commercial sectors.",
        "context_li3": "<strong>Binance Rate (P2P)</strong>: Generally the highest in the market and of variable nature.",
        "context_p3": "In this context, obtaining foreign currency in cash at reasonable rates for the regular operation of a poultry farm is practically impossible, since cash is usually traded under the Binance rate, which is more oriented to speculation.",
        "context_h3": "Financial Execution Mechanism",
        "context_p4": "To mitigate these risks and optimize resources, it was decided to mobilize the funds from a USD account on demand, employing two payment methodologies according to need:",
        "context_p4_li1": "<strong>Direct Payments</strong>: Direct transfers to suppliers of goods and services through the Zelle platform.",
        "context_p4_li2": "<strong>Conversion to Bolívares</strong>: For local expenses that required national currency, the USD funds were sent via Zelle to two highly trusted exchange operators (identified as Gabriel and Sierra). These operators converted the foreign currency at the rate of the day and transferred the Bolívares to the Farm's parent account at Banco Provincial. Two operators were selected to ensure the immediate availability of funds and guarantee operational continuity.",
        "context_note": "<strong>Clarifying note:</strong> Although this administrative procedure may seem complex, it proved to be the safest, fastest and most efficient way to execute the funds given the restrictions of the Venezuelan economic environment.",
        "structure_title": "📋 Report Structure",
        "structure_p1": "Below, the report is broken down into the following sections for your review:",
        "structure_li1": "<strong>Section 1</strong>: Detailed registry of all direct purchase transactions made to suppliers via Zelle.",
        "structure_li2": "<strong>Section 2</strong>: Financial charts showing the flow, management, and destination of funds executed in Bolívares from the Banco Provincial account.",
        "structure_li3": "<strong>Section 3</strong>: Complete administrative data in Bolívares, organized in three formats to facilitate analysis: General table, Calendar view, and Execution schedule.",
        "zelle_title": "💳 Section 1: Direct purchase transactions of goods and services via Zelle",
        "zelle_soporte_col": "Receipt",
        "zelle_soporte_help": "Digital support of the transaction",
        "zelle_monto_col": "Amount USD",
        "zelle_chart_header": "#### Direct Purchases (payment via Zelle)",
        "zelle_chart_x": "Total Amount ($ USD)",
        "zelle_chart_y": "Description",
        "zelle_chart_tooltip_cat": "Description",
        "zelle_chart_tooltip_total": "Total Amount ($ USD)",
        "zelle_chart_tooltip_ops": "No. of Transactions",
        "zelle_kpi_label": "Total Direct Operations",
        "zelle_kpi_sub": "registered operations",
        "prov_title": "📊 Section 2: Flow of operations through the administrative account in Bs",
        "prov_kpi_saldo_label": "USD Balance ($)",
        "prov_kpi_saldo_sub": "Net accumulated in range",
        "prov_kpi_flow_label": "USD Flow Details",
        "prov_kpi_flow_sub": "Income and expenses in foreign currency",
        "prov_kpi_tx_label": "Transactions",
        "prov_kpi_tx_sub": "Operations in selection",
        "prov_kpi_fallback_rows_label": "Loaded Rows",
        "prov_kpi_fallback_rows_sub": "Total filtered records",
        "prov_kpi_fallback_cols_label": "Available Columns",
        "prov_kpi_fallback_cols_sub": "Dataset structure",
        "prov_data_expander": "Banco Provincial transaction history data",
        "prov_no_records": "No records match the applied filters.",
        "prov_col_fecha": "Date",
        "prov_col_desc": "Description",
        "prov_col_det": "Details",
        "prov_col_monto": "Amount$",
        "prov_records_caption": "Showing {len_display} of {len_raw} records of sheet '{sheet}'.",
        "download_csv_label": "📥 Download CSV",
        "viz_title": "### Visualization",
        "tab_flow": "Cash Flow",
        "tab_income_detail": "Income(Detail)",
        "tab_income_summary": "Income Summary",
        "tab_expense_detail": "Expenses(Detail)",
        "tab_expense_summary": "Expenses Summary",
        "viz_flow_title": "#### Daily Cash Flow ($ USD)",
        "viz_flow_x": "Date",
        "viz_flow_y": "Net Amount ($ USD)",
        "viz_flow_tooltip_date": "Date",
        "viz_flow_tooltip_flow": "Amount ($ USD)",
        "viz_flow_tooltip_ops": "No. of Operations",
        "viz_flow_missing_info": "Temporal information is required to plot trend.",
        "viz_income_detail_title": "#### Income Distribution by Detail ($ USD)",
        "viz_income_detail_x": "Income Amount ($ USD)",
        "viz_income_detail_y": "Detail (Grouped)",
        "viz_income_detail_tooltip_concept": "Concept",
        "viz_income_detail_tooltip_amount": "Amount ($ USD)",
        "viz_income_detail_tooltip_ops": "No. of Operations",
        "viz_income_detail_dialog_title": "Operations Details",
        "viz_income_detail_dialog_header": "Operations of **{concepto}**",
        "viz_income_detail_dialog_total": "Total: **{len_df}** income transactions.",
        "viz_income_detail_dialog_caption": "Note: Click outside the popup or the 'X' at the top to close.",
        "viz_income_detail_no_records": "No positive transactions (income) registered in this selection.",
        "viz_desc_missing": "Description column not found.",
        "viz_income_summary_title": "#### Income Distribution ($ USD) Grouped by Main Group",
        "viz_income_summary_donut_legend": "Groups",
        "viz_income_summary_donut_tooltip_group": "Main Group",
        "viz_income_summary_donut_tooltip_amount": "Amount USD",
        "viz_income_summary_no_records": "No income (values greater than 0) registered in the filtered dataset.",
        "viz_expense_detail_title": "#### Expense Distribution by Detail ($ USD)",
        "viz_expense_detail_x": "Expense Amount ($ USD)",
        "viz_expense_detail_y": "Detail (Grouped)",
        "viz_expense_detail_tooltip_concept": "Concept",
        "viz_expense_detail_tooltip_amount": "Total Amount ($ USD)",
        "viz_expense_detail_tooltip_ops": "No. of Operations",
        "viz_expense_detail_dialog_title": "Expenses Details",
        "viz_expense_detail_dialog_header": "Expenses of **{concepto}**",
        "viz_expense_detail_dialog_total": "Total: **{len_df}** expense transactions.",
        "viz_expense_detail_dialog_caption": "Note: Click outside the popup or the 'X' at the top to close.",
        "viz_expense_detail_no_records": "No expense transactions (in $neg) registered in this selection.",
        "viz_expense_summary_title": "#### Expense Distribution ($ USD) Grouped by Main Group",
        "viz_expense_summary_donut_legend": "Groups",
        "sec3_title": "Section 3: Consolidated Total Expenses (direct + national account)",
        "sec3_table_title": "##### Consolidated Expenses Summary",
        "sec3_col_egreso": "Expense",
        "sec3_col_monto": "Amount ($)",
        "sec3_total_label": "Total Consolidated",
        "sec3_legend_title": "Expense Concepts",
        "footer_text": "Developed for the <strong>GABE Administrative Dashboard</strong> | ASIGLEH - Finance Division. All rights reserved."
    }
}

if 'language' not in st.session_state:
    st.session_state.language = 'es'

st.set_page_config(
    page_title=TRANSLATIONS['es']['page_title'] if st.session_state.language == 'es' else TRANSLATIONS['en']['page_title'],
    page_icon="📊",
    layout="wide"
)

# -------------------------------------------------------------------
# ESTILOS CSS PERSONALIZADOS (AESTHETIC DE ALTO NIVEL)
# -------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main-title {
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
    }
    
    .header-container {
        background: rgba(255, 255, 255, 0.9);
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
        border: 1px solid rgba(226, 232, 240, 0.8);
        margin-bottom: 25px;
    }
    
    .kpi-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
        border-left: 5px solid #2a5298;
        border-top: 1px solid #f1f5f9;
        border-right: 1px solid #f1f5f9;
        border-bottom: 1px solid #f1f5f9;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        margin-bottom: 15px;
    }
    
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.06);
    }
    
    .kpi-label {
        font-size: 0.85rem;
        color: #64748b;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .kpi-value {
        font-family: 'Outfit', sans-serif;
        font-size: 1.6rem;
        font-weight: 700;
        color: #1e293b;
        margin-top: 5px;
        margin-bottom: 0;
    }

    .kpi-subvalue {
        font-size: 0.8rem;
        margin-top: 4px;
        color: #94a3b8;
    }
    
    /* Separadores decorativos */
    .decor-line {
        height: 4px;
        width: 60px;
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        border-radius: 2px;
        margin-bottom: 20px;
    }
    
    .intro-container {
        background: rgba(255, 255, 255, 0.9);
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
        border: 1px solid rgba(226, 232, 240, 0.8);
        margin-bottom: 25px;
        color: #334155;
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------------
# INICIALIZACIÓN DE ESTADOS DE SESIÓN (ESTADO DEL DIALOG)
# -------------------------------------------------------------------
if 'active_dialog_concept' not in st.session_state:
    st.session_state.active_dialog_concept = None

if 'active_dialog_concept_neg' not in st.session_state:
    st.session_state.active_dialog_concept_neg = None

@st.dialog("Detalle de Operaciones" if st.session_state.language == "es" else "Operations Details")
def show_details_dialog(concepto, df_concept):
    lang = st.session_state.language
    st.markdown(f"### {TRANSLATIONS[lang]['viz_income_detail_dialog_header'].format(concepto=concepto)}")
    st.write(f"{TRANSLATIONS[lang]['viz_income_detail_dialog_total'].format(len_df=len(df_concept))}")
    
    df_display_dialog = df_concept.copy()
    
    desc_col = 'Descripción' if 'Descripción' in df_display_dialog.columns else ('Descripcion' if 'Descripcion' in df_display_dialog.columns else None)
    
    # Seleccionar solo las columnas solicitadas
    keep_cols = []
    if 'Fecha' in df_display_dialog.columns:
        keep_cols.append('Fecha')
    if desc_col:
        keep_cols.append(desc_col)
    if 'Detalle' in df_display_dialog.columns:
        keep_cols.append('Detalle')
    if 'en $' in df_display_dialog.columns:
        keep_cols.append('en $')
        
    df_display_dialog = df_display_dialog[keep_cols]
    
    # Cortar la columna Descripción a 20 caracteres
    if desc_col:
        df_display_dialog[desc_col] = df_display_dialog[desc_col].astype(str).str.slice(0, 20)
        
    if 'Fecha' in df_display_dialog.columns:
        df_display_dialog['Fecha'] = df_display_dialog['Fecha'].apply(lambda x: x.strftime('%d-%m-%Y') if pd.notna(x) and hasattr(x, 'strftime') else str(x))

    # Renombrar columnas para el idioma
    col_mapping = {
        'Fecha': 'Fecha' if lang == 'es' else 'Date',
        'Descripción': 'Descripción' if lang == 'es' else 'Description',
        'Descripcion': 'Descripción' if lang == 'es' else 'Description',
        'Detalle': 'Detalle' if lang == 'es' else 'Details',
        'en $': 'Monto$' if lang == 'es' else 'Amount$'
    }
    df_display_dialog = df_display_dialog.rename(columns=col_mapping)

    # Estilo de alto contraste (Verde para ingresos)
    def style_green(row):
        return ['background-color: #d1e7dd; color: #000000; font-weight: bold; border-bottom: 1px solid #b7d1c4;'] * len(row)
        
    styler_dialog = df_display_dialog.style.apply(style_green, axis=1)
    
    amount_col = 'Monto$' if lang == 'es' else 'Amount$'
    if amount_col in df_display_dialog.columns:
        styler_dialog = styler_dialog.format({amount_col: lambda x: f"{x:,.2f}" if (pd.notna(x) and isinstance(x, (int, float))) else ""})
        
    st.dataframe(styler_dialog, use_container_width=True, hide_index=True)
    st.caption(TRANSLATIONS[lang]['viz_income_detail_dialog_caption'])


@st.dialog("Detalle de Egresos" if st.session_state.language == "es" else "Expenses Details")
def show_details_dialog_neg(concepto, df_concept):
    lang = st.session_state.language
    st.markdown(f"### {TRANSLATIONS[lang]['viz_expense_detail_dialog_header'].format(concepto=concepto)}")
    st.write(f"{TRANSLATIONS[lang]['viz_expense_detail_dialog_total'].format(len_df=len(df_concept))}")
    
    df_display_dialog = df_concept.copy()
    
    desc_col = 'Descripción' if 'Descripción' in df_display_dialog.columns else ('Descripcion' if 'Descripcion' in df_display_dialog.columns else None)
    
    # Seleccionar solo las columnas solicitadas
    keep_cols = []
    if 'Fecha' in df_display_dialog.columns:
        keep_cols.append('Fecha')
    if desc_col:
        keep_cols.append(desc_col)
    if 'Detalle' in df_display_dialog.columns:
        keep_cols.append('Detalle')
    if 'en $' in df_display_dialog.columns:
        keep_cols.append('en $')
        
    df_display_dialog = df_display_dialog[keep_cols]
    
    # Cortar la columna Descripción a 20 caracteres
    if desc_col:
        df_display_dialog[desc_col] = df_display_dialog[desc_col].astype(str).str.slice(0, 20)
        
    if 'Fecha' in df_display_dialog.columns:
        df_display_dialog['Fecha'] = df_display_dialog['Fecha'].apply(lambda x: x.strftime('%d-%m-%Y') if pd.notna(x) and hasattr(x, 'strftime') else str(x))

    # Renombrar columnas para el idioma
    col_mapping = {
        'Fecha': 'Fecha' if lang == 'es' else 'Date',
        'Descripción': 'Descripción' if lang == 'es' else 'Description',
        'Descripcion': 'Descripción' if lang == 'es' else 'Description',
        'Detalle': 'Detalle' if lang == 'es' else 'Details',
        'en $': 'Monto$' if lang == 'es' else 'Amount$'
    }
    df_display_dialog = df_display_dialog.rename(columns=col_mapping)

    # Estilo de alto contraste (Rojo para egresos)
    def style_red(row):
        return ['background-color: #f8d7da; color: #000000; font-weight: bold; border-bottom: 1px solid #f5c2c7;'] * len(row)
        
    styler_dialog = df_display_dialog.style.apply(style_red, axis=1)
    
    amount_col = 'Monto$' if lang == 'es' else 'Amount$'
    if amount_col in df_display_dialog.columns:
        styler_dialog = styler_dialog.format({amount_col: lambda x: f"{x:,.2f}" if (pd.notna(x) and isinstance(x, (int, float))) else ""})
        
    st.dataframe(styler_dialog, use_container_width=True, hide_index=True)
    st.caption(TRANSLATIONS[lang]['viz_expense_detail_dialog_caption'])


# -------------------------------------------------------------------
# CARGA Y LIMPIEZA DE DATOS
# -------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXCEL_PATH = os.path.join(BASE_DIR, "gabe", "GabeEF.xlsx")
SELECTED_SHEET = "Hoja 2"

def clean_spanish_number(series):
    """Limpia números con formato español (separador de miles '.' y decimal ',')"""
    s = series.astype(str).str.strip()
    s = s.replace(['nan', 'None', '<NA>', ''], '0')
    s = s.str.replace('.', '', regex=False)
    s = s.str.replace(',', '.', regex=False)
    return pd.to_numeric(s, errors='coerce').fillna(0.0)

# -------------------------------------------------------------------
# CLASIFICACIÓN GLOBAL DE INGRESOS
# -------------------------------------------------------------------
def create_label_global(row, det_col, desc_col, lang="es"):
    """Clasifica una transacción de ingreso basándose en su detalle y descripción"""
    det = str(row.get(det_col) or "").strip() if det_col else ""
    desc = str(row.get(desc_col) or "").strip() if desc_col else ""
    label = det[:50] if (det and det.lower() not in ['nan', 'none', '']) else desc[:50]
    
    lbl_lower = label.lower()
    det_lower = det.lower()
    desc_lower = desc.lower()
    
    # Agrupar Gabriel
    if "gabriel" in lbl_lower:
        return "Gabriel"
        
    # Agrupar Sierra y las etiquetas específicas solicitadas
    if ("sierra" in lbl_lower or
        "gabe-prestamo" in lbl_lower or "gabe-prestamo" in det_lower or "gabe-prestamo" in desc_lower or
        "ingreso : 50 gabe" in lbl_lower or "ingreso : 50 gabe" in det_lower or "ingreso : 50 gabe" in desc_lower or
        "horeb" in lbl_lower or "horeb" in det_lower or "horeb" in desc_lower or
        "joel" in lbl_lower or "joel" in det_lower or "joel" in desc_lower or
        "gabe(100)" in lbl_lower or "gabe(100)" in det_lower or "gabe(100)" in desc_lower or
        "gabe-200" in lbl_lower or "gabe-200" in det_lower or "gabe-200" in desc_lower or
        "pmis-cierre" in lbl_lower or "pmis-cierre" in det_lower or "pmis-cierre" in desc_lower):
        return "Sierra"
        
    # Agrupar Betty / Betty Anselmi
    if "betty" in lbl_lower:
        return "Betty Anselmi"
        
    # Agrupar Tomas Manrique
    if "tomas" in lbl_lower or "tomás" in lbl_lower:
        return "Tomas Manrique"
        
    # Agrupar Carlos Niño
    if "niño" in lbl_lower or "nino" in lbl_lower:
        return "Carlos Niño"
        
    # Agrupar Josue Lobo
    if "lobo" in lbl_lower or "lobo" in det_lower or "lobo" in desc_lower:
        return "Josue Lobo"
        
    # Agrupar CarmenJulia
    if "ingreso-gabe-car" in lbl_lower or "ingreso-gabe-car" in det_lower or "ingreso-gabe-car" in desc_lower:
        return "CarmenJulia"
        
    # Agrupar Moriah-Elioenay
    if ("moriah" in lbl_lower or "moriah" in det_lower or "moriah" in desc_lower or
        "elioenay" in lbl_lower or "elioenay" in det_lower or "elioenay" in desc_lower or
        "gabe-ingreso-eli" in lbl_lower or "gabe-ingreso-eli" in det_lower or "gabe-ingreso-eli" in desc_lower):
        return "Moriah-Elioenay"
        
    # Agrupar Rafael Gonzalez
    if "rafael" in lbl_lower or "rafael" in det_lower or "rafael" in desc_lower:
        return "Rafael Gonzalez"
        
    # Agrupar El Shaddai
    if "gabe-ingreso-idl" in lbl_lower or "gabe-ingreso-idl" in det_lower or "gabe-ingreso-idl" in desc_lower or "idl" in lbl_lower or "idl" in det_lower or "idl" in desc_lower:
        return "El Shaddai"
        
    # Agrupar Gabe y ? o GABE-3$ -> ingreso desconocido
    if (("gabe" in lbl_lower and "?" in lbl_lower) or 
        ("gabe" in det_lower and "?" in det_lower) or 
        ("gabe" in desc_lower and "?" in desc_lower) or
        "gabe-3$" in lbl_lower or "gabe-3$" in det_lower or "gabe-3$" in desc_lower):
        return "ingreso desconocido" if lang == "es" else "unknown income"
        
    return label

# -------------------------------------------------------------------
# CLASIFICACIÓN GLOBAL DE EGRESOS
# -------------------------------------------------------------------
def classify_expense_global(row, det_col, desc_col, lang="es"):
    """Clasifica una transacción de egreso basándose en su detalle y descripción"""
    det = str(row.get(det_col) or "").strip() if det_col else ""
    desc = str(row.get(desc_col) or "").strip() if desc_col else ""
    label = det[:50] if (det and det.lower() not in ['nan', 'none', '']) else desc[:50]
    
    lbl_lower = label.lower()
    
    # Manu
    if "manu" in lbl_lower:
        return "Manu"
    # Roger
    if "roger" in lbl_lower:
        return "Roger"
    # VR or VictoR
    if "vr" in lbl_lower or "victor" in lbl_lower:
        return "VictoR"
    # Aceite
    if "aceite" in lbl_lower:
        return "Aceite" if lang == "es" else "Oil"
    # Gasolina
    if "gasolina" in lbl_lower:
        return "Gasolina" if lang == "es" else "Gasoline"
    # Juan
    if "juan" in lbl_lower:
        return "Juan"
    # Ronald
    if "ronald" in lbl_lower:
        return "Ronald"
    # Taxi
    if "taxi" in lbl_lower:
        return "Taxi"
    # Transporte (sin contener Manu o Roger, lo cual ya se garantiza al estar evaluado después)
    if "transporte" in lbl_lower:
        return "Transporte" if lang == "es" else "Transportation"
        
    return label


def map_zelle_desc(desc, lang="es"):
    desc_lower = str(desc).lower()
    if any(w in desc_lower for w in ['pollo', 'pollito', 'gallina']):
        return 'Comida Pollos y Gallinas' if lang == 'es' else 'Chickens and Hens Feed'
    elif any(w in desc_lower for w in ['limpieza', 'trabajo']):
        return 'Trabajos en Granja' if lang == 'es' else 'Farm Labor'
    elif 'limones' in desc_lower:
        return 'Siembras' if lang == 'es' else 'Planting'
    elif any(w in desc_lower for w in ['cuatrimoto', 'camión', 'camion']):
        return 'Vehiculos' if lang == 'es' else 'Vehicles'
    return desc


def donut_rollup_neg(concept, lang="es"):
    c_lower = str(concept).lower().strip()
    if any(p in c_lower for p in ['manu', 'juan', 'roger', 'victor', 'ronald', 'vr', 'staff', 'personal']):
        return 'Personal' if lang == 'es' else 'Staff'
    elif any(t in c_lower for t in ['transporte', 'gasolina', 'emergencia', 'transport', 'gasoline', 'emergency']):
        return 'para Transporte' if lang == 'es' else 'for Transportation'
    elif 'internet' in c_lower:
        return 'Internet' if lang == 'es' else 'Internet'
    else:
        return 'Activos y materiales' if lang == 'es' else 'Assets and Materials'


@st.cache_data(ttl=120)
def load_sheet_data(file_path, sheet_name):
    """Carga una hoja específica y aplica limpieza básica si es necesario"""
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        # Limpieza estándar si son las columnas financieras típicas
        if 'MontoBs' in df.columns:
            df['MontoBs_clean'] = clean_spanish_number(df['MontoBs'])
        if 'SaldoBs' in df.columns:
            df['SaldoBs_clean'] = clean_spanish_number(df['SaldoBs'])
        
        # Convertir Fecha a datetime si existe
        if 'Fecha' in df.columns:
            df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')
            
        return df
    except Exception as e:
        st.error(f"Error al cargar la hoja '{sheet_name}': {e}")
        return pd.DataFrame()

# Verificar existencia del archivo
if not os.path.exists(EXCEL_PATH):
    st.error(f"⚠️ No se encontró el archivo Excel en la ruta: {EXCEL_PATH}")
    st.info("Por favor, asegúrese de que el archivo 'GabeEF.xlsx' existe dentro de la carpeta 'gabe'.")
    st.stop()

# Cargar datos de la "Hoja 2"
df_raw = load_sheet_data(EXCEL_PATH, SELECTED_SHEET)
df_filtered = df_raw.copy()

# Verificar si tiene las columnas típicas de transacciones
has_financial_cols = all(col in df_raw.columns for col in ['Fecha', 'Descripción', 'MontoBs', 'en $'])

# -------------------------------------------------------------------
# SELECTOR DE IDIOMA / LANGUAGE SELECTOR
# -------------------------------------------------------------------
col_lang, _ = st.columns([1, 4])
with col_lang:
    selected_lang = st.selectbox(
        "🌐 Idioma / Language",
        options=["Español", "English"],
        index=0 if st.session_state.language == "es" else 1,
        key="lang_selector"
    )
    st.session_state.language = "es" if selected_lang == "Español" else "en"

lang_code = st.session_state.language

# -------------------------------------------------------------------
# CABECERA DEL DASHBOARD
# -------------------------------------------------------------------
st.markdown(
    f"""
    <div class="header-container">
        <h1 class="main-title">{TRANSLATIONS[lang_code]['header_title']}</h1>
        <div class="decor-line"></div>
    </div>
    """, 
    unsafe_allow_html=True
)

with st.expander(TRANSLATIONS[lang_code]['structure_title'], expanded=True):
    st.markdown(f"""
<div class="intro-container">
<p>{TRANSLATIONS[lang_code]['structure_p1']}</p>
<ul>
<li>{TRANSLATIONS[lang_code]['structure_li1']}</li>
<li>{TRANSLATIONS[lang_code]['structure_li2']}</li>
<li>{TRANSLATIONS[lang_code]['structure_li3']}</li>
</ul>
</div>
""", unsafe_allow_html=True)
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ") # Enlace provisional de YouTube

with st.expander(TRANSLATIONS[lang_code]['intro_title'], expanded=False):
    st.markdown(f"""
<div class="intro-container">
<p>{TRANSLATIONS[lang_code]['intro_p1']}</p>
<p>{TRANSLATIONS[lang_code]['intro_p2']}</p>
<p>{TRANSLATIONS[lang_code]['intro_p3']}</p>
<ul style="margin-bottom: 20px;">
<li>{TRANSLATIONS[lang_code]['intro_li1']}</li>
<li>{TRANSLATIONS[lang_code]['intro_li2']}</li>
</ul>
</div>
""", unsafe_allow_html=True)
    st.image(os.path.join("assets", "cheques.jpg"), caption=TRANSLATIONS[lang_code]['intro_img_caption'], use_container_width=True)

with st.expander(TRANSLATIONS[lang_code]['context_title'], expanded=False):
    st.markdown(f"""
<div class="intro-container">
<p>{TRANSLATIONS[lang_code]['context_p1']}</p>
<p>{TRANSLATIONS[lang_code]['context_p2']}</p>
<ol style="margin-bottom: 20px;">
<li>{TRANSLATIONS[lang_code]['context_li1']}</li>
<li>{TRANSLATIONS[lang_code]['context_li2']}</li>
<li>{TRANSLATIONS[lang_code]['context_li3']}</li>
</ol>
<p>{TRANSLATIONS[lang_code]['context_p3']}</p>
 
<h3 style="color: #2a5298; font-family: 'Outfit', sans-serif; font-size: 1.2rem; font-weight: 600; margin-top: 15px;">{TRANSLATIONS[lang_code]['context_h3']}</h3>
<p>{TRANSLATIONS[lang_code]['context_p4']}</p>
<ul style="margin-bottom: 20px;">
<li>{TRANSLATIONS[lang_code]['context_p4_li1']}</li>
<li>{TRANSLATIONS[lang_code]['context_p4_li2']}</li>
</ul>
<p style="background-color: #f8fafc; padding: 12px; border-left: 4px solid #3b82f6; border-radius: 4px; font-style: italic; margin-top: 15px;">
{TRANSLATIONS[lang_code]['context_note']}
</p>
</div>
""", unsafe_allow_html=True)

with st.expander(TRANSLATIONS[lang_code]['zelle_title'], expanded=False):
    # Definir datos
    zelle_data = [
        {"Proveedor": "Edgar Rincon Albarracin", "Fecha": "05-12-2025", "Monto USD": 560.00, "Descripción": "Comida Gallinas", "Imagen_Path": os.path.join("assets", "gabe01.jpg")},
        {"Proveedor": "Edgar Rincon Albarracin", "Fecha": "05-12-2025", "Monto USD": 150.00, "Descripción": "Por limpieza de granja ASIGLEH", "Imagen_Path": os.path.join("assets", "gabe02.jpg")},
        {"Proveedor": "Jose Zambrano", "Fecha": "08-12-2025", "Monto USD": 950.00, "Descripción": "Por cuatrimoto GABE", "Imagen_Path": os.path.join("assets", "gabe03.jpg")},
        {"Proveedor": "Juan Quinonez", "Fecha": "20-12-2025", "Monto USD": 261.00, "Descripción": "Compra comida para pollos", "Imagen_Path": os.path.join("assets", "gabe04.jpg")},
        {"Proveedor": "Vito Ingravallo Mendez", "Fecha": "22-01-2026", "Monto USD": 250.00, "Descripción": "Por reparación de camión de la granja", "Imagen_Path": os.path.join("assets", "gabe05.jpg")},
        {"Proveedor": "Edgar Rincon Albarracin", "Fecha": "02-02-2026", "Monto USD": 500.00, "Descripción": "Por pollitos GABE", "Imagen_Path": os.path.join("assets", "gabe06.jpg")},
        {"Proveedor": "Edgar Rincon Albarracin", "Fecha": "11-02-2026", "Monto USD": 56.00, "Descripción": "Por comida de gallinas", "Imagen_Path": os.path.join("assets", "gabe07.jpg")},
        
        {"Proveedor": "Brayan Diaz Marquez", "Fecha": "19-02-2026", "Monto USD": 200.00, "Descripción": "Por trabajos en la granja", "Imagen_Path": os.path.join("assets", "gabe09.jpg")},
        {"Proveedor": "Edgar Rincon Albarracin", "Fecha": "24-02-2026", "Monto USD": 350.00, "Descripción": "Por matas de limones GABE", "Imagen_Path": os.path.join("assets", "gabe10.jpg")},
        {"Proveedor": "Edgar Rincon Albarracin", "Fecha": "09-03-2026", "Monto USD": 108.00, "Descripción": "Por comida de gallinas", "Imagen_Path": os.path.join("assets", "gabe11.jpg")},
        {"Proveedor": "Edgar Rincon Albarracin", "Fecha": "09-03-2026", "Monto USD": 92.00, "Descripción": "Por comida de gallinas y pollos", "Imagen_Path": os.path.join("assets", "gabe12.jpg")}
    ]
    
    ZELLE_DESC_TRANSLATIONS = {
        "Comida Gallinas": "Hen Feed",
        "Por limpieza de granja ASIGLEH": "ASIGLEH Farm Cleaning",
        "Por cuatrimoto GABE": "GABE ATV/Quad",
        "Compra comida para pollos": "Chicken Feed Purchase",
        "Por reparación de camión de la granja": "Farm Truck Repair",
        "Por pollitos GABE": "GABE Chicks",
        "Por comida de gallinas": "Hen Feed",
        "Por trabajos en la granja": "Farm Labor/Works",
        "Por matas de limones GABE": "GABE Lemon Plants",
        "Por comida de gallinas y pollos": "Chicken and Hen Feed"
    }
    
    df_zelle = pd.DataFrame(zelle_data)
    
    # Agregar columna con base64 si existe, de lo contrario None
    def load_image_base64(path):
        if os.path.exists(path):
            try:
                import base64
                with open(path, "rb") as f:
                    encoded = base64.b64encode(f.read()).decode("utf-8")
                ext = os.path.splitext(path)[1].lower().replace(".", "")
                mime = f"image/{ext}" if ext in ["png", "jpg", "jpeg", "gif", "webp"] else "image/jpeg"
                return f"data:{mime};base64,{encoded}"
            except Exception:
                return None
        return None

    df_zelle["Soporte (Imagen)"] = df_zelle["Imagen_Path"].apply(load_image_base64)
    
    # Omitimos la columna Imagen_Path en la vista
    df_zelle_display = df_zelle.drop(columns=["Imagen_Path"])
    
    # Traducir los nombres de las columnas para visualización si es necesario
    df_zelle_display_lang = df_zelle_display.copy()
    if lang_code == "en":
        df_zelle_display_lang = df_zelle_display_lang.rename(columns={
            "Proveedor": "Supplier",
            "Fecha": "Date",
            "Descripción": "Description",
            "Monto USD": "Amount USD"
        })
        df_zelle_display_lang["Description"] = df_zelle_display_lang["Description"].map(ZELLE_DESC_TRANSLATIONS).fillna(df_zelle_display_lang["Description"])
        
    monto_col_name = "Monto USD" if lang_code == "es" else "Amount USD"
    
    st.dataframe(
        df_zelle_display_lang,
        column_config={
            "Soporte (Imagen)": st.column_config.ImageColumn(TRANSLATIONS[lang_code]['zelle_soporte_col'], help=TRANSLATIONS[lang_code]['zelle_soporte_help']),
            monto_col_name: st.column_config.NumberColumn(TRANSLATIONS[lang_code]['zelle_monto_col'], format="$%.2f")
        },
        use_container_width=True,
        hide_index=True
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.write(TRANSLATIONS[lang_code]['zelle_chart_header'])
    
    df_zelle_grouped = df_zelle.copy()
    df_zelle_grouped['Desc_Grouped'] = df_zelle_grouped['Descripción'].apply(lambda x: map_zelle_desc(x, lang_code))
    
    # Crear gráfico de barras horizontales
    df_desc = df_zelle_grouped.groupby("Desc_Grouped").agg(
        Monto_Total=("Monto USD", "sum"),
        Operaciones=("Monto USD", "count")
    ).reset_index()
    
    # Gráfico de barras horizontales usando Altair
    desc_chart = alt.Chart(df_desc).mark_bar().encode(
        x=alt.X('Monto_Total:Q', title=TRANSLATIONS[lang_code]['zelle_chart_x']),
        y=alt.Y('Desc_Grouped:N', sort='-x', title=TRANSLATIONS[lang_code]['zelle_chart_y']),
        color=alt.value('#1e3c72'),  # Azul institucional
        tooltip=[
            alt.Tooltip('Desc_Grouped:N', title=TRANSLATIONS[lang_code]['zelle_chart_tooltip_cat']),
            alt.Tooltip('Monto_Total:Q', title=TRANSLATIONS[lang_code]['zelle_chart_tooltip_total'], format=',.2f'),
            alt.Tooltip('Operaciones:Q', title=TRANSLATIONS[lang_code]['zelle_chart_tooltip_ops'])
        ]
    ).properties(height=250)
    
    st.altair_chart(desc_chart, use_container_width=True)
    
    # Calcular totales para el Card
    total_monto_directo = df_zelle["Monto USD"].sum()
    total_ops_directo = len(df_zelle)
    
    st.markdown(
        f"""
        <div class="kpi-card" style="border-left-color: #1e3c72; max-width: 350px; margin-top: 15px;">
            <div class="kpi-label">{TRANSLATIONS[lang_code]['zelle_kpi_label']}</div>
            <div class="kpi-value" style="color: #1e3c72;">${total_monto_directo:,.2f}</div>
            <div class="kpi-subvalue">{total_ops_directo} {TRANSLATIONS[lang_code]['zelle_kpi_sub']}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# -------------------------------------------------------------------
# SECCIÓN 2: FLUJO EN BS
# -------------------------------------------------------------------
with st.expander(TRANSLATIONS[lang_code]['prov_title'], expanded=False):
    # -------------------------------------------------------------------
    # SECCIÓN DE MÉTRICAS (KPIs) - SIN CARD "SALDO DE CAJA"
    # -------------------------------------------------------------------
    if not df_filtered.empty and has_financial_cols:
        # Preparar datos financieros
        total_tx = len(df_filtered)
        
        # Calcular sumas
        usd_col = 'en $'
        usd_pos_col = 'en $pos' if 'en $pos' in df_filtered.columns else None
        usd_neg_col = 'en $neg' if 'en $neg' in df_filtered.columns else None
        
        usd_total_net = df_filtered[usd_col].sum() if usd_col in df_filtered.columns else 0.0
        usd_total_pos = df_filtered[usd_pos_col].sum() if usd_pos_col and usd_pos_col in df_filtered.columns else df_filtered[df_filtered[usd_col] > 0][usd_col].sum()
        usd_total_neg = df_filtered[usd_neg_col].sum() if usd_neg_col and usd_neg_col in df_filtered.columns else df_filtered[df_filtered[usd_col] < 0][usd_col].sum()
        
        # Renderizar KPI Cards (3 columnas)
        col1, col2, col3 = st.columns(3)
        
        with col1:
            usd_color = "#16a34a" if usd_total_net >= 0 else "#dc2626"
            st.markdown(
                f"""
                <div class="kpi-card" style="border-left-color: {usd_color};">
                    <div class="kpi-label">{TRANSLATIONS[lang_code]['prov_kpi_saldo_label']}</div>
                    <div class="kpi-value" style="color: {usd_color};">${usd_total_net:,.2f}</div>
                    <div class="kpi-subvalue">{TRANSLATIONS[lang_code]['prov_kpi_saldo_sub']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
        with col2:
            st.markdown(
                f"""
                <div class="kpi-card" style="border-left-color: #16a34a;">
                    <div class="kpi-label">{TRANSLATIONS[lang_code]['prov_kpi_flow_label']}</div>
                    <div class="kpi-value" style="font-size: 1.25rem; display: flex; flex-direction: column;">
                        <span style="color: #16a34a;">🟢 +${usd_total_pos:,.2f}</span>
                        <span style="color: #dc2626; margin-top: 4px;">🔴 -${abs(usd_total_neg):,.2f}</span>
                    </div>
                    <div class="kpi-subvalue">{TRANSLATIONS[lang_code]['prov_kpi_flow_sub']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
        with col3:
            st.markdown(
                f"""
                <div class="kpi-card" style="border-left-color: #64748b;">
                    <div class="kpi-label">{TRANSLATIONS[lang_code]['prov_kpi_tx_label']}</div>
                    <div class="kpi-value">{total_tx}</div>
                    <div class="kpi-subvalue">{TRANSLATIONS[lang_code]['prov_kpi_tx_sub']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
    
    # Si la hoja no tiene las columnas financieras típicas
    elif not df_filtered.empty:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(
                f"""
                <div class="kpi-card" style="border-left-color: #2b5298;">
                    <div class="kpi-label">{TRANSLATIONS[lang_code]['prov_kpi_fallback_rows_label']}</div>
                    <div class="kpi-value">{df_filtered.shape[0]}</div>
                    <div class="kpi-subvalue">{TRANSLATIONS[lang_code]['prov_kpi_fallback_rows_sub']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with col2:
            st.markdown(
                f"""
                <div class="kpi-card" style="border-left-color: #475569;">
                    <div class="kpi-label">{TRANSLATIONS[lang_code]['prov_kpi_fallback_cols_label']}</div>
                    <div class="kpi-value">{df_filtered.shape[1]}</div>
                    <div class="kpi-subvalue">{TRANSLATIONS[lang_code]['prov_kpi_fallback_cols_sub']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # -------------------------------------------------------------------
    # SECCIÓN DEL EXPANDER "data" (REQUERIDO)
    # -------------------------------------------------------------------
    with st.expander(TRANSLATIONS[lang_code]['prov_data_expander'], expanded=True):
        if df_filtered.empty:
            st.info(TRANSLATIONS[lang_code]['prov_no_records'])
        else:
            # Preparar dataframe para mostrar
            df_display = df_filtered.copy()
            
            # Eliminar las columnas técnicas de limpieza y la columna SaldoBs solicitada
            cols_to_drop = [c for c in ['MontoBs_clean', 'SaldoBs_clean', 'SaldoBs'] if c in df_display.columns]
            if cols_to_drop:
                df_display = df_display.drop(columns=cols_to_drop)
                
            # Reemplazar None/NaN con celdas en blanco para en $pos y en $neg
            def clean_none_to_blank(val):
                if pd.isna(val) or val is None or str(val).strip().lower() in ['none', 'nan', '<na>', '']:
                    return ""
                try:
                    # Si es un número, devolverlo formateado
                    num = float(val)
                    return f"{num:,.2f}"
                except (ValueError, TypeError):
                    return str(val)
    
            for col in ['en $pos', 'en $neg', 'en$neg']:
                if col in df_display.columns:
                    df_display[col] = df_display[col].apply(clean_none_to_blank)
                    
            # Formatear la fecha para visualización limpia
            if 'Fecha' in df_display.columns:
                df_display['Fecha'] = df_display['Fecha'].apply(lambda x: x.strftime('%d-%m-%Y') if pd.notna(x) and hasattr(x, 'strftime') else str(x))
    
            # Definir la lógica de styling (Alto Contraste)
            def style_rows_by_usd(row):
                val = row.get('en $')
                try:
                    val_float = float(val) if pd.notna(val) else float('nan')
                except (ValueError, TypeError):
                    val_float = float('nan')
                    
                if pd.isna(val_float):
                    return ['background-color: #ffffff; color: #1e293b; border-bottom: 1px solid #e2e8f0;'] * len(row)
                    
                if val_float >= 0:
                    return ['background-color: #d1e7dd; color: #000000; font-weight: bold; border-bottom: 1px solid #b7d1c4;'] * len(row)
                else:
                    return ['background-color: #f8d7da; color: #000000; font-weight: bold; border-bottom: 1px solid #f5c2c7;'] * len(row)
    
            # Aplicar el estilo de alto contraste
            styler = df_display.style.apply(style_rows_by_usd, axis=1)
    
            # Formatear la columna 'en $' si es numérica
            if 'en $' in df_display.columns:
                styler = styler.format({'en $': lambda x: f"{x:,.2f}" if (pd.notna(x) and isinstance(x, (int, float))) else ""})
    
            desc_col = 'Descripción' if 'Descripción' in df_display.columns else ('Descripcion' if 'Descripcion' in df_display.columns else None)
            
            column_config_dict = {
                "en $": st.column_config.Column(TRANSLATIONS[lang_code]['prov_col_monto']),
                "en $pos": None,
                "en $neg": None,
                "en$neg": None,
                "Detalle": st.column_config.Column(TRANSLATIONS[lang_code]['prov_col_det'] if lang_code == "en" else "Detalle", width="large"),
                "Fecha": st.column_config.Column(TRANSLATIONS[lang_code]['prov_col_fecha'])
            }
            if desc_col:
                column_config_dict[desc_col] = st.column_config.Column(TRANSLATIONS[lang_code]['prov_col_desc'])
            
            # Mostrar DataFrame con el styler aplicado
            st.dataframe(
                styler, 
                column_config=column_config_dict,
                use_container_width=True,
                hide_index=True
            )
            
            # Fila de acciones adicionales dentro del expander
            c_info, c_dl = st.columns([4, 1])
            with c_info:
                st.caption(TRANSLATIONS[lang_code]['prov_records_caption'].format(len_display=len(df_display), len_raw=len(df_raw), sheet=SELECTED_SHEET))
            
            with c_dl:
                # Botón para descargar datos filtrados en formato CSV
                csv_data = df_display.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label=TRANSLATIONS[lang_code]['download_csv_label'],
                    data=csv_data,
                    file_name=f"gabe_data_{SELECTED_SHEET}_{datetime.date.today()}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
    # -------------------------------------------------------------------
    # SECCIÓN DE VISUALIZACIÓN GRÁFICA ADICIONAL (PREMIUM)
    # -------------------------------------------------------------------
    if not df_filtered.empty and has_financial_cols:
        st.markdown(TRANSLATIONS[lang_code]['viz_title'])
        
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            TRANSLATIONS[lang_code]['tab_flow'], 
            TRANSLATIONS[lang_code]['tab_income_detail'],
            TRANSLATIONS[lang_code]['tab_income_summary'],
            TRANSLATIONS[lang_code]['tab_expense_detail'],
            TRANSLATIONS[lang_code]['tab_expense_summary']
        ])
        
        with tab1:
            # Flujo de Fondos Diario ($ USD) con barras coloreadas según el signo
            df_trend = df_filtered.sort_values(by='Fecha', ascending=True).dropna(subset=['Fecha']).copy()
            if len(df_trend) > 0:
                df_trend['en $_numeric'] = pd.to_numeric(df_trend['en $'], errors='coerce').fillna(0.0)
                
                # Agrupar por Fecha para ver flujos consolidados diarios y operaciones
                df_daily = df_trend.groupby('Fecha').agg(
                    Flow_Total=('en $_numeric', 'sum'),
                    Operaciones=('en $_numeric', 'count')
                ).reset_index()
                df_daily['Fecha_str'] = df_daily['Fecha'].dt.strftime('%d-%m-%Y')
                
                st.write(TRANSLATIONS[lang_code]['viz_flow_title'])
                
                # Gráfico de barras interactivo con Altair
                daily_flow_chart = alt.Chart(df_daily).mark_bar().encode(
                    x=alt.X('Fecha:T', title=TRANSLATIONS[lang_code]['viz_flow_x']),
                    y=alt.Y('Flow_Total:Q', title=TRANSLATIONS[lang_code]['viz_flow_y']),
                    color=alt.condition(
                        alt.datum['Flow_Total'] >= 0,
                        alt.value('#16a34a'),  # Verde para flujo positivo
                        alt.value('#dc2626')   # Rojo para flujo negativo
                    ),
                    tooltip=[
                        alt.Tooltip('Fecha_str:N', title=TRANSLATIONS[lang_code]['viz_flow_tooltip_date']),
                        alt.Tooltip('Flow_Total:Q', title=TRANSLATIONS[lang_code]['viz_flow_tooltip_flow'], format=',.2f'),
                        alt.Tooltip('Operaciones:Q', title=TRANSLATIONS[lang_code]['viz_flow_tooltip_ops'])
                    ]
                ).properties(height=400)
                st.altair_chart(daily_flow_chart, use_container_width=True)
            else:
                st.info(TRANSLATIONS[lang_code]['viz_flow_missing_info'])
                
        with tab2:
            st.write(TRANSLATIONS[lang_code]['viz_income_detail_title'])
            desc_col_name = 'Descripción' if 'Descripción' in df_filtered.columns else ('Descripcion' if 'Descripcion' in df_filtered.columns else None)
            det_col_name = 'Detalle' if 'Detalle' in df_filtered.columns else None
            
            if desc_col_name:
                df_chart_data = df_filtered.copy()
                df_chart_data['en $_numeric'] = pd.to_numeric(df_chart_data['en $'], errors='coerce').fillna(0.0)
                
                # Filtro: Mostrar SOLO las positivas (Ingresos > 0)
                df_chart_data = df_chart_data[df_chart_data['en $_numeric'] > 0]
                
                if not df_chart_data.empty:
                    # Formar etiqueta usando create_label_global
                    df_chart_data['Concepto'] = df_chart_data.apply(lambda r: create_label_global(r, det_col_name, desc_col_name, lang_code), axis=1)
                    
                    # Agrupar, sumar monto y contar operaciones
                    desc_usd_sum = df_chart_data.groupby('Concepto').agg(
                        Monto_Total=('en $_numeric', 'sum'),
                        Operaciones=('en $_numeric', 'count')
                    ).reset_index()
                    
                    # Ordenar por monto descendente
                    desc_usd_sum = desc_usd_sum.sort_values(by='Monto_Total', ascending=False).head(15)
                    
                    # Gráfico de barras horizontales con Altair (incluye Nº Operaciones en Tooltip)
                    select_point = alt.selection_point(fields=['Concepto'], name='select_concept')
                    
                    horizontal_bar = alt.Chart(desc_usd_sum).mark_bar().encode(
                        x=alt.X('Monto_Total:Q', title=TRANSLATIONS[lang_code]['viz_income_detail_x']),
                        y=alt.Y('Concepto:N', sort='-x', title=TRANSLATIONS[lang_code]['viz_income_detail_y']),
                        color=alt.value('#16a34a'),  # Verde para ingresos
                        tooltip=[
                            alt.Tooltip('Concepto:N', title=TRANSLATIONS[lang_code]['viz_income_detail_tooltip_concept']), 
                            alt.Tooltip('Monto_Total:Q', title=TRANSLATIONS[lang_code]['viz_income_detail_tooltip_amount'], format=',.2f'),
                            alt.Tooltip('Operaciones:Q', title=TRANSLATIONS[lang_code]['viz_income_detail_tooltip_ops'])
                        ]
                    ).add_params(
                        select_point
                    ).properties(height=400)
                    
                    event_data = st.altair_chart(horizontal_bar, use_container_width=True, on_select="rerun")
                    
                    # Manejar la selección para el Dialog emergente
                    if event_data and "selection" in event_data:
                        selection = event_data["selection"].get("select_concept", [])
                        selected_concept = None
                        if selection and isinstance(selection, list) and len(selection) > 0:
                            selected_concept = selection[0].get("Concepto") if isinstance(selection[0], dict) else selection[0]
                        elif selection and isinstance(selection, dict):
                            concepts = selection.get("Concepto", [])
                            selected_concept = concepts[0] if concepts else None
                            
                        if selected_concept:
                            if st.session_state.active_dialog_concept != selected_concept:
                                st.session_state.active_dialog_concept = selected_concept
                                # Filtrar operaciones correspondientes a este concepto en df_chart_data
                                df_concept_ops = df_chart_data[df_chart_data['Concepto'] == selected_concept]
                                if not df_concept_ops.empty:
                                    show_details_dialog(selected_concept, df_concept_ops)
                        else:
                            st.session_state.active_dialog_concept = None
                else:
                    st.info(TRANSLATIONS[lang_code]['viz_income_detail_no_records'])
            else:
                st.info(TRANSLATIONS[lang_code]['viz_desc_missing'])
    
        with tab3:
            st.write(TRANSLATIONS[lang_code]['viz_income_summary_title'])
            desc_col_name = 'Descripción' if 'Descripción' in df_filtered.columns else ('Descripcion' if 'Descripcion' in df_filtered.columns else None)
            det_col_name = 'Detalle' if 'Detalle' in df_filtered.columns else None
            
            if desc_col_name:
                df_incomes = df_filtered.copy()
                df_incomes['en $_numeric'] = pd.to_numeric(df_incomes['en $'], errors='coerce').fillna(0.0)
                
                # Filtrar solo ingresos (monto > 0)
                df_only_incomes = df_incomes[df_incomes['en $_numeric'] > 0].copy()
                
                if not df_only_incomes.empty:
                    # Clasificar usando la clasificación global de los detalles
                    df_only_incomes['Concepto'] = df_only_incomes.apply(lambda r: create_label_global(r, det_col_name, desc_col_name, lang_code), axis=1)
                    
                    # Agrupar en exactamente 3 grupos: "Gabriel", "Sierra", y "Otros ingresos" / "Other income"
                    def donut_rollup(concept):
                        if concept in ["Gabriel", "Sierra"]:
                            return concept
                        return "Otros ingresos" if lang_code == "es" else "Other income"
                        
                    df_only_incomes['Grupo_Donut'] = df_only_incomes['Concepto'].apply(donut_rollup)
                    
                    # Agrupar y sumar
                    incomes_grouped = df_only_incomes.groupby('Grupo_Donut')['en $_numeric'].sum().reset_index()
                    incomes_grouped = incomes_grouped.sort_values(by='en $_numeric', ascending=False)
                    group_col_name = 'Grupo Principal' if lang_code == "es" else 'Main Group'
                    incomes_grouped.columns = [group_col_name, 'Monto USD']
                    
                    # Crear gráfico de donut con Altair
                    donut_chart = alt.Chart(incomes_grouped).mark_arc(innerRadius=60).encode(
                        theta=alt.Theta(field="Monto USD", type="quantitative"),
                        color=alt.Color(field=group_col_name, type="nominal", legend=alt.Legend(title=TRANSLATIONS[lang_code]['viz_income_summary_donut_legend'])),
                        tooltip=[group_col_name, alt.Tooltip('Monto USD:Q', format=',.2f')]
                    ).properties(height=450)
                    st.altair_chart(donut_chart, use_container_width=True)
                else:
                    st.info(TRANSLATIONS[lang_code]['viz_income_summary_no_records'])
            else:
                st.info(TRANSLATIONS[lang_code]['viz_desc_missing'])
    
        with tab4:
            st.write(TRANSLATIONS[lang_code]['viz_expense_detail_title'])
            desc_col_name = 'Descripción' if 'Descripción' in df_filtered.columns else ('Descripcion' if 'Descripcion' in df_filtered.columns else None)
            det_col_name = 'Detalle' if 'Detalle' in df_filtered.columns else None
            
            if desc_col_name:
                df_chart_neg = df_filtered.copy()
                
                # Filtrar donde en $neg no es nulo o vacío
                df_chart_neg['en $neg_numeric'] = pd.to_numeric(df_chart_neg['en $neg'], errors='coerce')
                
                # Quedarse con aquellas que tienen valor numérico (negativo)
                df_chart_neg = df_chart_neg[df_chart_neg['en $neg_numeric'].notna()]
                
                if not df_chart_neg.empty:
                    # Aplicar clasificación global de egresos
                    df_chart_neg['Concepto_Neg'] = df_chart_neg.apply(lambda r: classify_expense_global(r, det_col_name, desc_col_name, lang_code), axis=1)
                    
                    # Agrupar, sumar monto absoluto (para barras a la derecha)
                    df_chart_neg['en $neg_abs'] = df_chart_neg['en $neg_numeric'].abs()
                    
                    desc_neg_sum = df_chart_neg.groupby('Concepto_Neg').agg(
                        Monto_Total=('en $neg_abs', 'sum'),
                        Operaciones=('en $neg_numeric', 'count')
                    ).reset_index()
                    
                    # Ordenar por monto absoluto descendente
                    desc_neg_sum = desc_neg_sum.sort_values(by='Monto_Total', ascending=False).head(15)
                    
                    # Definir selección de puntos en Altair para egresos
                    select_point_neg = alt.selection_point(fields=['Concepto_Neg'], name='select_concept_neg')
                    
                    # Gráfico de barras horizontales con Altair (Rojo para egresos)
                    horizontal_bar_neg = alt.Chart(desc_neg_sum).mark_bar().encode(
                        x=alt.X('Monto_Total:Q', title=TRANSLATIONS[lang_code]['viz_expense_detail_x']),
                        y=alt.Y('Concepto_Neg:N', sort='-x', title=TRANSLATIONS[lang_code]['viz_expense_detail_y']),
                        color=alt.value('#dc2626'),  # Rojo para egresos
                        tooltip=[
                            alt.Tooltip('Concepto_Neg:N', title=TRANSLATIONS[lang_code]['viz_expense_detail_tooltip_concept']), 
                            alt.Tooltip('Monto_Total:Q', title=TRANSLATIONS[lang_code]['viz_expense_detail_tooltip_amount'], format=',.2f'),
                            alt.Tooltip('Operaciones:Q', title=TRANSLATIONS[lang_code]['viz_expense_detail_tooltip_ops'])
                        ]
                    ).add_params(
                        select_point_neg
                    ).properties(height=400)
                    
                    event_data_neg = st.altair_chart(horizontal_bar_neg, use_container_width=True, on_select="rerun")
                    
                    # Manejar la selección para el Dialog emergente de egresos
                    if event_data_neg and "selection" in event_data_neg:
                        selection_neg = event_data_neg["selection"].get("select_concept_neg", [])
                        selected_concept_neg = None
                        if selection_neg and isinstance(selection_neg, list) and len(selection_neg) > 0:
                            selected_concept_neg = selection_neg[0].get("Concepto_Neg") if isinstance(selection_neg[0], dict) else selection_neg[0]
                        elif selection_neg and isinstance(selection_neg, dict):
                            concepts_neg = selection_neg.get("Concepto_Neg", [])
                            selected_concept_neg = concepts_neg[0] if concepts_neg else None
                            
                        if selected_concept_neg:
                            if st.session_state.active_dialog_concept_neg != selected_concept_neg:
                                st.session_state.active_dialog_concept_neg = selected_concept_neg
                                # Filtrar operaciones correspondientes a este concepto
                                df_concept_ops_neg = df_chart_neg[df_chart_neg['Concepto_Neg'] == selected_concept_neg]
                                if not df_concept_ops_neg.empty:
                                    show_details_dialog_neg(selected_concept_neg, df_concept_ops_neg)
                        else:
                            st.session_state.active_dialog_concept_neg = None
                else:
                    st.info(TRANSLATIONS[lang_code]['viz_expense_detail_no_records'])
            else:
                st.info(TRANSLATIONS[lang_code]['viz_desc_missing'])
        
        with tab5:
            st.write(TRANSLATIONS[lang_code]['viz_expense_summary_title'])
            desc_col_name = 'Descripción' if 'Descripción' in df_filtered.columns else ('Descripcion' if 'Descripcion' in df_filtered.columns else None)
            det_col_name = 'Detalle' if 'Detalle' in df_filtered.columns else None
            
            if desc_col_name:
                df_expenses = df_filtered.copy()
                df_expenses['en $neg_numeric'] = pd.to_numeric(df_expenses['en $neg'], errors='coerce')
                
                # Filtrar solo egresos (donde en $neg no es nulo o vacío)
                df_only_expenses = df_expenses[df_expenses['en $neg_numeric'].notna()].copy()
                
                if not df_only_expenses.empty:
                    # Clasificar usando la clasificación global de egresos
                    df_only_expenses['Concepto_Neg'] = df_only_expenses.apply(lambda r: classify_expense_global(r, det_col_name, desc_col_name, lang_code), axis=1)
                    
                    df_only_expenses['Grupo_Donut_Neg'] = df_only_expenses['Concepto_Neg'].apply(lambda x: donut_rollup_neg(x, lang_code))
                    
                    # Obtener valor absoluto del monto egreso para el gráfico de donut
                    df_only_expenses['en $neg_abs'] = df_only_expenses['en $neg_numeric'].abs()
                    
                    # Agrupar y sumar
                    expenses_grouped = df_only_expenses.groupby('Grupo_Donut_Neg')['en $neg_abs'].sum().reset_index()
                    expenses_grouped = expenses_grouped.sort_values(by='en $neg_abs', ascending=False)
                    group_col_name = 'Grupo Principal' if lang_code == "es" else 'Main Group'
                    expenses_grouped.columns = [group_col_name, 'Monto USD']
                    
                    # Crear gráfico de donut con Altair
                    donut_chart_neg = alt.Chart(expenses_grouped).mark_arc(innerRadius=60).encode(
                        theta=alt.Theta(field="Monto USD", type="quantitative"),
                        color=alt.Color(field=group_col_name, type="nominal", legend=alt.Legend(title=TRANSLATIONS[lang_code]['viz_expense_summary_donut_legend'])),
                        tooltip=[group_col_name, alt.Tooltip('Monto USD:Q', format=',.2f')]
                    ).properties(height=450)
                    st.altair_chart(donut_chart_neg, use_container_width=True)
                else:
                    st.info(TRANSLATIONS[lang_code]['viz_expense_detail_no_records'])
            else:
                st.info(TRANSLATIONS[lang_code]['viz_desc_missing'])
        
# -------------------------------------------------------------------
# SECCIÓN 3: CONSOLIDADO TOTAL DE EGRESOS
# -------------------------------------------------------------------
with st.expander(TRANSLATIONS[lang_code]['sec3_title'], expanded=True):
    desc_col_name = 'Descripción' if 'Descripción' in df_filtered.columns else ('Descripcion' if 'Descripcion' in df_filtered.columns else None)
    det_col_name = 'Detalle' if 'Detalle' in df_filtered.columns else None
    
    # 1. Obtener egresos directos (Zelle)
    df_zelle_grouped = df_zelle.copy()
    df_zelle_grouped['Concepto'] = df_zelle_grouped['Descripción'].apply(lambda x: map_zelle_desc(x, lang_code))
    df_zelle_sum = df_zelle_grouped.groupby('Concepto')['Monto USD'].sum().reset_index()
    df_zelle_sum.columns = ['Concepto', 'Monto USD']
    
    # 2. Obtener egresos vía cuenta nacional (Banco Provincial)
    df_expenses = df_filtered.copy()
    df_expenses['en $neg_numeric'] = pd.to_numeric(df_expenses['en $neg'], errors='coerce')
    df_only_expenses = df_expenses[df_expenses['en $neg_numeric'].notna()].copy()
    
    if not df_only_expenses.empty and desc_col_name:
        df_only_expenses['Concepto_Neg'] = df_only_expenses.apply(lambda r: classify_expense_global(r, det_col_name, desc_col_name, lang_code), axis=1)
        df_only_expenses['Concepto'] = df_only_expenses['Concepto_Neg'].apply(lambda x: donut_rollup_neg(x, lang_code))
        df_only_expenses['en $neg_abs'] = df_only_expenses['en $neg_numeric'].abs()
        df_prov_sum = df_only_expenses.groupby('Concepto')['en $neg_abs'].sum().reset_index()
        df_prov_sum.columns = ['Concepto', 'Monto USD']
    else:
        df_prov_sum = pd.DataFrame(columns=['Concepto', 'Monto USD'])
        
    # 3. Combinar ambos
    df_combined = pd.concat([df_zelle_sum, df_prov_sum], ignore_index=True)
    df_consolidated = df_combined.groupby('Concepto')['Monto USD'].sum().reset_index()
    df_consolidated = df_consolidated.sort_values(by='Monto USD', ascending=False)
    
    # Crear gráfico de torta con Altair
    base = alt.Chart(df_consolidated).encode(
        theta=alt.Theta(field="Monto USD", type="quantitative"),
        color=alt.Color(field='Concepto', type="nominal", legend=alt.Legend(title=TRANSLATIONS[lang_code]['sec3_legend_title'])),
        tooltip=['Concepto', alt.Tooltip('Monto USD:Q', format=',.2f')]
    )
    
    pie_chart = base.mark_arc(outerRadius=120).properties(height=400)
    
    # Mostrar el gráfico de torta a lo ancho
    st.altair_chart(pie_chart, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.write(TRANSLATIONS[lang_code]['sec3_table_title'])
    
    # Preparar DataFrame para la tabla
    df_table = df_consolidated.copy()
    col_egreso = TRANSLATIONS[lang_code]['sec3_col_egreso']
    col_monto = TRANSLATIONS[lang_code]['sec3_col_monto']
    df_table.columns = [col_egreso, col_monto]
    
    # Calcular el total
    total_egresos = df_table[col_monto].sum()
    
    # Crear fila de total
    df_total = pd.DataFrame([{col_egreso: TRANSLATIONS[lang_code]['sec3_total_label'], col_monto: total_egresos}])
    df_table_with_total = pd.concat([df_table, df_total], ignore_index=True)
    
    # Función de estilo para resaltar la fila de Total con alto contraste
    def highlight_total(row):
        if row[col_egreso] == TRANSLATIONS[lang_code]['sec3_total_label']:
            # Fondo azul oscuro con texto blanco en negrita para alto contraste y legibilidad
            return ['background-color: #1e3c72; color: #ffffff; font-weight: bold; border-top: 2px solid #0f172a; font-size: 16px;'] * len(row)
        return [''] * len(row)
    
    # Formateador robusto para asegurar siempre 2 decimales en todos los montos (incluyendo numpy float64)
    def format_currency(val):
        try:
            num = float(val)
            return f"${num:,.2f}"
        except (ValueError, TypeError):
            return str(val)
    
    # Aplicar tamaño de fuente aumentado y estilos
    styler_table = df_table_with_total.style.set_properties(**{
        'font-size': '16px'
    }).apply(highlight_total, axis=1).format({
        col_monto: format_currency
    })
    
    st.dataframe(styler_table, use_container_width=True, hide_index=True)


# Pie de página elegante
st.markdown("---")
st.markdown(
    f"""
    <div style="text-align: center; color: #94a3b8; font-size: 0.85rem; margin-top: 20px;">
        {TRANSLATIONS[lang_code]['footer_text']}
    </div>
    """,
    unsafe_allow_html=True
)
