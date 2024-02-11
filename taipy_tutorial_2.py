# first, we import the necessary libraries
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from taipy import Gui, Config, Core
import taipy as tp

# we read in the dataset called 'faithful.csv', 
# a record of past eruptions from Yellowstone National Park, USA
df = pd.read_csv('faithful.csv')

# formatting the data to be useful to the KMeans model
X = df.values

# we now build the KMeans model
kmeans = KMeans(n_clusters=2, # specifies the number of clusters (can be based on intuition)
                init = 'random', # specifies how we want to initialize the centroids
                max_iter = 300, # want to specify the maximum number of iterations we will allow for kmeans
                )

kmeans.fit(X) # 'fit' method will fit the kmeans model to the faithful dataset

flags = kmeans.labels_ # shows the classifications that resulted from the model fit
category1 = df[flags == 0] # creating a mask that filters for only category 0
category2 = df[flags == 1] # creating a mask that filters for only category 1

data = {
    "x_1": category1["eruption"],
    "Category 1": category1["waiting"],
    "x_2": category2["eruption"],
    "Category 2": category2["waiting"],
}

layout = {
    # title the plot
    "title": "Old Faithful Geyser Eruptions",
    # Display the chart legend
    "showlegend": True,
    # Remove all ticks from the x axis and set the axis label
    "xaxis": {
        "title": "Eruption Length (minutes)",
        "showticklabels": False,
        "xlabel": "test"
    },
    # Remove all ticks from the y axis and set the axis label
    "yaxis": {
        "title": "Time b/w Eruptions (minutes)",
        "showticklabels": False
    }
}

def classify_eruption(user_eruption: float, user_waiting: float):
    if int(kmeans.predict([[user_eruption, user_waiting]])[0]):
        return "Cool, your eruption is a Category 1!"
    else:
        return "Cool, your eruption is a Category 2!"

# configure the data nodes...
input_eruption_data_node_cfg = Config.configure_data_node(id="eruption_stat")
input_waiting_data_node_cfg = Config.configure_data_node(id="waiting_stat")
message_data_node_cfg = Config.configure_data_node(id="message")

# configure the task, now. the input and output nodes must be specified, in addition to the function
build_msg_task_cfg = Config.configure_task(
    "build_msg", classify_eruption, [input_eruption_data_node_cfg, input_waiting_data_node_cfg], message_data_node_cfg)

# configure the scenario, composed of the tasks + nodes
scenario_cfg = Config.configure_scenario("scenario", task_configs=[build_msg_task_cfg])

# instantiate the variables in the scenario
eruption_stat=0.0
waiting_stat=0.0
message=""

page="""
<|{data}|chart|mode=markers|x[1]=x_1|x[2]=x_2|y[1]=Category 1|y[2]=Category 2|color[1]=green|color[2]=blue|layout={layout}|>

To add your own eruption, enter the data below!

Eruption length (minutes): <|{eruption_stat}|input|>
Time since last eruption (minutes): <|{waiting_stat}|input|>
<|submit|button|on_action=submit_scenario|>

<|{message}|text|>
"""

# now, we will abstract the .submit() method to a function
# this allows us to arbitrarily handle user inputs
def submit_scenario(state):
    # the state parameter is specific to each user's session
    scenario.eruption_stat.write(state.eruption_stat)
    # now, we'll also write the formality of the state
    scenario.waiting_stat.write(state.waiting_stat)
    # .submit()
    scenario.submit()
    # read the message as usual, but pass it to the state
    state.message = scenario.message.read()


# now, we'll build the scenario
if __name__ == "__main__":
    # this instantiates a "Core" service, which is necessary for Taipy to run appropriately
    Core().run()
    # now, create  the scenario
    scenario = tp.create_scenario(scenario_cfg)
    # run a GUI to interact with the scenario, instead of prescribing the functionality
    Gui(page).run()


