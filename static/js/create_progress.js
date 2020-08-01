"use strict";

window.onload = init();

function init() {
    updateTodaysProgressOnPageLoad();
}

function updateTodaysProgressOnPageLoad() {
    function updateProgressInfo(data) {
        if(!data.length) {
            return;
        }
        $('#dynamic_programming input[name="track_dp"]').val(data[0]);
        $('#graph_theory input[name="track_graphs"]').val(data[1]);
        $('#others input[name="track_others"]').val(data[5]);
        if(data[2]) {
            $('#operating_system .div_not_done').hide();
            $('#operating_system .div_done').show();
        }
        if(data[3]) {
            $('#system_design .div_not_done').hide();
            $('#system_design .div_done').show();
        }
        if(data[4]) {
            $('#machine_learning .div_not_done').hide();
            $('#machine_learning .div_done').show();
        }
    }

    let url = '/create_progress?action=todays_record';
    $.get(url, function(resp) {
        if(resp.status) {
            let data = resp.result.data;
            updateProgressInfo(data);
        }
    });
}

function updateTodaysProgress(tag) {
    let url = `/create_progress?action=create_todays_progress&tag=${tag}`;
    let request_ds = {};
    if(tag == 'dp') {
        request_ds['dp'] = $('#dynamic_programming input[name="track_dp"]').val();
    }
    if(tag == 'graphs') {
        request_ds['graphs'] = $('#graph_theory input[name="track_graphs"]').val();
    }

    if(tag == 'others') {
        request_ds['others'] = $('#others input[name="track_others"]').val();
    }

    $.post(url, request_ds, function(resp) {
        if(resp.status) {
            generateAlert(true, "Successfully Updated!");
            if(tag == 'os') {
                $('#operating_system .div_not_done').hide();
                $('#operating_system .div_done').show();
            }
            if(tag == 'sys_des') {
                $('#system_design .div_not_done').hide();
                $('#system_design .div_done').show();
            }
            if(tag == 'ml') {
                $('#machine_learning .div_not_done').hide();
                $('#machine_learning .div_done').show();
            }
        } else {
            generateAlert(true, "Something Went Wrong!");
        }
    });
}

$('#dynamic_programming input[name="track_dp"]').keydown(function (e) {
    if (e.ctrlKey && e.keyCode == 13) {
        updateTodaysProgress('dp');
    }
});

$('#graph_theory input[name="track_graphs"]').keydown(function (e) {
    if (e.ctrlKey && e.keyCode == 13) {
        updateTodaysProgress('graphs');
    }
});

$('#others input[name="track_others"]').keydown(function (e) {
    if (e.ctrlKey && e.keyCode == 13) {
        updateTodaysProgress('others');
    }
});

function generateAlert(status, msg) {
    $('.egAlertTop div').removeClass('alert-success');
    $('.egAlertTop div').removeClass('alert-danger');
    if (status) {
        $('.egAlertTop div').addClass('alert-success');
        $('.egAlertTop div strong').html(msg);
    } else {
        $('.egAlertTop div').addClass('alert-danger');
        $('.egAlertTop div strong').html(msg);
    }
    $(".egAlertTop").fadeIn(1000).delay(2000).fadeOut();
}