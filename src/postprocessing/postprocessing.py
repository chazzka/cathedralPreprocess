from dataclasses import dataclass
import matplotlib.pyplot as plt

import logging


def postprocess(ids: list, clusters: list, headers):
    logging.info("starting postprocessing")
    rows = prepareListOfRows(ids, clusters)
    
    x = prepareRowsXML(rows)
    return headers['result'][2].replace(
        '<ROWDATA/>', '<ROWDATA>' + '\n'.join(x) + '</ROWDATA>')


@dataclass(frozen=True)
class Row:
    id: int
    bDevdAvgCurrentAnomaly: bool


def prepareRow(id: int, cluster: bool):
    return Row(id, cluster)


# idColumn - array of IDs A POLE 1/0
# clusterBoolColumn - array of 1s and 0s (is cluster, not a cluster)
def prepareListOfRows(idColumn, clusterBoolColumn):
    return list(map(prepareRow, idColumn, clusterBoolColumn))


def prepareRowXML(row: Row):
    return f'<ROW ID=\"{row.id}\" bDevdAvgCurrentAnomaly=\"{not bool(row.bDevdAvgCurrentAnomaly)}\"/>'


def prepareRowsXML(idAnomalyDics: list[Row]):
    return list(map(prepareRowXML, idAnomalyDics))


def plotXyWithPredicted(xyArray, predicted):
    fig = plt.figure()
    ax1 = fig.add_subplot()

    ax1.scatter(*zip(*xyArray),  c=predicted)
    plt.legend(loc='upper left')
    plt.xlabel("Time")
    plt.ylabel("Observed value")
    plt.show()