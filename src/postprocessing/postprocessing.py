from service.request import fetchToJsonWithHeaders
from dataclasses import dataclass
import matplotlib.pyplot as plt
from sklearn.inspection import DecisionBoundaryDisplay

CLUSTER_BOOL_COLUMN = "isCluster"


def postprocess(df, config):
    data = {"_parameters": [config["args"]["apiDataIndentifier"], "", 0]}
    res = fetchToJsonWithHeaders(
        config["server"]["url"], tuple(config["auth"]), data)

    rows = prepareListOfRows(
        df, config["args"]["idColumnName"], CLUSTER_BOOL_COLUMN)

    x = prepareRowsXML(rows)
    return res['result'][2].replace(
        '<ROWDATA/>', '<ROWDATA>' + '\n'.join(x) + '</ROWDATA>')


@dataclass(frozen=True)
class Row:
    id: int
    bDevdAvgCurrentAnomaly: bool


def prepareRow(id: int, cluster: bool):
    return Row(id, cluster)


def prepareListOfRows(df, idColumn, clusterBoolColumn):
    return list(map(prepareRow, df[idColumn], df[clusterBoolColumn]))


def prepareRowXML(row: Row):
    return f'<ROW ID=\"{row.id}\" bDevdAvgCurrentAnomaly=\"{bool(row.bDevdAvgCurrentAnomaly)}\"/>'


def prepareRowsXML(idAnomalyDics: list[Row]):
    return list(map(prepareRowXML, idAnomalyDics))


def plotPredictedDataFrame(df, timeColumnName, averageColumnName):
    fig = plt.figure()
    ax1 = fig.add_subplot()

    yesCluster = df[(df.isAnomaly == -1)]
    noCluster = df[(df.isAnomaly == 1)]

    ax1.scatter(yesCluster[timeColumnName],
                yesCluster[averageColumnName], label='ano')
    ax1.scatter(noCluster[timeColumnName],
                noCluster[averageColumnName], label='no')
    plt.legend(loc='upper left')
    ax1.set_xlabel("Time")
    ax1.set_ylabel("Observed value")
    plt.show()

