__author__ = 'ivana'
# -*- coding: utf-8 -*-

import numpy
from Library import *

data = []


def getDataFromFiles(listOfNameFiles):
    results = []
    # en data vamos a añair listas con la información
    robustness = []
    nodos_perdidos = []
    # prje_nodos_removidos = []
    prje_nodos_perdidos = []

    for i in range(4000):
        robustness.append([])
        nodos_perdidos.append([])
        # prje_nodos_removidos.append([])
        prje_nodos_perdidos.append([])

    for name in listOfNameFiles:
        with open(name, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar=',')

            i = (-1)

            for row in reader:
                if i > (-1):
                    print i, row[1]
                    robustness[i].append(float(row[1]))
                    nodos_perdidos[i].append(float(row[2]))
                    # prje_nodos_removidos[i].append(float(row[prje_nodos_removidos]))
                    prje_nodos_perdidos[i].append(float(row[4]))
                    i += 1
                if i == (-1):
                    i = 0

    # mean_nodos_removidos = []
    # std_nodos_removidos = []
    mean_robustness = []
    std_robustness = []
    mean_nodos_perdidos = []
    std_nodos_perdidos = []
    # mean_prje_nodos_removidos = []
    # std_prje_nodos_removidos = []
    mean_prje_nodos_perdidos = []
    std_prje_nodos_perdidos = []
    for i in range(999):
        # mean_nodos_removidos.append(numpy.mean(nodos_removidos[i]))
        # std_nodos_removidos.append(numpy.std(nodos_removidos[i]))

        mean_robustness.append(numpy.mean(robustness[i]))
        std_robustness.append(numpy.std(robustness[i]))

        mean_nodos_perdidos.append(numpy.mean(nodos_perdidos[i]))
        std_nodos_perdidos.append(numpy.std(nodos_perdidos[i]))

        # mean_prje_nodos_removidos.append(numpy.mean(prje_nodos_removidos[i]))
        # std_prje_nodos_removidos.append(std.mean(prje_nodos_removidos[i]))

        mean_prje_nodos_perdidos.append(numpy.mean(prje_nodos_perdidos[i]))
        std_prje_nodos_perdidos.append(numpy.std(prje_nodos_perdidos[i]))

    results = [mean_robustness, std_robustness,
               mean_nodos_perdidos, std_nodos_perdidos,
               mean_prje_nodos_perdidos, std_prje_nodos_perdidos]
    return results


def writeResults(results, name):
    with open(name, 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["nodos removidos", "promedio robustness", "desviación robustness", "promedio nodos perdidos",
                         "desviación nodos perdidos",
                         "promedio p.nodos perdidos", "desviación p.nodos perdidos"])
        for i in range(999):
            writer.writerow(
                [i, results[0][i], results[1][i], results[2][i], results[3][i], results[4][i], results[5][i]])


# generateNames(name, amount,type)

metrics = ["miuz"]

for metrica in metrics:
    listOfNameFilesSeq = generate_names('PL19/edgeDecay/PL19v', 50, 'decay_by_seq_betweenness.csv')
    resultadosSeq = getDataFromFiles(listOfNameFilesSeq)
    write_results(resultadosSeq, 'PL19/edgeDecay/PL19_edgeBetweenness_resultados_seq_decay.csv')

    listOfNameFilesSeq = generate_names('PL19/edgeDecay/PL19v', 50, 'decay_by_seq_miuz.csv')
    resultadosSeq = getDataFromFiles(listOfNameFilesSeq)
    write_results(resultadosSeq, 'PL19/edgeDecay/PL19_edgeMiuz_resultados_seq_decay.csv')

    listOfNameFilesSeq = generate_names('PL18/edgeDecay/PL18v', 50, 'decay_by_seq_betweenness.csv')
    resultadosSeq = getDataFromFiles(listOfNameFilesSeq)
    write_results(resultadosSeq, 'PL18/edgeDecay/PL18_edgeBetweenness_resultados_seq_decay.csv')

    listOfNameFilesSeq = generate_names('PL18/edgeDecay/PL18v', 50, 'decay_by_seq_miuz.csv')
    resultadosSeq = getDataFromFiles(listOfNameFilesSeq)
    write_results(resultadosSeq, 'PL18/edgeDecay/PL18_edgeMiuz_resultados_seq_decay.csv')
