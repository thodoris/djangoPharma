$(document).ready(function () {


    syncLocalDB();
    function addDashboardMessage(msg, type) {
        if (!type) {
            type = 'info';
        }
        var now = new Date(Date.now());
        var formatted_time = now.getHours() + ":" + now.getMinutes() + ":" + now.getSeconds();

        $("#myMessages").append("<li class='" + type + "'><a><span>" + formatted_time + "</span>  - " + msg + "</a></li>");
    }

    function syncLocalDB() {
        $.ajax({
            type: 'GET',
            url: url + '/ajax/syncdb',
            success: function (data) {

                addDashboardMessage('Sync local DB result:' + data.result)
            },
            error: function (xhr, textStatus, errorThrown) {
                addDashboardMessage('Sync Error:' + data.error_message, 'danger')
            }
        });
    }
});
