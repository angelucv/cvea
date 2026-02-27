import streamlit as st

# Logo horizontal principal (letras negras) relativo a esta carpeta
LOGO_URL = "../../assets/logos/Logo-CVEA-horizontal-grande-letrasnegras.png"

CVEA_PRIMARY = "#38666A"
CVEA_DARK = "#1e3d40"
CVEA_LIGHT = "#f5f5f5"


def apply_cvea_theme() -> None:
    """Inyecta estilos básicos con la paleta CVEA y texto oscuro (sin afectar la barra lateral)."""
    st.markdown(
        f"""
<style>
:root {{
  --cvea-primary: {CVEA_PRIMARY};
  --cvea-dark: {CVEA_DARK};
  --cvea-light: {CVEA_LIGHT};
}}

body, .stApp {{
  background-color: white;
  color: #111111;
}}

/* Forzar texto oscuro en el área principal (contenedor central) */
.block-container, .block-container * {{
  color: #111111 !important;
}}

/* Reaplicar color corporativo solo a enlaces del área principal */
.block-container a, .block-container .stMarkdown a {{
  color: var(--cvea-primary) !important;
}}

.stButton>button {{
  background-color: var(--cvea-primary);
  color: white;
  border-radius: 6px;
  border: none;
  padding: 0.4rem 0.9rem;
}}

.stButton>button:hover {{
  background-color: {CVEA_DARK};
}}

.stMetric-label {{
  color: var(--cvea-dark) !important;
  font-weight: 600;
}}

.cvea-header-title {{
  font-size: 1.6rem;
  font-weight: 700;
  color: var(--cvea-dark) !important;
  margin-bottom: 0.15rem;
}}

.cvea-header-subtitle {{
  font-size: 0.95rem;
  color: #444444 !important;
}}
</style>
""",
        unsafe_allow_html=True,
    )


def cvea_header(title: str, subtitle: str | None = None) -> None:
    """Cabecera con logo CVEA, título y subtítulo."""
    apply_cvea_theme()
    col_logo, col_text = st.columns([1, 3])
    with col_logo:
        st.image(LOGO_URL)
    with col_text:
        st.markdown(f"<div class='cvea-header-title'>{title}</div>", unsafe_allow_html=True)
        if subtitle:
            st.markdown(f"<div class='cvea-header-subtitle'>{subtitle}</div>", unsafe_allow_html=True)

