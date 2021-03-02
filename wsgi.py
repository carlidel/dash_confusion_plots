import numpy as np
import plotly.graph_objects as go
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, MATCH, ALL
from dash.exceptions import PreventUpdate
import json
import matplotlib

import data_handler as dh

##### CONSTANTS ################################################################
COLORS = ["red", "blue", "green", "orange", "cyan"]
FIGURE_HEIGHT = 1000
FIGURE_WIDTH = 1200

data_options = [
#    {'label': 'Stability Time', 'value': 0},
    {'label': 'LI', 'value': 1},
    {'label': 'LEI', 'value': 2},
    {'label': 'RE', 'value': 3},
    {'label': 'REI', 'value': 4},
    {'label': 'SALI', 'value': 5},
    {'label': 'GALI', 'value': 6},
    {'label': 'MEGNO', 'value': 7},
    {'label': 'Frequency Map', 'value': 8},
]
handler_list = [
    dh.stability_data_handler,
    dh.LI_data_handler,
    dh.LEI_data_handler,
    dh.RE_data_handler,
    dh.REI_data_handler,
    dh.SALI_data_handler,
    dh.GALI_data_handler,
    dh.MEGNO_data_handler,
    dh.FQ_data_handler
]
################################################################################


##### DASH Framework ###########################################################
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
application = app.server
################################################################################

###### PLOTS LAYOUT ############################################################
block = dbc.Col([
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id="fig_main_confusion",
                figure=go.Figure()
            )
        ])
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id="fig_advanced_confusion",
                figure=go.Figure()
            )
        ])
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id="fig_data",
                figure=go.Figure()
            )
        ]),
        dbc.Col([
            dbc.Row(
                [
                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Label(
                                    children="Plot options",
                                ),
                                dcc.Checklist(
                                    id='options',
                                    options=[
                                        {'label': ' Log10 scale',
                                            'value': 'log10'},
                                        {'label': ' Reverse Threshold',
                                            'value': 'reverse'},    
                                    ],
                                    value=[]
                                ),
                            ]
                        )
                    ),
                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Label(
                                    id={
                                        'type': 'data_picker',
                                        'index': 0
                                    },
                                    children="Data selector",
                                ),
                                dcc.Dropdown(
                                    id={
                                        'type': 'main_dropdown',
                                        'index': 0
                                    },
                                    options=data_options,
                                    value=0,
                                    multi=False,
                                    clearable=False
                                ),
                            ]
                        )
                    )
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Label(
                                    id={
                                        'type': 'label_0',
                                        'index': 0
                                    },
                                    children="parameter_0",
                                ),
                                dcc.Dropdown(
                                    id={
                                        'type': 'dropdown_0',
                                        'index': 0
                                    },
                                    options=[],
                                    multi=False,
                                    clearable=False
                                ),
                            ]
                        )
                    ),
                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Label(
                                    id={
                                        'type': 'label_1',
                                        'index': 0
                                    },
                                    children="parameter_1",
                                ),
                                dcc.Dropdown(
                                    id={
                                        'type': 'dropdown_1',
                                        'index': 0
                                    },
                                    options=[],
                                    multi=False,
                                    clearable=False
                                ),
                            ]
                        )
                    ),
                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Label(
                                    id={
                                        'type': 'label_2',
                                        'index': 0
                                    },
                                    children="parameter_2",
                                ),
                                dcc.Dropdown(
                                    id={
                                        'type': 'dropdown_2',
                                        'index': 0
                                    },
                                    options=[],
                                    multi=False,
                                    clearable=False
                                ),
                            ]
                        )
                    ),
                ],
                form=True,
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Label(
                                    id={
                                        'type': 'label_3',
                                        'index': 0
                                    },
                                    children="parameter_3",
                                ),
                                dcc.Dropdown(
                                    id={
                                        'type': 'dropdown_3',
                                        'index': 0
                                    },
                                    options=[],
                                    multi=False,
                                    clearable=False
                                ),
                            ]
                        )
                    ),
                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Label(
                                    id={
                                        'type': 'label_4',
                                        'index': 0
                                    },
                                    children="parameter_4",
                                ),
                                dcc.Dropdown(
                                    id={
                                        'type': 'dropdown_4',
                                        'index': 0
                                    },
                                    options=[],
                                    multi=False,
                                    clearable=False
                                ),
                            ]
                        )
                    ),
                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Label(
                                    id={
                                        'type': 'label_5',
                                        'index': 0
                                    },
                                    children="parameter_5",
                                ),
                                dcc.Dropdown(
                                    id={
                                        'type': 'dropdown_5',
                                        'index': 0
                                    },
                                    options=[],
                                    multi=False,
                                    clearable=False
                                ),
                            ]
                        )
                    ),
                ],
            ),
            dbc.Row([
                dbc.Col(
                    dbc.FormGroup(
                        [
                            dbc.Label(
                                children="Positive Weight",
                            ),
                            dcc.Input(
                                id="input_positive",
                                value=1.0,
                                type="number"
                            ),
                            dbc.Label(
                                children="Negative Weight",
                            ),
                            dcc.Input(
                                id="input_negative",
                                value=1.0,
                                type="number"
                            ),
                        ]
                    )
                ),
                dbc.Col(
                    dbc.FormGroup(
                        [
                            dbc.Label(
                                children="N samples",
                            ),
                            dcc.Input(
                                id="input_samples",
                                value=100,
                                type="number"
                            ),
                        ]
                    )
                )
            ])
        ])
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id="fig_general_thresholds",
                figure=go.Figure()
            )
        ])
    ])
])

################################################################################

##### FINAL LAYOUT #############################################################
app.layout = html.Div([
    dbc.Toast(
        [html.P("Plot(s) updated!", className="mb-0")],
        id="notification-toast",
        header="Notification",
        icon="primary",
        dismissable=True,
        is_open=False,
        duration=4000,
        style={"position": "fixed-top", "top": 66, "right": 10, "width": 350},
    ),
    block
])
################################################################################


##### CALLBACKS ################################################################
#### Options update ####

@app.callback(
    [
        Output({'type': 'dropdown_0', 'index': MATCH}, 'options'),
        Output({'type': 'dropdown_0', 'index': MATCH}, 'value'),
        Output({'type': 'label_0', 'index': MATCH}, 'children'),
        Output({'type': 'dropdown_1', 'index': MATCH}, 'options'),
        Output({'type': 'dropdown_1', 'index': MATCH}, 'value'),
        Output({'type': 'label_1', 'index': MATCH}, 'children'),
        Output({'type': 'dropdown_2', 'index': MATCH}, 'options'),
        Output({'type': 'dropdown_2', 'index': MATCH}, 'value'),
        Output({'type': 'label_2', 'index': MATCH}, 'children'),
        Output({'type': 'dropdown_3', 'index': MATCH}, 'options'),
        Output({'type': 'dropdown_3', 'index': MATCH}, 'value'),
        Output({'type': 'label_3', 'index': MATCH}, 'children'),
        Output({'type': 'dropdown_4', 'index': MATCH}, 'options'),
        Output({'type': 'dropdown_4', 'index': MATCH}, 'value'),
        Output({'type': 'label_4', 'index': MATCH}, 'children'),
        Output({'type': 'dropdown_5', 'index': MATCH}, 'options'),
        Output({'type': 'dropdown_5', 'index': MATCH}, 'value'),
        Output({'type': 'label_5', 'index': MATCH}, 'children'),
    ],
    Input({'type': 'main_dropdown', 'index': MATCH}, 'value')
)
def update_dropdown_and_labels(value):
    value = handler_list[value]
    outputs = []
    
    for i in range(len(value.get_param_list())):
        outputs.append(
            [{'label': str(s), 'value': s} for s in 
                value.get_param_options(value.get_param_list()[i])]
        )
        outputs.append(outputs[-1][0]['value'])
        outputs.append(value.get_param_list()[i])
    
    for i in range(len(value.get_param_list()), 6):
        outputs.append([])
        outputs.append(None)
        outputs.append("parameter_{}".format(i))

    return outputs

#### Grab data and create figures ####

@app.callback(
    [
        Output('fig_main_confusion', 'figure'),
        Output('fig_advanced_confusion', 'figure')
    ],
    [
        Input({'type': 'dropdown_0', 'index': 0}, 'value'),     # 0
        Input({'type': 'dropdown_1', 'index': 0}, 'value'),     # 1
        Input({'type': 'dropdown_2', 'index': 0}, 'value'),     # 2
        Input({'type': 'dropdown_3', 'index': 0}, 'value'),     # 3
        Input({'type': 'dropdown_4', 'index': 0}, 'value'),     # 4
        Input({'type': 'dropdown_5', 'index': 0}, 'value'),     # 5
        Input('options', 'value'),                              # 6
        Input('input_positive', 'value'),                       # 7
        Input('input_negative', 'value'),                       # 8
        Input('input_samples', 'value')                         # 9
    ],
    State({'type': 'main_dropdown', 'index': 0}, 'value')       # 10
)
def update_confusion_plot(*args):
    handler = handler_list[args[10]]
    param_list = handler.get_param_list()
    param_dict = {}
    for i in range(len(param_list)):
        param_dict[param_list[i]] = args[i]
    stab_param = {
        'epsilon': param_dict["epsilon"],
        'mu': param_dict["mu"],
        'kick': 'no_kick'
    }
    stab_data = dh.stability_data_handler.get_data(stab_param).flatten()
    ind_data = handler.get_data(param_dict).flatten()

    if "log10" in args[6]:
        ind_data = np.log10(ind_data)
    max_ind = np.nanmax(ind_data)
    min_ind = np.nanmin(ind_data)
    samples = np.linspace(min_ind, max_ind, args[9]+2)[1:-1]

    tp = np.empty(args[9])
    tn = np.empty(args[9])
    fp = np.empty(args[9])
    fn = np.empty(args[9])

    for i, v in enumerate(samples):
        if "reverse" in args[6]:
            tp[i] = np.count_nonzero(stab_data[ind_data >= v] == 10000000)
            tn[i] = np.count_nonzero(stab_data[ind_data < v] != 10000000)
            fp[i] = np.count_nonzero(stab_data[ind_data < v] == 10000000)
            fn[i] = np.count_nonzero(stab_data[ind_data >= v] != 10000000)
        else:
            tp[i] = np.count_nonzero(stab_data[ind_data < v] == 10000000)
            tn[i] = np.count_nonzero(stab_data[ind_data >= v] != 10000000)
            fp[i] = np.count_nonzero(stab_data[ind_data >= v] == 10000000)
            fn[i] = np.count_nonzero(stab_data[ind_data < v] != 10000000)

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=samples,
            y=tp,
            name="True Positive",
            mode='lines',
            marker_color="red"
        ))
    fig.add_trace(
        go.Scatter(
            x=samples,
            y=tn,
            name="True Negative",
            mode='lines',
            marker_color="orange"
        ))
    fig.add_trace(
        go.Scatter(
            x=samples,
            y=fp,
            name="False Positive",
            mode='lines',
            marker_color="blue"
        ))
    fig.add_trace(
        go.Scatter(
            x=samples,
            y=fn,
            name="False Negative",
            mode='lines',
            marker_color="cyan"
        ))

    max_accuracy = np.nanargmax((tp + tn) / (tp + tn + fn + fp))
    fig.add_vline(samples[max_accuracy])

    fig.update_layout(
        title="Threshold evaluation",
        xaxis_title="Threshold position",
        yaxis_title="Samples"
    )

    fig_adv = go.Figure()
    fig_adv.add_trace(
        go.Scatter(
            x=samples,
            y=(tp+tn)/(tp+tn+fp+fn),
            name="Accuracy",
            mode='lines'
        )
    )
    fig_adv.add_trace(
        go.Scatter(
            x=samples,
            y=tp/(tp+fp),
            name="Precision",
            mode="lines"
        )
    )
    fig_adv.add_trace(
        go.Scatter(
            x=samples,
            y=tp/(tp+fn),
            name="Sensitivity",
            mode="lines"
        )
    )
    fig_adv.add_trace(
        go.Scatter(
            x=samples,
            y=tn/(tn+fp),
            name="Specificity",
            mode='lines'
        )
    )

    fig_adv.update_layout(
        xaxis_title="Threshold position",
        yaxis_title="Value"
    )

    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))
    fig_adv.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))
    fig.update_layout(hovermode="x")
    fig_adv.update_layout(hovermode="x")

    return [fig, fig_adv]



#### Toast ####

@app.callback(
    Output("notification-toast", "is_open"),
    [
        Input("fig_main_confusion", 'figure'),
    ]
)
def update_toast(*p):
    return True

################################################################################


##### RUN THE SERVER ###########################################################
if __name__ == '__main__':
    app.run_server(port=8080, debug=True)
################################################################################
