import streamlit as st

# URL pública del logo en GitHub Pages (ajustable si cambia la ruta)
LOGO_URL = "https://angelucv.github.io/cvea/assets/logos/Logo-CVEA-icono-sin%20fondo%20letrasblancas.png"

CVEA_PRIMARY = "#38666A"
CVEA_DARK = "#1e3d40"
CVEA_LIGHT = "#f5f5f5"


def apply_cvea_theme() -> None:
    """Inyecta estilos básicos con la paleta CVEA."""
    st.markdown(
        f"""
<style>
:root {{
  --cvea-primary: {CVEA_PRIMARY};
  --cvea-dark: {CVEA_DARK};
  --cvea-light: {CVEA_LIGHT};
}}

body {{
  background-color: white;
}}

a, .stMarkdown a {{
  color: var(--cvea-primary);
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
  color: var(--cvea-dark);
  font-weight: 600;
}}

.stApp {{
  background-color: white;
}}

.cvea-header-title {{
  font-size: 1.6rem;
  font-weight: 700;
  color: var(--cvea-dark);
  margin-bottom: 0.15rem;
}}

.cvea-header-subtitle {{
  font-size: 0.95rem;
  color: #555;
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
        st.image(LOGO_URL, use_column_width=True)
    with col_text:
        st.markdown(f"<div class='cvea-header-title'>{title}</div>", unsafe_allow_html=True)
        if subtitle:
            st.markdown(f"<div class='cvea-header-subtitle'>{subtitle}</div>", unsafe_allow_html=True)

