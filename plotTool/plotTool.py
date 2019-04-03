import argparse
from pathlib import Path
import csv

import plotly.plotly as py
import plotly.graph_objs as go
import plotly.io as pio

def main(args):
    # check if target file exists and load it
    if(not Path(args.target_csv).is_file()):
        print("Error loading target csv file")
        exit(-1)

    if(args.title is not None):
        title = args.title
    else:
        title = "Bandwidth over time"

    csv_data = {
        "excess": [],
        "demand_h1h3": [],
        "allocation_h1h3": [],
        # "actual_h1h3": [],
        "demand_h2h3": [],
        "allocation_h2h3": [],
        # "actual_h2h3": [],
        "x_axis": []
    }

    with Path(args.target_csv).open() as csv_file:
        csv_format = csv.Sniffer().sniff(csv_file.read())
        csv_file.seek(0)
        csv_reader = csv.reader(csv_file, csv_format)
        column_count = len(next(csv_reader))
        csv_file.seek(0)
        for row in csv_reader:
            csv_data["excess"].append(float(row[0]))
            csv_data["demand_h1h3"].append(float(row[1]))
            csv_data["demand_h2h3"].append(float(row[2]))
            csv_data["allocation_h1h3"].append(float(row[3]))
            csv_data["allocation_h2h3"].append(float(row[4]))
            # csv_data["actual_h1h3"].append(float(row[5]))
            # csv_data["actual_h2h3"].append(float(row[6]))

        csv_data["x_axis"] = list(range(len(csv_data["excess"])))

    # print(csv_data)

    data = full_graph(csv_data)

    # Edit the layout
    layout = dict(title = title,
                xaxis = dict(title = "Time"),
                yaxis = dict(title = "Bandwidth (Mbps)"),)

    fig = dict(data=data, layout=layout)

    pio.write_image(fig, args.output_name, width=1200, height=700, scale=1)

    
# full detailed graph
def full_graph(csv_data):
    # Create and style traces
    trace0 = go.Scatter(
        x = csv_data["x_axis"],
        y = csv_data["excess"],
        name = "Excess Bandwidth",
        line = dict(
            color = ("#B18FCF"),
            width = 4,
            dash = "dashdot")
    )
    trace1 = go.Scatter(
        x = csv_data["x_axis"],
        y = csv_data["demand_h1h3"],
        name = "Demand H1->H3",
        line = dict(
            color = ("#DF2935"),
            width = 4,)
    )
    trace2 = go.Scatter(
        x = csv_data["x_axis"],
        y = csv_data["allocation_h1h3"],
        name = "Allocation H1->H3",
        line = dict(
            color = ("#E9724C"),
            width = 4,
            dash = "dot") # dash options include 'dash', 'dot', and 'dashdot'
    )
    # trace3 = go.Scatter(
    #     x = csv_data["x_axis"],
    #     y = csv_data["actual_h1h3"],
    #     name = "Actual H1->H3",
    #     line = dict(
    #         color = ("#FFC857"),
    #         width = 4,
    #         dash = "dash")
    # )
    trace4 = go.Scatter(
        x = csv_data["x_axis"],
        y = csv_data["demand_h2h3"],
        name = "Demand H2->H3",
        line = dict(
            color = ("#0E79B2"),
            width = 4,)
    )
    trace5 = go.Scatter(
        x = csv_data["x_axis"],
        y = csv_data["allocation_h2h3"],
        name = "Allocation H2->H3",
        line = dict(
            color = ("#06D6A0"),
            width = 4,
            dash = "dot")
    )
    # trace6 = go.Scatter(
    #     x = csv_data["x_axis"],
    #     y = csv_data["actual_h2h3"],
    #     name = "Actual H2->H3",
    #     line = dict(
    #         color = ("#2C365E"),2C365E
    #         width = 4,
    #         dash = "dash")
    # )
    # data = [trace0, trace1, trace2, trace3, trace4, trace5, trace6]
    data = [trace0, trace1, trace2, trace4, trace5]
    return data


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("target_csv", help="the csv file to be parsed")
    parser.add_argument("output_name", help="filename of graph to output")
    parser.add_argument("-t", "--title", metavar="graph_title", help="graph title")
    args = parser.parse_args()
    main(args)
