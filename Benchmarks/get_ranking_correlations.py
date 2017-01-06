# -*- coding: utf-8 -*-
__author__ = 'ivana'
import Library
import numpy
import scipy.stats
import scipy
import argparse
import ntpath

parser = argparse.ArgumentParser(description="get_ranking_correlations obtains the correlation rankings generated"
                                             " by ordering nodes by its metric value for two graph metrics."
                                             " This process is made over a list of graphs and returns a list of "
                                             "correlations for each graph on the list.")

parser.add_argument('-m', '--metrics', metavar='metric', type=str, nargs='+',
                    help='Set of metrics that will be used to calculate over the input graph or generated graph.\n'
                         ' Available metrics:\n'
                         '- betweenness \n'
                         '- degree \n'
                         '- harmonic \n'
                         '- miuz \n'
                         '- clustering \n'
                         '- eigenvector \n'
                         '- coreness \n'
                         '- closeness \n'
                         '- value \n'
                         '- lcc -')
################################# value parameters #######################################
parser.add_argument('-d', '--delta', type=str, default=0,
                    help='This parameter is for the use of the metric value only. In any other case it will be ignored')

parser.add_argument('-w', '--weight', type=str, default=0,
                    help='This parameter is for the use of the metric value only. In any other case it will be ignored.'
                         ' Depending on the type specified the weight will be the same for everyone or not.')

parser.add_argument('-c', '--cost', type=str, default=0,
                    help='This parameter is for the use of the metric value only. In any other case it will be ignored.'
                         ' The cost will be the same for every edge.')

parser.add_argument('-t', '--type', type=str, default='all',
                    help='This parameter is for the use of the metric value only. In any other case it will be ignored.'
                         ' If the type is \'all\' every node has the same weight. If the type is \'ten\' then only the '
                         '10 percent of the nodes with the higher degree.')
###########################################################################################

parser.add_argument('-i', '--input', type=str, nargs='+', default='',
                    help='Calculations will be made over every graph of the input.Each graph must contain a csv file '
                         'with the following'
                         ' format: Every line must contain an edge, this edge is represented by the node_a and node_b'
                         ' '
                         'it connects as \'node_a,node_b\'.')

parser.add_argument('-o', '--output',metavar='OUTPUT_FOLDER', type=str, default='',
                    help='Path to the folder where results of the calculations will be stored. Defaults to current'
                         ' working directory.')
parser.add_argument('-n', '--output_name', type=str, default='',
                    help='name of the output FILE, do not include type')


args = parser.parse_args()
ho,to = ntpath.split(args.output)
output_path = ho
# This is a list
input_path_list = args.input
metrics = args.metrics
output_name = args.output_name

####
# Aca tiene que ir la verificacion de que me pasaron las cosas que necesito
#
# --> una lista no vacia de archivos
# --> 2 metricas (ni mas ni menos)
# --> ver que las metricas las tenga hechas
####

correlation_lst = []
results = []
for file_name in input_path_list:
    rankings = {}
    rankings[metrics[0]] = []
    rankings[metrics[1]] = []
    for metric in metrics:
        # Obtener un ranking por cada metrica
        g = Library.generate_graph_from_file(file_name)
        params = []
        if metric == "value":
            delta = float(args.delta)
            weight =float(args.weight)
            cost = float(args.cost)
            if args.cost != 0:
                cost_list = [cost]*len(g.es)
            else:
                cost_list = []
            if args.type == 'all':
                weight_list = [weight]*len(g.vs)
            elif args.type =='ten':
                weight_list = [0]*len(g.vs)
                Library.set_one_metric(g,'degree')
                lst = g.vs['degree']
                sorted_node_lst = []
                for p in range(len(lst)):
                    sorted_node_lst.append((p, lst[p]))
                sorted_node_lst = sorted(sorted_node_lst, key=Library.get_second_key, reverse=True)
                weight_list = [0]*len(g.vs)
                for i in range(int(0.1*len(g.vs))):
                    index = sorted_node_lst[i][0]
                    weight_list[index] = weight
            print "-------------", len(weight_list)
            params = [delta, weight_list, cost_list]

        Library.set_one_metric(g,metric, parameters=params)
        lst = g.vs[metric]
        sorted_node_lst = []
        for p in range(len(lst)):
            sorted_node_lst.append((p, lst[p]))
        sorted_node_lst = sorted(sorted_node_lst, key=Library.get_second_key, reverse=True)
        rankings[metric] = sorted_node_lst
    #calcular la correlacion
    tau, p_value = scipy.stats.kendalltau(rankings[metrics[0]], rankings[metrics[1]])
    #agregar la correlacion a una lista de correlaciones
    correlation_lst.append(tau)
    results.append([file_name,str(tau)])
#calcular el promedio de las correlaciones
correlation_mean = numpy.mean(correlation_lst)
#calcular la desviación estándar de las correlaciones
correlation_std = numpy.std(correlation_lst)
# imprimir : 'filename' 'correlacion'
#            'promedio' 'desviación estandar'
## el filename debe indicar que tipo de métricas se correlacionaron
results.append([str(correlation_mean),str(correlation_std)])
save_file_name = ""
if not ho == "":
    save_file_name = ho + "/" + output_name + ".csv"
    print save_file_name
Library.write_results(["filename/mean","correlation/std"],results,save_file_name)
