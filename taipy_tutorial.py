# "Config" module lets us configure a Taipy scenario
# "Core" module processes the configuration
# "Gui" module will add interactivity
import taipy as tp
from taipy import Config, Core, Gui

# now, let's write a function (build_message)
# this function is the key element of the "task" block
def build_message(name: str, formal: int):
    if formal=="Yes":
        return f"Greetings, {name}!"
    else:
        return f"Hey there, {name}!"

# configure the data nodes...
input_name_data_node_cfg = Config.configure_data_node(id="input_name")
input_formality_data_node_cfg = Config.configure_data_node(id="formality")
message_data_node_cfg = Config.configure_data_node(id="message")

# configure the task, now. the input and output nodes must be specified, in addition to the function
build_msg_task_cfg = Config.configure_task(
    "build_msg", build_message, [input_name_data_node_cfg, input_formality_data_node_cfg], message_data_node_cfg)

# configure the scenario, composed of the tasks + nodes
scenario_cfg = Config.configure_scenario("scenario", task_configs=[build_msg_task_cfg])

# instantiate the variables in the scenario
input_name="Adam Smith"
message=""
formality="No"

# define the page variable, which is the UI layout
page = """
Name: <|{input_name}|input|>
<|submit|button|on_action=submit_scenario|>

Message: <|{message}|text|>

Formality: <|{formality}|toggle|lov=Yes;No|>
"""

# now, we will abstract the .submit() method to a function
# this allows us to arbitrarily handle user inputs
def submit_scenario(state):
    # the state parameter is specific to each user's session
    scenario.input_name.write(state.input_name)
    # now, we'll also write the formality of the state
    scenario.formality.write(state.formality)
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

