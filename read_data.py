
def read_class_functions(path_file):
    import re
    import pandas as pd


    """
    Dado el path del archivo .pl
    devuelve un DF de pandas e imprime el head del df

     Args:
         file: str(path)
     Returns:
         Data Frame de Panda
    """

    load_file = open(path_file, "r")
    read_it = load_file.read().splitlines()
    load_file.close()

    r = re.compile("class.*")
    clases = list(filter(r.search, read_it))

    r_2 = re.compile("function.*")
    funcionts = list(filter(r_2.search, read_it))

    ids = []
    descripciones = []

    for i in clases:
        i = i.replace("(", "")
        i = i.replace(")", "")
        i = i.replace("class", "")
        i = i.replace(".", "")
        id = i[0:9]
        ids.append(id)
        descript = str(i[11:])
        descript = descript.replace('"', "")
        descript = descript.rstrip()
        descripciones.append(descript)

    clases_df = pd.DataFrame({'Ids': ids, 'Descripciones':descripciones})

    orf = []
    for i in funcionts:
        i = i.replace("(", "")
        i = i.replace(")", "")
        i = i.replace("function", "")
        i = i.replace(".", "")
        i = i.replace("'\'", "")
        orf.append(i)

    funciones = pd.DataFrame(orf)
    funciones = funciones[0].str.split('"',expand=True)
    description_ORF = funciones[1]
    funciones = funciones[0].str.split("'",expand=True)
    gen_name = funciones[1]

    fg = []
    for i in funciones[0]:
        i = i.replace(",[", "|[")
        i = i.replace("],", "]")
        fg.append(i)

    funciones_df = pd.DataFrame({"ORF": fg, "gen_name":gen_name, "description_ORF": description_ORF})
    funciones_df[["ORF", "Ids"]] = funciones_df["ORF"].str.split("|",expand=True)
    funciones_clases_df = pd.merge(funciones_df, clases_df, how='left', left_on="Ids", right_on="Ids")
    print("El head del DF: \n\n")
    print(funciones_clases_df.head(5))

    return funciones_clases_df



def read_ORFs_data(files):

    import re
    import pandas as pd

    """
    Dada una lista de archivos de data de ORFs .txt
    devuelve un DataFrame de Pandas con campos:

    ORF: el código o nombre del ORF
    ORF_Related: el ORF con el que se relaciona el ORF del primer campo
    Value: Valor de la relación

     Args:
         file: list(files) una lista de archivos.
     Returns:
         Data Frame de Panda
    """

    def open_and_process(file):
        load_file = open(file, "r")
        read_it = load_file.read().splitlines()
        load_file.close()
        r = re.compile('begin.*|end.*|tb_to_tb_evalue.*')
        read_it = list(filter(r.match, read_it))
        return read_it

    results = list(map(open_and_process, files))
    flat_list = [item for sublist in results for item in sublist]
    pattern = re.compile("begin*.")
    pattern_2 = re.compile("tb_to_tb_evalue*.")

    flat_list_2 = []
    for i in flat_list:
        if pattern.match(i):
            i = i.replace(".", "")
            flat_list_2.append(i)
        elif pattern_2.match(i):
            flat_list_2.append(i)

    records = []
    for i in flat_list_2:
        if pattern.match(i):
            e = i
            e = e.replace("begin(model(", "")
            e = e.replace("))", "")
        else:
            o = i
            o = o.replace('tb_to_tb_evalue(', "")
            o = o.replace(').', "")
            lista = [e, o]
            records.append(lista)

    relaciones = pd.DataFrame.from_records(records, columns = ["ORF", "ORF_Related"])
    relaciones[["ORF_Related", "Value"]] = relaciones["ORF_Related"].str.split(",",expand=True)

    print("Head de los datos de las relaciones entre ORFs: \n")
    print(relaciones.head(5))

    return relaciones
