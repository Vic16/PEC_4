def ORFs_per_class(df):

    import pandas as pd

    """
    Dado un Daframe de pandas
    Agrupa los datos por Ids y cuenta
    el número de ORFs, guarda el resultado
    en un file tipo .csv

     Args:
         df: pandas DataFrame
     Returns:
    """
    count_class = df.groupby('Ids', as_index=True)['ORF'].count().sort_values(ascending = False)
    count_class.to_csv("data/orfs_per_class.csv", index = False)

    print("Estas son las clases con más ORFs: \n")
    print(count_class.head(10))
    print("Se ha guardado un archivo .csv con la información completa!")


def ORFs_respiration(df):

    import pandas as pd

    """
    Dado un Daframe de pandas
    filtra los datos por las clases
    relacionadas a la respiración
     Args:
         df: pandas DataFrame
     Returns:
        int: numero de clases
    """
    # filtra por los IDs relacionados a la respiración

    df = df[(df["Ids"] == "[1,2,6,2]") | (df["Ids"] == "[1,2,6,1]")]
    df.to_csv("data/ORFs_respiration.csv", index = False)
    df_2 = df.groupby("Descripciones")["Ids"].count().sort_values(ascending = False)

    print("\n Se ha guardado un archivo con todos los ORFs relacionados respiración")
    print(df_2.plot.bar(x='Descripciones'))

    return(len(df))

    #print("Cantidad de ORFs que se relacionan a la respiración: \n{}".format(df_2))
    #print("\n Se ha guardado un archivo con todos los ORFs relacionados respiración")
    #print(df_2.plot.bar(x='Descripciones'))


def count_class(df, pattern):

    import pandas as pd
    import re

    """
    Dado un Daframe de pandas
    y patrón de búsqueda tipo regex
    cuenta el número de clases que cumplen
    con el patrón.

     Args:
         df: pandas DataFrame
         pattern: patron a buscar dentro
                  del DF tipo str()
     Returns:
        int: numero de clases
    """

    description_ORF = list(set(df["description_ORF"]))
    r_pattern = re.compile(pattern)
    pattern_list = list(filter(r_pattern.match, description_ORF))

    data = df[df['description_ORF'].isin(pattern_list)]
    data_2 = data.groupby("Ids")["Ids"].count().sort_values(ascending = False).head(5)

    #print("Número de clases en el patrón:  {}".format(pattern))
    #print("\n{}".format(len(data)))
    print("\n Principales Clases del pattern: \n")
    print(data_2.plot.bar())
    return len(data)



def mean_ORF_related (df_class, df_ORF, pattern):

    import pandas as pd
    import re

    """
    Dado un Daframe de pandas
    y patrón de búsqueda tipo regex
    calcula la media del número ORFs con
    los que se relaciona el ORF analizado

     Args:
         df: pandas DataFrame
         pattern: patron a buscar dentro
                  del DF tipo str()
     Returns:
        int: numero de clases
    """

    description_ORF = list(set(df_class["description_ORF"]))
    r_pattern = re.compile(pattern)
    pattern_list = list(filter(r_pattern.match, description_ORF))
    data = df_class[df_class['description_ORF'].isin(pattern_list)]
    df_total = pd.merge(data, df_ORF, on="ORF")
    gruped = df_total.groupby("ORF")["ORF_Related"].count().sort_values(ascending = False)
    mean = gruped.mean()

    #print("Número promedio de ORFs con los cuales se relacionan el ORF con el patrón indicado: {}".format(gruped.mean()))
    print("Top ORFs con mayor cantidad de relaciones: \n {}".format(gruped.head(10).plot.bar()))
    return mean


def count_class_multiplos(entero, list_class):


    """
    Dada una lista de clases y
    un número entero, devuelve el
    número de clases que tienen como
    mínimo una dimensión mayor estricta (>) que 0 y a la vez
    múltiple del entero

    Args:
        entero: int, número de interés
        list_class: list Lista de clases

    Returns:
       int: longitud de la lista de clases seleccionadas

    """

    lista = []
    list_class_with_out_none = list(filter(None.__ne__, list_class))
    for i in list_class_with_out_none:
        u = i.strip('][').split(',')
        u = [int(x) for x in u]
        for e in u:
            if e >= entero:
                if (e % entero == 0):
                    if(e >= 1):
                        if(e <= 9):
                            lista.append(i)
    return(len(lista))
    #print("La cantidad de clases de M={}: {}".format(entero, len(lista)))
