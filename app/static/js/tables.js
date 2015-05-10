deletedHidden = false;
unapprovedHidden = false;
var table = false;

function hideDeleted() {
        if (deletedHidden == true)
            return true;

        else {
            var oTable = $('#viewBlocksTable').dataTable();
            oTable.fnFilter("No", 3, false, false);

            $("#toggleDeletedButton")
                .removeClass("btn-success")
                .addClass("btn-danger")
                .button('refresh');

            deletedHidden = true;
        }
    }

    function toggleDeleted() {
        var oTable = $('#viewBlocksTable').dataTable();

        //if not hidden -> hide
        if (deletedHidden == false) {
            oTable.fnFilter("No", 3, false, false);
            deletedHidden = true;
            $("#toggleDeletedButton")
                .removeClass("btn-success")
                .addClass("btn-danger")
                .button('refresh');

        } else {
            //unhide
            oTable.fnFilter("", 3, false, false);
            deletedHidden = false;
            $("#toggleDeletedButton")
                .removeClass("btn-danger")
                .addClass("btn-success")
                .button('refresh');
        }
    }

    function toggleUnapproved() {
        var oTable = $('#viewBlocksTable').dataTable();

        if (unapprovedHidden == false) {
            oTable.fnFilter("@", 6, false, false);
            unapprovedHidden = true;

            $("#toggleUnapprovedButton")
                .removeClass("btn-success")
                .addClass("btn-danger")
                .button('refresh');

        } else {
            oTable.fnFilter("", 6, false, false);
            unapprovedHidden = false;
            $("#toggleUnapprovedButton")
                .removeClass("btn-danger")
                .addClass("btn-success")
                .button('refresh');
        }
    }

$(document).ready(function() {
    $('#viewBlocksTable').dataTable({
        'lengthMenu': [100, 500, 1000],
        'order': [[7, "desc"], [5, "desc"]],
        'stateSave': true, //fixme: only false for debug
        'initComplete': function() { hideDeleted(); },
        'dom': '<"container" <"row" <"top" <"span2 pull-left"<"toolbar">> <"span4 pull-right"  ' +
        'f>>>>rt<"bottom"><"span2 pull-right" p><"clear">'
    });

    table = $('#viewBlocksTable').DataTable();

    $("div.toolbar").html(
        "<div class=\"btn-group\"><button id=\"toggleUnapprovedButton\" type=\"button\" " +
        "class=\"btn btn-success\" onclick=\"javascript:toggleUnapproved();\">Toggle Unapproved</button>" +

        "<button id=\"toggleDeletedButton\"  type=\"button\" class=\"btn btn-success\" " +
        "onclick=\"javascript:toggleDeleted();\">Toggle Deleted</button></div>");

    //hideDeleted();
});

