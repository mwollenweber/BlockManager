//need to rename this file. It's not really whoisxml only.

function showalert(message, alerttype) {
    $('#alert_placeholder').append('<div id="alertdiv" class="alert ' + alerttype + '"><a class="close" data-dismiss="alert">×</a><span>' + message + '</span></div>')
    setTimeout(function () { // this will automatically close the alert and remove this if the users doesnt close it in 5 secs
        $("#alertdiv").remove();
    }, 4200);

};

function showalertReload(message, alerttype) {
    $('#alert_placeholder').append('<div id="alertdiv" class="alert ' + alerttype + '"><a class="close" data-dismiss="alert">×</a><span>' + message + '</span></div>')
    setTimeout(function () { // this will automatically close the alert and remove this if the users doesnt close it in 5 secs
        location.reload();
    }, 5000);
};


function showalertStay(message, alerttype) {
    $('#alert_placeholder').append('<div id="alertdiv" class="alert ' + alerttype + '"><a class="close" data-dismiss="alert">×</a><span>' + message + '</span></div>');
};

$(document).ready(function () {
    $("#blockbutton .dropdown-menu a").click(function () {
        var success = true;
        var msg = "<strong>Success: </strong>";
        var action = $(this).text();
        var block_id = $(this).attr("block_id");

        var blockData = {
            "block_id": block_id
        };
        var data = JSON.stringify(blockData);

        if (action == "Approve") {
            $.ajax({
                type: "POST",
                url: "/approveBlock",
                data: JSON.stringify(blockData),
                contentType: 'application/json;charset=UTF-8',
                success: function (result) {
                    console.log(result);
                }
            });
            msg = msg + " Approve block completed";
        } else if (action == "Delete") {
            $.ajax({
                type: "POST",
                url: "/deleteBlock",
                data: JSON.stringify(blockData),
                contentType: 'application/json;charset=UTF-8',
                success: function (result) {
                    console.log(result);
                }
            });
            msg = msg + "Delete block completed";
        } else if (action == "Undelete") {
            $.ajax({
                type: "POST",
                url: "/undeleteBlock",
                data: JSON.stringify(blockData),
                contentType: 'application/json;charset=UTF-8',
                success: function (result) {
                    console.log(result);
                }
            });
            msg = msg + "Undelete block completed";
        }

        if (success == true) showalertReload(msg, "alert-success");
        else showalertReload(msg, "alert-danger");
     }); //end of dropdown-menu a

}); //end of document ready
