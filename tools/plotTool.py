import argparse
from pathlib import Path
import csv
import statistics

import plotly.graph_objs as go
import plotly.io as pio


# Graphs the output csvs from the controller.py
# Only works for the H1,H2 -> H3 setup
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
        "demand_h2h3": [],
        "alloc_h1h3": [],
        "alloc_h2h3": [],
        "high_h1h3": [],
        "high_h2h3": [],
        "med_h1h3": [],
        "med_h2h3": [],
        "low_h1h3": [],
        "low_h2h3": [],
        "minrate_h1": [],
        "minrate_h2": [],
        "actual_h1h3": [],
        "actual_h2h3": [],
        "x_axis": [],
    }

    with Path(args.target_csv).open() as csv_file:
        csv_format = csv.Sniffer().sniff(csv_file.read())
        csv_file.seek(0)
        csv_reader = csv.reader(csv_file, csv_format)
        for row in csv_reader:
            csv_data["excess"].append(float(row[0]))

            csv_data["demand_h1h3"].append(float(row[1]))
            csv_data["demand_h2h3"].append(float(row[2]))

            csv_data["alloc_h1h3"].append(float(row[3]))
            csv_data["alloc_h2h3"].append(float(row[4]))

            csv_data["high_h1h3"].append(float(row[5]))
            csv_data["high_h2h3"].append(float(row[6]))

            csv_data["med_h1h3"].append(float(row[7]))
            csv_data["med_h2h3"].append(float(row[8]))

            csv_data["low_h1h3"].append(float(row[9]))
            csv_data["low_h2h3"].append(float(row[10]))

            csv_data["minrate_h1"].append(float(row[11]))
            csv_data["minrate_h2"].append(float(row[12]))

        csv_data["actual_h1h3"] = [sum(pair) for pair in zip(csv_data["high_h1h3"], csv_data["med_h1h3"])]
        csv_data["actual_h2h3"] = [sum(pair) for pair in zip(csv_data["high_h2h3"], csv_data["med_h2h3"])]

        csv_data["x_axis"] = list(range(len(csv_data["excess"])))

    if(args.type is not None):
        if(args.type == "h1"):
            data = h1_graph(csv_data)
        elif(args.type == "h2"):
            data = h2_graph(csv_data)
        else:
            data = full_graph(csv_data)
    else:
        data = full_graph(csv_data)

    # Edit the layout
    layout = dict(
        title=title,
        xaxis=dict(title="Time (seconds)"),
        yaxis=dict(title="Bandwidth (Mbps)"),
        )

    fig = dict(data=data, layout=layout)

    if(args.output_name is None):
        output_file = "{}_{}.png".format(Path(args.target_csv).stem, args.type)
    else:
        output_file = args.output_name

    pio.write_image(fig, output_file, width=FIG_WIDTH, height=FIG_HEIGHT, scale=1)
    print("Graph written to {}".format(output_file))
    if(args.stats is not None):
        print("--- STATS ---")
        print("- Median -")
        for name, col in csv_data.items():
            col_median = statistics.median(col)
            print("{}: \t{}".format(name, col_median))
        print("-------------")


# full detailed graph
# shows:
# H1 demand
# H2 demand
# H1 alloc
# H2 alloc
# H1 actual
# H2 actual
def full_graph(csv_data):
    # Create and style traces

    # excess_trace = go.Scatter(
    #     x = csv_data["x_axis"],
    #     y = csv_data["excess"],
    #     name = "Excess Bandwidth",
    #     line = dict(
    #         color = ("#B18FCF"),
    #         width = 4,
    #         dash = "dashdot")
    # )
    h1_demand_trace = go.Scatter(
        x=csv_data["x_axis"],
        y=csv_data["demand_h1h3"],
        name="Demand H1->H3",
        line=dict(
            color=D_RED,
            width=TWO_LINE_SIZE,
            ),
    )
    h1_alloc_trace = go.Scatter(
        x=csv_data["x_axis"],
        y=csv_data["alloc_h1h3"],
        name="Allocation H1->H3",
        line=dict(
            color=D_ORANGE,
            width=TWO_LINE_SIZE,
            dash="dot",  # dash options include 'dash', 'dot', and 'dashdot'
            ),
    )
    h1_actual_trace = go.Scatter(
        x=csv_data["x_axis"],
        y=csv_data["actual_h1h3"],
        name="Actual H1->H3",
        line=dict(
            color=D_YELLOW,
            width=TWO_LINE_SIZE,
            dash="dashdot",
            ),
    )
    h2_demand_trace = go.Scatter(
        x=csv_data["x_axis"],
        y=csv_data["demand_h2h3"],
        name="Demand H2->H3",
        line=dict(
            color=D_GREEN,
            width=TWO_LINE_SIZE,
            ),
    )
    h2_alloc_trace = go.Scatter(
        x=csv_data["x_axis"],
        y=csv_data["alloc_h2h3"],
        name="Allocation H2->H3",
        line=dict(
            color=D_BLUE,
            width=TWO_LINE_SIZE,
            dash="dot",
            ),
    )
    h2_actual_trace = go.Scatter(
        x=csv_data["x_axis"],
        y=csv_data["actual_h2h3"],
        name="Actual H2->H3",
        line=dict(
            color=D_PURPLE,
            width=TWO_LINE_SIZE,
            dash="dashdot",
            ),
    )

    data = [h1_demand_trace, h2_demand_trace, h1_alloc_trace, h2_alloc_trace, h1_actual_trace, h2_actual_trace]
    return data


# h1 graph - warm colours
# shows:
# H1 demand
# H1 allocation
# H1 actual
# H1 high priority
# H1 med priority
# H1 low priority (dropped)
def h1_graph(csv_data):
    # Create and style traces
    demand_trace = go.Scatter(
        x=csv_data["x_axis"],
        y=csv_data["demand_h1h3"],
        name="Demand H1->H3",
        line=dict(
            color=D_RED,
            width=ONE_LINE_SIZE,
            ),
    )
    alloc_trace = go.Scatter(
        x=csv_data["x_axis"],
        y=csv_data["alloc_h1h3"],
        name="Allocation H1->H3",
        line=dict(
            color=D_ORANGE,
            width=ONE_LINE_SIZE,
            dash="dot",
            ),
    )
    actual_trace = go.Scatter(
        x=csv_data["x_axis"],
        y=csv_data["actual_h1h3"],
        name="Actual H1->H3",
        line=dict(
            color=D_YELLOW,
            width=TWO_LINE_SIZE,
            dash="dashdot",
            ),
    )
    high_trace = go.Scatter(
        x=csv_data["x_axis"],
        y=csv_data["high_h1h3"],
        name="High Priority H1->H3",
        line=dict(
            color=D_GREEN,
            width=ONE_LINE_SIZE,
            ),
    )
    med_trace = go.Scatter(
        x=csv_data["x_axis"],
        y=csv_data["med_h1h3"],
        name="Medium Priority H1->H3",
        line=dict(
            color=D_BLUE,
            width=ONE_LINE_SIZE,
            ),
    )
    low_trace = go.Scatter(
        x=csv_data["x_axis"],
        y=csv_data["low_h1h3"],
        name="Low Priority H1->H3",
        line=dict(
            color=D_PURPLE,
            width=ONE_LINE_SIZE,
            ),
    )
    minrate_trace = go.Scatter(
        x=csv_data["x_axis"],
        y=csv_data["minrate_h1"],
        name="Minimum Rate H1",
        line=dict(
            color=BLACK,
            width=MIN_RATE_LINE_SIZE,
            dash="dash",
            ),
    )
    data = [minrate_trace, demand_trace, alloc_trace, actual_trace, high_trace, med_trace, low_trace]
    return data


# h2 graph - cold colours
# shows:
# H2 demand
# H2 allocation
# H2 actual
# H2 high priority
# H2 med priority
# H2 low priority (dropped)
def h2_graph(csv_data):
    # Create and style traces

    demand_trace = go.Scatter(
        x=csv_data["x_axis"],
        y=csv_data["demand_h2h3"],
        name="Demand H2->H3",
        line=dict(
            color=D_RED,
            width=ONE_LINE_SIZE,
            ),
    )
    alloc_trace = go.Scatter(
        x=csv_data["x_axis"],
        y=csv_data["alloc_h2h3"],
        name="Allocation H2->H3",
        line=dict(
            color=D_ORANGE,
            width=ONE_LINE_SIZE,
            dash="dot",
            ),
    )
    actual_trace = go.Scatter(
        x=csv_data["x_axis"],
        y=csv_data["actual_h2h3"],
        name="Actual H2->H3",
        line=dict(
            color=D_YELLOW,
            width=TWO_LINE_SIZE,
            dash="dashdot",
            ),
    )
    high_trace = go.Scatter(
        x=csv_data["x_axis"],
        y=csv_data["high_h2h3"],
        name="High Priority H2->H3",
        line=dict(
            color=D_GREEN,
            width=ONE_LINE_SIZE,
            ),
    )
    med_trace = go.Scatter(
        x=csv_data["x_axis"],
        y=csv_data["med_h2h3"],
        name="Medium Priority H2->H3",
        line=dict(
            color=D_BLUE,
            width=ONE_LINE_SIZE,
            ),
    )
    low_trace = go.Scatter(
        x=csv_data["x_axis"],
        y=csv_data["low_h2h3"],
        name="Low Priority H2->H3",
        line=dict(
            color=D_PURPLE,
            width=ONE_LINE_SIZE,
            ),
    )
    minrate_trace = go.Scatter(
        x=csv_data["x_axis"],
        y=csv_data["minrate_h2"],
        name="Minimum Rate H2",
        line=dict(
            color=BLACK,
            width=MIN_RATE_LINE_SIZE,
            dash="dash",
            ),
    )
    data = [minrate_trace, demand_trace, alloc_trace, actual_trace, high_trace, med_trace, low_trace]
    return data


# --- Constants ---

# warm palette
WARM_1 = "#900C3F"
WARM_2 = "#C70039"
WARM_3 = "#FF5733"
WARM_4 = "#CC7178"
WARM_5 = "#FFC300"

# cold palette
COLD_1 = "#113F67"
COLD_2 = "#34699A"
COLD_3 = "#408AB4"
COLD_4 = "#65C6C4"
COLD_5 = "#ACDEAA"

# distinct palette
D_RED = "#E6194B"
D_ORANGE = "#F58231"
D_YELLOW = "#FFE119"
D_OLIVE = "#808000"
D_GREEN = "#3CB44B"
D_BLUE = "#4363D8"
D_PURPLE = "#911EB4"

# other colours
BLACK = "#000000"

# line sizes
ONE_LINE_SIZE = 5
TWO_LINE_SIZE = 5
MIN_RATE_LINE_SIZE = 3

# graph size
FIG_WIDTH = 1200
FIG_HEIGHT = 700

# main
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("target_csv", help="the csv file to be parsed")
    parser.add_argument("-o", "--output_name", metavar="output_name", help="filename of graph to output")
    parser.add_argument("-gt", "--title", metavar="graph_title", help="graph title")
    parser.add_argument("-t", "--type", metavar="graph_type",
                        default="both",
                        choices=["h1", "h2", "both"],
                        help="type of graph")
    parser.add_argument("-s", "--stats", action="store_true", help="outputs the median stats for each col")
    args = parser.parse_args()
    main(args)
