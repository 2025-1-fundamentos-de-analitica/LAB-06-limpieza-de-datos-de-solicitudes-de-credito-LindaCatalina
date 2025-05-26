"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""
import pandas as pd 
import os

def pregunta_01():
    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"

    """

    file_path = 'files/input/solicitudes_de_credito.csv' 
    DATOS = pd.read_csv(file_path, sep=';') 
    DATOS.drop(['Unnamed: 0'], axis=1, inplace=True) 
    DATOS.dropna(inplace=True) 
    DATOS.drop_duplicates(inplace=True) 

    DATOS[['día', 'mes', 'año']] = DATOS['fecha_de_beneficio'].str.split('/', expand=True) 
    DATOS.loc[DATOS['año'].str.len() < 4, ['día', 'año']] = DATOS.loc[DATOS['año'].str.len() < 4, ['año', 'día']].values  
    DATOS['fecha_de_beneficio'] = DATOS['año'] + '-' + DATOS['mes'] + '-' + DATOS['día'] 
    DATOS.drop(['día', 'mes', 'año'], axis=1, inplace=True)

    object_columns = ['sexo', 'tipo_de_emprendimiento', 'idea_negocio', 'línea_credito'] 
    DATOS[object_columns] = DATOS[object_columns].apply(lambda x: x.str.lower().replace(['-', '_'], ' ', regex=True).str.strip()) 
    DATOS['barrio'] = DATOS['barrio'].str.lower().replace(['-', '_'], ' ', regex=True) 

    DATOS['monto_del_credito'] = DATOS['monto_del_credito'].str.replace("[$, ]", "", regex=True).str.strip() 
    DATOS['monto_del_credito'] = pd.to_numeric(DATOS['monto_del_credito'], errors='coerce')  
    DATOS['monto_del_credito'] = DATOS['monto_del_credito'].fillna(0).astype(int) 
    DATOS['monto_del_credito'] = DATOS['monto_del_credito'].astype(str).str.replace('.00', '') 

    DATOS.drop_duplicates(inplace=True)

    output_dir = 'files/output' 
    os.makedirs(output_dir, exist_ok=True) 

    output_path = f'{output_dir}/solicitudes_de_credito.csv'
    DATOS.to_csv(output_path, sep=';', index=False)

    return DATOS.head()

dataframe_limpio = pregunta_01()
print(dataframe_limpio.head())