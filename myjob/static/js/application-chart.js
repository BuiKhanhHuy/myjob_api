var myApplicationChart = undefined;

$(function () {
    var start = moment().subtract(29, 'days');
    var end = moment();

    function cb(start, end) {
        $('#application-chart-filter span').html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
        if (myApplicationChart) {
            myApplicationChart.destroy();
        }
        const ctx = document.getElementById("application-chart-bar").getContext("2d");

        fetch('/admin/api/application-chart/', {
            method: 'POST', headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                "startDate": start,
                "endDate": end
            })
        })
            .then(response => response.json())
            .then(data => {

                const dataInput = {
                    labels: data?.labels || [], datasets: [{
                        label: 'Application',
                        data: data?.data|| [],
                        backgroundColor: data?.backgroundColors || [],
                    }]
                };
                myApplicationChart = new Chart(ctx, {
                    type: 'bar', data: dataInput, options: {
                        maintainAspectRatio: false,
                        responsive: true, plugins: {
                            legend: {
                                position: 'bottom',
                            },
                        }
                    },
                });

            });
    }

    $('#application-chart-filter').daterangepicker({
        startDate: start, endDate: end, ranges: {
            'Today': [moment(), moment()],
            'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
            'Last 7 Days': [moment().subtract(6, 'days'), moment()],
            'Last 30 Days': [moment().subtract(29, 'days'), moment()],
            'This Month': [moment().startOf('month'), moment().endOf('month')],
            'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
        }
    }, cb);

    cb(start, end);
});