import argparse
from pathlib import Path
import csv

import plotly.plotly as py
import plotly.graph_objs as go
import plotly.io as pio

def main(args):
    # check if target file exists and load it
    if(not Path(args.target_csv).is_file()):
        print("Error loading config file")
        exit(-1)

    csv_data = {
        "excess": [],
        "demand_h1h3": [],
        "allocation_h1h3": [],
        "actual_h1h3": [],
        "demand_h2h3": [],
        "allocation_h2h3": [],
        "actual_h2h3": [],
        "x_axis": []
    }

    with Path(args.target_csv).open() as csv_file:
        csv_format = csv.Sniffer().sniff(csv_file.read())
        csv_file.seek(0)
        csv_reader = csv.reader(csv_file, csv_format)
        column_count = len(next(csv_reader))
        csv_file.seek(0)
        for row in csv_reader:
            csv_data["excess"].append(int(row[0]))
            csv_data["demand_h1h3"].append(int(row[1]))
            csv_data["demand_h2h3"].append(int(row[2]))
            csv_data["allocation_h1h3"].append(int(row[3]))
            csv_data["allocation_h2h3"].append(int(row[4]))
            csv_data["actual_h1h3"].append(int(row[5]))
            csv_data["actual_h2h3"].append(int(row[6]))

        csv_data["x_axis"] = list(range(len(csv_data["excess"])))

    print(csv_data)

    if(args.simple):
        simple_graph(csv_data)
    else:
        full_graph(csv_data)

def full_graph(csv_data):

    # Create and style traces
    trace0 = go.Scatter(
        x = csv_data["x_axis"],
        y = csv_data["excess"],
        name = "Excess Bandwidth",
        line = dict(
            color = ('rgb(205, 12, 24)'),
            width = 4)
    )
    trace1 = go.Scatter(
        x = csv_data["x_axis"],
        y = csv_data["demand_h1h3"],
        name = 'Demand H1->H3',
        line = dict(
            color = ('rgb(22, 96, 167)'),
            width = 4,)
    )
    trace2 = go.Scatter(
        x = csv_data["x_axis"],
        y = csv_data["allocation_h1h3"],
        name = "Allocation H1->H3",
        line = dict(
            color = ('rgb(205, 12, 24)'),
            width = 4,
            dash = 'dash') # dash options include 'dash', 'dot', and 'dashdot'
    )
    trace3 = go.Scatter(
        x = csv_data["x_axis"],
        y = csv_data["actual_h1h3"],
        name = 'Actual H1->H3',
        line = dict(
            color = ('rgb(22, 96, 167)'),
            width = 4,
            dash = 'dash')
    )
    trace4 = go.Scatter(
        x = csv_data["x_axis"],
        y = csv_data["demand_h2h3"],
        name = 'Demand H2->H3',
        line = dict(
            color = ('rgb(205, 12, 24)'),
            width = 4,
            dash = 'dot')
    )
    trace5 = go.Scatter(
        x = csv_data["x_axis"],
        y = csv_data["allocation_h2h3"],
        name = 'Allocation H2->H3',
        line = dict(
            color = ('rgb(22, 96, 167)'),
            width = 4,
            dash = 'dot')
    )
    trace6 = go.Scatter(
        x = csv_data["x_axis"],
        y = csv_data["actual_h2h3"],
        name = 'Actual H2->H3',
        line = dict(
            color = ('rgb(22, 96, 167)'),
            width = 4,
            dash = 'dot')
    )
    data = [trace0, trace1, trace2, trace3, trace4, trace5, trace6]

    # Edit the layout
    layout = dict(title = 'Title',
                xaxis = dict(title = 'Time'),
                yaxis = dict(title = 'Bandwidth (Mbps)'),
                )

    fig = dict(data=data, layout=layout)
    #py.plot(fig, filename='styled-line')

    pio.write_image(fig, "fig1.png", format='png', width=1200, height=700, scale=1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("target_csv", help="the csv file to be parsed")
    parser.add_argument("-s", "--simple", action="store_true", help="don't show allocated")
    args = parser.parse_args()
    main(args)
