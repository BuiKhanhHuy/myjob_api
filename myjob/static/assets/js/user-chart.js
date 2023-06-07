var myUserChart = undefined;

$(function () {
    var start = moment().subtract(29, 'days');
    var end = moment();

    function cb(start, end) {
        $('#user-chart-filter span').html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
        if (myUserChart) {
            myUserChart.destroy();
        }
        const ctx = document.getElementById("user-chart-line").getContext("2d");

        fetch('/admin/api/user-chart/', {
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
                    labels: data.labels, datasets: [{
                        label: data?.title1, data: data?.data1, borderColor: data.color1, backgroundColor: data.color1
                    }, {
                        label: data?.title2, data: data?.data2, borderColor: data.color2, backgroundColor: data.color2
                    }]
                };
                myUserChart = new Chart(ctx, {
                    type: 'line', data: dataInput, options: {
                        responsive: true, maintainAspectRatio: false, plugins: {
                            legend: {
                                position: 'bottom',
                            }, title: {
                                display: false,
                            }
                        }
                    },

                });
            });
    }

    $('#user-chart-filter').daterangepicker({
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