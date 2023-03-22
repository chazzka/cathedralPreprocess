from service.request import fetchToJsonWithHeaders
from dataclasses import dataclass
import matplotlib.pyplot as plt

import logging


def postprocess(ids: list, clusters: list, headers):
    logging.info("starting postprocessing")
    # TODO: SEM BUDE VSTUPOVAT JEN DVĚ POLE Z FUNKCE postData
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


# TODO: SEM SE NOVĚ VRAZÍ JEN POLE IDČEK A POLE 1/0 - JE CLUSTER NENI CLUSTER
def prepareListOfRows(idColumn, clusterBoolColumn):
    return list(map(prepareRow, idColumn, clusterBoolColumn))


def prepareRowXML(row: Row):
    return f'<ROW ID=\"{row.id}\" bDevdAvgCurrentAnomaly=\"{not bool(row.bDevdAvgCurrentAnomaly)}\"/>'


def prepareRowsXML(idAnomalyDics: list[Row]):
    return list(map(prepareRowXML, idAnomalyDics))


# @deprecated
def plotPredictedDataFrame(df, timeColumnName, averageColumnName):
    fig = plt.figure()
    ax1 = fig.add_subplot()

    yesCluster = df[(df.isCluster == 0)]
    noCluster = df[(df.isCluster == 1)]

    ax1.scatter(yesCluster[timeColumnName],
                yesCluster[averageColumnName], label='cluster of anomalies')
    ax1.scatter(noCluster[timeColumnName],
                noCluster[averageColumnName], label='correct')
    plt.legend(loc='upper left')
    plt.xlabel("Time")
    plt.ylabel("Observed value")
    plt.show()


def plotXyWithPredicted(xyArray, predicted):
    fig = plt.figure()
    ax1 = fig.add_subplot()

    ax1.scatter(*zip(*xyArray),  c=predicted)
    plt.legend(loc='upper left')
    plt.xlabel("Time")
    plt.ylabel("Observed value")
    plt.show()