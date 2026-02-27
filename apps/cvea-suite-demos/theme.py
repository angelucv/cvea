import streamlit as st
from pathlib import Path

# Directorio raíz del proyecto (dos niveles arriba de esta carpeta)
ROOT = Path(__file__).resolve().parents[2]

# Logos con ruta absoluta, independiente del directorio donde se ejecute streamlit
LOGO_HORIZONTAL_COLOR = str(ROOT / "assets" / "logos" / "Logo-CVEA-horizontal-grande-letrascolor.png")
LOGO_VERTICAL_WHITE = str(ROOT / "assets" / "logos" / "Logo-CVEA-vertical-fondocolorletrasblancas.png")
LOGO_VERTICAL_W = str(ROOT / "assets" / "logos" / "Logo-CVEA-vertical-w.png")

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

/* Mantener letras blancas en la barra lateral */
.stSidebar, .stSidebar * {{
  color: white !important;
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

.cvea-topbar {{
  background-color: #000000;
  color: white !important;
  padding: 0.35rem 0.9rem;
  font-weight: 600;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}}

.cvea-back {{
  display: inline-block;
  margin-bottom: 0.5rem;
  padding: 0.25rem 0.75rem;
  background-color: #38666A;
  color: white !important;
  border-radius: 4px;
  text-decoration: none;
  font-size: 0.85rem;
}}
</style>
""",
        unsafe_allow_html=True,
    )


def cvea_header(title: str, subtitle: str | None = None) -> None:
    """Cabecera con logo CVEA vertical, título y subtítulo, más logo pequeño en sidebar."""
    apply_cvea_theme()
    # Cinta negra superior con texto
    st.markdown("<div class='cvea-topbar'>CVEA Suite — Demos interactivos</div>", unsafe_allow_html=True)
    # Logo pequeño en sidebar
    st.sidebar.image(LOGO_VERTICAL_W)
    col_logo, col_text = st.columns([1, 3])
    with col_logo:
        st.image(LOGO_VERTICAL_WHITE)
    with col_text:
        st.markdown(f"<div class='cvea-header-title'>{title}</div>", unsafe_allow_html=True)
        if subtitle:
            st.markdown(f"<div class='cvea-header-subtitle'>{subtitle}</div>", unsafe_allow_html=True)

