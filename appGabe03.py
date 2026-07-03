import os
import pandas as pd
import streamlit as st
import datetime
import altair as alt

TRANSLATIONS = {
    "es": {
        "page_title": "Informe Financiero: GABE - Barnabas Aid",
        "sidebar_nav_title": "Navegación / Navigation",
        "page_gabe2026": "🏠 Proyecto GABE 2026 (Subvención GFI)",
        "page_dashboard": "📊 Dashboard Financiero (Barnabas Aid)",
        "landing_header": "Grant Agropecuario 2026-2027",
        "landing_title": "Fortalecimiento Productivo y Misionero GABE",
        "landing_sub": "Propuesta unificada para la soberanía alimentaria, formación técnica y fortalecimiento comunitario en Mérida, Táchira y Apure/Guárico",
        "unified_vision_title": "🌐 Visión del proyecto de Fortalecimiento Productivo y Misionero GABE",
        "unified_vision_desc": "El proyecto <strong>GABE 2026</strong> integra de manera estratégica tres grandes pilares para lograr impacto social y autosostenibilidad: <br><br>1. <strong>El Origen - Picalqui (Ecuador)</strong>: Capacitación técnica inicial. Tres de nuestros técnicos se capacitaron en agricultura orgánica y agroecológica en Ecuador (agosto de 2023), y hoy están listos para la fase de réplica.<br>2. <strong>El Motor Operativo - Voluntariado Cubano</strong>: Una pareja misionera cubana reside a tiempo completo en la granja para gestionar la producción, el mantenimiento y coordinar las actividades comunitarias.<br>3. <strong>La Red de Distribución - Iglesias de San Cristóbal</strong>: Circuito colaborativo de 5 congregaciones que apoya con jornadas de trabajo y canaliza la distribución de alimentos y la reinversión de beneficios.",
        "picalqui_title": "🎓 Galería del Pasado y Presente: Capacitación en Picalqui, Ecuador",
        "picalqui_desc": "En agosto de 2023, <strong>Global Food Initiative (GFI)</strong> financió la formación de 3 líderes técnicos en el Centro Picalqui, Ecuador. Esta inversión previa ya dio frutos y capacitó a nuestro equipo en abonos fermentados y cultivos de ladera, estableciendo la base para la actual fase de réplica.",
        "tech1_name": "Ewgleis Susanne Moreno Padilla",
        "tech1_bio": "Técnica agroecológica capacitada en Picalqui (2023). Encargada de dictar talleres y capacitar en el Estado Guárico y en la Granja GABE.",
        "tech2_name": "Victor Gerardo Fuentes",
        "tech2_bio": "Técnico especialista en bio-preparados y control de plagas. Responsable del soporte técnico en el Estado Apure.",
        "tech3_name": "Gilber Borjas",
        "tech3_bio": "Técnico especialista en cultivos andinos y riego localizado. Responsable de la réplica técnica directa en el Estado Mérida.",
        "sustainability_title": "🐷 Modelo de Sostenibilidad: Limones Persa y Cerdos",
        "sustainability_desc": "La autosostenibilidad económica del proyecto está planificada con seriedad y se basa en dos rubros productivos principales: <br><br>• <strong>Siembra de Limón Persa</strong>: 300 plántulas de limón persa que se sumarían a las 100 que ya hemos plantado y que tienen 3 meses de crecimiento. Estas plantas se adaptan óptimamente al terreno y sus frutos tienen un valor comercial competitivo.<br>• <strong>Cría de Cerdos</strong>: Producción por lotes de 15 cerdos en chiqueros adecuados, generando ingresos rápidos para reinversión y abono orgánico.",
        "nuestra_granja_title": "🚜 Nuestra Granja: Estado Actual",
        "nuestra_granja_desc": "Vista actual de siembras, cultivos, infraestructura y producción avícola de la Granja",
        "flow_title": "🗺️ Red de Cooperación y Flujo Comunitario",
        "flow_desc": "Las iglesias de San Cristóbal y la Granja GABE cooperan activamente a pesar de las 3 horas de distancia de viaje. Los equipos de las iglesias viajan para jornadas de trabajo y apoyo en cosecha. <br><br>Las utilidades de las ventas se dividen equitativamente entre las 5 iglesias de San Cristóbal y la reinversión en la propia granja, logrando soberanía alimentaria autónoma.",
        "leaders_title": "👥 Perfil de Líderes y Voluntarios",
        "leaders_desc": "GFI apoya a personas comprometidas que ponen rostro y corazón al proyecto en las comunidades locales.",
        "roger_title": "Roger Moreno Padilla (Presidente y Administrador GABE)",
        "roger_bio": "Presidente de GABE y Administrador General. Coordina la logística, compras de insumos y alianzas institucionales. Cuenta con amplia experiencia en la dirección de proyectos agropecuarios y de desarrollo social.",
        "pastors_title": "Equipo de Pastores (Mérida y San Cristóbal)",
        "pastors_bio": "El equipo de pastores colidera la planificación laboral y social, asegurando que los alimentos lleguen a las familias más vulnerables y se mantenga la coordinación interiglesias.",
        "classroom_title": "🏫 El Aula de Clases Comunitaria",
        "classroom_desc": "En la casa principal de la granja se acondicionará un aula. La esposa del pastor cubano (quien domina tres idiomas: español, inglés y francés) dictará clases de tareas dirigidas, inglés y francés a muy bajo costo para los niños de la comunidad rural, haciendo el proyecto tangible y conmovedor.",
        "transparency_title": "🤝 Transparencia y Rendición de Cuentas en Venezuela",
        "transparency_blog": "<strong>Historias de Aprendizaje: Administrando en Hiperinflación</strong><br>Operar en una economía compleja nos ha enseñado a ser flexibles y honestos. A lo largo de los últimos 8 años de confianza mutua con GFI, hemos aprendido a mitigar los riesgos del contexto país mediante conversión bajo demanda, compras directas y préstamos puente con ASIGLEH para mantener el proyecto en marcha sin paralizaciones.",
        "impact_reports_title": "📄 Informes de Impacto Previos (Últimos 8 Años)",
        "impact_reports_desc": "Dedica un espacio para descargar o leer los resúmenes de los proyectos financiados por GFI, validando la trayectoria institucional y la confianza mutua construida.",
        "btn_download_report": "Descargar Historial de Proyectos GFI (PDF)",
        "alliance_title": "🤝 Alianzas y Cooperación Institucional",
        "alliance_desc": "Agradecemos a las instituciones y redes que apoyan y acompañan el desarrollo de la Granja GABE.",
        "btn_alliance": "Conoce más sobre nuestros aliados institucionales como la Iglesia de los Hermanos",
        "contact_title": "📞 Datos de Contacto",
        "contact_desc": "Para verificar la autenticidad de la organización y evitar dudas de seguridad, puedes comunicarte por los canales oficiales declarados en la propuesta:<br><br>• 📧 <strong>cobvenezuela@gmail.com</strong> (Coordinación)<br>• 📧 <strong>rogerpadilla592@gmail.com</strong> (Administración)<br>• 💬 <strong>Contacto WhatsApp Roger Padilla</strong>: +58 412 384 1926",

        "header_title": "Informe Proyecto Granja Alas de Bendición y Esperanza (GABE)",
        "intro_title": "📝 1. Reporte Operativo: Ejecución de Fondos y Sostenibilidad de la Granja GABE",
        "intro_body": """
        <div class="intro-container">
        <p>El presente reporte detalla la administración transparente y el uso estratégico de los recursos recibidos a través de una donación destinada al desarrollo operativo de la Granja Alas de Bendición y Esperanza (GABE).</p>
        <p>Como se ilustra de manera detallada en la imagen adjunta, el proyecto dispuso de un fondo neto de USD 10,000, el cual se ejecuta minuciosamente para garantizar la continuidad, expansión y autosostenibilidad de nuestras unidades socio-productivas. Estos recursos cubren de forma directa los siguientes frentes esenciales para el arranque y consolidación del proyecto:</p>
        <ul style="margin-bottom: 20px;">
            <li><strong>Producción Avícola Activa:</strong> Costos asociados a la adquisición, alimentación y cría de pollos de engorde y gallinas ponedoras para reactivación comercial y sustento comunitario.</li>
            <li><strong>Infraestructura:</strong> Adecuación, reparaciones críticas y preparación de los espacios físicos destinados a los galpones avícolas.</li>
            <li><strong>Equipamiento y Habitabilidad:</strong> Compra de herramientas fundamentales para la ejecución de mejoras físicas en las áreas de producción y optimización de las instalaciones residenciales para el personal.</li>
            <li><strong>Expansión Agroecológica:</strong> Apoyo operativo para la diversificación de cultivos permanentes y de ciclo corto dentro de la granja.</li>
        </ul>
        <p>El desglose pormenorizado, los comprobantes de uso de recursos y el impacto en tiempo real de estos USD 10,000 netos ejecutados son los que se muestran de forma minuciosa en las secciones siguientes de este informe.</p>
        </div>
        """,
        "intro_img_caption": "cheques de donaciones para el soporte operativo de GABE",
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
        "zelle_chart_header": "#### Compras Directas(pago via Zelle)",
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
        "relacion_title": "📊 Relación de Ingresos y Gastos",
        "sec3_table_title": "##### Resumen de Egresos Consolidados",
        "sec3_col_egreso": "Egreso",
        "sec3_col_monto": "Monto ($)",
        "sec3_total_label": "Total Consolidado",
        "sec3_legend_title": "Conceptos de Egreso",
        "footer_text": "Desarrollado para el <strong>Dashboard Administrativo GABE</strong> | ASIGLEH - Dirección de Finanzas. Todos los derechos reservados.",
        "avicola_header": "### 🤝 Producción Avícola 👥👥",
        "inversion_aves_title": "Inversión en Aves: Se adquirieron 380 gallinas ponedoras y 100 pollos de engorde.",
        "inversion_aves_content": """
**Resumen de Crianza y Manejo:**
* **Pollitos BB**: Sistemas de calefacción y comederos especiales para maximizar la supervivencia.
* **Gallinas Ponedoras**: 380 aves alojadas en galpones protegidos y ventilados para producción de huevos.
* **Pollos de Engorde**: 100 pollos alimentados con tolva y bebederos colgantes en ciclos de 2 meses.
""",
        "pollos_engorde_title": "Pollos de Engorde: El ciclo se cumplió exitosamente a los dos meses. No obstante, se presentó un inconveniente técnico con el nuevo refrigerador adquirido, lo que resultó en la pérdida de unas pocas aves beneficiadas.",
        "pollos_engorde_content": """
**Detalles sobre el ciclo de engorde, el percance técnico y el impacto social:**
* **Crianza y Procesamiento**: Producción en campo y beneficio higiénico de las aves (limpieza y empaque individual) con control de peso en balanza digital para asegurar la calidad del producto entregado.
* **Incidente de Cadena de Frío**: Ante la avería mecánica del congelador, se actuó de emergencia adaptando ventilación asistida temporal y movilizando el lote para preservar la cadena de frío de las aves beneficiadas.
* **Respuesta Social y Comercialización**: Como medida de mitigación y en línea con el compromiso misionero de ayuda social, una parte de las aves fue donada de inmediato a la comunidad y comedores misioneros. El volumen restante se comercializó exitosamente en el mercado regional para sustentar el flujo de caja del proyecto.
""",
        "desafios_mercado_title": "Desafíos de Mercado: La producción de huevos es constante, pero enfrentamos un entorno económico adverso. El precio del cartón de huevos bajó de una expectativa de $5.50 a un rango de $3.50 - $5.00, mientras que los costos del alimento balanceado siguen en aumento, reduciendo el margen de ganancia operativa.",
        "desafios_mercado_content": "Análisis de costos de alimento y fluctuación de precios de venta en el mercado regional.",
        "diversificacion_header": "### 🤝 Diversificación Agroecológica 🌱🌿🍊",
        "siembra_cafe_title": "Adquisición y siembra de 100 matas de café.",
        "siembra_cafe_content": """
**Detalles sobre la adquisición y siembra de café:**
* **Logística y Selección**: Traslado e introducción de 100 plántulas de café seleccionadas para resistir las condiciones climáticas de la zona montañosa.
* **Siembra e Infraestructura**: Colocación en campo usando fertilización y protección de suelo para garantizar el desarrollo del cultivo.
""",
        "siembra_limon_title": "Adquisición y siembra de 100 plantas de limón persa.",
        "siembra_limon_content": """
**Detalles sobre el cultivo de limón persa:**
* **Siembra y Riego**: Adecuación del terreno para las 100 plantas de limón persa y aplicación de sistemas de riego localizado.
* **Establecimiento**: Distribución de las plántulas para aprovechar al máximo la luz solar y favorecer un desarrollo vegetativo robusto.
""",
        "siembra_cambur_title": "Adquisición y siembra de 250 plantas de cambur y otros cultivos (Cebollín, Maíz, Yuca, Auyama,...).",
        "siembra_cambur_content": """
**Detalles sobre la siembra de cambur y otros rubros asociados:**
* **Establecimiento de Cambur**: Plantación de 250 matas de cambur distribuidas en pendientes para aprovechamiento del terreno.
* **Asociación de Cultivos**: Cultivo intercalado de ciclos cortos (cebollín, maíz, yuca, auyama) que favorecen el uso eficiente del suelo y proporcionan seguridad alimentaria a corto plazo.
""",
        "testimonios_header": "### 💬 Testimonios y Agradecimientos",
        "testimonios_title": "💬 Testimonios y Agradecimientos",
        "testimonios_content": "Espacio para testimonios del equipo de trabajo de la Granja y agradecimientos a Barnabas Aid por el apoyo brindado.",
        "informe_gestion_title": "### INFORME DE GESTIÓN Y RESULTADOS:",
        "dirigido_a_title": "Dirigido a:",
        "antecedentes_header": "### 📜 Antecedentes de GABE (Granja Alas de Bendición)",
        "antecedentes_title": "✈️ ANTECEDENTES GABE (2024-2025)",
        "objetivos_title": "✅ OBJETIVOS DEL PROYECTO (2025-2026)",
        "resultados_header": "### 🎯 Gestión y capacidad Institucional GABE",
        "resultados_title": "🎯 Transparencia en Acción: Resultados Alcanzados y Capacidad Institucional (Periodo 2025-2026)",
        "activos_title": "<h4 style='color: #4361ee;'>🔭 Activos</h4>",
        "moto_desc": "Adquisición de una Cuatrimoto, necesaria para la movilidad en la finca y hacia Tovar y pueblos aledaños para la búsqueda de insumos y venta de productos (huevos, pollos, etc.)",
        "moto_title": "Cuatrimoto",
        "freezer_title": "Adquisición de un freezer/congelador para el mantenimiento de las aves beneficiadas",
        "cocina_title": "Adquisición de tope de cocina",
        "herramientas_title": "Adquisición de herramientas de trabajo",
        "materiales_title": "Adquisición de materiales de construcción y operativos",
        "infraestructura_header": "### 🛠️ Infraestructura y Adecuación Física",
        "sistema_hidrico_title": "Sistema Hídrico: Se repararon, asearon y sellaron los tanques de almacenamiento de agua y se renovó el sistema de tuberías principales para garantizar el acceso al agua en galpones y viviendas.",
        "sistema_electrico_title": "Sistema Eléctrico: Se realizaron mejoras integrales en el cableado y puntos eléctricos de las casas y galpones, optimizando la seguridad y eficiencia.",
        "techos_title": "Adecuación de parte del techo de una de las instalaciones",
        "espacios_title": "Adecuación física de espacios de trabajo y habitación",
        "gestion_financiera_header": "### 💼 Gestión Financiera",
        "gestion_financiera_title": "💼 Gestión Financiera",
        "dirigido_junta": "Junta Directiva ASIGLEH",
        "dirigido_convencion": "Convención Nacional ASIGLEH",
        "antecedentes_p1": "El proyecto de la Granja Alas de Bendición y Esperanza (GABE) nació en mayo de 2024 con la visión de crear una unidad de producción agroecológica autosustentable de 7 hectáreas en Tovar, Mérida, bajo la cobertura de ASIGLEH. Este proyecto ya en marcha, tiene una visión estratégica de transformar capitales semilla en un motor autosustentable en un plazo de 5 años —del cual ya hemos transitado con mucho esfuerzo y un buen grado de éxito los primeros 2 años—, integrando la producción alimentaria con el desarrollo comunitario y la expansión misionera.",
        "antecedentes_pilares_caption": "Pilares del proyecto Granja 'Alas de Bendición' (GABE)",
        "antecedentes_fc1_caption": "Arquitectura del Flujo de Caja I: El Ciclo de Engorde",
        "antecedentes_fc2_caption": "Arquitectura del Flujo de Caja II: El Ciclo de Ponedoras",
        "antecedentes_body": "Tras concretarse la adquisición de la finca, el equipo asumió el desafío de reorientar esfuerzos iniciales hacia la reparación y estabilización crítica de una infraestructura residencial y de servicios que se encontraba en avanzado estado de deterioro. Superada esta etapa de habitabilidad, el periodo 2025-2026 marcó el inicio formal de las operaciones productivas mediante el establecimiento de una unidad avícola con gallinas ponedoras y pollos de engorde bajo un esquema de dos ciclos comerciales para generar liquidez diaria. A pesar de los obstáculos logísticos y operativos propios del entorno, esta experiencia fundacional consolidó los cimientos técnicos necesarios para diversificar la producción y asegurar el autoabastecimiento futuro de la granja.",
        "antecedentes_gestion": "También se han dado pasos en la diversificación agrícola de la finca.\n\nEn cuanto a infraestructura se ha avanzado en la adecuación de los diferentes espacios y estamos casi listos para la configuración de un sitio de entrenamiento en técnicas agroecológicas y orgánicas.",
        "objetivos_intro": "La subvención de Barnabas Aid se enfocó en tres ejes fundamentales:",
        "objetivos_body": "* **Adecuación de Infraestructura Vital**: Restaurar la capacidad operativa de la finca mediante la recuperación y estabilización de los sistemas de agua y electricidad para garantizar la continuidad operativa. Tambien se refiere a mejoras en infraestructuras como techos, ventanas, puertas, baños y cocina.\n* **Producción Avícola de Ciclo Corto y Largo**: Establecer una producción de pollos de engorde para liquidez inmediata y de gallinas ponedoras para sostenibilidad a largo plazo.\n* **Diversificación Agroecológica**: Expandir la capacidad de la finca mediante siembras permanentes (café y limón) y ciclos cortos (maíz, cambur, yuca...).\n* **Seguridad Alimentaria y Proyección Comunitaria**: Proveer proteína animal a precios accesibles o mediante donaciones a la comunidad local y proyectos misioneros de la Iglesia de los Hermanos.",
        "freezer_body": "**Detalles sobre la cadena de frío y conservación:**\n* **Equipamiento**: Adquisición de un congelador/freezer horizontal de gran capacidad para el almacenamiento seguro de las aves.\n* **Operación**: Conservación y mantenimiento de la cadena de frío para las aves beneficiadas (limpias y embolsadas individualmente), asegurando su frescura antes de la distribución y venta.",
        "herramientas_body": "**Equipos y herramientas adquiridos para el mantenimiento operativo de la granja:**\n* **Caja de herramientas de mano completa** (martillo, alicates, destornilladores, segueta, llaves de tubo, nivel, flexómetro, pelacables, etc.).\n* **Escalera de extensión de aluminio** para trabajos de altura en galpones y viviendas.\n* **Esmeril angular (amoladora) inalámbrico de 20V** para corte y pulido de materiales.\n* **Taladro inalámbrico de 20V** para trabajos de fijación e instalación en campo.\n* **Bebederos plásticos para aves** para la hidratación controlada en los galpones.",
        "materiales_body": "**Materiales, mobiliario y equipos operativos adquiridos para el desarrollo de la granja:**\n* **Mobiliario de oficina**: Mesas de trabajo plegables y sillas ergonómicas para labores administrativas.\n* **Materiales de construcción**: Láminas de zinc corrugadas para la reparación de techos de galpones y viviendas.\n* **Equipamiento de cocina y baño**: Grifería cuello de cisne para fregadero, lavamanos de cerámica y espejo organizador de pared.\n* **Tecnología y conectividad**: Router TP-Link Wi-Fi 6 Archer AX12 (instalación de internet en la granja).\n* **Electrodomésticos básicos**: Cafetera eléctrica de goteo.\n* **Materiales de control climático**: Malla de sombreo (polisombra) para regulación de luz y temperatura.",
        "sistema_hidrico_body": "**Detalles del mantenimiento y adecuación del sistema de distribución de agua:**\n* **Mantenimiento de tanques**: Limpieza profunda, desinfección, sellado de fisuras y colocación de cubiertas protectoras en los tanques de mampostería principales.\n* **Tuberías principales**: Tendido y ensamblaje de nuevas tuberías de alta resistencia para el transporte de agua hacia la zona residencial y de producción.\n* **Sistemas de control**: Instalación de llaves de paso, uniones mecánicas y sistemas de bypass en el terreno para la distribución por sectores.\n* **Conectividad a galpones**: Acometida directa de agua a los galpones avícolas para garantizar la hidratación constante y automatizada de las aves.",
        "sistema_electrico_body": "**Detalles del mantenimiento y adecuación del sistema eléctrico:**\n* **Renovación de cableado**: Reemplazo total del cableado deteriorado por conductores nuevos y de calibre adecuado para soportar la carga operativa.\n* **Tableros de distribución**: Organización e instalación de tableros de control con breakers de seguridad para proteger los equipos y las viviendas.\n* **Iluminación y fuerza**: Instalación de luminarias LED de alta eficiencia y nuevos puntos de tomacorrientes en galpones y áreas comunes.\n* **Sistemas de respaldo**: Adecuación de conexiones y canalizaciones preparadas para la integración de sistemas de energía alternativa/respaldo.",
        "techos_body": "**Detalles sobre las reparaciones y mejoras en la cubierta de las instalaciones:**\n* **Desmontaje y limpieza**: Remoción de las láminas antiguas y limpieza de la estructura de soporte.\n* **Refuerzo estructural**: Reparación de vigas y soportes de madera/metal comprometidos por humedad.\n* **Cubierta nueva**: Colocación de láminas nuevas de zinc corrugadas para evitar filtraciones y goteras.\n* **Sellado e impermeabilización**: Ajuste de uniones y sellado de tornillos para garantizar hermeticidad ante las lluvias.",
        "espacios_body": "**Detalles sobre la remodelación y adecuación de los ambientes habitacionales y de trabajo:**\n* **Espacios habitacionales**: Acondicionamiento de habitaciones para el personal residente de la granja (pintura, reparaciones y acabados).\n* **Cocina y baños**: Instalación de topes de cocina, griferías, lavamanos y espejos nuevos para garantizar condiciones dignas de habitabilidad.\n* **Áreas administrativas**: Organización y equipamiento de la oficina con el mobiliario ergonómico adquirido.\n* **Adecuación de galpones**: Reparaciones menores y preparación física de los espacios avícolas antes de la entrada de lotes de aves.",
        "resultados_intro_highlight": """
        <div class="intro-highlight-card">
            Para la Iglesia de los Hermanos Venezuela (ASIGLEH) y la Granja Alas de Bendición y Esperanza (GABE), la transparencia no es solo un valor ético, sino el pilar fundamental que sostiene nuestra misión comunitaria. En entornos económicos de alta complejidad e hiperinflación, la rendición de cuentas precisa y el manejo estratégico de los recursos son las herramientas que transforman los fondos de subvención en un impacto social tangible y duradero. Con el firme propósito de respaldar nuestra capacidad de gestión institucional ante nuestros aliados de la Global Food Initiative (GFI) y la comunidad global, presentamos de forma abierta el Resumen Ejecutivo de Logros del periodo 2025-2026. Este histórico de ejecución demuestra cómo el compromiso del equipo de la granja, la optimización financiera y la inversión transparente en activos e infraestructura han preparado el terreno para escalar con éxito hacia el nuevo Grant Agropecuario 2026-2027. A continuación, detallamos las metas alcanzadas y los cimientos operativos consolidados gracias a una administración responsable:
        </div>
        """,
        "resultados_summary": """
        <div class="summary-card">
            <strong>Resumen Ejecutivo de Logros (Periodo 2025-2026):</strong>
            <ul>
                <li><strong>🔭 Adquisición de Activos:</strong> Incorporación de transporte clave (cuatrimoto), equipamiento de cadena de frío (congelador), herramientas de trabajo y materiales operativos fundamentales para el desarrollo de la granja.</li>
                <li><strong>🛠️ Adecuación de Infraestructura:</strong> Estabilización crítica y mejoras profundas de habitabilidad (sistemas hídricos, cableado eléctrico y tableros de seguridad, techado e instalaciones residenciales).</li>
                <li><strong>🐓 Producción Avícola Activa:</strong> Crianza de 380 gallinas ponedoras y 100 pollos de engorde para sustento, reactivación comercial y donaciones comunitarias.</li>
                <li><strong>🌱 Diversificación Agroecológica:</strong> Establecimiento de cultivos permanentes (100 plántulas de café, 100 plantas de limón persa y 250 matas de cambur) intercalados con siembras de ciclo corto para seguridad alimentaria.</li>
                <li><strong>💼 Gestión Financiera Unificada:</strong> Ejecución de recursos de forma óptima a través de compras directas (Zelle) y conversiones controladas a moneda nacional en Banco Provincial para mitigar la hiperinflación.</li>
            </ul>
        </div>
        """,
        "cerca_header": "🚧 Cerca y Portón",
        "poda_header": "🌳 Poda del Gran Árbol",
        "directiva_header": "👥 Directiva de ASIGLEH en la Granja",
        "otras_adecuaciones_header": "🏠 Otras Adecuaciones",
        "videos_obra_header": "🎥 Videos de la Obra",
        "video_1_title": "Video I: Trabajos exteriores y mantenimiento en campo",
        "video_2_title": "Video II: Remodelación extrema de espacios internos",
        "video_2_desc": "Este video muestra las renovaciones realizadas en la casa principal de la granja. Se han reparado los sistemas eléctricos y de plomería, además de pintar paredes, ajustar ventanas y reacondicionar baños, habitaciones y cocina, logrando un aspecto funcional y elegante. En el exterior, se observan vehículos, cultivos de cambur, árboles frutales como aguacate y guanábana, además de un huerto con cebollín.",
    },
    "en": {
        "page_title": "Financial Report: GABE - Barnabas Aid",
        "sidebar_nav_title": "Navegación / Navigation",
        "page_gabe2026": "🏠 GABE 2026 Project (GFI Grant)",
        "page_dashboard": "📊 Financial Dashboard (Barnabas Aid)",
        "landing_header": "Agricultural Grant 2026-2027",
        "landing_title": "GABE Productive and Missionary Strengthening",
        "landing_sub": "Unified proposal for food sovereignty, technical training, and community strengthening in Mérida, Táchira, and Apure/Guárico",
        "unified_vision_title": "🌐 GABE Productive and Missionary Strengthening Project Vision",
        "unified_vision_desc": "The <strong>GABE 2026</strong> project strategically integrates three main pillars for social impact and self-sustainability: <br><br>1. <strong>The Origin - Picalqui (Ecuador)</strong>: Initial technical training. Three of our technicians trained in organic and agroecological agriculture in Ecuador (August 2023), and are now ready for the replication phase.<br>2. <strong>The Operational Engine - Cuban Volunteers</strong>: A Cuban missionary couple resides full-time at the farm to manage production, maintenance, and coordinate community activities.<br>3. <strong>The Distribution Network - San Cristóbal Churches</strong>: A collaborative circuit of 5 congregations that supports with workdays and channels food distribution and profit reinvestment.",
        "picalqui_title": "🎓 Past & Present Gallery: Picalqui Training, Ecuador",
        "picalqui_desc": "In August 2023, <strong>Global Food Initiative (GFI)</strong> funded the training of 3 technical leaders at the Picalqui Center, Ecuador. This previous investment has already borne fruit, training our team in fermented fertilizers and hillside farming, establishing the foundation for the current replication phase.",
        "tech1_name": "Ewgleis Susanne Moreno Padilla",
        "tech1_bio": "Agroecological technician trained in Picalqui (2023). In charge of teaching workshops and training in Guárico State and at the GABE Farm.",
        "tech2_name": "Victor Gerardo Fuentes",
        "tech2_bio": "Technician specializing in bio-preparations and natural pest control. Responsible for technical support in Apure State.",
        "tech3_name": "Gilber Borjas",
        "tech3_bio": "Technician specializing in Andean crops and localized irrigation. Responsible for direct technical replication in Mérida State.",
        "sustainability_title": "🐷 Sustainability Model: Persian Lemons and Pigs",
        "sustainability_desc": "The project's economic self-sustainability is seriously planned and based on two main productive areas: <br><br>• <strong>Persian Lemon Planting</strong>: 300 Persian lemon seedlings that would add to the 100 we have already planted and which have 3 months of growth. These plants adapt optimally to the terrain and their fruits have a competitive commercial value.<br>• <strong>Pig Rearing</strong>: Batch production of 15 pigs in suitable pigpens, generating quick income for reinvestment and organic fertilizer.",
        "nuestra_granja_title": "🚜 Our Farm: Current State",
        "nuestra_granja_desc": "Current view of sowing, crops, infrastructure, and poultry production of the Farm",
        "flow_title": "🗺️ Cooperation Network and Community Flow",
        "flow_desc": "The San Cristóbal churches and GABE Farm actively cooperate despite the 3-hour travel distance. Church teams travel for workdays and harvest support. <br><br>Profits from sales are split equally among the 5 San Cristóbal churches and reinvestment in the farm itself, achieving autonomous food sovereignty.",
        "leaders_title": "👥 Leaders and Volunteers Profiles",
        "leaders_desc": "GFI finances committed people who put a face and a heart to the project in their local communities.",
        "roger_title": "Roger Moreno Padilla (President and GABE Administrator)",
        "roger_bio": "GABE President and General Administrator. Coordinates logistics, supply purchases, and institutional alliances. He has extensive experience in directing agricultural and social development projects.",
        "pastors_title": "Pastors Team (Mérida and San Cristóbal)",
        "pastors_bio": "The pastors team co-leads work and social planning, ensuring food reaches the most vulnerable families and inter-church coordination is maintained.",
        "classroom_title": "🏫 The Community Classroom",
        "classroom_desc": "A classroom will be set up in the main house of the farm. The Cuban pastor's wife (who speaks Spanish, English, and French) will teach directed homework and languages at a very low cost to rural children, making the project tangible and touching.",
        "transparency_title": "🤝 Transparency and Accountability in Venezuela",
        "transparency_blog": "<strong>Learning Stories: Managing in Hyperinflation</strong><br>Operating in a complex economy has taught us to be flexible and honest. Throughout the last 8 years of mutual trust with GFI, we have learned to mitigate country context risks through on-demand conversion, direct purchases, and bridge loans with ASIGLEH to keep the project running without halts.",
        "impact_reports_title": "📄 Previous Impact Reports (Past 8 Years)",
        "impact_reports_desc": "A dedicated space to download or read summaries of GFI-funded projects, validating our institutional history and mutual trust.",
        "btn_download_report": "Download GFI Project History (PDF)",
        "alliance_title": "🤝 Partnerships and Institutional Cooperation",
        "alliance_desc": "We thank the institutions and networks that support and accompany the GABE Farm development.",
        "btn_alliance": "Learn more about our institutional allies such as the Church of the Brethren",
        "contact_title": "📞 Contact Data",
        "contact_desc": "To verify the organization's authenticity and avoid security concerns, you can communicate through the official channels declared in the proposal:<br><br>• 📧 <strong>cobvenezuela@gmail.com</strong> (Coordination)<br>• 📧 <strong>rogerpadilla592@gmail.com</strong> (Administration)<br>• 💬 <strong>WhatsApp Contact Roger Padilla</strong>: +58 412 384 1926",
        "header_title": "Project Report: Alas de Bendición y Esperanza Farm (GABE)",
        "intro_title": "📝 1. Operational Report: Fund Execution and Sustainability of the GABE Farm",
        "intro_body": """
        <div class="intro-container">
        <p>This report details the transparent administration and strategic use of resources received through a donation intended for the operational development of the Alas de Bendición y Esperanza Farm (GABE).</p>
        <p>As illustrated in detail in the attached image, the project had a net fund of USD 10,000, which is executed meticulously to guarantee the continuity, expansion, and self-sustainability of our socio-productive units. These resources directly cover the following essential fronts for the start and consolidation of the project:</p>
        <ul style="margin-bottom: 20px;">
            <li><strong>Active Poultry Production:</strong> Costs associated with the acquisition, feeding, and rearing of broiler chickens and laying hens for commercial reactivation and community sustenance.</li>
            <li><strong>Infrastructure:</strong> Adaptation, critical repairs, and preparation of physical spaces intended for poultry coops.</li>
            <li><strong>Equipment and Habitability:</strong> Purchase of fundamental tools for the execution of physical improvements in production areas and optimization of residential facilities for staff.</li>
            <li><strong>Agroecological Expansion:</strong> Operational support for the diversification of permanent and short-cycle crops within the farm.</li>
        </ul>
        <p>The detailed breakdown, proof of resource use, and real-time impact of these net USD 10,000 executed are shown in detail in the following sections of this report.</p>
        </div>
        """,
        "intro_img_caption": "donation checks for GABE operational support",
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
        "viz_flow_tooltip_ops": "No. of Transactions",
        "viz_flow_missing_info": "Temporal information is required to plot trend.",
        "viz_income_detail_title": "#### Income Distribution by Detail ($ USD)",
        "viz_income_detail_x": "Income Amount ($ USD)",
        "viz_income_detail_y": "Detail (Grouped)",
        "viz_income_detail_tooltip_concept": "Concept",
        "viz_income_detail_tooltip_amount": "Amount ($ USD)",
        "viz_income_detail_tooltip_ops": "No. of Transactions",
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
        "viz_expense_detail_tooltip_ops": "No. of Transactions",
        "viz_expense_detail_dialog_title": "Expenses Details",
        "viz_expense_detail_dialog_header": "Expenses of **{concepto}**",
        "viz_expense_detail_dialog_total": "Total: **{len_df}** expense transactions.",
        "viz_expense_detail_dialog_caption": "Note: Click outside the popup or the 'X' at the top to close.",
        "viz_expense_detail_no_records": "No expense transactions (in $neg) registered in this selection.",
        "viz_expense_summary_title": "#### Expense Distribution ($ USD) Grouped by Main Group",
        "viz_expense_summary_donut_legend": "Groups",
        "sec3_title": "Section 3: Consolidated Total Expenses (direct + national account)",
        "relacion_title": "📊 Statement of Income and Expenses",
        "sec3_table_title": "##### Consolidated Expenses Summary",
        "sec3_col_egreso": "Expense",
        "sec3_col_monto": "Amount ($)",
        "sec3_total_label": "Total Consolidated",
        "sec3_legend_title": "Expense Concepts",
        "footer_text": "Developed for the <strong>GABE Administrative Dashboard</strong> | ASIGLEH - Finance Division. All rights reserved.",
        "avicola_header": "### 🤝 Poultry Production 👥👥",
        "inversion_aves_title": "Poultry Investment: 380 laying hens and 100 broiler chickens were acquired.",
        "inversion_aves_content": """
**Rearing and Management Summary:**
* **Chicks**: Specialized heating and feeders to maximize survival rate.
* **Laying Hens**: 380 hens housed in protected and ventilated coops for egg production.
* **Broilers**: 100 chickens reared using hoppers and hanging drinkers in 2-month cycles.
""",
        "pollos_engorde_title": "Broiler Chickens: The cycle was successfully completed at two months. However, a technical issue arose with the newly acquired refrigerator, resulting in the loss of a few processed birds.",
        "pollos_engorde_content": """
**Details on the broiler cycle, technical incident, and social impact:**
* **Rearing and Processing**: Free-range production and hygienic slaughtering of the birds (cleaning and individual packaging) with weight control using a digital scale to ensure delivery quality.
* **Cold Chain Incident**: Facing the freezer mechanical breakdown, emergency actions were taken by adapting temporary forced ventilation and shifting the flock to preserve the cold chain of the processed poultry.
* **Social Response and Commercialization**: As a mitigation measure and in line with our missionary commitment to social aid, a portion of the poultry was immediately donated to the local community and soup kitchens. The remaining volume was successfully marketed in the regional market to support the project's cash flow.
""",
        "desafios_mercado_title": "Market Challenges: Egg production is constant, but we face an adverse economic environment. The price of a carton of eggs fell from an expectation of $5.50 to a range of $3.50 - $5.00, while the costs of balanced feed continue to rise, reducing the operating profit margin.",
        "desafios_mercado_content": "Analysis of feed costs and sales price fluctuation in the regional market.",
        "diversificacion_header": "### 🤝 Agroecological Diversification 🌱🌿🍊",
        "siembra_cafe_title": "Acquisition and planting of 100 coffee plants.",
        "siembra_cafe_content": """
**Details on coffee acquisition and planting:**
* **Logistics and Selection**: Transport and introduction of 100 coffee seedlings selected to withstand local mountainous climate conditions.
* **Planting and Soil**: Field placement employing organic fertilization and ground cover protection to guarantee plant health.
""",
        "siembra_limon_title": "Acquisition and planting of 100 Persian lemon plants.",
        "siembra_limon_content": """
**Details on Persian lemon crop cultivation:**
* **Planting and Irrigation**: Land preparation for the 100 Persian lemon plants and implementation of localized watering systems.
* **Flourishing**: Distribution of seedlings to maximize sunlight exposure and support robust vegetative growth.
""",
        "siembra_cambur_title": "Acquisition and planting of 250 plantain plants and other crops (Chives, Corn, Cassava, Pumpkin,...).",
        "siembra_cambur_content": """
**Details on plantain planting and associated crops:**
* **Plantain Establishment**: Planting of 250 plantain crops distributed on slopes for optimal terrain usage.
* **Crop Association**: Intercropping of short cycle species (chives, corn, cassava, pumpkin) to promote efficient soil use and provide short-term food security.
""",
        "testimonios_header": "### 💬 Testimonials and Acknowledgements",
        "testimonios_title": "💬 Testimonials and Acknowledgements",
        "testimonios_content": "Space for testimonials from the Farm work team and acknowledgements to Barnabas Aid for the support provided.",
        "informe_gestion_title": "### MANAGEMENT & RESULTS REPORT:",
        "dirigido_a_title": "Addressed to:",
        "antecedentes_header": "### 📜 Project Background and Objectives",
        "antecedentes_title": "✈️ PROJECT BACKGROUND (2024 - 2025)",
        "objetivos_title": "✅ PROJECT OBJECTIVES (2025-2026)",
        "resultados_header": "### 🎯 GABE Management and Institutional Capacity",
        "resultados_title": "🎯 Transparency in Action: Results Achieved and Institutional Capacity (2025-2026 Period)",
        "activos_title": "<h4 style='color: #4361ee;'>🔭 Assets</h4>",
        "moto_desc": "Acquisition of an ATV/Quad, necessary for mobility on the farm and to Tovar and surrounding towns to search for supplies and sell products (eggs, chickens, etc.)",
        "moto_title": "ATV / Quad",
        "freezer_title": "Acquisition of a freezer for the preservation of processed poultry",
        "cocina_title": "Acquisition of cooktop",
        "herramientas_title": "Acquisition of work tools",
        "materiales_title": "Acquisition of construction and operational materials",
        "infraestructura_header": "### 🛠️ Infrastructure and Physical Rehabilitation",
        "sistema_hidrico_title": "Water System: Main water storage tanks were repaired, cleaned, and sealed, and the main pipe system was renewed to guarantee water access in coops and housing.",
        "sistema_electrico_title": "Electrical System: Comprehensive improvements were made to wiring and electrical outlets in coops and housing, optimizing safety and efficiency.",
        "techos_title": "Roof rehabilitation of one of the facilities",
        "espacios_title": "Physical rehabilitation of workspace and living areas",
        "gestion_financiera_header": "### 💼 Financial Management",
        "gestion_financiera_title": "💼 Financial Management",
        "dirigido_junta": "ASIGLEH Board of Directors",
        "dirigido_convencion": "ASIGLEH National Convention",
        "antecedentes_p1": "The Alas de Bendición y Esperanza Farm (GABE) project started in May 2024 with the vision of creating a self-sustaining agroecological production unit of 7 hectares in Tovar, Mérida, under the coverage of ASIGLEH. This active project has a strategic vision to transform seed capital into a self-sustaining engine within a 5-year timeframe —of which we have already traversed the first 2 years with great effort and a good degree of success—, integrating food production with community development and missionary expansion.",
        "antecedentes_pilares_caption": "Alas de Bendición Farm (GABE) Project Pillars",
        "antecedentes_fc1_caption": "Cash Flow Architecture I: The Broiler Cycle",
        "antecedentes_fc2_caption": "Cash Flow Architecture II: The Layer Hen Cycle",
        "antecedentes_body": "Upon completing the acquisition of the farm, the team took on the challenge of redirecting initial efforts towards the critical repair and stabilization of a residential and service infrastructure that was in an advanced state of decay. Once this habitability stage was overcome, the 2025-2026 period marked the formal beginning of productive operations through the establishment of a poultry unit with laying hens and broilers under a two-cycle commercial scheme to generate daily liquidity. Despite the logistical and operational obstacles inherent to the environment, this foundational experience consolidated the technical bases needed to diversify production and ensure the future self-sufficiency of the farm.",
        "antecedentes_gestion": "Steps have also been taken towards the agricultural diversification of the farm.\n\nIn terms of infrastructure, progress has been made in adapting the various spaces and we are almost ready to set up a training site for agroecological and organic techniques.",
        "objetivos_intro": "The Barnabas Aid subsidy focused on three fundamental pillars:",
        "objetivos_body": "* **Vital Infrastructure Rehabilitation**: Restore the operational capacity of the farm by recovering and stabilizing water and electricity systems to guarantee operational continuity. It also refers to improvements in infrastructure such as roofs, windows, doors, bathrooms, and kitchen.\n* **Short and Long Cycle Poultry Production**: Establish broiler chicken production for immediate liquidity and laying hens for long-term sustainability.\n* **Agroecological Diversification**: Expand the farm's capacity through permanent plantings (coffee and lemon) and short cycles (corn, plantain, cassava...).\n* **Food Security and Community Projection**: Provide animal protein at affordable prices or through donations to the local community and missionary projects of the Church of the Brethren.",
        "freezer_body": "**Details on cold chain and conservation:**\n* **Equipment**: Acquisition of a large-capacity horizontal freezer/congelador for safe poultry storage.\n* **Operation**: Preservation and maintenance of the cold chain for processed birds (clean and individually bagged), ensuring freshness before distribution and sale.",
        "herramientas_body": "**Equipment and tools acquired for farm operational maintenance:**\n* **Complete hand tool box** (hammer, pliers, screwdrivers, hacksaw, pipe wrenches, level, tape measure, wire stripper, etc.).\n* **Aluminum extension ladder** for high-altitude work in coops and housing.\n* **20V wireless angle grinder** for cutting and polishing materials.\n* **20V wireless drill** for fixing and installation works in the field.\n* **Plastic poultry drinkers** for controlled hydration in coops.",
        "materiales_body": "**Materials, furniture, and operational equipment acquired for farm development:**\n* **Office furniture**: Foldable work tables and ergonomic chairs for administrative tasks.\n* **Construction materials**: Corrugated zinc sheets for coop and housing roof repairs.\n* **Kitchen and bathroom equipment**: Gooseneck faucet for sink, ceramic sink, and wall organizer mirror.\n* **Technology and connectivity**: Archer AX12 TP-Link Wi-Fi 6 Router (farm internet installation).\n* **Basic appliances**: Electric drip coffee maker.\n* **Climate control materials**: Shading net (polisombra) for light and temperature regulation.",
        "sistema_hidrico_body": "**Details of maintenance and adaptation of the water distribution system:**\n* **Tank maintenance**: Deep cleaning, disinfection, crack sealing, and placement of protective covers on main masonry tanks.\n* **Main pipes**: Laying and assembly of new high-resistance pipes for water transport to the residential and production areas.\n* **Control systems**: Installation of shut-off valves, mechanical joints, and bypass systems in the field for sector distribution.\n* **Connection to coops**: Direct water supply to poultry coops to guarantee constant and automated hydration of the birds.",
        "sistema_electrico_body": "**Details of electrical system maintenance and adaptation:**\n* **Wiring renewal**: Total replacement of deteriorated wiring with new conductors of adequate gauge to support the operational load.\n* **Distribution boards**: Organization and installation of control panels with safety breakers to protect equipment and housing.\n* **Lighting and power**: Installation of high-efficiency LED luminaires and new outlet points in coops and common areas.\n* **Backup systems**: Adaptation of connections and conduits prepared for integration of alternative/backup energy systems.",
        "techos_body": "**Details on repairs and improvements to the facility roof:**\n* **Disassembly and cleaning**: Removal of old sheets and cleaning of the support structure.\n* **Structural reinforcement**: Repair of wooden/metal beams and supports compromised by humidity.\n* **New roof**: Placement of new corrugated zinc sheets to prevent leaks and drips.\n* **Sealing and waterproofing**: Adjustment of joints and sealing of screws to guarantee tightness against rain.",
        "espacios_body": "**Details on remodeling and adaptation of living and working environments:**\n* **Living spaces**: Conditioning of rooms for resident farm staff (painting, repairs, and finishes).\n* **Kitchen and bathrooms**: Installation of cooktops, new faucets, sinks, and mirrors to guarantee decent living conditions.\n* **Administrative areas**: Organization and equipping of the office with the acquired ergonomic furniture.\n* **Coop adaptation**: Minor repairs and physical preparation of poultry spaces before the entry of new batches of birds.",
        "resultados_intro_highlight": """
        <div class="intro-highlight-card">
            For the Church of the Brethren Venezuela (ASIGLEH) and the Alas de Bendición y Esperanza Farm (GABE), transparency is not just an ethical value, but the foundational pillar that sustains our community mission. In highly complex and hyperinflationary economic environments, precise accountability and strategic resource management are the tools that transform grant funds into tangible, lasting social impact. With the firm purpose of backing our institutional management capacity before our allies of the Global Food Initiative (GFI) and the global community, we openly present the Executive Summary of Achievements for the 2025-2026 period. This execution history demonstrates how the farm team's commitment, financial optimization, and transparent investment in assets and infrastructure have paved the way to successfully scale towards the new 2026-2027 Agricultural Grant. Below, we detail the goals achieved and the operational foundations consolidated thanks to responsible administration:
        </div>
        """,
        "resultados_summary": """
        <div class="summary-card">
            <strong>Executive Summary of Achievements (2025-2026 Period):</strong>
            <ul>
                <li><strong>🔭 Asset Acquisition:</strong> Integration of vital transportation (quad bike), cold chain equipment (freezer), work tools, and administrative supplies essential for daily operations.</li>
                <li><strong>🛠️ Infrastructure Rehabilitation:</strong> Critical repair and improvement of living and working conditions (potable water systems, electrical grid safety, roofs, and farm buildings).</li>
                <li><strong>🐓 Active Poultry Production:</strong> Rearing of 380 laying hens and 100 broiler chickens to provide nutritional security, market commercialization, and emergency community aid.</li>
                <li><strong>🌱 Agroecological Diversification:</strong> Planting of permanent cash crops (100 coffee seedlings, 100 Persian lemon trees, and 250 banana plants) alongside short-cycle food crops.</li>
                <li><strong>💼 Unified Financial Management:</strong> Efficient resource allocation through direct supplier payments (Zelle) and controlled conversion to local currency (Provincial Bank) to navigate high inflation.</li>
            </ul>
        </div>
        """,
        "cerca_header": "🚧 Fence and Gate",
        "poda_header": "🌳 Pruning of the Big Tree",
        "directiva_header": "👥 ASIGLEH Board of Directors at the Farm",
        "otras_adecuaciones_header": "🏠 Other Rehabilitations",
        "videos_obra_header": "🎥 Construction Videos",
        "video_1_title": "Video I: Outdoor works and field maintenance",
        "video_2_title": "Video II: Extreme remodeling of interior spaces",
        "video_2_desc": "This video shows the renovations carried out in the farm's main house. Electrical and plumbing systems have been repaired, along with painting walls, adjusting windows, and reconditioning bathrooms, bedrooms, and kitchen, achieving a functional and elegant look. Outside, vehicles, banana crops, fruit trees like avocado and soursop are observed, as well as a garden with chives.",


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
    
    /* Limitar el alto máximo de los videos para que se vean completos verticalmente */
    
    /* Styles for the landing page GABE 2026 */
    .landing-hero {
        background: linear-gradient(135deg, #134e5e 0%, #2a5298 100%);
        padding: 35px 25px;
        border-radius: 16px;
        color: white !important;
        margin-bottom: 30px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.15);
        text-align: center;
    }
    
    .landing-hero, .landing-hero * {
        color: white !important;
    }
    
    .landing-hero h1 {
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        font-size: 2.2rem;
        margin: 0;
        color: white !important;
    }
    .landing-hero p {
        font-size: 1.1rem;
        opacity: 0.95;
        margin-top: 10px;
        color: white !important;
    }
    
    .glass-card {
        background: white;
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
        border: 1px solid #e2e8f0;
        margin-bottom: 25px;
    }
    
    .section-title {
        font-family: 'Outfit', sans-serif;
        font-weight: 600;
        font-size: 1.5rem;
        color: var(--text-color) !important;
        border-bottom: 2px solid var(--primary-color, #1e3c72);
        padding-bottom: 8px;
        margin-bottom: 15px;
    }
    
    .bio-card {
        background: #f8fafc;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        margin-bottom: 15px;
        color: #1e293b !important;
    }
    .bio-name {
        font-family: 'Outfit', sans-serif;
        font-weight: 600;
        font-size: 1.1rem;
        color: #0f172a !important;
    }
    .bio-text {
        font-size: 0.9rem;
        color: #334155 !important;
        margin-top: 5px;
    }
    
    .blog-container {
        background: #fdfbf7;
        border-left: 5px solid #d97706;
        padding: 20px;
        border-radius: 4px 12px 12px 4px;
        margin-bottom: 20px;
        color: #1a202c !important;
    }
    
    .blog-container * {
        color: #1a202c !important;
    }
    
    .contact-card {
        background-color: #f1f5f9;
        color: #0f172a !important;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        margin-bottom: 15px;
    }
    .contact-card h4 {
        margin-top: 0;
        color: #1e3c72 !important;
    }
    .contact-card div, .contact-card strong, .contact-card p, .contact-card li, .contact-card span {
        color: #2d3748 !important;
    }
    
    .alliance-btn {
        display: inline-block;
        background: #1e3c72;
        color: white !important;
        padding: 10px 20px;
        border-radius: 8px;
        text-decoration: none;
        font-weight: bold;
        transition: background 0.3s ease;
    }
    .alliance-btn:hover {
        background: #2a5298;
    }
    
    .image-placeholder {
        background: #f1f5f9;
        border: 2px dashed #cbd5e1;
        border-radius: 8px;
        padding: 40px 20px;
        text-align: center;
        color: #64748b;
        font-family: 'Inter', sans-serif;
        margin-bottom: 15px;
    }
    
    video {
        max-height: 80vh;
        object-fit: contain;
    }
    
    .summary-card {
        background: #f8fafc;
        border-left: 5px solid #2563eb;
        padding: 20px;
        border-radius: 4px 12px 12px 4px;
        margin-bottom: 25px;
        color: #0f172a !important;
        font-size: 1rem;
        line-height: 1.6;
        border-top: 1px solid #e2e8f0;
        border-right: 1px solid #e2e8f0;
        border-bottom: 1px solid #e2e8f0;
    }
    .summary-card * {
        color: #0f172a !important;
    }
    .summary-card strong {
        color: #1e3c72 !important;
    }
    .summary-card ul {
        margin-top: 10px;
        margin-bottom: 0;
        padding-left: 20px;
    }
    .summary-card li {
        margin-bottom: 8px;
    }
    .intro-highlight-card {
        font-family: 'Outfit', sans-serif;
        font-size: 1.05rem;
        font-style: italic;
        line-height: 1.7;
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        border-left: 5px solid #1e3c72;
        padding: 24px;
        border-radius: 8px;
        margin-bottom: 25px;
        color: #1e293b !important;
        border-top: 1px solid #e2e8f0;
        border-right: 1px solid #e2e8f0;
        border-bottom: 1px solid #e2e8f0;
        box-shadow: inset 0 0 10px rgba(0,0,0,0.02);
    }
    .intro-highlight-card * {
        color: #1e293b !important;
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
    elif 'limones' in desc_lower or 'cafe' in desc_lower or 'café' in desc_lower:
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
# NAVEGACIÓN Y CONFIGURACIÓN GENERAL
# -------------------------------------------------------------------

def safe_image(img_path, caption=None, use_container_width=True, width=None):
    if os.path.exists(img_path):
        if width:
            st.image(img_path, caption=caption, width=width)
        else:
            st.image(img_path, caption=caption, use_container_width=use_container_width)
    else:
        file_name = os.path.basename(img_path)
        lang = st.session_state.language
        text_es = f"📷 [Imagen: {file_name}] - Cargando recurso... (Se mostrará aquí al confirmarse la copia de archivos)"
        text_en = f"📷 [Image: {file_name}] - Loading asset... (Will display here once file transfer completes)"
        placeholder_text = text_es if lang == "es" else text_en
        st.markdown(f'<div class="image-placeholder">{placeholder_text}</div>', unsafe_allow_html=True)

def render_gabe2026_landing(lang_code, df_filtered, df_raw, has_financial_cols, SELECTED_SHEET):
    # Header Banner Hero
    import base64
    logo_path = os.path.join("assets", "GFIlogo01.png")
    logo_html = ""
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            logo_base64 = base64.b64encode(f.read()).decode()
            logo_html = f'<img src="data:image/png;base64,{logo_base64}" style="max-height: 80px; margin-bottom: 15px; display: block; margin-left: auto; margin-right: auto;" />'

    st.markdown(
        f"""
        <div class="landing-hero">
            {logo_html}
            <span style="font-size: 0.9rem; text-transform: uppercase; letter-spacing: 2px; opacity: 0.8;">{TRANSLATIONS[lang_code]['landing_header']}</span>
            <h1>{TRANSLATIONS[lang_code]['landing_title']}</h1>
            <div style="height: 3px; width: 80px; background: #e2e8f0; margin: 15px auto; border-radius: 2px;"></div>
            <p>{TRANSLATIONS[lang_code]['landing_sub']}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Antecedentes del Proyecto
    st.markdown(TRANSLATIONS[lang_code]['antecedentes_header'])
    with st.expander(TRANSLATIONS[lang_code]['antecedentes_title'], expanded=True):
        col_ant1, col_ant2 = st.columns([1, 1.5])
        with col_ant1:
            st.image(os.path.join("assets", "gabe001.png"), caption=TRANSLATIONS[lang_code]['antecedentes_pilares_caption'], use_container_width=True)
        with col_ant2:
            st.markdown(f"<p style='line-height: 1.6;'>{TRANSLATIONS[lang_code]['antecedentes_p1']}</p>", unsafe_allow_html=True)
        
        st.markdown(TRANSLATIONS[lang_code]['antecedentes_body'])
        
        col_fc1, col_fc2 = st.columns([1, 1])
        with col_fc1:
            st.image(os.path.join("assets", "gabe002.png"), caption=TRANSLATIONS[lang_code]['antecedentes_fc1_caption'], use_container_width=True)
        with col_fc2:
            st.image(os.path.join("assets", "gabe003.png"), caption=TRANSLATIONS[lang_code]['antecedentes_fc2_caption'], use_container_width=True)
            
        st.markdown(TRANSLATIONS[lang_code]['antecedentes_gestion'])
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 1. Visión Unificada
    with st.container():
        st.markdown(f'<div class="section-title">{TRANSLATIONS[lang_code]["unified_vision_title"]}</div>', unsafe_allow_html=True)
        col_v1, col_v2 = st.columns([1.5, 1])
        with col_v1:
            st.markdown(f'<div style="line-height: 1.7; font-size: 1.05rem;">{TRANSLATIONS[lang_code]["unified_vision_desc"]}</div>', unsafe_allow_html=True)
        with col_v2:
            st.image(os.path.join("assets", "GabeBanner002.png"), use_container_width=True)
            
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 2. Galería de Picalqui
    with st.container():
        st.markdown(f'<div class="section-title">{TRANSLATIONS[lang_code]["picalqui_title"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="line-height: 1.6; margin-bottom: 20px;">{TRANSLATIONS[lang_code]["picalqui_desc"]}</div>', unsafe_allow_html=True)
        
        # Display the main technical training image
        safe_image(os.path.join("assets", "picalquiCom1.png"), caption="Capacitación en Picalqui, Ecuador (Agosto 2023)" if lang_code == "es" else "Technical training in Picalqui, Ecuador (August 2023)")
        
        col_t1, col_t2, col_t3 = st.columns(3)
        with col_t1:
            st.markdown(
                f"""
                <div class="bio-card">
                    <div class="bio-name">👤 {TRANSLATIONS[lang_code]['tech1_name']}</div>
                    <div style="font-size:0.8rem; font-weight:bold; color:#1e3c72; margin-top:2px;">Guárico State</div>
                    <div class="bio-text">{TRANSLATIONS[lang_code]['tech1_bio']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            safe_image(os.path.join("assets", "susanne001.jpg"))
        with col_t2:
            st.markdown(
                f"""
                <div class="bio-card">
                    <div class="bio-name">👤 {TRANSLATIONS[lang_code]['tech2_name']}</div>
                    <div style="font-size:0.8rem; font-weight:bold; color:#1e3c72; margin-top:2px;">Apure State</div>
                    <div class="bio-text">{TRANSLATIONS[lang_code]['tech2_bio']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            safe_image(os.path.join("assets", "picalqui001.jpg"))
        with col_t3:
            st.markdown(
                f"""
                <div class="bio-card">
                    <div class="bio-name">👤 {TRANSLATIONS[lang_code]['tech3_name']}</div>
                    <div style="font-size:0.8rem; font-weight:bold; color:#1e3c72; margin-top:2px;">Mérida State</div>
                    <div class="bio-text">{TRANSLATIONS[lang_code]['tech3_bio']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            safe_image(os.path.join("assets", "Gilbert001.jpg"))

    st.markdown("<br>", unsafe_allow_html=True)

    # Resultados alcanzados
    render_resultados_alcanzados(lang_code, df_filtered, df_raw, has_financial_cols, SELECTED_SHEET)

    st.markdown("<br>", unsafe_allow_html=True)

    # 3. Sostenibilidad y Flujo Comunitario
    with st.container():
        st.markdown(f'<div class="section-title">{TRANSLATIONS[lang_code]["sustainability_title"]}</div>', unsafe_allow_html=True)
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.markdown(f'<h4>{TRANSLATIONS[lang_code]["nuestra_granja_title"]}</h4>', unsafe_allow_html=True)
            safe_image(os.path.join("assets", "gabeEnproduccion.png"), caption=TRANSLATIONS[lang_code]["nuestra_granja_desc"])
            st.markdown(f'<div style="line-height: 1.6; margin-top: 15px;">{TRANSLATIONS[lang_code]["sustainability_desc"]}</div>', unsafe_allow_html=True)
            safe_image(os.path.join("assets", "procesoCerdos02.png"), caption="Cría de cerdos en la Granja GABE" if lang_code == "es" else "Pig rearing at GABE Farm")
            
        with col_s2:
            st.markdown(f'<h4>{TRANSLATIONS[lang_code]["flow_title"]}</h4>', unsafe_allow_html=True)
            safe_image(os.path.join("assets", "pastSanCrist01.png"), caption="Red de pastores de Iglesias involucradas en San Cristóbal - Mérida " if lang_code == "es" else "Network of pastors from involved churches in San Cristóbal - Mérida")
            st.markdown(f'<div style="line-height: 1.6; margin-top: 15px;">{TRANSLATIONS[lang_code]["flow_desc"]}</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 4. Perfil de Líderes y Voluntarios
    with st.container():
        st.markdown(f'<div class="section-title">{TRANSLATIONS[lang_code]["leaders_title"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="line-height: 1.6; margin-bottom: 20px;">{TRANSLATIONS[lang_code]["leaders_desc"]}</div>', unsafe_allow_html=True)
        
        # Roger Profile
        col_r1, col_r2 = st.columns([1, 2.5])
        with col_r1:
            safe_image(os.path.join("assets", "roger001.jpg"))
        with col_r2:
            st.markdown(f'<h4>{TRANSLATIONS[lang_code]["roger_title"]}</h4>', unsafe_allow_html=True)
            st.markdown(f'<div style="line-height: 1.6; font-size:1.05rem;">{TRANSLATIONS[lang_code]["roger_bio"]}</div>', unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Pastors Profile
        col_p1, col_p2 = st.columns([1, 2.5])
        with col_p1:
            safe_image(os.path.join("assets", "pastMerida01.png"))
        with col_p2:
            st.markdown(f'<h5>{TRANSLATIONS[lang_code]["pastors_title"]}</h5>', unsafe_allow_html=True)
            st.markdown(f'<div style="line-height: 1.6; font-size:0.95rem; opacity: 0.85;">{TRANSLATIONS[lang_code]["pastors_bio"]}</div>', unsafe_allow_html=True)

        st.markdown("<br><hr style='border: 1px dashed #cbd5e1;'><br>", unsafe_allow_html=True)
        
        # Classroom
        col_c1, col_c2 = st.columns([1.5, 1])
        with col_c1:
            st.markdown(f'<h4>{TRANSLATIONS[lang_code]["classroom_title"]}</h4>', unsafe_allow_html=True)
            st.markdown(f'<div style="line-height: 1.6; font-size:1.05rem;">{TRANSLATIONS[lang_code]["classroom_desc"]}</div>', unsafe_allow_html=True)
        with col_c2:
            safe_image(os.path.join("assets", "clases01.png"), caption="Aula de clases en la casa principal de la Granja. Imagen generada con IA" if lang_code == "es" else "Classroom inside the main house of the Farm. AI-generated image")

    st.markdown("<br>", unsafe_allow_html=True)

    # 5. Contacto
    with st.container():
        # Verified contact info
        st.markdown(
            f"""
            <div class="contact-card">
                <h4 style="margin-top:0;">{TRANSLATIONS[lang_code]['contact_title']}</h4>
                <div style="line-height:1.7;">{TRANSLATIONS[lang_code]['contact_desc']}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")
    st.markdown(
        f"""
        <div style="text-align: center; color: #94a3b8; font-size: 0.85rem; margin-top: 20px;">
            {TRANSLATIONS[lang_code]['footer_text']}
        </div>
        """,
        unsafe_allow_html=True
    )

def render_resultados_alcanzados(lang_code, df_filtered, df_raw, has_financial_cols, SELECTED_SHEET):
    
    st.markdown(TRANSLATIONS[lang_code]['resultados_header'])
    with st.expander(TRANSLATIONS[lang_code]['resultados_title'], expanded=True):
        st.markdown(TRANSLATIONS[lang_code]['resultados_intro_highlight'], unsafe_allow_html=True)
        st.markdown(TRANSLATIONS[lang_code]['resultados_summary'], unsafe_allow_html=True)
        st.markdown(TRANSLATIONS[lang_code]['activos_title'], unsafe_allow_html=True)
        with st.expander("🔭 Activos" if lang_code == "es" else "🔭 Assets", expanded=True):
            # 1. Cuatrimoto
            st.markdown(f"### 🚜 {TRANSLATIONS[lang_code]['moto_title']}")
            st.markdown(TRANSLATIONS[lang_code]['moto_desc'])
            col_m1, col_m2 = st.columns(2)
            with col_m1:
                st.image(os.path.join("assets", "cuatrimoto01.png"), use_container_width=True)
                col_sub1, col_sub2 = st.columns(2)
                with col_sub1:
                    st.image(os.path.join("assets", "cuatrimoto02.png"), use_container_width=True)
                with col_sub2:
                    st.image(os.path.join("assets", "photo_2026-06-08_14-38-24.jpg"), use_container_width=True)
            with col_m2:
                st.video(os.path.join("assets", "GabeCuatrimoto.mp4"))
                
            st.markdown("<hr style='border: 1px dashed #cccccc;'>", unsafe_allow_html=True)
            
            # 2. Freezer & Cocina
            col_fc1, col_fc2 = st.columns(2)
            with col_fc1:
                st.markdown(f"### ❄️ {TRANSLATIONS[lang_code]['freezer_title']}")
                st.markdown(TRANSLATIONS[lang_code]['freezer_body'])
                st.image(os.path.join("assets", "IMG-20251223-WA0015.jpg"), use_container_width=True)
                col_subf1, col_subf2 = st.columns(2)
                with col_subf1:
                    st.image(os.path.join("assets", "neverasmall.jpg"), use_container_width=True)
                with col_subf2:
                    st.image(os.path.join("assets", "photo_2026-04-24_11-48-07.jpg"), use_container_width=True)
            with col_fc2:
                st.markdown(f"### 🍳 {TRANSLATIONS[lang_code]['cocina_title']}")
                st.image(os.path.join("assets", "IMG-20251223-WA0019.jpg.png"), use_container_width=True)
                
            st.markdown("<hr style='border: 1px dashed #cccccc;'>", unsafe_allow_html=True)
            
            # 3. Herramientas & Materiales
            col_hm1, col_hm2 = st.columns(2)
            with col_hm1:
                st.markdown(f"### 🛠️ {TRANSLATIONS[lang_code]['herramientas_title']}")
                st.markdown(TRANSLATIONS[lang_code]['herramientas_body'])
                st.image(os.path.join("assets", "IMG-20251223-WA0020.jpg"), use_container_width=True)
                col_subh1, col_subh2 = st.columns(2)
                with col_subh1:
                    st.image(os.path.join("assets", "IMG-20250129-WA0040.png"), use_container_width=True)
                with col_subh2:
                    st.image(os.path.join("assets", "IMG-20250129-WA0041.jpg"), use_container_width=True)
            with col_hm2:
                st.markdown(f"### 📦 {TRANSLATIONS[lang_code]['materiales_title']}")
                st.markdown(TRANSLATIONS[lang_code]['materiales_body'])
                st.image(os.path.join("assets", "IMG-20251223-WA0022.jpg.png"), use_container_width=True)
                col_subm1, col_subm2 = st.columns(2)
                with col_subm1:
                    st.image(os.path.join("assets", "IMG-20251223-WA0016.jpg"), use_container_width=True)
                with col_subm2:
                    st.image(os.path.join("assets", "polisombra.jpg"), use_container_width=True)
        
        # Divider
        st.markdown("<hr style='border: 2px solid #8B7A5F;'>", unsafe_allow_html=True)
        
        # Header
        st.markdown(TRANSLATIONS[lang_code]['infraestructura_header'])
        
        # Sistema Hídrico
        with st.expander(TRANSLATIONS[lang_code]['sistema_hidrico_title'], expanded=True):
            st.markdown(TRANSLATIONS[lang_code]['sistema_hidrico_body'])
            # Row 1
            col_hid1_1, col_hid1_2, col_hid1_3, col_hid1_4 = st.columns(4)
            with col_hid1_1:
                st.image(os.path.join("assets", "IMG-20250118-WA0047 (2).jpg"), use_container_width=True)
            with col_hid1_2:
                st.image(os.path.join("assets", "IMG-20250118-WA0051 (2).jpg"), use_container_width=True)
            with col_hid1_3:
                st.image(os.path.join("assets", "IMG-20250118-WA0049 (2).jpg"), use_container_width=True)
            with col_hid1_4:
                st.image(os.path.join("assets", "IMG-20250130-WA0029.jpg"), use_container_width=True)
                
            # Row 2
            col_hid2_1, col_hid2_2, col_hid2_3, col_hid2_4 = st.columns(4)
            with col_hid2_1:
                st.image(os.path.join("assets", "IMG-20250118-WA0066.jpg"), use_container_width=True)
            with col_hid2_2:
                st.image(os.path.join("assets", "IMG-20250118-WA0063.jpg"), use_container_width=True)
            with col_hid2_3:
                st.image(os.path.join("assets", "IMG-20250118-WA0060.jpg"), use_container_width=True)
            with col_hid2_4:
                st.image(os.path.join("assets", "photo_2026-04-24_11-52-10.jpg"), use_container_width=True)
        
            # Row 3
            col_hid3_1, col_hid3_2, col_hid3_3, col_hid3_4 = st.columns(4)
            with col_hid3_1:
                st.image(os.path.join("assets", "photo_2026-04-24_11-54-45.jpg"), use_container_width=True)
            with col_hid3_2:
                st.image(os.path.join("assets", "photo_2026-04-24_11-54-38.jpg"), use_container_width=True)
            with col_hid3_3:
                st.image(os.path.join("assets", "photo_2026-04-24_11-51-14.jpg"), use_container_width=True)
            with col_hid3_4:
                st.image(os.path.join("assets", "IMG-20250118-WA0045.jpg"), use_container_width=True)
        
            # Row 4
            col_hid4_1, col_hid4_2, col_hid4_3, col_hid4_4 = st.columns(4)
            with col_hid4_1:
                st.image(os.path.join("assets", "photo_2026-04-24_11-54-17.jpg"), use_container_width=True)
            with col_hid4_2:
                st.image(os.path.join("assets", "photo_2026-04-24_11-52-53.jpg"), use_container_width=True)
            with col_hid4_3:
                st.image(os.path.join("assets", "photo_2026-04-24_11-52-57.jpg"), use_container_width=True)
            with col_hid4_4:
                st.video(os.path.join("assets", "video_2026-04-24_11-54-22.mp4"))
        
        # Sistema Eléctrico
        with st.expander(TRANSLATIONS[lang_code]['sistema_electrico_title'], expanded=True):
            st.markdown(TRANSLATIONS[lang_code]['sistema_electrico_body'])
            col_el1, col_el2, col_el3 = st.columns(3)
            with col_el1:
                st.image(os.path.join("assets", "IMG-20250212-WA0025.jpg"), use_container_width=True)
            with col_el2:
                st.image(os.path.join("assets", "IMG-20250115-WA0134 (2).jpg"), use_container_width=True)
                st.image(os.path.join("assets", "IMG-20260206-WA0000.jpg"), use_container_width=True)
            with col_el3:
                st.image(os.path.join("assets", "IMG-20250128-WA0069.jpg"), use_container_width=True)
                st.video(os.path.join("assets", "video_2026-04-24_11-50-46.mp4"))
        
        # Adecuación de techos
        with st.expander(TRANSLATIONS[lang_code]['techos_title'], expanded=True):
            st.markdown(TRANSLATIONS[lang_code]['techos_body'])
            col_tec1, col_tec2, col_tec3 = st.columns(3)
            with col_tec1:
                st.image(os.path.join("assets", "IMG-20250212-WA0006.jpg"), use_container_width=True)
                st.image(os.path.join("assets", "IMG-20250212-WA0033.jpg"), use_container_width=True)
            with col_tec2:
                st.image(os.path.join("assets", "IMG-20250212-WA0031.jpg"), use_container_width=True)
                st.image(os.path.join("assets", "IMG-20250212-WA0037.jpg"), use_container_width=True)
            with col_tec3:
                st.image(os.path.join("assets", "IMG-20250212-WA0035.jpg"), use_container_width=True)
        
        # Adecuación física de espacios
        with st.expander(TRANSLATIONS[lang_code]['espacios_title'], expanded=True):
            st.markdown(TRANSLATIONS[lang_code]['espacios_body'])
            
            st.markdown("<hr style='border: 1px dashed #cccccc; margin-top: 15px; margin-bottom: 15px;'>", unsafe_allow_html=True)
            
            # Cerca y Portón
            st.markdown(f"<h4 style='margin-bottom: 15px;'>{TRANSLATIONS[lang_code]['cerca_header']}</h4>", unsafe_allow_html=True)
            col_c1_1, col_c1_2, col_c1_3 = st.columns(3)
            with col_c1_1:
                st.image(os.path.join("assets", "IMG-20260310-WA0041.jpg"), use_container_width=True)
            with col_c1_2:
                st.image(os.path.join("assets", "photo_2026-04-24_11-47-56.jpg"), use_container_width=True)
            with col_c1_3:
                st.image(os.path.join("assets", "photo_2026-04-24_11-48-35.jpg"), use_container_width=True)
                
            col_c2_1, col_c2_2, col_c2_3 = st.columns(3)
            with col_c2_1:
                st.image(os.path.join("assets", "photo_2026-04-24_11-48-40.jpg"), use_container_width=True)
            with col_c2_2:
                st.image(os.path.join("assets", "photo_2026-04-24_11-48-45.jpg"), use_container_width=True)
                
            st.markdown("<hr style='border: 1px dashed #cccccc; margin-top: 15px; margin-bottom: 15px;'>", unsafe_allow_html=True)
            
            # Poda del gran árbol
            st.markdown(f"<h4 style='margin-bottom: 15px;'>{TRANSLATIONS[lang_code]['poda_header']}</h4>", unsafe_allow_html=True)
            col_p1, col_p2, col_p3 = st.columns(3)
            with col_p1:
                st.image(os.path.join("assets", "IMG-20260205-WA0027.jpg"), use_container_width=True)
            with col_p2:
                st.image(os.path.join("assets", "IMG-20260205-WA0031.jpg"), use_container_width=True)
            with col_p3:
                st.image(os.path.join("assets", "IMG-20260205-WA0032.jpg"), use_container_width=True)
                
            st.markdown("<hr style='border: 1px dashed #cccccc; margin-top: 15px; margin-bottom: 15px;'>", unsafe_allow_html=True)
            
            # Directiva de ASIGLEH en la Granja
            st.markdown(f"<h4 style='margin-bottom: 15px;'>{TRANSLATIONS[lang_code]['directiva_header']}</h4>", unsafe_allow_html=True)
            col_d1, col_d2 = st.columns(2)
            with col_d1:
                st.image(os.path.join("assets", "IMG-20250118-WA0065.jpg"), use_container_width=True)
            with col_d2:
                st.image(os.path.join("assets", "IMG-20250118-WA0059.jpg"), use_container_width=True)
                
            st.markdown("<hr style='border: 1px dashed #cccccc; margin-top: 15px; margin-bottom: 15px;'>", unsafe_allow_html=True)
            
            # Otras Adecuaciones
            st.markdown(f"<h4 style='margin-bottom: 15px;'>{TRANSLATIONS[lang_code]['otras_adecuaciones_header']}</h4>", unsafe_allow_html=True)
            col_oa1, col_oa2, col_oa3 = st.columns(3)
            with col_oa1:
                st.image(os.path.join("assets", "IMG-20260205-WA0048.jpg"), use_container_width=True)
            with col_oa2:
                st.image(os.path.join("assets", "IMG-20260203-WA0040.jpg"), use_container_width=True)
            with col_oa3:
                st.image(os.path.join("assets", "IMG-20260217-WA0033.jpg"), use_container_width=True)
                
            st.markdown("<hr style='border: 1px dashed #cccccc; margin-top: 15px; margin-bottom: 15px;'>", unsafe_allow_html=True)
            
            # Videos de la Obra
            st.markdown(f"<h4 style='margin-bottom: 15px;'>{TRANSLATIONS[lang_code]['videos_obra_header']}</h4>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-weight: bold; margin-bottom: 5px;'>{TRANSLATIONS[lang_code]['video_1_title']}</p>", unsafe_allow_html=True)
            st.video(os.path.join("assets", "video_2026-04-24_11-55-11.mp4"))
            
            st.markdown(f"<p style='font-weight: bold; margin-top: 15px; margin-bottom: 5px;'>{TRANSLATIONS[lang_code]['video_2_title']}</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='line-height: 1.6; margin-bottom: 10px;'>{TRANSLATIONS[lang_code]['video_2_desc']}</p>", unsafe_allow_html=True)
            col_v2_1, col_v2_2, col_v2_3 = st.columns([1, 2, 1])
            with col_v2_2:
                st.video(os.path.join("assets", "makeoverExtreme.mp4"))
        
        
        # Divider
        st.markdown("<hr style='border: 2px solid #8B7A5F;'>", unsafe_allow_html=True)
        
        # -------------------------------------------------------------------
        # PRODUCCIÓN AVÍCOLA
        # -------------------------------------------------------------------
        st.markdown(TRANSLATIONS[lang_code]['avicola_header'])
        
        with st.expander(TRANSLATIONS[lang_code]['inversion_aves_title'], expanded=True):
            st.markdown(TRANSLATIONS[lang_code]['inversion_aves_content'])
            col_av1, col_av2, col_av3 = st.columns(3)
            with col_av1:
                st.image(os.path.join("assets", "IMG-20250212-WA0053.jpg"), use_container_width=True)
            with col_av2:
                st.image(os.path.join("assets", "IMG-20250716-WA0081.jpg.png"), use_container_width=True)
                st.image(os.path.join("assets", "IMG-20250201-WA0029.jpg"), use_container_width=True)
            with col_av3:
                st.image(os.path.join("assets", "IMG-20250116-WA0028 (2).jpg"), use_container_width=True)
                st.image(os.path.join("assets", "IMG-20250201-WA0028.jpg"), use_container_width=True)
                
        with st.expander(TRANSLATIONS[lang_code]['pollos_engorde_title'], expanded=True):
            st.markdown(TRANSLATIONS[lang_code]['pollos_engorde_content'])
            col_pe1, col_pe2 = st.columns([1.2, 1])
            with col_pe1:
                st.image(os.path.join("assets", "photo_2026-04-24_11-53-49.jpg"), use_container_width=True)
                st.image(os.path.join("assets", "photo_2026-04-24_11-53-39.jpg"), use_container_width=True)
                st.image(os.path.join("assets", "photo_2026-04-24_11-47-05.jpg.png"), use_container_width=True)
            with col_pe2:
                st.image(os.path.join("assets", "photo_2026-04-24_11-48-07.jpg"), use_container_width=True)
        
        # -------------------------------------------------------------------
        # DIVERSIFICACIÓN AGROECOLÓGICA
        # -------------------------------------------------------------------
        st.markdown("<hr style='border: 2px solid #8B7A5F;'>", unsafe_allow_html=True)
        st.markdown(TRANSLATIONS[lang_code]['diversificacion_header'])
        
        with st.expander("Diversificación Agroecológica" if lang_code == "es" else "Agroecological Diversification", expanded=True):
            # 1. Café
            st.markdown(f"#### ☕ {TRANSLATIONS[lang_code]['siembra_cafe_title']}")
            st.markdown(TRANSLATIONS[lang_code]['siembra_cafe_content'])
            col_c1, col_c2 = st.columns(2)
            with col_c1:
                st.video(os.path.join("assets", "video_2026-04-24_11-49-19.mp4"))
            with col_c2:
                col_subc1, col_subc2 = st.columns(2)
                with col_subc1:
                    st.image(os.path.join("assets", "photo_2026-04-24_11-49-30.jpg"), use_container_width=True)
                with col_subc2:
                    st.image(os.path.join("assets", "photo_2026-04-24_11-49-35.jpg"), use_container_width=True)
                    
            st.markdown("<hr style='border: 1px dashed #cccccc;'>", unsafe_allow_html=True)
            
            # 2. Limón Persa
            st.markdown(f"#### 🍋 {TRANSLATIONS[lang_code]['siembra_limon_title']}")
            st.markdown(TRANSLATIONS[lang_code]['siembra_limon_content'])
            col_l1, col_l2 = st.columns(2)
            with col_l1:
                st.video(os.path.join("assets", "doc_2026-04-24_11-47-33.mp4"))
            with col_l2:
                st.video(os.path.join("assets", "video_2026-04-24_11-47-41.mp4"))
                
            st.markdown("<hr style='border: 1px dashed #cccccc;'>", unsafe_allow_html=True)
            
            # 3. Cambur y otros cultivos
            st.markdown(f"#### 🍌 {TRANSLATIONS[lang_code]['siembra_cambur_title']}")
            st.markdown(TRANSLATIONS[lang_code]['siembra_cambur_content'])
            st.video(os.path.join("assets", "video_2026-04-24_11-49-46.mp4"))
            
            col1, col2, col3 = st.columns(3)
            images = [
                "photo_2026-04-24_11-49-51.jpg",
                "photo_2026-04-24_11-50-30.jpg",
                "photo_2026-04-24_11-50-35.jpg",
                "photo_2026-04-24_11-51-31.jpg",
                "photo_2026-04-24_11-54-50.jpg"
            ]
            for idx, img_name in enumerate(images):
                col = [col1, col2, col3][idx % 3]
                with col:
                    st.image(os.path.join("assets", img_name), use_container_width=True)
        
        # Divider
        st.markdown("<hr style='border: 2px solid #8B7A5F;'>", unsafe_allow_html=True)
        
        # 💼 Gestión Financiera
        render_gestion_financiera(lang_code, df_filtered, df_raw, has_financial_cols, SELECTED_SHEET)

def render_gestion_financiera(lang_code, df_filtered, df_raw, has_financial_cols, SELECTED_SHEET):
    st.markdown(TRANSLATIONS[lang_code]['gestion_financiera_header'])
    with st.expander(TRANSLATIONS[lang_code]['gestion_financiera_title'], expanded=True):
        with st.expander(TRANSLATIONS[lang_code]['intro_title'], expanded=False):
            st.markdown(TRANSLATIONS[lang_code]['intro_body'], unsafe_allow_html=True)
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
                {"Proveedor": "Edgar Rincon Albarracin", "Fecha": "09-03-2026", "Monto USD": 92.00, "Descripción": "Por comida de gallinas y pollos", "Imagen_Path": os.path.join("assets", "gabe12.jpg")},
                {"Proveedor": "Edgar Rincon Albarracin", "Fecha": "24-03-2026", "Monto USD": 450.00, "Descripción": "Por matas de cafe GABE", "Imagen_Path": ""}
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
                "Por comida de gallinas y pollos": "Chicken and Hen Feed",
                "Por matas de cafe GABE": "GABE Coffee Plants"
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
            
    
    
# Main Execution routing
# -------------------------------------------------------------------
# HEADER Y SELECCIÓN DE IDIOMA EN PÁGINA PRINCIPAL
# -------------------------------------------------------------------
col_hdr_logo, col_hdr_lang = st.columns([8, 2])
with col_hdr_logo:
    safe_image(os.path.join("assets", "AsiglehLogo01.jpg"), width=150)
with col_hdr_lang:
    selected_lang = st.selectbox(
        "Idioma / Language",
        options=["Español", "English"],
        index=0 if st.session_state.language == "es" else 1,
        key="main_lang_selector",
        label_visibility="collapsed"
    )
st.session_state.language = "es" if selected_lang == "Español" else "en"
lang_code = st.session_state.language

render_gabe2026_landing(lang_code, df_filtered, df_raw, has_financial_cols, SELECTED_SHEET)
