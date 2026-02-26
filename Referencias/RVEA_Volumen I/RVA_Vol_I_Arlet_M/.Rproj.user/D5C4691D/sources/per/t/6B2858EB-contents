# Cargar bibliotecas necesarias
if (!requireNamespace("pacman", quietly = TRUE)) install.packages("pacman")
pacman::p_load(tidyverse, sf, readr, geodata, stringr, scales, viridisLite, stringi)

# Definición de filepaths para la carga de datos (archivos cargados)
mortality_filepath <- "Mort_Territ_2016.csv"
population_filepath <- "Pob_Territ_2011.csv"

# Función para cargar la geometría municipal (ADM2) de Venezuela
cargar_geometria_gadm <- function() {
  message("Descargando geometría de Venezuela a nivel municipal (ADM2) usando el paquete 'geodata'...")
  
  mapa_vzla <- tryCatch({
    # Intenta descargar la geometría GADM (Nivel 2: Municipio)
    mapa_temporal <- geodata::gadm(country = "VEN", level = 2, path = tempdir())
    sf::st_as_sf(mapa_temporal)
  }, error = function(e) {
    stop(paste("ERROR AL CARGAR GEOMETRÍA MUNICIPAL:", e$message))
  })
  
  # Renombrar columnas a la convención usada
  mapa_vzla <- mapa_vzla %>%
    # geodata usa los nombres NAME_1 (Estado) y NAME_2 (Municipio)
    rename(
      ESTADO = NAME_1,
      DIV_POL = NAME_2
    ) %>%
    # Eliminar Dependencias Federales, que no tienen datos de población/mortalidad
    filter(ESTADO != "Dependencias Federales") %>%
    # Seleccionar solo las columnas necesarias
    select(ESTADO, DIV_POL, geometry)
  
  message(paste("[ÉXITO] Geometría municipal (ADM2) cargada. Total de geometrías:", nrow(mapa_vzla)))
  return(mapa_vzla)
}

# Función para normalizar claves de unión (limpieza y estandarización de nombres)
# Esta función crea la clave de unión base, removiendo acentos, prefijos y espacios.
normalize_key <- function(name_vector) {
  name_vector <- str_to_upper(name_vector)
  
  # 1. Correcciones de texto y estandarización de abreviaturas/typos (se mantiene la lógica original)
  name_vector <- str_replace_all(name_vector, "TEHIRA", "TACHIRA")
  name_vector <- str_replace_all(name_vector, "JOSAC", "JOSÉ")
  name_vector <- str_replace_all(name_vector, "FACLIX", "FÉLIX")
  name_vector <- str_replace_all(name_vector, "MUAOS", "MUÑOZ")
  name_vector <- str_replace_all(name_vector, "MUNOS", "MUÑOZ")
  name_vector <- str_replace_all(name_vector, "RIVAS", "RIBAS")
  # Se ajusta la corrección para asegurar consistencia con el nombre que resulta de la limpieza de prefijos
  name_vector <- str_replace_all(name_vector, "SIR ARTUR MC\\. GREGOR", "SIR ARTUR MCGREGOR")
  name_vector <- str_replace_all(name_vector, "LIC\\. DIEGO BAUTISTA URBANEJA", "DIEGO BAUTISTA URBANEJA")
  
  # CORRECCIÓN DE TYPOS EN LA DATA DE POBLACIÓN o MORTALIDAD
  name_vector <- str_replace_all(name_vector, "VARELA", "VALERA")
  # Se revierte el cambio de LOSTANQUES a LOS TAQUES ya que la data de Población usa la forma larga
  name_vector <- str_replace_all(name_vector, "LOS TAQUES", "LOSTANQUES")
  name_vector <- str_replace_all(name_vector, "JESÚS ENRIQUE LOSADA", "JESUS ENRIQUE LOSSADA")
  name_vector <- str_replace_all(name_vector, "PEÑALVER", "PENALVER")
  name_vector <- str_replace_all(name_vector, "SAN FELIPE", "SANFELIPE")
  name_vector <- str_replace_all(name_vector, "COCOROTE", "COCOROTE")
  
  # 2. Eliminación de prefijos de la data que no existen en el mapa
  name_vector <- str_replace(name_vector, "MUNICIPIO\\s*", "")
  name_vector <- str_replace(name_vector, "PARROQUIA\\s*", "")
  name_vector <- str_replace_all(name_vector, "AUTÓNOMO\\s*", "")
  name_vector <- str_replace_all(name_vector, "LIC\\.\\s*", "")
  name_vector <- str_replace_all(name_vector, "GRAL\\.\\s*", "GENERAL ")
  name_vector <- str_replace(name_vector, "ESTADO\\s*", "")
  
  # 3. Eliminar acentos y eñes para crear la clave ASCII
  name_vector <- stringi::stri_trans_general(name_vector, "Latin-ASCII")
  
  # 4. Limpieza final: Eliminar TODOS los caracteres no alfanuméricos, incluyendo espacios.
  name_vector <- str_replace_all(name_vector, "[^[:alnum:]]", "")
  name_vector <- str_trim(name_vector)
  
  return(name_vector)
}

# Función para aplicar correcciones manuales a los datos de Población (Long Name)
corregir_claves_poblacion_manual <- function(df) {
  df_corregido <- df %>%
    mutate(
      Clave_Union_Final = case_when(
        
        # === 1. CASOS VARGAS/LA GUAIRA y DISTRITO CAPITAL (Consolidación) ===
        # VARGAS/LA GUAIRA
        Clave_Union_Final == "VARGAS_VARGAS" ~ "LAGUAIRA_LAGUAIRA",
        # DISTRITO CAPITAL
        Clave_Union_Final == "DISTRITOCAPITAL_LIBERTADOR" ~ "DISTRITOCAPITAL_DISTRITOCAPITAL",
        
        # === 2. ESTANDARIZACIÓN INTERNA DE POBLACIÓN ===
        # ZULIA: Mapear el nombre antiguo/población GUAJIRA al nombre largo canónico de la data
        Clave_Union_Final == "ZULIA_INDIGENABOLIVARIANOGUAJIRA" ~ "ZULIA_INDIGENABOLIVARIANOGUAJIRA",
        
        # CRÍTICO: COJEDES - Re-mapear el municipio 'FALCON' en COJEDES a 'TINAQUILLO'
        Clave_Union_Final == "COJEDES_FALCON" ~ "COJEDES_TINAQUILLO",
        
        # DEFAULT: Mantiene todas las demás claves como están
        TRUE ~ Clave_Union_Final
      )
    ) %>%
    # Filtro adicional para eliminar filas de resumen
    filter(Clave_Union_Final != "TOTALNACIONAL_NACIONAL") %>%
    filter(!str_detect(Clave_Union_Final, "^TOTAL") & Clave_Union_Final != "NACIONAL_NACIONAL")
  
  return(df_corregido)
}

# Función para aplicar correcciones manuales a los datos de Mortalidad (Alineación a Población Long Name)
corregir_claves_mortalidad_manual <- function(df) {
  df_corregido <- df %>%
    mutate(
      Clave_Union_Final = case_when(
        # === 1. ELIMINACION DE FILAS NO-GEOGRAFICAS Y CONSOLIDACIONES ===
        MUNICIPIO_CLEAN %in% c("NOESPECIFICADO", "FUERZASARMADAS", "INDIGENA", "RESIDENTEENALEXTERIOR", "INDIGENA", "TOTALNACIONAL") ~ NA_character_,
        ESTADO_CLEAN == MUNICIPIO_CLEAN & ESTADO_CLEAN != "LAGUAIRA" ~ NA_character_,
        
        # CONSOLIDACIONES ESTATALES
        ESTADO_CLEAN == "DISTRITOCAPITAL" ~ "DISTRITOCAPITAL_DISTRITOCAPITAL",
        ESTADO_CLEAN == "VARGAS" | ESTADO_CLEAN == "LAGUAIRA" ~ "LAGUAIRA_LAGUAIRA",
        
        # === 2. CORRECCIONES GEOGRAFICAS ESPECIFICAS (Alineación Mortalidad -> Población Long Name) ===
        
        # CRÍTICO FIX: COJEDES - Alineación a Población canónica (FALCON -> TINAQUILLO)
        Clave_Union_Final == "COJEDES_FALCON" ~ "COJEDES_TINAQUILLO", 
        
        # ANZOATEGUI
        Clave_Union_Final == "ANZOATEGUI_DIEGOBAUTISTAURBANEJA" ~ "ANZOATEGUI_TURISTICODIEGOBAUTISTAURBANEJA",
        Clave_Union_Final == "ANZOATEGUI_SIRARTHURMCGREGOR" ~ "ANZOATEGUI_SIRARTURMCGREGOR",
        Clave_Union_Final == "ANZOATEGUI_FERNANDOPENALVER" ~ "ANZOATEGUI_FERNANDODEPENALVER",
        
        # ARAGUA
        Clave_Union_Final == "ARAGUA_OCUMAREDELACOSTA" ~ "ARAGUA_OCUMAREDELACOSTADEORO",
        Clave_Union_Final == "ARAGUA_FRANCISCOLINARES" ~ "ARAGUA_FRANCISCOLINARESALCANTARA",
        
        # BOLIVAR
        Clave_Union_Final == "BOLIVAR_RAULLEONI" ~ "BOLIVAR_PIAR",
        
        # GUÁRICO (Mapear el nombre corto de Mortalidad al nombre largo de Población)
        Clave_Union_Final == "GUARICO_MIRANDA" ~ "GUARICO_FRANCISCODEMIRANDA",
        Clave_Union_Final == "GUARICO_GUAYABAL" ~ "GUARICO_SANGERONIMODEGUAYABAL",
        Clave_Union_Final == "GUARICO_MELLADO" ~ "GUARICO_JULIANMELLADO",
        Clave_Union_Final == "GUARICO_INFANTE" ~ "GUARICO_LEONARDOINFANTE",
        Clave_Union_Final == "GUARICO_RIBAS" ~ "GUARICO_JOSEFELIXRIBAS",
        Clave_Union_Final == "GUARICO_ROSCIO" ~ "GUARICO_JUANGERMANROSCIO",
        Clave_Union_Final == "GUARICO_ZARAZA" ~ "GUARICO_PEDROZARAZA",
        Clave_Union_Final == "GUARICO_MONAGAS" ~ "GUARICO_JOSETADEOMONAGAS",
        
        # COJEDES (Nota: SANCARLOS es un error, el municipio es EZEQUIELZAMORA en Población)
        Clave_Union_Final == "COJEDES_SANCARLOS" ~ "COJEDES_EZEQUIELZAMORA",
        
        # FALCON (El nombre ya fue corregido en normalize_key a LOSTANQUES, por lo que este fix es para un posible remanente)
        Clave_Union_Final == "FALCON_LOSTAQUES" ~ "FALCON_LOSTANQUES",
        
        # ZULIA
        Clave_Union_Final == "ZULIA_JESUSENRIQUELOSADA" ~ "ZULIA_JESUSENRIQUELOSSADA",
        Clave_Union_Final == "ZULIA_PAEZ" ~ "ZULIA_INDIGENABOLIVARIANOGUAJIRA",
        
        # APURE
        Clave_Union_Final == "APURE_MUNOS" ~ "APURE_MUNOZ",
        
        # TACHIRA
        Clave_Union_Final == "TACHIRA_ROMULOCOSTA" ~ "TACHIRA_ANTONIOROMULOCOSTA",
        
        # MÉRIDA: 
        Clave_Union_Final == "MERIDA_ALBERTOADRIAN" ~ "MERIDA_ALBERTOADRIANI", 
        Clave_Union_Final == "MERIDA_CARRACCIOLOPARRAOLMEDO" ~ "MERIDA_CARACCIOLOPARRAOLMEDO", 
        
        # DEFAULT
        TRUE ~ Clave_Union_Final
      )
    ) %>%
    # Eliminar las filas que se marcaron con NA_character_
    filter(!is.na(Clave_Union_Final))
  
  return(df_corregido)
}

# 2.1. Cargar el mapa de Venezuela
message("\nCargando Geometría...")
mapa_venezuela_gadm <- cargar_geometria_gadm()

message("\nIniciando carga y depuración de Datos de Población (2011)...")
# 2.2. Leemos el archivo de Población
datos_poblacion_raw <- readr::read_delim(
  population_filepath,
  delim = ",",
  col_names = c("ESTADO_RAW", "MUNICIPIO_RAW", "PARROQUIA_RAW", "TOTAL_POBLACION_RAW"),
  col_types = cols(.default = col_character()),
  skip = 1,
  show_col_types = FALSE
)

# 2.3. Limpieza de Población
datos_poblacion_depurado_pre_agg <- datos_poblacion_raw %>%
  mutate(
    # Limpieza de cifras: La población usa coma como separador de miles.
    Poblacion_2011 = as.numeric(gsub(",", "", TOTAL_POBLACION_RAW))
  ) %>%
  # Normalización de claves
  mutate(
    ESTADO_CLEAN = normalize_key(ESTADO_RAW),
    # [NUEVA CORRECCIÓN CRÍTICA] Estandarizar el nombre largo del estado Miranda al nombre corto
    ESTADO_CLEAN = str_replace_all(ESTADO_CLEAN, "BOLIVARIANODEMIRANDA", "MIRANDA"),
    
    # Extraer solo el nombre del municipio (está después de la coma y espacio)
    MUNICIPIO_CLEAN = str_extract(MUNICIPIO_RAW, "(?<=,\\s).*"),
    MUNICIPIO_CLEAN = normalize_key(MUNICIPIO_CLEAN),
    
    # Creación de la clave de unión inicial: ESTADO_MUNICIPIO (con underscore)
    Clave_Union_Final = paste0(ESTADO_CLEAN, "_", MUNICIPIO_CLEAN)
  ) %>%
  # Aplicar correcciones manuales y filtrar totales
  corregir_claves_poblacion_manual()
# Agrupamos por clave final para sumar la población de todas las parroquias
datos_poblacion_depurado <- datos_poblacion_depurado_pre_agg %>%
  select(Clave_Union_Final, Poblacion_2011) %>%
  group_by(Clave_Union_Final) %>%
  summarise(
    Poblacion_2011 = sum(Poblacion_2011, na.rm = TRUE),
    .groups = 'drop'
  )

message(paste("[Población 2011] Claves de Unión Únicas:", n_distinct(datos_poblacion_depurado$Clave_Union_Final)))

# =============================================================================
# VERIFICACIÓN ADICIONAL 1: Claves de Población en Miranda (Debe ser sin 'S')
# =============================================================================
message("\n[VERIFICACIÓN 1: CLAVES CANÓNICAS EN POBLACIÓN (MIRANDA) - Post Fix]")
print(datos_poblacion_depurado %>% 
        filter(str_detect(Clave_Union_Final, "^MIRANDA_")) %>% 
        select(Clave_Union_Final) %>% 
        distinct() %>% 
        arrange(Clave_Union_Final))
message("[FIN VERIFICACIÓN 1] La clave canónica NO debe terminar en 'S'.")

message("\nIniciando carga y depuración de Datos de Mortalidad (2016)...")
# 2.4. Leemos el archivo de Mortalidad
datos_mortalidad_raw <- readr::read_delim(
  mortality_filepath,
  delim = ",",
  col_types = cols(.default = col_character()),
  skip = 1,
  show_col_types = FALSE
)
New_names <- c(
  "ESTADO_RAW", "MUNICIPIO_RAW", "OCURRENCIA_TOTAL",
  "VARONES_O", "HEMBRAS_O", "RESIDENCIA_TOTAL",
  "VARONES_R", "HEMBRAS_R", "ANO"
)
colnames(datos_mortalidad_raw) <- New_names[1:ncol(datos_mortalidad_raw)]

# 2.5. Limpieza de Mortalidad (Pre-Agregación para diagnóstico)
datos_mortalidad_depurado_pre_agg <- datos_mortalidad_raw %>%
  # Limpieza de cifras: Las cifras en Mortalidad usan punto como separador de miles.
  mutate(
    OCURRENCIA_TOTAL = as.numeric(gsub("\\.", "", OCURRENCIA_TOTAL)),
    RESIDENCIA_TOTAL = as.numeric(gsub("\\.", "", RESIDENCIA_TOTAL))
  ) %>%
  # Normalización de claves
  mutate(
    ESTADO_CLEAN = normalize_key(ESTADO_RAW),
    MUNICIPIO_CLEAN = normalize_key(MUNICIPIO_RAW),
    
    # Creación de la clave de unión inicial: ESTADO_MUNICIPIO (con underscore)
    Clave_Union_Final = paste0(ESTADO_CLEAN, "_", MUNICIPIO_CLEAN)
  ) %>%
  # Aplicar correcciones manuales y filtrar no-geográficos
  corregir_claves_mortalidad_manual(.)

# Agregamos los datos de Mortalidad
datos_mortalidad_depurado <- datos_mortalidad_depurado_pre_agg %>%
  # Seleccionamos solo las columnas necesarias y agrupamos
  select(Clave_Union_Final, OCURRENCIA_TOTAL, RESIDENCIA_TOTAL) %>%
  group_by(Clave_Union_Final) %>%
  summarise(
    Defunciones_Ocurrencia = sum(OCURRENCIA_TOTAL, na.rm = TRUE),
    Defunciones_Residencia = sum(RESIDENCIA_TOTAL, na.rm = TRUE),
    .groups = 'drop'
  )

message(paste("[Mortalidad 2016] Claves de Unión Únicas:", n_distinct(datos_mortalidad_depurado$Clave_Union_Final)))

# =============================================================================
# VERIFICACIÓN ADICIONAL 2: Claves Únicas Antes de la Unión (Post Fix)
# =============================================================================
message("\n[VERIFICACIÓN 2: ANÁLISIS DE CLAVES PRE-UNIÓN - Post Fix MIRANDA]")
claves_poblacion <- unique(datos_poblacion_depurado$Clave_Union_Final)
claves_mortalidad <- unique(datos_mortalidad_depurado$Clave_Union_Final)
claves_solo_en_poblacion <- setdiff(claves_poblacion, claves_mortalidad)
claves_solo_en_mortalidad <- setdiff(claves_mortalidad, claves_poblacion)
message(paste("Claves solo en Población (sin datos de Mortalidad):", length(claves_solo_en_poblacion)))
if (length(claves_solo_en_poblacion) > 0) {
  message("Las primeras 10 claves solo en Población son:")
  print(head(sort(claves_solo_en_poblacion), 10))
}
message(paste("Claves solo en Mortalidad (sin datos de Población):", length(claves_solo_en_mortalidad)))
if (length(claves_solo_en_mortalidad) > 0) {
  message("Las primeras 10 claves solo en Mortalidad son:")
  print(head(sort(claves_solo_en_mortalidad), 100))
}
message("[FIN VERIFICACIÓN 2] Este reporte ayuda a identificar los desajustes pendientes.")

message("\nIniciando Unión de Datos y Cálculo de Tasas...")
datos_tbm <- datos_mortalidad_depurado %>%
  # Unir los dos datasets usando Clave_Union_Final.
  left_join(datos_poblacion_depurado, by = "Clave_Union_Final") %>%
  
  # Calcular la Tasa Bruta de Mortalidad (TBM) por cada 1000 habitantes
  mutate(
    Tasa_Bruta_Mortalidad = (Defunciones_Residencia / Poblacion_2011) * 1000,
    Tasa_Bruta_Mortalidad = if_else(Poblacion_2011 == 0 | is.na(Poblacion_2011), NA_real_, Tasa_Bruta_Mortalidad),
    # Imputar Defunciones_Residencia con 0 para los que no coincidieron pero existen en el mapa
    Defunciones_Residencia = if_else(is.na(Defunciones_Residencia), 0, Defunciones_Residencia)
  )

# Reporte de Unión
coincidencias <- datos_tbm %>% filter(!is.na(Poblacion_2011))
no_coincidencias <- datos_tbm %>% filter(is.na(Poblacion_2011))
message("\n[REPORTE DE UNIÓN DE DATOS TBM]")
message(paste("Claves de Unión que COINCIDIERON (tienen población):", nrow(coincidencias)))
message(paste("Claves de Unión que NO COINCIDIERON (no tienen población, TBM es NA):", nrow(no_coincidencias)))
message("--------------------------------------------------")
message("CLAVES DE MORTALIDAD SIN MATCH EN POBLACIÓN (DEBE SER 0 O MUY CERCANO A CERO):")
print(no_coincidencias %>% select(Clave_Union_Final))

# 1. Normalización de GADM
mapa_venezuela_clean <- mapa_venezuela_gadm %>%
  mutate(
    ESTADO_MAP = normalize_key(ESTADO),
    DIV_POL_MAP = normalize_key(DIV_POL)
  ) %>%
  # 2. Correcciones de estado
  mutate(
    # Fija el cambio de estado de Vargas a La Guaira
    ESTADO_MAP = if_else(ESTADO_MAP == "VARGAS", "LAGUAIRA", ESTADO_MAP)
  ) %>%
  # 3. Correcciones CRÍTICAS de municipio (alinear GADM a la clave canónica de Población)
  mutate(
    DIV_POL_MAP = case_when(
      
      # === CRÍTICO: CONSOLIDACIONES Y CASOS ESPECIALES ===
      # DISTRITO CAPITAL
      ESTADO_MAP == "DISTRITOCAPITAL" ~ "DISTRITOCAPITAL",
      # LA GUAIRA (Evita el error LAGUAIRA_VARGAS -> Consolida en LAGUAIRA_LAGUAIRA)
      ESTADO_MAP == "LAGUAIRA" ~ "LAGUAIRA",
      
      # COJEDES: GADM tiene 'FALCON', Población canónica es 'TINAQUILLO'
      ESTADO_MAP == "COJEDES" & DIV_POL_MAP == "FALCON" ~ "TINAQUILLO",
      # COJEDES: GADM typo
      ESTADO_MAP == "COJEDES" & DIV_POL_MAP == "EZEQUIELZOMORA" ~ "EZEQUIELZAMORA",
      
      # ZULIA: GADM tiene PAEZ, Población tiene INDIGENABOLIVARIANOGUAJIRA. GADM también tiene GUAJIRA.
      ESTADO_MAP == "ZULIA" & (DIV_POL_MAP == "PAEZ" | DIV_POL_MAP == "GUAJIRA") ~ "INDIGENABOLIVARIANOGUAJIRA",
      
      # MÉRIDA: GADM tiene 'ALBERTOADRIAN', Población canónica es 'ALBERTOADRIANI'
      ESTADO_MAP == "MERIDA" & DIV_POL_MAP == "ALBERTOADRIAN" ~ "ALBERTOADRIANI",
      
      # ARAGUA: Alinea el nombre corto/GADM al nombre largo/canónico de Población
      ESTADO_MAP == "ARAGUA" & DIV_POL_MAP == "FRANCISCOLINARES" ~ "FRANCISCOLINARESALCANTARA",
      
      # === FIX: CARABOBO (Arévalo typo and long name) ===
      ESTADO_MAP == "CARABOBO" & DIV_POL_MAP == "CARLOSAREVALO" ~ "CARLOSARVELO",
      ESTADO_MAP == "CARABOBO" & DIV_POL_MAP == "LAGOVALENCIA" ~ "LAGOENVALENCIA",
      
      # === FIX: GUARICO (Mapeo de nombres cortos a largos - Faltantes en la versión anterior) ===
      ESTADO_MAP == "GUARICO" & DIV_POL_MAP == "INFANTE" ~ "LEONARDOINFANTE",
      ESTADO_MAP == "GUARICO" & DIV_POL_MAP == "MELLADO" ~ "JULIANMELLADO",
      ESTADO_MAP == "GUARICO" & DIV_POL_MAP == "MIRANDA" ~ "FRANCISCODEMIRANDA",
      ESTADO_MAP == "GUARICO" & DIV_POL_MAP == "MONAGAS" ~ "JOSETADEOMONAGAS",
      ESTADO_MAP == "GUARICO" & DIV_POL_MAP == "RIBAS" ~ "JOSEFELIXRIBAS",
      ESTADO_MAP == "GUARICO" & DIV_POL_MAP == "ROSCIO" ~ "JUANGERMANROSCIO",
      ESTADO_MAP == "GUARICO" & DIV_POL_MAP == "ZARAZA" ~ "PEDROZARAZA",
      
      # === FIX: NOMBRES CANÓNICOS EN ANZOATEGUI (Alineación a Población Long Name) ===
      ESTADO_MAP == "ANZOATEGUI" & DIV_POL_MAP == "GENERALSIRARTHURMCGREGOR" ~ "SIRARTURMCGREGOR",
      ESTADO_MAP == "ANZOATEGUI" & DIV_POL_MAP == "DIEGOBAUTISTAURBANEJA" ~ "TURISTICODIEGOBAUTISTAURBANEJA",
      ESTADO_MAP == "ANZOATEGUI" & DIV_POL_MAP == "BOLIVAR" ~ "SIMONBOLIVAR",
      ESTADO_MAP == "ANZOATEGUI" & DIV_POL_MAP == "BRUZUAL" ~ "MANUELEZEQUIELBRUZUAL", # CORREGIDO: Ezequiel en lugar de Antonio
      ESTADO_MAP == "ANZOATEGUI" & DIV_POL_MAP == "CAJIGAL" ~ "PEDROMARIACARRENO",
      ESTADO_MAP == "ANZOATEGUI" & DIV_POL_MAP == "CARVAJAL" ~ "SANJUANDECAPISTRANO",
      ESTADO_MAP == "ANZOATEGUI" & DIV_POL_MAP == "FREITES" ~ "PEDROJOAQUINFREITES",
      ESTADO_MAP == "ANZOATEGUI" & DIV_POL_MAP == "GUANIPA" ~ "SANJOSEDEGUANIPA",
      ESTADO_MAP == "ANZOATEGUI" & DIV_POL_MAP == "ISLA" ~ "JUANPEDROLOPIS",
      ESTADO_MAP == "ANZOATEGUI" & DIV_POL_MAP == "MIRANDA" ~ "FRANCISCOMIRANDA",
      ESTADO_MAP == "ANZOATEGUI" & DIV_POL_MAP == "MONAGAS" ~ "JOSETADEOMONAGAS",
      ESTADO_MAP == "ANZOATEGUI" & DIV_POL_MAP == "SOTILLO" ~ "JUANANTONIOSOTILLO",
      
      # === FIX: CASOS ESPECÍFICOS DE NOMBRES CORTOS EN GADM (GADM vs Población) ===
      ESTADO_MAP == "ARAGUA" & DIV_POL_MAP == "JOSERREVENGA" ~ "JOSEANGELREVENGA",
      # FIX: BARINAS (Simón Bolívar en GADM debe coincidir con BARINAS de la data INE)
      ESTADO_MAP == "BARINAS" & DIV_POL_MAP == "SIMONBOLIVAR" ~ "BARINAS",
      # BOLIVAR: La capital en GADM es ANGOSTURA, pero la data usa HERES
      ESTADO_MAP == "BOLIVAR" & DIV_POL_MAP == "ANGOSTURA" ~ "HERES",
      # FIX: Falcón Capital
      ESTADO_MAP == "FALCON" & DIV_POL_MAP == "FALCON" ~ "BOLIVARIANODECHURUGUARA",
      # NUEVA ESPARTA: Villalba es la Isla de Coche
      ESTADO_MAP == "NUEVAESPARTA" & DIV_POL_MAP == "ISLADECOCHE" ~ "VILLALBA",
      # FIX: TACHIRA (El GADM largo ANTONIOROMULOCOSTA debe mapear al ROMULOCOSTA de la data)
      ESTADO_MAP == "TACHIRA" & DIV_POL_MAP == "ANTONIOROMULOCOSTA" ~ "ROMULOCOSTA",
      # SUCRE: La capital en GADM es SUCRE, pero la data usa MARINOS.
      ESTADO_MAP == "SUCRE" & DIV_POL_MAP == "SUCRE" ~ "MARINOS", 
      # TRUJILLO: La capital en GADM es TRUJILLO, pero la data usa TRUJILLOCAPITAL
      ESTADO_MAP == "TRUJILLO" & DIV_POL_MAP == "TRUJILLO" ~ "TRUJILLOCAPITAL", 
      
      # DEFAULT
      TRUE ~ DIV_POL_MAP
    )
  ) %>%
  # Creación de la clave final de unión para el mapa (debe coincidir con la de los datos)
  mutate(
    Clave_Union_Final = paste0(ESTADO_MAP, "_", DIV_POL_MAP)
  ) %>%
  select(-ESTADO, -DIV_POL, -ESTADO_MAP, -DIV_POL_MAP)

# Realizar la unión final de los datos con el mapa
mapa_datos_final_tbm <- mapa_venezuela_clean %>%
  # Unión izquierda: mantiene todos los municipios del mapa
  left_join(datos_tbm, by = "Clave_Union_Final") %>%
  
  # Imputar NA en TBM por 0 defunciones si existe el municipio en el mapa pero no en los datos
  mutate(
    # Si la Tasa es NA, Defunciones es 0, y SÍ tenemos población, asumimos TBM = 0
    Tasa_Bruta_Mortalidad = if_else(is.na(Tasa_Bruta_Mortalidad) & Defunciones_Residencia == 0 & !is.na(Poblacion_2011), 0, Tasa_Bruta_Mortalidad)
  )

# =============================================================================
# GENERACIÓN DEL MAPA
# =============================================================================
titulo_mapa_tbm <- "Tasa Bruta de Mortalidad (por 1000 hab.) por Municipio - Venezuela, 2016"
# Creación del objeto ggplot para el mapa
mapa_tbm_ggplot <- ggplot(data = mapa_datos_final_tbm) +
  
  # Usar geom_sf para dibujar la geometría, rellenando con TBM
  geom_sf(
    aes(fill = Tasa_Bruta_Mortalidad),
    color = "gray70",
    lwd = 0.05
  ) +
  
  # Contorno más grueso para la frontera externa del país
  geom_sf(
    data = mapa_datos_final_tbm %>% sf::st_union(),
    fill = NA,
    color = "black",
    lwd = 0.7
  ) +
  
  # PALETA DE COLOR: USANDO 'VIRIDIS' para un gradiente secuencial
  scale_fill_viridis_c(
    name = "Tasa Bruta de\nMortalidad\n(por 1000 hab.)",
    option = "viridis",
    direction = -1, # Invertir para que los valores más altos sean más oscuros/intensos
    na.value = "gray90", # Color para los municipios sin datos (No Coincidencias)
    labels = scales::number_format(accuracy = 0.01)
  ) +
  
  # Etiquetas y tema
  labs(
    title = titulo_mapa_tbm,
    caption = "Fuente: INE 2011 (Población) | Datos 2016 (Mortalidad) | GADM (Geometría)"
  ) +
  theme_minimal() +
  theme(
    plot.title = element_text(hjust = 0.5, face = "bold", size = 16),
    legend.position = "right",
    panel.grid.major = element_line(colour = 'transparent'),
    axis.text = element_blank(),
    axis.title = element_blank(),
    plot.caption = element_text(size = 8, color = "gray50")
  )

# Imprimir el mapa resultante
print(mapa_tbm_ggplot)

# Reporte final: Claves del mapa que NO tienen datos después de la unión
claves_no_mapeadas_mapa_final <- mapa_datos_final_tbm %>%
  filter(is.na(Poblacion_2011)) %>%
  sf::st_drop_geometry() %>%
  select(Clave_Union_Final) %>%
  distinct()

message("\n[CLAVES FINALES DEL MAPA (GADM) QUE AÚN NO ENCONTRARON POBLACIÓN/MORTALIDAD]")
message(paste("Total de municipios GADM que NO coincidieron:", nrow(claves_no_mapeadas_mapa_final)))
print(claves_no_mapeadas_mapa_final)

