__author__ = 'ivana'
# -*- coding: utf-8 -*-

from igraph import *
import random
import datetime
import csv

def write_graph(graph, title):
    number_of_nodes = len(graph.vs)
    title += '_graph_numberOfNodes_' + str(number_of_nodes) + '.csv'
    with open(title, 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
        lst = graph.get_edgelist()
        for i in range(len(lst)):
            writer.writerow([lst[i][0], lst[i][1]])


def is_on_available_metrics(lst):
    metrics = ["miuz", "miuz2", "closeness", "coreness", "clustering", "degree", "harmonic", "eigenvector", "betweenness", "lcc"]
    for m in lst:
        if m not in metrics:
            return False
    return True


def set_one_metric(graph, metric, edge_metric=False, parameters=[]):
    if metric == "betweenness":
        set_betweenness(graph, edge_metric)
    if metric == "miuz":
        set_miuz(graph, edge_metric)
    if metric == "closeness":
        graph.vs["closeness"] = graph.closeness()
    if metric == "clustering":
        graph.vs["clustering"] = graph.transitivity_local_undirected(mode="nan")
    if metric == "eigenvector":
        graph.vs["eigenvector"] = graph.eigenvector_centrality(directed=False)
    if metric == "coreness":
        graph.vs["coreness"] = graph.coreness()
    if metric == "degree":
        graph.vs["degree"] = graph.degree()
    if metric == "harmonic":
        set_harmonic(graph)
    if metric == "lcc":
        set_largest_cc_inverted(graph, edge_metric)
    if metric == "miuz2":
        set_miuz2(graph, edge_metric)
    if metric == "value":
        initial_value = graph_value(graph, parameters[0], parameters[1], parameters[2])
        set_graph_value(graph, initial_value, parameters)


def set_harmonic(graph):
    number_of_nodes = len(graph.vs)
    distances = graph.shortest_paths()
    sum = 0
    harmonics = []
    for i in range(number_of_nodes):
        for j in range(number_of_nodes):
            if i != j:
                sum += 1.0 / distances[i][j]
        harmonics.append((1.0 / (number_of_nodes - 1)) * sum)
        sum = 0
    graph.vs["harmonic"] = harmonics


def get_length_key(item):
    return len(item)


def make_graph_copy(graph, attribute_list=[]):
    new_graph = Graph()
    new_graph.add_vertices(len(graph.vs))
    new_graph.add_edges(graph.get_edgelist())
    for attribute in attribute_list:
        new_graph.vs[attribute] = graph.vs[attribute]
    return new_graph


def get_second_key(item):
    return item[1]


def set_betweenness(graph, edgeMetric=False):
    if edgeMetric:
        graph.es["betweenness"] = graph.edge_betweenness(directed=False)
    else:
        n = len(graph.vs)
        betweenness_list = graph.betweenness(directed=False)
        if n > 2:
            graph.vs["betweenness"] = [var / ((n - 1) * (n - 2) / 2.0) for var in betweenness_list]
        else:
            graph.vs["betweenness"] = betweenness_list


def weight_function(item):
    return len(item) * 1.0


def set_largest_cc_inverted(original_graph, edge_metric=False):
    if edge_metric:
        original_graph_node_list = original_graph.es
        original_graph_number_of_nodes = len(original_graph_node_list)
        original_graph.es["lcc"] = [0] * original_graph_number_of_nodes
    else:
        original_graph_node_list = original_graph.vs
        original_graph_number_of_nodes = len(original_graph_node_list)
        original_graph.vs["lcc"] = [0] * original_graph_number_of_nodes

    for i in range(original_graph_number_of_nodes):
        is_isolated = True
        if not edge_metric:
            is_isolated = len(original_graph.neighbors(i)) <= 1
        if edge_metric:
            node_1 = original_graph.get_edgelist()[i][0]
            node_2 = original_graph.get_edgelist()[i][1]
            node_1_degree = len(original_graph.neighbors(node_1))
            node_2_degree = len(original_graph.neighbors(node_2))
            is_isolated = node_1_degree <= 1 or node_2_degree <= 1
            if is_isolated:
                lcc = 1.0 / (1.0 * len(original_graph.vs) - 1.0)
                original_graph.es[i]["lcc"] = lcc

        if not is_isolated:
            graph = make_graph_copy(original_graph)
            if edge_metric:
                graph.delete_edges(i)
            else:
                graph.delete_vertices([i])

            connected_components = graph.components(mode=STRONG)
            ordered_connected_components = sorted(connected_components, key=get_length_key, reverse=True)
            lcc = 1.0/get_length_key(ordered_connected_components[0])
            if edge_metric:
                original_graph.es[i]["lcc"] = lcc
            else:
                original_graph.vs[i]["lcc"] = lcc

def set_miuz(original_graph, edge_metric=False):

    if edge_metric:
        original_graph_node_list = original_graph.es
        original_graph_number_of_nodes = len(original_graph_node_list)
        original_graph.es["miuz"] = [0] * original_graph_number_of_nodes
    else:
        original_graph_node_list = original_graph.vs
        original_graph_number_of_nodes = len(original_graph_node_list)
        original_graph.vs["miuz"] = [0] * original_graph_number_of_nodes

    for i in range(original_graph_number_of_nodes):
        is_isolated = True
        if not edge_metric:
            is_isolated = len(original_graph.neighbors(i)) <= 1
        if edge_metric:
            node_1 = original_graph.get_edgelist()[i][0]
            node_2 = original_graph.get_edgelist()[i][1]
            node_1_degree = len(original_graph.neighbors(node_1))
            node_2_degree = len(original_graph.neighbors(node_2))
            is_isolated = node_1_degree <= 1 or node_2_degree <= 1
            if is_isolated:
                miuz = 1.0 / (1.0 * len(original_graph.vs) - 1.0)
                original_graph.es[i]["miuz"] = miuz

        if not is_isolated:
            graph = make_graph_copy(original_graph)
            initial_number_of_connected_components = len(graph.components(mode=STRONG))
            if edge_metric:
                graph.delete_edges(i)
            else:
                graph.delete_vertices([i])

                # cambiar por quitarle los arcos

            connected_components = graph.components(mode=STRONG)
            number_of_connected_components = len(connected_components)
            if number_of_connected_components > initial_number_of_connected_components:
                ordered_connected_components = sorted(connected_components, key=get_length_key)
                sum = 0
                for n in range(number_of_connected_components - 1):
                    sum += weight_function(ordered_connected_components[n])
                print sum, len(ordered_connected_components[number_of_connected_components - 1]), i
                miuz = sum / len(ordered_connected_components[number_of_connected_components - 1])
                if edge_metric:
                    original_graph.es[i]["miuz"] = miuz
                else:
                    original_graph.vs[i]["miuz"] = miuz
    #print original_graph.vs["miuz"], "miuz"


def set_miuz2(original_graph, edge_metric=False):

    if edge_metric:
        original_graph_node_list = original_graph.es
        original_graph_number_of_nodes = len(original_graph_node_list)
        original_graph.es["miuz2"] = [0] * original_graph_number_of_nodes
    else:
        original_graph_node_list = original_graph.vs
        original_graph_number_of_nodes = len(original_graph_node_list)
        original_graph.vs["miuz2"] = [0] * original_graph_number_of_nodes

    for i in range(original_graph_number_of_nodes):
        is_isolated = True
        if not edge_metric:
            is_isolated = len(original_graph.neighbors(i)) <= 1
        if edge_metric:
            node_1 = original_graph.get_edgelist()[i][0]
            node_2 = original_graph.get_edgelist()[i][1]
            node_1_degree = len(original_graph.neighbors(node_1))
            node_2_degree = len(original_graph.neighbors(node_2))
            is_isolated = node_1_degree <= 1 or node_2_degree <= 1
            if is_isolated:
                miuz = 1.0 / (1.0 * len(original_graph.vs) - 1.0)
                original_graph.es[i]["miuz2"] = miuz

        if not is_isolated:
            graph = make_graph_copy(original_graph)
            initial_number_of_connected_components = len(graph.components(mode=STRONG))
            if edge_metric:
                graph.delete_edges(i)
            else:
                for n in graph.neighborhood(i):
                    if n != i:
                        graph.delete_edges([(n,i)])
            connected_components = graph.components(mode=STRONG)
            number_of_connected_components = len(connected_components)
            if number_of_connected_components > initial_number_of_connected_components:
                ordered_connected_components = sorted(connected_components, key=get_length_key)
                sum = 0
                for n in range(number_of_connected_components - 1):
                    sum += weight_function(ordered_connected_components[n])
                print sum, len(ordered_connected_components[number_of_connected_components - 1]),"miuz2",i
                miuz = sum / len(ordered_connected_components[number_of_connected_components - 1])
                if edge_metric:
                    original_graph.es[i]["miuz2"] = miuz
                else:
                    original_graph.vs[i]["miuz2"] = miuz
    #print original_graph.vs["miuz2"]



def weighted_choice(choices):
    total = sum(w for c, w in choices)
    r = random.uniform(0, total)
    up_to = 0
    for c, w in choices:
        if up_to + w > r:
            return c
        up_to += w
    assert False, "Shouldn't get here"


def get_degrees_power_law(n, lamda):
    choices = []
    for i in range(n):
        choices.append(((i + 1), math.pow((i + 1), -1.0 * lamda)))
    node_degrees = []
    for i in range(n):
        node_degrees.append(weighted_choice(choices))
    if sum(node_degrees) % 2 != 0:
        node_degrees[0] += 1
    return node_degrees


def generate_power_law_graph(n, lamda, epsilon):
    node_degrees = get_degrees_power_law(n, lamda)
    while True:
        try:
             g = Graph.Degree_Sequence(node_degrees, method="vl")
             # print "------------------------", alpha, lamda, "--------------------------"
             print "success"
             return g
        except Exception, e:
             #diff = epsilon + 1
             node_degrees = get_degrees_power_law(n, lamda)
             #print "try again"
             pass

    return g
    # results = powerlaw.Fit(node_degrees, discrete=True)
    # alpha = results.power_law.alpha
    # diff = math.fabs(alpha - lamda)
    #
    # while True:
    #     while (diff > epsilon):
    #         node_degrees = get_degrees_power_law(n, lamda)
    #         results = powerlaw.Fit(node_degrees, discrete=True, suppress_output=True)
    #
    #         alpha = results.power_law.alpha
    #         diff = math.fabs(alpha - lamda)
    #     try:
    #         g = Graph.Degree_Sequence(node_degrees, method="vl")
    #         print "------------------------", alpha, lamda, "--------------------------"
    #         return g
    #     except Exception, e:
    #         diff = epsilon + 1
    #         pass



def generate_names(ubication_and_name, amount, end_and_type):
    result = []
    for i in range(amount):
        file_name = ubication_and_name + str(i + 1) + end_and_type
        result.append(file_name)
    return result


def write_results(columns, results, save_file_name):
    results_len = len(results)
    with open(save_file_name, 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(columns)
        for i in range(results_len):
            writer.writerow(results[i])


def generate_graph_from_file(file_name):
    rename_map = {}
    k = 0
    with open(file_name, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar=',')
        edge_list = []
        for row in reader:
            first = row[0]
            second = row[1]
            if first not in rename_map:
                rename_map[first] = k
                k += 1
            if second not in rename_map:
                rename_map[second] = k
                k += 1
            edge_list.append((rename_map[first], rename_map[second]))
    number_of_nodes = len(rename_map)
    g = Graph()
    g.add_vertices(number_of_nodes)
    g.add_edges(edge_list)
    return g


def order_list_of_metric(lst, dict=None):
    metric_list = []
    for p in range(len(lst)):
        metric_list.append((p, lst[p]))
        if dict is not None:
            dict[p] = lst[p]
    metric_list = sorted(metric_list, key=get_second_key, reverse=True)
    return metric_list


def remove_by_seq(graph_attack, graph_states, edge_metric=False):
    g = make_graph_copy(graph_states[0], ["estoy"])
    elements_lost = 0
    current_cc = len(g.components(mode=STRONG))
    graph_attack.decide_attack(g, edge_metric)
    element = graph_attack.get_element_to_remove()
    if edge_metric:
        g.delete_edges(element)
    else:
        neighbors = g.neighbors(element)
        for n in neighbors:
            g.delete_edges([(element, n)])

    graph_states[0] = g
    connected_components = sorted(g.components(mode=STRONG), key=get_length_key, reverse=True)
    survivor_component = connected_components[0]
    if len(g.components(mode=STRONG)) > current_cc:
        for j in range(len(g.vs)):
            if j not in survivor_component:
                g.vs[j]["estoy"] = False
                elements_lost += 1
            else:
                g.vs[j]["estoy"] = True
    else:
        for j in range(len(g.vs)):
            if not g.vs[j]["estoy"]:
                elements_lost += 1
    return elements_lost


def get_robustness(graph):
    connected_components = sorted(graph.components(mode=STRONG), key=get_length_key, reverse=True)
    big_component = connected_components[0]
    robustness = len(big_component) * 1.0 / (len(graph.vs))
    return robustness


def write_decay_by(graph, title, attack_name, graph_attack, is_seq=True, edge_metric=False):
    if is_seq:
        title += 'decay_by_seq_' + attack_name + '.csv'
    else:
        title += 'decay_by_' + attack_name + '.csv'
    total = len(graph.vs)
    amount_of_nodes = total
    if edge_metric:
        total = len(graph.es)

    graph.vs["estoy"] = [True] * len(graph.vs)
    graph_states = [graph]
    with open(title, 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
        if edge_metric:
            writer.writerow(['edges removed', 'Robustness', 'nodes lost', 'percentage of edges removed',
                             'percentage of nodes lost'])
        else:
            writer.writerow(['nodes removed', 'Robustness', 'nodes lost', 'percentage of nodes removed',
                             'percentage of nodes lost'])
        for i in range(total - 1):
            j = i + 1
            if is_seq:
                if edge_metric:
                    elements_lost = remove_by_seq(graph_attack, graph_states, edge_metric=True)
                else:
                    elements_lost = remove_by_seq(graph_attack, graph_states)
            else:
                pass
            robustness = get_robustness(graph_states[0])
            nodes_removed = j
            percentage_of_elemts_lost = elements_lost * 1.0 / amount_of_nodes
            percentage_of_nodes_removed = nodes_removed * 1.0 / amount_of_nodes
            writer.writerow([nodes_removed, robustness, elements_lost, percentage_of_nodes_removed,
                             percentage_of_elemts_lost])


def graph_value(graph, delta, weight_list = [], link_cost = []):

    value = 0
    recent_sum = 0

    if weight_list != [] and len(graph.vs) == len(weight_list):
        graph.vs["weight"] = weight_list
    elif weight_list != [] and len(graph.vs) != len(weight_list):
        print "Error, weights list must have the same size as the node list", len(weight_list), len(graph.vs)

    shortest_path_matrix = [[0 for x in range(len(graph.vs))] for y in range(len(graph.vs))]

    for node_1 in graph.vs:
        for node_2 in graph.vs:
            if shortest_path_matrix[node_1.index][node_2.index] == 0:
                path = graph.get_shortest_paths(node_1.index)
                for i in range(len(graph.vs)):
                    shortest_path_matrix[node_1.index][i] = path[i]
                    shortest_path_matrix[i][node_1.index] = list(reversed(path[i]))
            path = shortest_path_matrix[node_1.index][node_2.index]
            if node_1.index != node_2.index:
                if path != []:
                    path = filter(lambda x: x != node_1.index, path)
                    for i in range(len(path)):
                        recent_sum += graph.vs["weight"][path[i]]*pow(delta,(i+1))
                        value += graph.vs["weight"][path[i]]*pow(delta,(i+1))
                    recent_sum = 0
            else:
                recent_sum += graph.vs["weight"][path[0]]*pow(delta,(0))
                value += graph.vs["weight"][path[0]]*pow(delta,(0))
                recent_sum = 0
    if len(link_cost) > 0 and len(graph.es) == len(link_cost):
        # Here you should put how to use the costs, do I just put 'em or do I specify which ones I'd like to count
        # For now I consider that the list is all considered (if sth has no cost its cost must be 0)
        graph.es["cost"] = link_cost
    elif len(link_cost) > 0 and len(graph.es) != len(link_cost):
        print "Error, costs list must have the same size as the edge list"
    cost = 0
    if len(link_cost) > 0:
        cost = sum(graph.es["cost"])
    return value


def value_damage(initial_value, node, graph, delta, weight_list = [], link_cost = []):
    #value = graph_value(graph, delta, weight_list, link_cost)
    graph_copy = make_graph_copy(graph)
    graph_copy.delete_vertices(node)
    new_weight_list = list(weight_list)
    new_weight_list.remove(new_weight_list[node])
    value_after_removal = graph_value(graph_copy, delta, new_weight_list, link_cost)
    print "VALUE",initial_value - value_after_removal
    return (initial_value - value_after_removal)

def set_graph_value(graph, initial_value, parameters):
    delta = parameters[0]
    weight_lst = parameters[1]
    link_cost_list = parameters[2]
    graph.vs["value"] = [0]*len(graph.vs)
    for node in graph.vs:
        print node.index, "NODE --------------", datetime.datetime.now().time()
        graph.vs["value"][node.index] = value_damage(initial_value, node.index, graph, delta, weight_list = weight_lst,
                                                     link_cost = link_cost_list)




# g = Graph()
# g.add_vertices(3)
# g.add_edges([(0,1),(0,2)])
# set_graph_value(g, [0.9,[1,1,1],[]])
#print value_damage(0,g,0.9,weight_list = [1,1,1])

