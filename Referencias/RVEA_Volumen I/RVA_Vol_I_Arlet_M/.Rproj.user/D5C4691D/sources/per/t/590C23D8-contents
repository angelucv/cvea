# ==============================================================================
# SCRIPT COMPLETO DE MEO DE MORTALIDAD MUNICIPAL - VENEZUELA (2016)
# Incluye Normalización Intensiva y Correcciones Manuales para Unir el 99% de los datos
# ==============================================================================

# Cargar bibliotecas necesarias
if (!requireNamespace("pacman", quietly = TRUE)) install.packages("pacman")
pacman::p_load(tidyverse, sf, readr, geodata, stringr, scales)

# Definición del filepath para la carga de datos (asumiendo el archivo subido)
# Ajustar según el nombre exacto de su archivo cargado
data_filepath <- "Mort_Territ_2016.csv"

# ==============================================================================
# FUNCIÓN DE CARGA DE GEOMETRÍA MUNICIPAL (ADM2)
# ==============================================================================

cargar_geometria_gadm <- function() {
  message("Descargando geometría de Venezuela a nivel municipal (ADM2) usando el paquete 'geodata'...")
  
  mapa_vzla <- tryCatch({
    # Intenta descargar la geometría GADM (Nivel 2: Municipio)
    mapa_temporal <- geodata::gadm(country = "VEN", level = 2, path = tempdir())
    sf::st_as_sf(mapa_temporal)
  }, error = function(e) {
    # Muestra error y usa stop para detener la ejecución si falla la descarga
    stop(paste("ERROR AL CARGAR GEOMETRÍA MUNICIPAL:", e$message, 
               "\nAsegúrese de tener conexión a internet o reemplace esta función con la carga de su archivo .shp local."))
  })
  
  # Renombrar columnas a la convención usada
  mapa_vzla <- mapa_vzla %>%
    # geodata usa los nombres NAME_1 (Estado) y NAME_2 (Municipio)
    rename(
      ESTADO = NAME_1,
      DIV_POL = NAME_2
    ) %>%
    # Eliminar Dependencias Federales, ya que no están en los datos de mortalidad
    filter(ESTADO != "Dependencias Federales") %>%
    # Seleccionar solo las columnas necesarias
    select(ESTADO, DIV_POL, geometry)
  
  message(paste("[ÉXITO] Geometría municipal (ADM2) cargada. Total de geometrías:", nrow(mapa_vzla)))
  return(mapa_vzla)
}

# ==============================================================================
# FUNCIÓN DE NORMALIZACIÓN INTENSIVA (PASO 1)
# Elimina acentos, prefijos comunes y corrige errores ortográficos conocidos.
# ==============================================================================

normalize_key <- function(name_vector) {
  name_vector <- str_to_upper(name_vector)
  
  # 1. Correcciones de texto y estandarización de abreviaturas/typos
  name_vector <- str_replace_all(name_vector, "TEHIRA", "TACHIRA") # Error de estado en la data
  name_vector <- str_replace_all(name_vector, "JOSAC", "JOSÉ")
  name_vector <- str_replace_all(name_vector, "FACLIX", "FÉLIX")
  name_vector <- str_replace_all(name_vector, "MUAOS", "MUÑOZ")
  name_vector <- str_replace_all(name_vector, "SIR ARTUR MC. GREGOR", "SIR ARTHUR MCGREGOR")
  name_vector <- str_replace_all(name_vector, "LIC\\. DIEGO BAUTISTA URBANEJA", "DIEGO BAUTISTA URBANEJA")
  name_vector <- str_replace_all(name_vector, "LOS TAQUES", "LOS TANQUES") # Error común de ortografía en data/mapas
  name_vector <- str_replace_all(name_vector, "VARELA", "VALERA") # Error de data
  
  # 2. Eliminación de prefijos de la data que no existen en el mapa
  name_vector <- str_replace(name_vector, "MUNICIPIO\\s*", "")
  name_vector <- str_replace(name_vector, "PARROQUIA\\s*", "") # Para Distrito Capital
  name_vector <- str_replace_all(name_vector, "AUTÓNOMO\\s*", "")
  name_vector <- str_replace_all(name_vector, "LIC\\.\\s*", "")
  name_vector <- str_replace_all(name_vector, "GRAL\\.\\s*", "GENERAL ")
  
  # 3. Eliminar acentos y eñes para crear la clave ASCII (Ñ -> N, Á -> A)
  name_vector <- iconv(name_vector, from="UTF-8", to="ASCII//TRANSLIT")
  
  # 4. Limpieza final de espacios y caracteres especiales
  name_vector <- str_replace_all(name_vector, "[^[:alnum:]\\s]", "") # Quitar puntos, comas, etc.
  name_vector <- str_trim(name_vector)
  name_vector <- str_replace_all(name_vector, "\\s+", "_")
  
  return(name_vector)
}

# ==============================================================================
# FUNCIÓN DE CORRECCIÓN MANUAL DE CLAVES DE UNIÓN (PASO 2)
# Resuelve los faltantes específicos (nombres largos vs. nombres cortos y typos)
# ==============================================================================

corregir_claves_manual <- function(df_mortalidad) {
  df_mortalidad %>%
    mutate(
      Clave_Union_Final = case_when(
        # ESTADO ANZOATEGUI
        Clave_Union_Final == "ANZOATEGUI_SIMON_BOLIVAR" ~ "ANZOATEGUI_BOLIVAR",
        Clave_Union_Final == "ANZOATEGUI_MANUEL_EZEQUIEL_BRUZUAL" ~ "ANZOATEGUI_BRUZUAL",
        Clave_Union_Final == "ANZOATEGUI_JUAN_MANUEL_CAJIGAL" ~ "ANZOATEGUI_CAJIGAL",
        Clave_Union_Final == "ANZOATEGUI_FRANCISCO_DEL_CARMEN_CARVAJAL" ~ "ANZOATEGUI_CARVAJAL",
        Clave_Union_Final == "ANZOATEGUI_FERNANDO_PENALVER" ~ "ANZOATEGUI_FERNANDO_DE_PENALVER",
        Clave_Union_Final == "ANZOATEGUI_PEDRO_MARIA_FREITES" ~ "ANZOATEGUI_FREITES",
        Clave_Union_Final == "ANZOATEGUI_SIR_ARTHUR_MCGREGOR" ~ "ANZOATEGUI_GENERAL_SIR_ARTHUR_MCGREGOR",
        Clave_Union_Final == "ANZOATEGUI_SAN_JOSE_DE_GUANIPA" ~ "ANZOATEGUI_GUANIPA",
        Clave_Union_Final == "ANZOATEGUI_DIEGO_BAUTISTA_URBANEJA" ~ "ANZOATEGUI_DIEGO_BAUTISTA_URBAN",
        Clave_Union_Final == "ANZOATEGUI_FRANCISCO_DE_MIRANDA" ~ "ANZOATEGUI_MIRANDA",
        Clave_Union_Final == "ANZOATEGUI_JOSE_GREGORIO_MONAGAS" ~ "ANZOATEGUI_MONAGAS",
        Clave_Union_Final == "ANZOATEGUI_JUAN_ANTONIO_SOTILLO" ~ "ANZOATEGUI_SOTILLO",
        
        # ESTADO APURE (Typo en MUNOZ)
        Clave_Union_Final == "APURE_MUNOS" ~ "APURE_MUNOZ", 
        
        # ESTADO ARAGUA
        Clave_Union_Final == "ARAGUA_FRANCISCO_LINARES_ALCANTARA" ~ "ARAGUA_FRANCISCO_LINARES",
        Clave_Union_Final == "ARAGUA_JOSE_FELIX_RIVAS" ~ "ARAGUA_JOSE_FELIX_RIBAS", 
        Clave_Union_Final == "ARAGUA_JOSE_RAFAEL_REVENGA" ~ "ARAGUA_JOSE_R_REVENGA",
        Clave_Union_Final == "ARAGUA_OCUMARE_DE_LA_COSTA" ~ "ARAGUA_OCUMARE_DE_LA_COSTA_DE_ORO",
        
        # ESTADO BOLIVAR (Raúl Leoni no tiene contraparte en GADM, se une a Angostura)
        Clave_Union_Final == "BOLIVAR_RAUL_LEONI" ~ "BOLIVAR_ANGOSTURA", 
        
        # ESTADO CARABOBO
        Clave_Union_Final == "CARABOBO_CARLOS_ARVELO" ~ "CARABOBO_CARLOS_AREVALO", 
        
        # ESTADO COJEDES 
        Clave_Union_Final == "COJEDES_SAN_CARLOS" ~ "COJEDES_EZEQUIEL_ZOMORA",
        
        # DISTRITO CAPITAL (Todas las parroquias a LIBERTADOR - ya manejado en el paso 1)
        grepl("DISTRITO_CAPITAL_", Clave_Union_Final) ~ "DISTRITO_CAPITAL_LIBERTADOR",
        
        # ESTADO FALCON
        Clave_Union_Final == "FALCON_PALMASOLA" ~ "FALCON_PALMA_SOLA",
        
        # ESTADO GUARICO 
        Clave_Union_Final == "GUARICO_GUAYABAL" ~ "GUARICO_SAN_GERONIMO_DE_GUAYABAL",
        
        # ESTADO MERIDA 
        Clave_Union_Final == "MERIDA_ALBERTO_ADRIAN" ~ "MERIDA_ALBERTO_ADRIANI", 
        Clave_Union_Final == "MERIDA_CARRACCIOLO_PARRA_OLMEDO" ~ "MERIDA_CARACCIOLO_PARRA_OLMEDO", 
        
        # ESTADO NUEVA ESPARTA 
        Clave_Union_Final == "NUEVA_ESPARTA_VILLALBA" ~ "NUEVA_ESPARTA_ISLA_DE_COCHE",
        
        # ESTADO TACHIRA
        Clave_Union_Final == "TACHIRA_ANTONIO_ROMULO_ACOSTA" ~ "TACHIRA_ANTONIO_ROMULO_COSTA",
        
        # ESTADO TRUJILLO
        Clave_Union_Final == "TRUJILLO_JOSE_FELIPE_MARQUEZ_CANIZALES" ~ "TRUJILLO_JOSE_FELIPE_MARQUEZ_CANIZALEZ",
        Clave_Union_Final == "TRUJILLO_JUAN_VICENTE_CAMPO_ELIAS" ~ "TRUJILLO_JUAN_VICENTE_CAMPOS_ELIAS", 
        
        # ESTADO VARGAS (Todas las parroquias a VARGAS_VARGAS)
        grepl("^VARGAS_", Clave_Union_Final) ~ "VARGAS_VARGAS",
        
        # ESTADO ZULIA
        Clave_Union_Final == "ZULIA_JESUS_ENRIQUE_LOSADA" ~ "ZULIA_JESUS_ENRIQUE_LOSSADA", 
        Clave_Union_Final == "ZULIA_PAEZ" ~ "ZULIA_GUAJIRA", 
        
        # Mantiene la clave original si no hay coincidencia
        TRUE ~ Clave_Union_Final
      )
    )
}

# ==============================================================================
# III. EJECUCIÓN DEL FLUJO DE TRABAJO
# ==============================================================================

# 1. Cargar el mapa de Venezuela
mapa_venezuela_gadm <- cargar_geometria_gadm()

# 2. Cargar datos de mortalidad
datos_mortalidad_raw <- readr::read_delim(
  data_filepath,
  delim = ",", 
  col_select = c(ESTADO, DIV_POL, OCURRENCIA), # Columna renombrada
  col_types = cols(
    ESTADO = col_character(), 
    DIV_POL = col_character(), 
    OCURRENCIA = col_number()
  ),
  locale = locale(grouping_mark = "."), # Maneja el punto como separador de miles
  show_col_types = FALSE
) %>%
  rename(DIV_POL = DIV_POL) %>% # Renombrar para consistencia interna
  mutate(
    ESTADO = str_to_upper(ESTADO),
    DIV_POL_DATA = str_trim(DIV_POL)
  ) %>%
  select(-DIV_POL)

# 3. Aplicar normalización (Intensiva) y agregación inicial a los datos
datos_mortalidad_clean <- datos_mortalidad_raw %>%
  mutate(
    ESTADO = normalize_key(ESTADO),
    DIV_POL_CLEAN = normalize_key(DIV_POL_DATA)
  ) %>%
  # Agregación especial para Distrito Capital (Parroquia -> Municipio Libertador)
  mutate(
    DIV_POL_CLEAN = if_else(ESTADO == "DISTRITOCAPITAL", "LIBERTADOR", DIV_POL_CLEAN)
  ) %>%
  # Crear la clave final de unión (antes de corrección manual)
  mutate(
    Clave_Union_Final = str_replace_all(paste0(ESTADO, "_", DIV_POL_CLEAN), "[^[:alnum:]_]", "")
  ) %>%
  # Agrupar y resumir. Esto es crucial para unir las 22 parroquias de DC al Libertador
  group_by(Clave_Union_Final) %>%
  summarise(Mortalidad_Total = sum(OCURRENCIA, na.rm = TRUE), .groups = 'drop')

# 4. Aplicar correcciones manuales y re-agregar los datos de mortalidad
datos_mortalidad_manual_fix <- datos_mortalidad_clean %>%
  corregir_claves_manual() %>%
  # Se vuelve a sumar para consolidar los datos de Vargas y otras correcciones
  group_by(Clave_Union_Final) %>%
  summarise(Mortalidad_Total = sum(Mortalidad_Total, na.rm = TRUE)) %>%
  ungroup()

# 5. Aplicar normalización al mapa GADM
mapa_venezuela_clean <- mapa_venezuela_gadm %>%
  mutate(
    ESTADO_MAP = normalize_key(ESTADO),
    DIV_POL_MAP = normalize_key(DIV_POL)
  ) %>%
  # CRÍTICO: Asegurar que el municipio del Distrito Capital también se llame "LIBERTADOR"
  mutate(
    DIV_POL_MAP = if_else(ESTADO_MAP == "DISTRITOCAPITAL", "LIBERTADOR", DIV_POL_MAP)
  ) %>%
  # Crear la clave final de unión para el mapa
  mutate(
    Clave_Union_Final = str_replace_all(paste0(ESTADO_MAP, "_", DIV_POL_MAP), "[^[:alnum:]_]", "")
  ) %>%
  select(-ESTADO, -DIV_POL)

# 6. Realizar la unión final de los datos con el mapa
mapa_datos_final_corregido <- mapa_venezuela_clean %>%
  # Unión izquierda: mantiene todos los municipios del mapa
  left_join(datos_mortalidad_manual_fix, by = "Clave_Union_Final") %>%
  
  # === NUEVA CORRECCIÓN: IMPUTAR CERO EN LUGAR DE NA ===
  mutate(
    # Si Mortalidad_Total es NA, significa que la clave del municipio existía
    # en el mapa pero no en los datos, por lo que se asume 0 ocurrencias.
    Mortalidad_Total = if_else(is.na(Mortalidad_Total), 0, Mortalidad_Total)
  )
# ==============================================================================
# IV. VERIFICACIÓN Y REPORTE FINAL
# ==============================================================================

# A. Municipios en el mapa que AÚN NO tienen datos (Debería ser 0, pero se verifica la columna antes de la imputación)
# Nota: La columna ya no contendrá NAs, por lo que esta verificación es solo para reportar.
municipios_con_cero <- mapa_datos_final_corregido %>%
  filter(Mortalidad_Total == 0)

print(paste("REPORTE FINAL: ", nrow(municipios_con_cero), " municipios tienen 0 casos (Imputados o reales)."))
print("==================================================================")
print("CLAVES DEL MAPA (GADM) CON 0 CASOS DE MORTALIDAD REGISTRADOS:")
print("==================================================================")
# Mostramos los que tienen 0 (asumiendo que los 4 que faltaban están aquí)
print(municipios_con_cero %>% sf::st_drop_geometry() %>% select(ESTADO_MAP, DIV_POL_MAP, Clave_Union_Final, Mortalidad_Total) %>% arrange(desc(Mortalidad_Total)) %>% head(10))

# B. Claves de datos que AÚN NO coinciden con el mapa (Debería ser 0)
datos_perdidos_corregido <- anti_join(datos_mortalidad_manual_fix, mapa_venezuela_clean %>% sf::st_drop_geometry(), by = "Clave_Union_Final")

if (nrow(datos_perdidos_corregido) > 0) {
  print(paste("ADVERTENCIA FINAL: Se encontraron ", nrow(datos_perdidos_corregido), " CLAVES DE DATOS que AÚN NO coinciden con NINGÚN municipio del mapa (¡Datos perdidos!)."))
} else {
  print("¡ÉXITO! Todos los datos fueron unidos a una geometría del mapa.")
}


# ==============================================================================
# V. GENERACIÓN DEL MAPA FINAL
# ==============================================================================

titulo_mapa_corregido <- "Mortalidad Total por Municipio (Ocurrencia) - Venezuela, 2016 (Final)"

mapa_mortalidad_municipal_corregido <- ggplot(data = mapa_datos_final_corregido) +
  # Usar geom_sf para dibujar la geometría
  geom_sf(
    # Rellena con Mortalidad_Total (donde NA ahora es 0)
    aes(fill = Mortalidad_Total),
    color = "gray70",
    lwd = 0.05
  ) +
  # Aplicar un contorno más grueso para la frontera externa del país
  geom_sf(
    data = mapa_datos_final_corregido %>% st_union(),
    fill = NA,
    color = "black",
    lwd = 0.7
  ) +
  # === PALETA DE COLOR MODIFICADA: USANDO 'MAGMA' ===
  # Usamos scale_fill_gradientn con la paleta 'magma' para mejor contraste
  scale_fill_gradientn(
    name = "Total de Casos\n(Ocurrencia)",
    # Definir los colores: 'white' para 0, luego un degradado de la paleta 'magma'
    colors = c("white", viridisLite::magma(20, begin = 0.15)), 
    # Definir los valores de la leyenda (0 a max)
    values = scales::rescale(c(0, max(mapa_datos_final_corregido$Mortalidad_Total, na.rm = TRUE))),
    # Formato de miles con puntos
    labels = scales::label_number(big.mark = ".", decimal.mark = ","),
    # Asegura que la leyenda cubre todo el rango de datos
    limits = c(0, max(mapa_datos_final_corregido$Mortalidad_Total, na.rm = TRUE)),
    oob = scales::squish
  ) +
  # Personalización del tema
  labs(
    title = titulo_mapa_corregido,
    subtitle = "Los municipios sin registro en la fuente han sido imputados con un valor de 0 (mostrados en blanco).",
    caption = "Fuente: Anuario de Mortalidad de Venezuela (2016), GADM (Límites Geográficos Nivel 2). Correcciones manuales aplicadas."
  ) +
  # Tema simple y sin ejes (recomendado para mapas)
  theme_void() +
  theme(
    plot.title = element_text(hjust = 0.5, face = "bold", size = 16, margin = margin(t = 10)),
    plot.subtitle = element_text(hjust = 0.5, size = 10, margin = margin(b = 10)),
    legend.position = "right",
    legend.title = element_text(size = 10, face = "bold"),
    legend.text = element_text(size = 9),
    plot.caption = element_text(size = 8, margin = margin(b = 5))
  )

# Imprimir el mapa generado
print(mapa_mortalidad_municipal_corregido)
