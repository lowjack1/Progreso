"use strict";
var LINE_CHART_INSTANCE = null;

window.onload = init();

function init() {
    updateHomepageSingleCards();
    updateProgrammingLineGraph('month');
}

function updateHomepageSingleCards() {
    let url = "/homepage?action=progress_data";
    $.get(url, function(resp) {
        if(resp.status) {
            let data = resp.result.data;

            $("#dp_single_card .overall").html(data['dp']['overall'].toLocaleString("en-IN"));
            $("#dp_single_card .this-month").html(data['dp']['this_month'].toLocaleString("en-IN"));
            $("#dp_single_card .today").html(data['dp']['today'].toLocaleString("en-IN"));
            $('#dp_single_card').fadeTo(400, 1);

            $("#graphs_single_card .overall").html(data['graphs']['overall'].toLocaleString("en-IN"));
            $("#graphs_single_card .this-month").html(data['graphs']['this_month'].toLocaleString("en-IN"));
            $("#graphs_single_card .today").html(data['graphs']['today'].toLocaleString("en-IN"));
            $('#graphs_single_card').fadeTo(400, 1);

            $("#others_single_card .overall").html(data['others']['overall'].toLocaleString("en-IN"));
            $("#others_single_card .this-month").html(data['others']['this_month'].toLocaleString("en-IN"));
            $("#others_single_card .today").html(data['others']['today'].toLocaleString("en-IN"));
            $('#others_single_card').fadeTo(400, 1);
        }
    });
}

function updateProgrammingLineGraph(date_unit) {
    console.log("hello");
    let url = "/homepage?action=programming_line_chart&date_unit="+date_unit;

    $.get(url, function(resp) {
        if(resp.status) {
            let resp_data = resp.result.data;

            let line_chart_ds = {
                'dp': {
                    'data': [],
                    'total_value': 0,
                },
                'graphs': {
                    'data': [],
                    'total_value': 0,
                },
                'others':{
                    'data': [],
                    'total_value': 0,
                },
            };

            let total_value = 0;
            $.each(resp_data, function(_, node) {
                line_chart_ds['dp']['data'].push({x: node[0], y: node[1]});
                line_chart_ds['graphs']['data'].push({x: node[0], y: node[2]});
                line_chart_ds['others']['data'].push({x: node[0], y: node[3]});
                line_chart_ds['dp']['total_value'] += node[1];
                line_chart_ds['graphs']['total_value'] += node[2];
                line_chart_ds['others']['total_value'] += node[3];
            });

            drawMultiLineGraph(line_chart_ds, date_unit);
        }
    });
}


function drawMultiLineGraph(line_chart_ds, date_unit) {
    let date_format = getDateFormatFromDateUnit(date_unit);
    $('#programming_line_chart').fadeTo(400, 1);

    if (LINE_CHART_INSTANCE != null) {
        // To update the current graph, its important to destroy the original
        LINE_CHART_INSTANCE.destroy();
    }

    // Prepare chart
    LINE_CHART_INSTANCE = new Chart($('#programming_line_chart canvas'), {
        responsive: true,
        type: 'line',
        data: {
            datasets: [
                {
                    label: "DP",
                    data: line_chart_ds['dp']['data'],
                    fill: false,
                    borderWidth: 2,
                    pointRadius: 2,
                    pointHoverRadius: 2,
                    total_value: line_chart_ds['dp']['total_value']
                },
                {
                    label: "Graphs",
                    data: line_chart_ds['graphs']['data'],
                    fill: false,
                    borderWidth: 2,
                    pointRadius: 2,
                    pointHoverRadius: 2,
                    total_value: line_chart_ds['graphs']['total_value']
                },
                {
                    label: "Others",
                    data: line_chart_ds['others']['data'],
                    fill: false,
                    borderWidth: 2,
                    pointRadius: 2,
                    pointHoverRadius: 2,
                    total_value: line_chart_ds['others']['total_value']
                },
            ]
        },
        options: {
            scales: {
                xAxes: [{
                    type: 'time',
                    distribution: 'series',
                    time: {
                        tooltipFormat: date_format,
                        unit: date_unit,
                    },
                    ticks: {
                        autoSkip: true,
                        autoSkipPadding: 90,
                        maxRotation: 0
                    }
                }],
            },
            tooltips: {
                mode: 'index',                  // Show information of all datasets on hover
                intersect: false                // If true, the tooltip mode applies only when the mouse position intersects with an element. If false, the mode will be applied at all times.
            },
            legend: {
                display: true,
                labels: {
                    filter: function(item, data) {
                        let dataset_index = item.datasetIndex;
                        let total_value = data.datasets[dataset_index]['total_value']

                        item['text'] = `${item['text']} (${total_value})`;
                        return item;
                    }
                }
            },
            plugins: {
                colorschemes: {
                  scheme: 'tableau.Classic10',
                }
            },
            maintainAspectRatio: false,         // We set the height & width explicitly to achieve a consistent, non-cluttered look. So no need for this parameter.
        }
    });
}

function getDateFormatFromDateUnit(date_unit) {
    if(date_unit == 'year')  return 'YYYY';
    if(date_unit == 'month') return 'MMM YYYY';
    if(date_unit == 'day')   return 'MMM D';
}
