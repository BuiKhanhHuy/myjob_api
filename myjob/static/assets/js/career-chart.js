var myCareerChart = undefined;

$(function () {
    var start = moment().subtract(29, 'days');
    var end = moment();

    function cb(start, end) {
        $('#career-chart-filter span').html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
        if (myCareerChart) {
            myCareerChart.destroy();
        }
        const ctx1 = document.getElementById("chart-career-pie").getContext("2d");

        fetch('/admin/api/career-chart/', {
            method: 'POST', headers: {
                'Content-Type': 'application/json',
            }, body: JSON.stringify({
                "startDate": start, "endDate": end
            })
        })
            .then(response => response.json())
            .then(data => {

                const inputData = {
                    labels: data.labels || [],
                    datasets: [
                        {
                            label: '',
                            data: data.data || [],
                            backgroundColor: data.backgroundColors || [],
                        }
                    ]
                }
                myCareerChart = new Chart(ctx1, {
                    type: 'pie',
                    data: inputData,
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: {
                                position: 'bottom',
                            },
                            title: {
                                display: false,
                            }
                        }
                    },
                });


            });
    }

    $('#career-chart-filter').daterangepicker({
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
