### Demo Actuarial Insurtech (Streamlit)

Versión demostrativa en **Python / Streamlit** inspirada en el dashboard `ActuarialInsurtechCARAMELS` (Shiny, R).  
Utiliza datos **simulados** con fines pedagógicos.

#### Ejecución local

1. Crear (opcional) un entorno virtual de Python.
2. Instalar dependencias:

```bash
cd apps/insurtech-streamlit
pip install -r requirements.txt
```

3. Ejecutar la app:

```bash
streamlit run app.py
```

La aplicación levantará un servidor local (por defecto en `http://localhost:8501`) con:

- **Visión general del mercado:** KPIs y series de PNC y siniestralidad.
- **Mi compañía vs mercado:** comparación de siniestralidad entre una compañía seleccionada y el agregado del mercado.
- **Cartera técnica simulada:** distribución de primas y siniestros por ramo y canal de distribución.

