var myJobPostChart = undefined;

$(function () {
    var start = moment().subtract(29, 'days');
    var end = moment();

    function cb(start, end) {
        $('#job-post-chart-filter span').html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
        if (myJobPostChart) {
            myJobPostChart.destroy();
        }
        const ctx = document.getElementById("job-post-chart-bar").getContext("2d");

        fetch('/admin/api/job-post-chart/', {
            method: 'POST', headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': Cookies.get('csrftoken'),
            }, body: JSON.stringify({
                "startDate": start, "endDate": end
            })
        })
            .then(response => response.json())
            .then(data => {

                const dataInput = {
                    labels: data?.labels || [], datasets: [{
                        label: data?.title1, data: data?.data1 || [], backgroundColor: data?.color1, stack: 'Stack 0',
                    }, {
                        label: data?.title2, data: data?.data2 || [], backgroundColor: data?.color2, stack: 'Stack 0',
                    }, {
                        label: data?.title3, data: data?.data3 || [], backgroundColor: data?.color3, stack: 'Stack 0',
                    }]
                };
                myJobPostChart = new Chart(ctx, {
                    type: 'bar', data: dataInput, options: {
                        maintainAspectRatio: false,
                        plugins: {
                            title: {
                                display: false, text: 'Chart.js Bar Chart - Stacked'
                            },
                        }, responsive: true, interaction: {
                            intersect: false,
                        }, scales: {
                            x: {
                                stacked: true,
                            }, y: {
                                stacked: true
                            }
                        }
                    }
                });
            });
    }

    $('#job-post-chart-filter').daterangepicker({
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