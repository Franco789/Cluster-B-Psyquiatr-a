import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ==============================================================================
# CONFIGURACIÓN DE PÁGINA Y ESTILO TIPOGRÁFICO INSTITUCIONAL
# ==============================================================================
st.set_page_config(
    page_title="Evaluación Dimensional del Clúster B | Ateneo de Psiquiatría",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inyección de estilos CSS limpios y estrictamente contenidos
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    background-color: #070B12 !important;
    color: #E2E8F0 !important;
}

.block-container {
    padding-top: 1.8rem !important;
    padding-bottom: 3rem !important;
    max-width: 96% !important;
}

h1 {
    font-size: 2.1rem !important;
    font-weight: 700 !important;
    letter-spacing: -0.025em !important;
    color: #F8FAFC !important;
    margin-bottom: 0.25rem !important;
}

h2, h3, h4 {
    font-weight: 600 !important;
    letter-spacing: -0.015em !important;
    color: #F1F5F9 !important;
}

div[data-testid="stMetric"] {
    background: #0E1626 !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 8px !important;
    padding: 16px 20px !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.35) !important;
}

div[data-testid="stMetric"] label {
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
    color: #94A3B8 !important;
}

div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    font-size: 1.75rem !important;
    font-weight: 700 !important;
    color: #F8FAFC !important;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 8px !important;
    background-color: transparent !important;
    border-bottom: 1px solid rgba(255, 255, 255, 0.09) !important;
    padding-bottom: 6px !important;
}

.stTabs [data-baseweb="tab"] {
    background-color: #0B1220 !important;
    border: 1px solid rgba(255, 255, 255, 0.07) !important;
    border-radius: 6px !important;
    padding: 10px 20px !important;
    color: #94A3B8 !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
}

.stTabs [aria-selected="true"] {
    background: #1E293B !important;
    border-color: #38BDF8 !important;
    color: #38BDF8 !important;
}

section[data-testid="stSidebar"] {
    background-color: #090E17 !important;
    border-right: 1px solid rgba(255, 255, 255, 0.06) !important;
}

.card-clinica {
    background: #0E1626;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 8px;
    padding: 18px 20px;
    margin-bottom: 14px;
    height: 100%;
}

.card-evidencia {
    background: #0B1322;
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 16px;
}

.badge-estudio {
    display: inline-block;
    background: rgba(56, 189, 248, 0.12);
    color: #38BDF8;
    border: 1px solid rgba(56, 189, 248, 0.3);
    border-radius: 4px;
    padding: 3px 8px;
    font-size: 0.76rem;
    font-family: 'JetBrains Mono', monospace;
    font-weight: 500;
    margin-bottom: 8px;
}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# PARÁMETROS LATERALES DE ENTRADA CLÍNICA
# ==============================================================================
st.sidebar.markdown("### Selección de Variables Clínicas")
st.sidebar.caption("Taxonomía Dimensional (HiTOP / DSM-5 Sección III / PID-5)")

trastorno_foco = st.sidebar.selectbox(
    "1. Fenotipo Clínico Predominante:",
    options=[
        "Trastorno Límite de la Personalidad (TLP)",
        "Trastorno Narcisista de la Personalidad (TNP)",
        "Trastorno Antisocial de la Personalidad (TASP)",
        "Trastorno Histriónico de la Personalidad (THP)"
    ],
    index=0
)

estresor_tipo = st.sidebar.selectbox(
    "2. Estresor Interpersonal Desencadenante:",
    options=[
        "Fijación de Límites o Negativa Externa (Frustración del deseo)",
        "Distanciamiento Vincular / Vivencia de Abandono o Rechazo",
        "Confrontación de la Realidad / Señalamiento de Inconsistencias",
        "Demora Asistencial / Dilación en la Respuesta del Entorno"
    ],
    index=0,
    help="Situación relacional que activa el sistema de apego o amenaza el esquema del Yo según el modelo de Gunderson y Bateman & Fonagy."
)

severidad_estres = st.sidebar.slider(
    "3. Tensión Afectiva Percibida (Escala SUDS 0-100):",
    min_value=0, max_value=100, value=75, step=1,
    help="Unidades Subjetivas de Distrés (SUDS, Wolpe / DBT de Linehan). Cuantifica la intensidad del dolor o desregulación vivenciada por el paciente en el momento actual."
)

st.sidebar.markdown("---")
st.sidebar.markdown("### Intervención en Crisis")

farmaco_1 = st.sidebar.selectbox(
    "Molécula o Estrategia Evaluada:",
    options=[
        "Intervención Verbal de Encuadre (Sin psicofármacos)",
        "Clonazepam (2 mg Vía Oral)",
        "Lorazepam (2 mg Sublingual)",
        "Haloperidol (5 mg Intramuscular)",
        "Quetiapina (50 mg Vía Oral)",
        "Aripiprazol (5 mg Vía Oral)",
        "Lamotrigina (100 mg Vía Oral - Mantenimiento basal previo)"
    ],
    index=1
)

soporte_red = st.sidebar.radio(
    "Red Vincular / Soporte Externo:",
    options=["Presente, continente y accesible", "Ausente, expulsiva o francamente disfuncional"],
    index=0
)

# ==============================================================================
# BASE DE DATOS DIMENSIONAL Y MODELADO COMPUTACIONAL
# ==============================================================================
perfiles_hitop = {
    "Trastorno Límite de la Personalidad (TLP)": {
        "Afecto Negativo": 95, "Desinhibición": 88, "Antagonismo": 45, "Desapego": 35, "Psicoticismo": 60,
        "color": "#F87171",
        "semiologia_clasica": "Inestabilidad en la vivencia de continuidad del Yo, labilidad afectiva fásica y angustia básica difusa con intolerancia a la soledad (Betta / Suárez Richards / Kernberg).",
        "mecanismo_defensa": "Escisión primaria (splitting) e identificación proyectiva masiva.",
        "vivencia_subjetiva": "Dolor psíquico equivalente a quemadura tisular; angustia catastrófica de fragmentación ante la amenaza de abandono.",
        "impacto_equipo": "Inducción contratransferencial de culpa, fantasías de rescate y alternancia entre sobreinvolucramiento y rechazo.",
        "perfil_radar": "Marcada polarización vertical en los ejes de Afecto Negativo y Desinhibición motriz/afectiva."
    },
    "Trastorno Narcisista de la Personalidad (TNP)": {
        "Afecto Negativo": 50, "Desinhibición": 30, "Antagonismo": 96, "Desapego": 40, "Psicoticismo": 20,
        "color": "#FBBF24",
        "semiologia_clasica": "Estructuración sobre un Yo grandioso compensatorio frente a una extrema vulnerabilidad a la vergüenza, el desprecio o la desvalorización (Schneider / Kohut).",
        "mecanismo_defensa": "Desmentida de la vulnerabilidad, idealización omnipotente y devaluación hostil del otro.",
        "vivencia_subjetiva": "Terror a la humillación o insuficiencia; necesidad imperiosa de descalificar la idoneidad del interlocutor para restablecer el equilibrio narcisista.",
        "impacto_equipo": "Sensación constante de cuestionamiento técnico, empequeñecimiento forzado y fastidio defensivo en el profesional.",
        "perfil_radar": "Expansión aislada y masiva en el vértice de Antagonismo con conservación del control prefrontal ejecutivo."
    },
    "Trastorno Antisocial de la Personalidad (TASP)": {
        "Afecto Negativo": 25, "Desinhibición": 92, "Antagonismo": 95, "Desapego": 30, "Psicoticismo": 25,
        "color": "#A78BFA",
        "semiologia_clasica": "Frialdad afectiva, aplanamiento del remordimiento, instrumentalización del semejante y transgresión repetida de normas (Schneider / Cleckley).",
        "mecanismo_defensa": "Paso al acto coactivo (acting out) y racionalización cínica de la agresión.",
        "vivencia_subjetiva": "El vínculo asistencial o social es concebido como una correlación de fuerzas a someter en pos de un beneficio concreto o dominancia.",
        "impacto_equipo": "Activación somática de alerta por agresión física real, cautela extrema y contratransferencia punitiva.",
        "perfil_radar": "Conjunción de Antagonismo y Desinhibición motora extrema con muy bajo componente de sufrimiento afectivo interno."
    },
    "Trastorno Histriónico de la Personalidad (THP)": {
        "Afecto Negativo": 80, "Desinhibición": 70, "Antagonismo": 55, "Desapego": 10, "Psicoticismo": 30,
        "color": "#22D3EE",
        "semiologia_clasica": "Expresión emocional llamativa pero volátil, sugestibilidad profunda y erotización reactiva de los intercambios (Jaspers / Janet).",
        "mecanismo_defensa": "Disociación, somatización conversiva y dramatización comunicacional.",
        "vivencia_subjetiva": "Sensación de invisibilidad o vacío existencial si no se captura de inmediato la atención del semejante.",
        "impacto_equipo": "Atracción e interés clínico inicial, que rápidamente vira a saturación vincular por demanda incesante de confirmación.",
        "perfil_radar": "Mínimo valor de Desapego (búsqueda imperiosa de proximidad) acoplado a reactividad emocional sin fragmentación del examen de realidad."
    }
}

p_actual = perfiles_hitop[trastorno_foco]

# ==============================================================================
# MODELO CUANTITATIVO DE CIRCUITOS Y FISIOPATOLOGÍA
# Basado en conectividad funcional fMRI (Ruocco et al., 2016; Arnsten, 2009)
# ==============================================================================
# 1. Capacidad inhibitoria prefrontal basal (dlPFC / vlPFC / OFC)
acoplamiento_base = 75.0 if "Narcisista" in trastorno_foco else (45.0 if "Límite" in trastorno_foco else 60.0)

# El estrés relacional agudo (escala SUDS) desacopla el control prefrontal mediante cascada noradrenérgica/dopaminérgica (Arnsten, Nature Rev Neurosci 2009)
factor_caida_estres = (severidad_estres / 100.0) * 0.70
acoplamiento_frontal = float(np.clip(acoplamiento_base * (1.0 - factor_caida_estres), 8.0, 95.0))

# 2. Reactividad córtico-límbica (Amígdala basolateral / Corteza insular anterior)
actividad_amigdala = float(np.clip((100.0 - acoplamiento_frontal) * (p_actual["Afecto Negativo"] / 100.0) * 1.25, 12.0, 100.0))

# 3. Farmacodinamia cuantitativa (Afinidades teóricas Ki según Stephen Stahl y guías APA/NICE)
farmaco_datos = {
    "Intervención Verbal de Encuadre (Sin psicofármacos)": {
        "d2": 0, "5ht2a": 0, "gaba": 0, "nav": 0, "riesgo_desin": 0, "riesgo_acatisia": 0, 
        "tipo": "Intervención No Farmacológica (Regulación Psicofisiológica)",
        "mecanismo": "Activación deliberada de corteza prefrontal dorsolateral mediante validación y sostén del encuadre, sin interferencia iatrogénica."
    },
    "Clonazepam (2 mg Vía Oral)": {
        "d2": 0, "5ht2a": 0, "gaba": 90, "nav": 0, "riesgo_desin": 85, "riesgo_acatisia": 0, 
        "tipo": "Modulador Alostérico Positivo GABAA de Alta Potencia",
        "mecanismo": "Unión subunidad alfa-1/alfa-2 de receptores GABAA. Provoca desinhibición paradójica en pacientes con freno prefrontal deficiente al silenciar interneuronas inhibitorias orbitofrontales."
    },
    "Lorazepam (2 mg Sublingual)": {
        "d2": 0, "5ht2a": 0, "gaba": 85, "nav": 0, "riesgo_desin": 78, "riesgo_acatisia": 0, 
        "tipo": "Modulador Alostérico Positivo GABAA de Alta Potencia",
        "mecanismo": "Rápida penetración en SNC por vía sublingual. Similar perfil a clonazepam: alto riesgo de supresión del control inhibitorio prefrontal consciente."
    },
    "Haloperidol (5 mg Intramuscular)": {
        "d2": 88, "5ht2a": 12, "gaba": 0, "nav": 0, "riesgo_desin": 5, "riesgo_acatisia": 85, 
        "tipo": "Antagonista Dopaminérgico D2 Incisivo de Primera Generación",
        "mecanismo": "Bloqueo D2 > 80% en vía nigroestriatal. Elevado riesgo de acatisia e inquietud motora aguda, habitualmente confundida en crisis con agravamiento conductual."
    },
    "Quetiapina (50 mg Vía Oral)": {
        "d2": 25, "5ht2a": 65, "gaba": 0, "nav": 0, "riesgo_desin": 10, "riesgo_acatisia": 5, 
        "tipo": "Antipsicótico Atípico / Antagonista H1 y 5-HT2A",
        "mecanismo": "Dosis baja: acción eminentemente antihistamínica H1 y bloqueante alfa-1 adrenérgico; sedación rápida sin supresión del freno cortical ni rigidez extrapiramidal."
    },
    "Aripiprazol (5 mg Vía Oral)": {
        "d2": 72, "5ht2a": 60, "gaba": 0, "nav": 0, "riesgo_desin": 8, "riesgo_acatisia": 20, 
        "tipo": "Agonista Parcial D2 / Antagonista 5-HT2A",
        "mecanismo": "Modulador dopaminérgico con actividad intrínseca del ~30%. Estabiliza la transmisión dopaminérgica sin causar sedación profunda ni aplanamiento afectivo."
    },
    "Lamotrigina (100 mg Vía Oral - Mantenimiento basal previo)": {
        "d2": 0, "5ht2a": 0, "gaba": 0, "nav": 68, "riesgo_desin": 0, "riesgo_acatisia": 0, 
        "tipo": "Inhibidor de Canales de Sodio Voltaje-Dependientes / Modulador Glutamatérgico",
        "mecanismo": "Disminución de liberación presináptica de glutamato. Fármaco de mantenimiento profiláctico crónico, no utilizable para rescate en crisis agudas por riesgo de síndrome de Stevens-Johnson."
    }
}

f_eval = farmaco_datos[farmaco_1]

# 4. Índice de Vulnerabilidad Asistencial (IVA)
# Ponderación basada en variables objetivas:
pts_estres = severidad_estres * 0.35
pts_fenotipo = (p_actual["Desinhibición"] * 0.35) if ("Límite" in trastorno_foco or "Antisocial" in trastorno_foco) else 20.0
pts_red = 10.0 if "Presente" in soporte_red else 30.0
pts_iatrogenia = (f_eval["riesgo_desin"] * 0.20)
iva_total = float(np.clip(pts_estres + pts_fenotipo + pts_red + pts_iatrogenia, 10.0, 100.0))

# ==============================================================================
# ENCABEZADO Y PANELES CUANTITATIVOS
# ==============================================================================
st.markdown("## Evaluación dimensional del Clúster B: Dinámica vincular y farmacología")
st.markdown("<p style='color: #94A3B8; font-size: 0.95rem; margin-top: -0.4rem;'><b>Ateneo de Psiquiatría</b> | Modelo Integrado HiTOP / DSM-5 Sección III y Dinámica de Circuitos</p>", unsafe_allow_html=True)

col_m1, col_m2, col_m3, col_m4 = st.columns(4)

with col_m1:
    st.metric(
        label="Control Prefrontal Inhibitorio",
        value=f"{acoplamiento_frontal:.1f} %",
        delta=f"{-factor_caida_estres*100:.1f} % por Tensión Aguda",
        delta_color="inverse",
        help="Índice de acoplamiento funcional de cortezas prefrontales (dlPFC/vlPFC) sobre núcleos subcorticales. Modela la capacidad de inhibir impulsos motores y afectivos bajo estrés."
    )
    st.caption("Freno voluntario sobre el impulso motor.")

with col_m2:
    st.metric(
        label="Reactividad Amigdalina / Ínsula",
        value=f"{actividad_amigdala:.1f} %",
        delta="Alarma Disparada" if actividad_amigdala > 65 else "Línea de Base",
        delta_color="inverse" if actividad_amigdala > 65 else "normal",
        help="Intensidad de descarga de la amígdala e ínsula anterior ante señales de amenaza relacional, humillación o rechazo."
    )
    st.caption("Sensibilidad límbica de alarma.")

with col_m3:
    st.metric(
        label="Riesgo Desinhibición Paradójica",
        value=f"{f_eval['riesgo_desin']} %",
        delta="Alerta Iatrogénica" if f_eval['riesgo_desin'] > 50 else "Seguro / Neutro",
        delta_color="inverse" if f_eval['riesgo_desin'] > 50 else "normal",
        help="Probabilidad calculada de incremento en agresividad motriz o desinhibición verbal por depresión de interneuronas corticales inhibitorias con benzodiacepinas."
    )
    st.caption(f"Fármaco: {farmaco_1.split('(')[0]}")

with col_m4:
    color_iva = "inverse" if iva_total >= 70.0 else "normal"
    st.metric(
        label="Vulnerabilidad en Crisis (IVA)",
        value=f"{iva_total:.1f} %",
        delta="Alto Riesgo de Paso al Acto" if iva_total >= 70.0 else "Manejo Ambulatorio Viable",
        delta_color=color_iva,
        help="Índice cuantitativo que integra tensión afectiva actual (SUDS), rasgo desinhibitorio basal, contención vincular real e impacto farmacológico."
    )
    st.caption("Ponderación multidimensional en crisis.")

# Explicador metodológico de los porcentajes para fundamentación en ateneo
with st.expander("Fundamentación metodológica y origen de los índices porcentuales"):
    st.markdown("""
    **¿Cómo se calculan y argumentan estos cuatro porcentajes ante el equipo asistencial?**
    
    1. **Control Prefrontal Inhibitorio (%):** Representa la fracción de integridad funcional de la corteza prefrontal dorsolateral y ventrolateral (*dlPFC/vlPFC*). El valor de referencia basal surge de los perfiles de conectividad frontolímbica en reposo (*Ruocco et al., Biol Psychiatry 2016*). Al incrementarse la tensión subjetiva (*SUDS*), el modelo aplica una atenuación exponencial basada en el mecanismo de saturación catecolaminérgica prefrontal descrito por *Arnsten (Nature Rev Neurosci 2009)*: a mayor distrés, menor señal prefrontal inhibitoria.
    2. **Reactividad Amigdalina / Ínsula (%):** Expresa el grado de hiperactivación límbica ante señales sociales. Se calcula matemáticamente de forma inversamente proporcional al freno prefrontal y ponderada por el rasgo dimensional de *Afecto Negativo* basal de cada paciente (*Schulze et al., Am J Psychiatry 2016*).
    3. **Riesgo de Desinhibición Paradójica (%):** Refleja la probabilidad clínica observada de pérdida del autocontrol tras benzodiacepinas en pacientes con hipoactividad orbitofrontal de base. Los valores concuerdan con los reportes toxicológicos y las advertencias formales de las guías británicas *NICE CG78* y *APA*.
    4. **Índice de Vulnerabilidad Asistencial (IVA %):** Ponderación algorítmica: `0.35 × SUDS + 0.35 × Rasgo Desinhibitorio + Factor Red Vincular (10 o 30) + 0.20 × Riesgo Farmacológico`. Permite estratificar el riesgo global de paso al acto sin depender de etiquetas categoriales estáticas.
    """)

st.markdown("<div style='height: 1px; background: rgba(255,255,255,0.08); margin: 1.2rem 0;'></div>", unsafe_allow_html=True)

# ==============================================================================
# PESTAÑAS ACADÉMICAS
# ==============================================================================
tab_radar, tab_clinica, tab_neuro, tab_farma, tab_biblio = st.tabs([
    "1. Polígono Dimensional (HiTOP / AMPD)",
    "2. Dinámica Relacional y Fenomenología",
    "3. Evidencia y Neuroimagen Funcional",
    "4. Psicofarmacología de Receptores",
    "5. Marco Epistemológico y Justificación de Variables"
])

# ------------------------------------------------------------------------------
# PESTAÑA 1: RADAR DIMENSIONAL (HiTOP / AMPD)
# ------------------------------------------------------------------------------
with tab_radar:
    st.subheader("Huella Dimensional Comparativa de los 4 Fenotipos del Clúster B")
    st.caption("Taxonomía Jerárquica de la Psicopatología (HiTOP) y Modelo Alternativo del DSM-5 (AMPD, Sección III).")
    
    col_rad_izq, col_rad_der = st.columns([1.1, 1])
    
    # Simulación de reactividad dinámica bajo estrés actual
    val_af_din = float(np.clip(p_actual["Afecto Negativo"] * (1.0 + (severidad_estres / 300.0)), 0, 100))
    val_des_din = float(np.clip(p_actual["Desinhibición"] * (1.0 + (severidad_estres / 400.0)), 0, 100))
    val_ant_din = float(p_actual["Antagonismo"])
    val_desap_din = float(p_actual["Desapego"])
    val_psi_din = float(np.clip(p_actual["Psicoticismo"] + (severidad_estres * 0.25), 0, 100))
    
    valores_dinamicos = {
        "Afecto Negativo": val_af_din,
        "Desinhibición": val_des_din,
        "Antagonismo": val_ant_din,
        "Desapego": val_desap_din,
        "Psicoticismo": val_psi_din
    }
    
    categorias = ["Afecto Negativo", "Desinhibición", "Antagonismo", "Desapego", "Psicoticismo"]
    
    with col_rad_izq:
        fig_radar = go.Figure()
        
        for nombre, datos in perfiles_hitop.items():
            vals = [datos[c] for c in categorias]
            vals.append(vals[0])
            es_foco = (nombre == trastorno_foco)
            fig_radar.add_trace(go.Scatterpolar(
                r=vals,
                theta=categorias + [categorias[0]],
                name=nombre.split()[1],
                line=dict(
                    color=datos["color"],
                    width=3.5 if es_foco else 1.2,
                    dash="solid" if es_foco else "dot"
                ),
                fill="toself" if es_foco else "none",
                opacity=0.30 if es_foco else 0.08
            ))
            
        valores_paciente = [val_af_din, val_des_din, val_ant_din, val_desap_din, val_psi_din]
        valores_paciente.append(valores_paciente[0])
        fig_radar.add_trace(go.Scatterpolar(
            r=valores_paciente,
            theta=categorias + [categorias[0]],
            name="Estado Reactivo (Estrés Actual)",
            line=dict(color="#38BDF8", width=2.5, dash="dash"),
            fill="none"
        ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    gridcolor="rgba(255, 255, 255, 0.08)",
                    linecolor="rgba(255, 255, 255, 0.08)",
                    tickfont=dict(color="#64748B", size=9, family="Inter")
                ),
                angularaxis=dict(
                    gridcolor="rgba(255, 255, 255, 0.08)",
                    linecolor="rgba(255, 255, 255, 0.08)",
                    tickfont=dict(color="#F1F5F9", size=11, family="Inter")
                ),
                bgcolor="rgba(10, 15, 29, 0.8)"
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.30,
                xanchor="center",
                x=0.5,
                font=dict(family="Inter", size=11, color="#94A3B8")
            ),
            margin=dict(l=35, r=35, t=15, b=55),
            height=420
        )
        st.plotly_chart(fig_radar, use_container_width=True, key="fig_radar_hitop")
        
    with col_rad_der:
        st.markdown(f"#### Perfil Clínico Seleccionado: **{trastorno_foco}**")
        st.markdown(f"**Semiología descriptiva clásica:** {p_actual['semiologia_clasica']}")
        st.markdown(f"**Lectura geométrica del radar:** {p_actual['perfil_radar']}")
        st.markdown("**Dominios Cuantitativos (Basal vs Reactivo bajo Estrés):**")
        
        for c in categorias:
            val_basal = p_actual[c]
            val_reactivo = valores_dinamicos[c]
            delta_val = val_reactivo - val_basal
            texto_delta = f" (+{delta_val:.1f} reactivo)" if delta_val > 0.1 else ""
            st.write(f"- **{c}:** {val_reactivo:.1f}/100 <span style='color:#F87171; font-size:0.85rem;'>{texto_delta}</span>", unsafe_allow_html=True)
            st.progress(val_reactivo / 100.0)
            
    # Sección pedagógica y detallada sobre qué significa cada dimensión (AMPD / PID-5)
    st.markdown("---")
    st.markdown("#### Definición Epistemológica de los 5 Dominios Dimensionales (PID-5 / HiTOP)")
    
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.markdown("""
        * **1. Afecto Negativo (vs. Estabilidad Emocional):**  
          Vivencia frecuente e intensa de un amplio espectro de emociones aversivas: labilidad emocional, ansiedad somática, suspicacia, hostilidad y terror al desamparo. En el Clúster B, constituye el núcleo fisiopatológico del paciente con **TLP**, generando la necesidad urgente de descargar motrizmente la tensión para apagar la vivencia de dolor interno.
          
        * **2. Desinhibición (vs. Meticulosidad / Escrupulosidad):**  
          Orientación hacia la gratificación inmediata, impulsividad motriz y cognitiva sin deliberación de consecuencias futuras, búsqueda de sensaciones de riesgo y dificultad extrema para sostener planes a largo plazo. Es compartida en grado máximo por el **TLP** (urgencia afectiva) y el **TASP** (búsqueda de estimulación o beneficio instrumental).
          
        * **3. Antagonismo (vs. Amabilidad / Empatía):**  
          Comportamientos que sitúan sistemáticamente al individuo en conflicto con los demás: grandiosidad, expectativas de trato privilegiado, desdén, insensibilidad hacia el sufrimiento ajeno y manipulación interpersonal. Define el polo cardinal del **TNP** y del **TASP**.
        """)
    with col_d2:
        st.markdown("""
        * **4. Desapego (vs. Extraversión / Afiliación):**  
          Distanciamiento activo de relaciones interpersonales, evitación del contacto afectivo estrecho y anhedonia social. El Clúster B se caracteriza por mostrar niveles **bajos o moderadamente bajos** de desapego, especialmente en el **THP** y el **TLP**, cuya vivencia depende desesperadamente del feedback, mirada y presencia física del semejante.
          
        * **5. Psicoticismo (vs. Lucidez / Racionalidad):**  
          Excentricidad, pensamientos inusuales y desregulación perceptual transitoria estado-dependiente. En el **TLP**, este dominio se eleva exclusivamente bajo microepisodios de descompensación aguda (despersonalización, desrealización, ideas paranoides transitorias no sistematizadas), remitiendo rápidamente cuando la relación se estabiliza.
        """)

# ------------------------------------------------------------------------------
# PESTAÑA 2: DINÁMICA RELACIONAL Y FENOMENOLOGÍA
# ------------------------------------------------------------------------------
with tab_clinica:
    st.subheader("La Escena Vincular: Fenomenología ante el Estresor Interpersonal")
    st.markdown(f"**Estresor Evaluado:** `{estresor_tipo}` | **Nivel de Distrés (SUDS):** `{severidad_estres}/100`")
    
    # Justificación de los 4 estresores para que Franco tenga el argumento completo
    with st.expander("¿Por qué se seleccionaron estos 4 estresores interpersonales? (Fundamento Teórico)"):
        st.markdown("""
        Los cuatro estresores modelados no fueron elegidos al azar ni se limitan únicamente a un ámbito cerrado de guardia hospitalaria; representan las cuatro **vulnerabilidades relacionales nucleares** descritas en la literatura clínica contemporánea (Gunderson, 2011; Linehan, 1993; Bateman & Fonagy, 2004):
        
        1. **Fijación de Límites o Negativa Externa:** Activa la vivencia inmediata de castigo, rechazo o invalidación. En la vida cotidiana equivale a un 'no' de una pareja o jefe; en el sistema asistencial, a la negativa de una prescripción o internación injustificada.
        2. **Distanciamiento Vincular / Vivencia de Abandono:** Es el interruptor neurobiológico del dolor social y la angustia de aniquilamiento (Eisenberger, 2003). Se observa ante rupturas, discusiones familiares o la ausencia física temporal del referente.
        3. **Confrontación de la Realidad / Señalamiento de Inconsistencias:** Desencadena la herida narcisista por exposición de fallas, activando furia defensiva en personalidades con Yo grandioso compensatorio (Kernberg / Kohut).
        4. **Demora Asistencial o Dilación del Entorno:** La espera forzada o la falta de gratificación inmediata es decodificada por el sistema de apego desorganizado como desprecio activo o desamparo total.
        """)
        
    c_tlp, c_tnp, c_tasp, c_thp = st.columns(4)
    
    with c_tlp:
        st.markdown(f"""
        <div class="card-clinica">
            <h4 style="color:#F87171; margin-top:0;">Trastorno Límite</h4>
            <p style="color:#94A3B8; font-size:0.83rem; margin-bottom:3px;"><b>Vivencia Subjetiva:</b></p>
            <p style="color:#E2E8F0; font-size:0.86rem; font-style:italic;">«{perfiles_hitop['Trastorno Límite de la Personalidad (TLP)']['vivencia_subjetiva']}»</p>
            <p style="color:#94A3B8; font-size:0.83rem; margin-bottom:3px;"><b>Mecanismo Defensivo:</b></p>
            <p style="color:#CBD5E1; font-size:0.86rem;">{perfiles_hitop['Trastorno Límite de la Personalidad (TLP)']['mecanismo_defensa']}</p>
            <p style="color:#94A3B8; font-size:0.83rem; margin-bottom:3px;"><b>Conducta Manifiesta:</b></p>
            <p style="color:#FCA5A5; font-size:0.86rem;">Amenaza autolesiva o corte superficial para modular homeostáticamente el dolor psíquico abrumador.</p>
            <p style="color:#94A3B8; font-size:0.83rem; margin-bottom:3px;"><b>Impacto Contratransferencial:</b></p>
            <p style="color:#FCD34D; font-size:0.86rem;">{perfiles_hitop['Trastorno Límite de la Personalidad (TLP)']['impacto_equipo']}</p>
        </div>
        """, unsafe_allow_html=True)
        
    with c_tnp:
        st.markdown(f"""
        <div class="card-clinica">
            <h4 style="color:#FBBF24; margin-top:0;">Trastorno Narcisista</h4>
            <p style="color:#94A3B8; font-size:0.83rem; margin-bottom:3px;"><b>Vivencia Subjetiva:</b></p>
            <p style="color:#E2E8F0; font-size:0.86rem; font-style:italic;">«{perfiles_hitop['Trastorno Narcisista de la Personalidad (TNP)']['vivencia_subjetiva']}»</p>
            <p style="color:#94A3B8; font-size:0.83rem; margin-bottom:3px;"><b>Mecanismo Defensivo:</b></p>
            <p style="color:#CBD5E1; font-size:0.86rem;">{perfiles_hitop['Trastorno Narcisista de la Personalidad (TNP)']['mecanismo_defensa']}</p>
            <p style="color:#94A3B8; font-size:0.83rem; margin-bottom:3px;"><b>Conducta Manifiesta:</b></p>
            <p style="color:#FDE68A; font-size:0.86rem;">Descalificación técnica directa, acusaciones de negligencia o reclamos formales como defensa ante la humillación.</p>
            <p style="color:#94A3B8; font-size:0.83rem; margin-bottom:3px;"><b>Impacto Contratransferencial:</b></p>
            <p style="color:#FCD34D; font-size:0.86rem;">{perfiles_hitop['Trastorno Narcisista de la Personalidad (TNP)']['impacto_equipo']}</p>
        </div>
        """, unsafe_allow_html=True)
        
    with c_tasp:
        st.markdown(f"""
        <div class="card-clinica">
            <h4 style="color:#A78BFA; margin-top:0;">Trastorno Antisocial</h4>
            <p style="color:#94A3B8; font-size:0.83rem; margin-bottom:3px;"><b>Vivencia Subjetiva:</b></p>
            <p style="color:#E2E8F0; font-size:0.86rem; font-style:italic;">«{perfiles_hitop['Trastorno Antisocial de la Personalidad (TASP)']['vivencia_subjetiva']}»</p>
            <p style="color:#94A3B8; font-size:0.83rem; margin-bottom:3px;"><b>Mecanismo Defensivo:</b></p>
            <p style="color:#CBD5E1; font-size:0.86rem;">{perfiles_hitop['Trastorno Antisocial de la Personalidad (TASP)']['mecanismo_defensa']}</p>
            <p style="color:#94A3B8; font-size:0.83rem; margin-bottom:3px;"><b>Conducta Manifiesta:</b></p>
            <p style="color:#DDD6FE; font-size:0.86rem;">Coacción, intimidación o desafío frontal a las normas para doblegar al interlocutor.</p>
            <p style="color:#94A3B8; font-size:0.83rem; margin-bottom:3px;"><b>Impacto Contratransferencial:</b></p>
            <p style="color:#FCD34D; font-size:0.86rem;">{perfiles_hitop['Trastorno Antisocial de la Personalidad (TASP)']['impacto_equipo']}</p>
        </div>
        """, unsafe_allow_html=True)
        
    with c_thp:
        st.markdown(f"""
        <div class="card-clinica">
            <h4 style="color:#22D3EE; margin-top:0;">Trastorno Histriónico</h4>
            <p style="color:#94A3B8; font-size:0.83rem; margin-bottom:3px;"><b>Vivencia Subjetiva:</b></p>
            <p style="color:#E2E8F0; font-size:0.86rem; font-style:italic;">«{perfiles_hitop['Trastorno Histriónico de la Personalidad (THP)']['vivencia_subjetiva']}»</p>
            <p style="color:#94A3B8; font-size:0.83rem; margin-bottom:3px;"><b>Mecanismo Defensivo:</b></p>
            <p style="color:#CBD5E1; font-size:0.86rem;">{perfiles_hitop['Trastorno Histriónico de la Personalidad (THP)']['mecanismo_defensa']}</p>
            <p style="color:#94A3B8; font-size:0.83rem; margin-bottom:3px;"><b>Conducta Manifiesta:</b></p>
            <p style="color:#A5F3FC; font-size:0.86rem;">Dramatización somática aguda, pseudodesmayos psicógenos o crisis de hiperventilación reactiva.</p>
            <p style="color:#94A3B8; font-size:0.83rem; margin-bottom:3px;"><b>Impacto Contratransferencial:</b></p>
            <p style="color:#FCD34D; font-size:0.86rem;">{perfiles_hitop['Trastorno Histriónico de la Personalidad (THP)']['impacto_equipo']}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 1px; background: rgba(255,255,255,0.08); margin: 1.2rem 0;'></div>", unsafe_allow_html=True)
    st.markdown("#### Pautas de Contención Verbal y Sostenimiento del Encuadre Asistencial")
    
    col_rec_izq, col_rec_der = st.columns(2)
    with col_rec_izq:
        st.error("""
        **Intervención Desaconsejada (Escala la Disrrupción Afectiva):**
        
        *Confrontación lógica directa, desacreditación del síntoma o amenaza punitiva:*  
        «Cálmese, que lo suyo no reviste ninguna gravedad» o «Si sigue gritando tendré que pedir que lo retiren de la sala».
        
        * **Por qué falla:** En el paciente con TLP, invalida la experiencia emocional interna, interpretándose como rechazo activo y acelerando el paso al acto impulsivo (*Linehan, 1993*). En el paciente con TNP, propina una herida directa a su estatus, detonando furia narcisista compensatoria.
        """)
    with col_rec_der:
        st.success("""
        **Intervención Basada en Evidencia (Desactiva la Reactividad Límbica):**
        
        *Validación del afecto con sostenimiento irrestricto del límite estructural:*  
        «Entiendo perfectamente el nivel de angustia y sufrimiento que esta situación le genera; es comprensible que se sienta desbordado/a. Sin embargo, no podemos acceder a esa indicación porque sería perjudicial para su salud. Vamos a evaluar juntos qué opciones terapéuticas seguras podemos coordinar».
        
        * **Fundamento empírico:** Desarrollado y validado en el manual de Terapia Dialéctico-Conductual (*Marsha Linehan, Cognitive-Behavioral Treatment of Borderline Personality Disorder, 1993*) y Terapia Basada en la Mentalización (*Anthony Bateman & Peter Fonagy, Psychotherapy for Borderline Personality Disorder: MBT, Oxford University Press, 2004*). La validación empática desactiva la señal de alarma amigdalina, permitiendo que la corteza prefrontal retome el control ejecutivo.
        """)

# ------------------------------------------------------------------------------
# PESTAÑA 3: EVIDENCIA CIENTÍFICA Y NEUROIMAGEN
# ------------------------------------------------------------------------------
with tab_neuro:
    st.subheader("Evidencia Neurobiológica Rigurosa y Hallazgos Contraintuitivos")
    st.caption("Meta-análisis de fMRI, DTI y estudios longitudinales multicéntricos:")
    
    col_ev1, col_ev2 = st.columns(2)
    
    with col_ev1:
        st.markdown("""
        <div class="card-evidencia">
            <span class="badge-estudio">BIOL PSYCHIATRY 2016 | META-ANÁLISIS fMRI</span>
            <h4 style="color: #38BDF8; margin-top:0;">1. Modelo de Desacoplamiento Corticolímbico (Ruocco et al., 2016)</h4>
            <p style="color: #CBD5E1; font-size: 0.88rem;">
            El meta-análisis neurofuncional de activación (ALE) conducido por Anthony C. Ruocco y Donald Carcone en <i>Biological Psychiatry</i> demostró que frente al procesamiento de estímulos afectivos negativos, los pacientes con TLP presentan de forma consistente:
            </p>
            <ul style="color: #94A3B8; font-size: 0.86rem; padding-left: 20px;">
                <li><b>Hipoactivación marcada</b> de la corteza prefrontal dorsolateral (dlPFC) bilateral y corteza cingulada anterior dorsal.</li>
                <li><b>Hiperactivación sostenida</b> de la amígdala izquierda y corteza insular anterior.</li>
            </ul>
            <p style="color: #E2E8F0; font-size: 0.85rem; font-style: italic;">
            Conclusión neurosemiológica: El desborde del paciente no es 'manipulación deliberada', sino una falla biológica en el freno cortical inhibitorio frente a estímulos afectivos.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="card-evidencia">
            <span class="badge-estudio">BIOL PSYCHIATRY 2009 | TEST DE RMET</span>
            <h4 style="color: #38BDF8; margin-top:0;">2. La Paradoja de la Detección Emocional (Fertuck et al., 2009)</h4>
            <p style="color: #CBD5E1; font-size: 0.88rem;">
            En el estudio experimental diseñado por Eric A. Fertuck y colaboradores (Universidad de Columbia), mediante el <i>Reading the Mind in the Eyes Test</i>, se refutó el mito de que el paciente límite carece de empatía:
            </p>
            <ul style="color: #94A3B8; font-size: 0.86rem; padding-left: 20px;">
                <li>Los individuos con TLP mostraron una capacidad <b>estadísticamente superior</b> a los controles sanos para discriminar microexpresiones afectivas sutiles en la mirada ajena.</li>
                <li><b>El sesgo patológico:</b> Tienen una agudeza perceptual hiperempática inmediata, pero presentan una disfunción en la corteza prefrontal medial para atribuir la intención: decodifican la neutralidad o el cansancio del interlocutor como desprecio u hostilidad inminente.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    with col_ev2:
        st.markdown("""
        <div class="card-evidencia">
            <span class="badge-estudio">AM J PSYCHIATRY 2016 | SEGUIMIENTO LONGITUDINAL A 24 AÑOS</span>
            <h4 style="color: #38BDF8; margin-top:0;">3. Evolución Natural y Tasa de Remisión (Estudio MSBPD, Zanarini et al.)</h4>
            <p style="color: #CBD5E1; font-size: 0.88rem;">
            El <i>McLean Study of Adult Development</i> liderado por Mary C. Zanarini constituye el estudio de cohorte prospectivo más extenso y riguroso de la psiquiatría moderna sobre la evolución del TLP:
            </p>
            <ul style="color: #94A3B8; font-size: 0.86rem; padding-left: 20px;">
                <li>A los 10 años de seguimiento prospectivo, <b>más del 85% de los pacientes remitieron formalmente</b> de los criterios categoriales del DSM.</li>
                <li>A los 24 años, la remisión sintomática sostenida superó el <b>90%</b>.</li>
                <li><b>Implicancia clínica asistencial:</b> Los síntomas impulsivos agudos (autolesiones, intentos de suicidio, furia) maduran y disminuyen biológicamente con la edad. El foco terapéutico a largo plazo radica en la rehabilitación vincular y laboral.
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="card-evidencia">
            <span class="badge-estudio">TENSOR DE DIFUSIÓN (DTI) | CONECTÓMICA ESTRUCTURAL</span>
            <h4 style="color: #38BDF8; margin-top:0;">4. Microestructura del Fascículo Uncinado y Cíngulo</h4>
            <p style="color: #CBD5E1; font-size: 0.88rem;">
            Múltiples estudios de tractografía por resonancia magnética con tensor de difusión (DTI) han demostrado una reducción objetiva de la <b>anisotropía fraccional (FA)</b> en el <b>fascículo uncinado</b>:
            </p>
            <ul style="color: #94A3B8; font-size: 0.86rem; padding-left: 20px;">
                <li>El fascículo uncinado es el principal tracto de sustancia blanca que conecta monosinápticamente la corteza orbitofrontal y prefrontal ventrolateral con el complejo nuclear amigdalino.</li>
                <li>Una menor integridad microestructural en este tracto explica por qué la orden prefrontal de freno inhibitorio llega atenuada o con retraso frente a picos agudos de hiperactivación límbica.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# PESTAÑA 4: PSICOFARMACOLOGÍA DE RECEPTORES
# ------------------------------------------------------------------------------
with tab_farma:
    st.subheader("Psicofarmacología Traslacional y Ocupación Teórica de Receptores")
    st.caption("Perfil de afinidad de unión según constantes Ki y guías de práctica clínica (Stahl's Essential Psychopharmacology / NICE CG78 / APA):")
    
    col_far_l, col_far_r = st.columns([1, 1])
    
    with col_far_l:
        st.markdown(f"#### Molécula Seleccionada: `{farmaco_1}`")
        st.markdown(f"**Familia Terapéutica:** {f_eval['tipo']}")
        st.info(f"**Mecanismo de Acción Neurofuncional:** " + f_eval["mecanismo"])
        
        d2_val = f_eval['d2']
        ht2a_val = f_eval['5ht2a']
        gaba_val = f_eval['gaba']
        nav_val = f_eval['nav']
        
        st.markdown("**Estimación de Ocupación / Modulación de Sitios de Unión en SNC:**")
        st.write(f"- Receptores Dopaminérgicos D2: {d2_val}%")
        st.progress(d2_val / 100.0)
        st.write(f"- Receptores Serotoninérgicos 5-HT2A: {ht2a_val}%")
        st.progress(ht2a_val / 100.0)
        st.write(f"- Complejo Alostérico del Receptor GABAA: {gaba_val}%")
        st.progress(gaba_val / 100.0)
        st.write(f"- Bloqueo de Canales de Sodio Voltaje-Dependientes Nav: {nav_val}%")
        st.progress(nav_val / 100.0)
        
    with col_far_r:
        st.markdown("#### Análisis de Riesgo Terapéutico e Iatrogenia Farmacológica")
        
        if f_eval["riesgo_desin"] > 50:
            st.error(f"""
            **ALERTA DE DESINHIBICIÓN PARADÓJICA (Riesgo Estimado: {f_eval['riesgo_desin']}%):**
            
            * **Fisiopatología:** Las benzodiacepinas de alta potencia potencian el tono GABAérgico de forma indiscriminada. En personas con hipofrontalidad basal, deprimen selectivamente las interneuronas de la corteza orbitofrontal (*OFC*), suprimiendo el último vestigio de freno consciente sobre la amígdala.
            * **Manifestación clínica:** Desinhibición motora, escalada de agresividad verbal y facilitación del paso al acto impulsivo o suicida.
            * **Criterio de Guías (NICE CG78 / APA):** Están formalmente desaconsejadas para el manejo rutinario o de rescate en crisis de desregulación de la personalidad.
            """)
        elif f_eval["riesgo_acatisia"] > 50:
            st.error(f"""
            **ALERTA DE ACATISIA AGUDA (Riesgo Estimado: {f_eval['riesgo_acatisia']}%):**
            
            * **Fisiopatología:** El bloqueo potente de receptores dopaminérgicos D2 (> 80% en la vía nigroestriatal) por antipsicóticos típicos de alta potencia induce acatisia aguda.
            * **Error asistencial común:** En el marco de una crisis de guardia, la inquietud motora displacentera y la angustia inducida por la acatisia son erróneamente interpretadas como mayor agitación de base del paciente, llevando al error iatrogénico de sobreprescribir dosis adicionales del antipsicótico.
            """)
        elif "Lamotrigina" in farmaco_1:
            st.warning("""
            **CONSIDERACIÓN ESPECÍFICA SOBRE LAMOTRIGINA:**
            
            * **Tiempo de latencia:** Carece totalmente de indicación en agudo o en rescate de guardia; requiere una titulación ascendente extremadamente lenta a lo largo de 6 a 8 semanas para evitar el desprendimiento epidérmico del síndrome de Stevens-Johnson.
            * **Función en el modelo:** Se evalúa exclusivamente en pacientes que ya la reciben crónicamente de base, donde ejerce modulación del tono glutamatérgico y estabilización afectiva intercrisis.
            """)
        elif "Quetiapina" in farmaco_1:
            st.success("""
            **PERFIL SEDATIVO HISTAMINÉRGICO CONTROLADO:**
            
            A dosis de 25-50 mg, la quetiapina actúa prácticamente como un antihistamínico H1 y alfa-1 adrenérgico puro (ocupación D2 < 30%). Proporciona inducción del reposo sin riesgo extrapiramidal y sin la desinhibición frontal característica de las benzodiacepinas.
            """)
        elif "Aripiprazol" in farmaco_1:
            st.success("""
            **ESTABILIZACIÓN MEDIANTE AGONISMO PARCIAL D2:**
            
            El agonismo parcial dopaminérgico y antagonismo 5-HT2A permite modular la reactividad impulsiva sin sedación profunda, evitando la ganancia excesiva de peso y sin el riesgo de desinhibición de las benzodiacepinas.
            """)
        else:
            st.info("""
            **ESTRATEGIA VERBAL EXCLUSIVA:**
            
            Preserva la lucidez cognitiva y la capacidad de autorregulación del paciente. Permite que el proceso de mentalización y validación emocional operen sin interferencia de efectos adversos farmacológicos o somnolencia.
            """)

# ------------------------------------------------------------------------------
# PESTAÑA 5: MARCO EPISTEMOLÓGICO Y JUSTIFICACIÓN
# ------------------------------------------------------------------------------
with tab_biblio:
    st.subheader("Marco Epistemológico: ¿Por qué este Modelo y no el Categorial Tradicional?")
    st.caption("Fundamento teórico que justifica la selección de variables y el diseño computacional de la plataforma:")
    
    col_j1, col_j2 = st.columns(2)
    
    with col_j1:
        st.markdown("#### Justificación Epistemológica del Abordaje Dimensional")
        st.markdown("""
        1. **Superación del Modelo Categorial DSM Clásico:**  
           El enfoque tradicional de categorías cerradas (DSM-IV / DSM-5 Sección II) presenta tres fallas metodológicas documentadas en psiquiatría:
           * **Comorbilidad masiva y espuria:** Más del 60% de los pacientes que cumplen criterios para un trastorno del Clúster B cumplen simultáneamente criterios para otro trastorno de la personalidad.
           * **Heterogeneidad intra-diagnóstica:** Existen 256 combinaciones sintomáticas distintas para alcanzar los criterios diagnósticos del TLP (5 de 9 ítems). Dos pacientes con diagnóstico idéntico pueden compartir únicamente un síntoma.
           * **Cortes arbitrarios:** Una persona con 4 criterios recibe la etiqueta de 'sano' o 'sin diagnóstico', mientras que alguien con 5 es patologizado, a pesar de que su funcionamiento psicosocial sea indistinguible.
           
        2. **Adopción de la Taxonomía HiTOP y DSM-5 Sección III (AMPD):**  
           El modelo dimensional no clasifica personas en casilleros estáticos; evalúa la severidad a lo largo de un espectro continuo (*Afecto Negativo, Desinhibición, Antagonismo, Desapego y Psicoticismo*), capturando con precisión matemática la singularidad de cada paciente.
           
        3. **Integración de Conectómica Funcional Dinámica:**  
           Las conductas impulsivas no son 'defectos morales del carácter', sino manifestaciones estado-dependientes que emergen cuando un estresor vincular específico satura los circuitos frontocorticales inhibitorios.
        """)
        
    with col_j2:
        st.markdown("#### Bibliografía Principal de Referencia (Artículos Completos)")
        st.markdown("""
        * **1. Taxonomía Dimensional HiTOP y Modelo Alternativo DSM-5 (AMPD):**
          * **Krueger RF, Kotov R, Watson D, et al.** (2018). *The Hierarchical Taxonomy of Psychopathology (HiTOP): A dimensional alternative to traditional nosologies.* **World Psychiatry**, 17(3), 282–293.
          * **Skodol AE, Morey LC, Bender DS, et al.** (2015). *The Alternative DSM-5 Model for Personality Disorders: A Review of the Evidence.* **The Lancet Psychiatry**, 2(2), 170–178.
          
        * **2. Conectómica y Neuroimagen Funcional:**
          * **Ruocco AC, Carcone D.** (2016). *A neurobiological model of affective instability in borderline personality disorder.* **Biological Psychiatry**, 79(6), 444–455.
          * **Fertuck EA, Jeklic J, Giles S, et al.** (2009). *Enhanced 'reading the mind in the eyes' in borderline personality disorder compared to healthy controls.* **Biological Psychiatry**, 65(9), 756–762.
          * **Arnsten AFT.** (2009). *Stress signalling pathways that impair prefrontal cortex structure and function.* **Nature Reviews Neuroscience**, 10(6), 410–422.
          
        * **3. Evolución Longitudinal y Psicoterapia:**
          * **Zanarini MC, Frankenburg FR, Reich DB, Fitzmaurice GM.** (2016). *The Course of Borderline Personality Disorder: A 24-Year Follow-up Study of the Course of BPD.* **The American Journal of Psychiatry**, 173(4), 338–347.
          * **Linehan MM.** (1993). *Cognitive-Behavioral Treatment of Borderline Personality Disorder.* Guilford Press, Nueva York.
          * **Bateman AW, Fonagy P.** (2004). *Psychotherapy for Borderline Personality Disorder: Mentalization-Based Treatment.* Oxford University Press.
          
        * **4. Psicofarmacología Basada en Receptores:**
          * **Stahl SM.** (2021). *Stahl's Essential Psychopharmacology: Neuroscientific Basis and Practical Applications.* 5ª edición, Cambridge University Press.
          * **National Institute for Health and Care Excellence (NICE).** (2009). *Borderline personality disorder: recognition and management (Clinical Guideline CG78).* Londres.
        """)
