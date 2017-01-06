import argparse
import ntpath
__author__ = 'ivana'
def plot_coef_and_betweenness(graph):
    # setBetweenness(graph,True)
    # getMiuz(graph,True)
    colorList = ["#feebe2", "#fbb4b9", "#f768a1", "#c51b8a", "#7a0177"]
    ranList = [0.2, 0.4, 0.6, 0.8, 1.0]
    sizesList = [1, 1, 1, 1, 1]
    styleCommponent = []
    # styleCommponent.append("edge_color")
    styleCommponent.append("edge_width")
    prop = []
    # prop.append("betweenness")
    prop.append("miuz")
    attributeList = []
    # attributeList.append(colorList)
    attributeList.append(sizesList)
    rangeList = []
    # rangeList.append(ranList)
    rangeList.append(ranList)
    plot_graph_by(graph, styleCommponent, prop, attributeList, rangeList)


def plot_graph_by(graph, styleCommponent, prop, attributeList, rangeList):
    layout = graph.layout_fruchterman_reingold()
    visual_style = {}
    for i in range(len(prop)):
        propList = graph.es[prop[i]]
        ran = rangeList[i]
        attr = create_attribute_list(propList, attributeList[i], ran)
        visual_style[styleCommponent[i]] = attr

    visual_style["edge_label"] = graph.es["name"]
    visual_style["edge_width"] = graph.es["width"]
    visual_style["vertex_color"] = ["#f768a1"] * len(graph.vs)
    visual_style["layout"] = layout
    visual_style["margin"] = 20
    visual_style["bbox"] = (800, 800)
    print "miau"
    plot(graph, **visual_style)


def create_attribute_list(propList, attributeList, rangeList):
    attribute = []
    for value in propList:
        for i in range(len(rangeList)):
            if value <= rangeList[i]:
                attribute.append(attributeList[i])
                break
    return attribute
