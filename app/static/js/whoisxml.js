function UpdateWhoisTable(ip) {
    var ipDict = {"ip": ip};
    $.ajax({
        type: "POST",
        url: "/getWhois",
        data: JSON.stringify(ipDict),
        contentType: 'application/json;charset=UTF-8',
        success: function (result) {
            var table = document.getElementById('WhoisData');

            var cell = table.rows[0].cells[1];
            var hostnames = result.whois.record.hostnames;
            cell.innerHTML = "";
            for (x in hostnames) {
                cell.innerHTML = cell.innerHTML + "<td> " + hostnames[x] + "</td><br>";
                //cell.add(x);
            } //end for

            cell = table.rows[1].cells[1];
            cell.innerHTML = result.whois.record.registrant;

            cell = table.rows[2].cells[1];
            cell.innerHTML = result.whois.record.email;

            cell = table.rows[4].cells[1];
            cell.innerHTML = result.whois.record.city;

            cell = table.rows[5].cells[1];
            cell.innerHTML = result.whois.record.country;

        }
    });
}; //end UpdateWhoisTable

function UpdateAlexaStatus(ip) {
    var popover_content = "<div class='body'>No Alexa Top Records Matching that Address.</div>";
    var ipDict = {"ip": ip};
    $.ajax({
        type: "POST",
        url: "/alexa/getInfo",
        data: JSON.stringify(ipDict),
        contentType: 'application/json;charset=UTF-8',
        success: function (result) {
            var record = result.alexa.record;
            if (record == null) {
                popover_content = "<div class='body'>No Alexa Top Records Matching that Address.</div>";
                $("#alexa_status")
                    .removeClass("btn-default")
                    .removeClass("disabled")
                    .removeClass("btn-danger")
                    .removeAttr("popover_content")
                    .addClass("btn-success")
                    .button('refresh')
                    .text("Not on Alexa Top 1M")
                    .attr("popover_content", popover_content);

            } else {
                popover_content = "<div class=\"body\"><div class=\"container\">";
                popover_content = popover_content + "<div class=\"row\"> Row 1: Data Found  &nbsp;</div>";
                popover_content = popover_content + "<div class=\"row\"> Row 2: Details &nbsp;</div>";
                popover_content = popover_content + "</div></div>";


                showalertStay("Warning: You're about to block a very popular site", "alert-danger");
            }
        }
    });

    $('#alexa_status').popover({
                trigger: 'hover',
                placement: 'left',
                container: 'body',
                content: function () { return $('#alexa_status').attr("popover_content").toString();},
                html: 'true'
            });

}; //end of UpdateAlexaStatus
function UpdateInternalStatus(ip) {
    var popover_content = "<div class='body'>No Results</div>";
    var ipDict = {"ip": ip };
    $.ajax({
        type: "POST",
        url: "/internal/getInfo",
        data: JSON.stringify(ipDict),
        contentType: 'application/json;charset=UTF-8',
        success: function (result) {
            var record = result.internal.record;
            if (record == null) {
                popover_content = "<div class='body'>No Results</div>";
                $("#internal_status")
                    .removeClass("disabled")
                    .removeClass("btn-default")
                    .removeClass("btn-danger")
                    .removeAttr("popover_content")
                    .addClass("btn-success")
                    .button('refresh')
                    .text("Not a Protected Address")
                    .attr("popover_content", popover_content);

            } else {
                popover_content = "<div class=\"body\"><div class=\"container\">";
                popover_content = popover_content + "<div class=\"row\"> Row 1: Data Found  &nbsp;</div>";
                popover_content = popover_content + "<div class=\"row\"> Row 2: Details &nbsp;</div>";
                popover_content = popover_content + "</div></div>";

                $("#internal_status")
                    .removeClass("disabled")
                    .removeClass("btn-default")
                    .removeClass("btn-success")
                    .removeAttr("popover_content")
                    .addClass("btn-danger")
                    .button('refresh')
                    .text("Protected Address")
                    .append($('<span class=\"badge pull-left\">alert</span>'))
                    .attr("popover_content", popover_content);

                showalertStay("Warning: You're about to block a site with an internal note", "alert-warning");
            }

            $('#internal_status').popover({
                trigger: 'hover',
                placement: 'left',
                container: 'body',
                content: function () { return $('#internal_status').attr("popover_content").toString();},
                html: 'true'
            });
        }
    });
}; //end of UpdateProtectedStatus
function UpdateMDLStatus(ip) {
    var ipDict = { "ip": ip };
    var popover_content = "<div class='body'>No Results</div>";

    $.ajax({
        type: "POST",
        url: "/mdl/getInfo",
        data: JSON.stringify(ipDict),
        contentType: 'application/json;charset=UTF-8',
        success: function (result) {
            var record = result.mdl.record;
            if (record == null) {
                popover_content = "<div class='body'>No Results</div>";
                $("#mdl_status")
                    .button('reset')
                    .removeClass("disabled")
                    .removeClass("btn-default")
                    .removeClass("btn-danger")
                    .removeAttr("popover_content")
                    .addClass("btn-success")
                    .button('refresh')
                    .attr("popover_content", popover_content);

            } else {
                popover_content = "<div class=\"body\"><div class=\"container\">";
                popover_content = popover_content + "<div class=\"row\"> Date: " + record.date + "&nbsp;</div>";
                popover_content = popover_content + "<div class=\"row\"> Domain: " + record.domain + "&nbsp;</div>";
                popover_content = popover_content + "<div class=\"row\"> Registrant: >" + record.registrant + "&nbsp;</div>";
                popover_content = popover_content + "</div></div>";

                $("#mdl_status")
                    .removeClass("disabled")
                    .removeClass("btn-default")
                    .removeClass("btn-success")
                    .removeAttr("popover_content")
                    .addClass("btn-danger")
                    .button('refresh')
                    .append($('<span class=\"badge pull-left\">alert</span>'))
                    .attr("popover_content", popover_content);
            }; //end else
        }
    });

    $('#mdl_status').popover({
        trigger: 'hover',
        placement: 'left',
        container: 'body',
        content: function () { return $('#mdl_status').attr("popover_content").toString();},
        html: 'true'
    });

}; //end of UpdateMDLStatus
function UpdateETStatus(ip) {
    var ipDict = {"ip": ip };
    var popover_content = "<div class='body'>No Results</div>";

    $.ajax({
        type: "POST",
        url: "/et/getInfo",
        data: JSON.stringify(ipDict),
        contentType: 'application/json;charset=UTF-8',
        success: function (result) {
            var record = result.et.record;

            //if there is no record, address is not known to ET
            if (record == null) {
                popover_content = "<div class='body'>No Results</div>";
                $("#et_status")
                    .removeClass("btn-default")
                    .removeClass("disabled")
                    .removeClass("btn-danger")
                    .removeAttr("popover_content")
                    .addClass("btn-success")
                    .button('refresh')
                    .text("Not on Emerging Threats")
                    .attr("popover_content", popover_content);

            } else {
                popover_content = "<div class=\"body\"><div class=\"container\">";
                popover_content = popover_content + "<div class=\"row\"> Row 1: Data Found  &nbsp;</div>";
                popover_content = popover_content + "<div class=\"row\"> Row 2: Details &nbsp;</div>";
                popover_content = popover_content + "</div></div>";

                $("#et_status")
                    .removeClass("btn-default")
                    .removeClass("disabled")
                    .removeClass("btn-success")
                    .removeAttr("popover_content")
                    .addClass("btn-danger")
                    .button('refresh')
                    .text("Emerging Threats")
                    .append($('<span class=\"badge pull-left\">alert</span>'))
                    .attr("popover_content", popover_content);
            }
        }
    });

    $('#et_status').popover({
                trigger: 'hover',
                placement: 'left',
                container: 'body',
                content: function () { return $('#et_status').attr("popover_content").toString();},
                html: 'true'
    });

}; //end of UpdateETStatus
function UpdatephishTankStatus(ip) {
    var ipDict = {"ip": ip };
    var popover_content = "<div class='body'>No Results</div>";

    $.ajax({
        type: "POST",
        url: "/phishTank/getInfo",
        data: JSON.stringify(ipDict),
        contentType: 'application/json;charset=UTF-8',
        success: function (result) {
            var record = result.phishTank.record;

            if (record == null) {
                popover_content = "<div class='body'>No Results</div>";
                $("#phishtank_status")
                    .removeClass("btn-default")
                    .removeClass("disabled")
                    .removeClass("btn-danger")
                    .removeAttr("popover_content")
                    .addClass("btn-success")
                    .button('refresh')
                    .text("Not Found in phishTank")
                    .attr("popover_content", popover_content);

            } else {
                popover_content = "<div class=\"body\"><div class=\"container\">";
                popover_content = popover_content + "<div class=\"row\"> Row 1: Data Found  &nbsp;</div>";
                popover_content = popover_content + "<div class=\"row\"> Row 2: Details &nbsp;</div>";
                popover_content = popover_content + "</div></div>";

                $("#phishtank_status")
                    .removeClass("btn-default")
                    .removeClass("disabled")
                    .removeClass("btn-success")
                    .removeAttr("popover_content")
                    .addClass("btn-danger")
                    .button('refresh')
                    .text("Found in phishTank")
                    .append($('<span class=\"badge pull-left\">alert</span>'))
                    .attr("popover_content", popover_content);
            }

        }
    });

    $('#phishtank_status').popover({
                    trigger: 'hover',
                    placement: 'left',
                    container: 'body',
                    content: function () { return $('#phishtank_status').attr("popover_content").toString();},
                    html: 'true'
    });
}; //end of UpdatephishTankStatus
function fetchIPInfo(ip) {

    UpdateWhoisTable(ip);
    UpdateMDLStatus(ip);
    UpdateAlexaStatus(ip);
    UpdateInternalStatus(ip);
    UpdateETStatus(ip);
    UpdatephishTankStatus(ip);

    document.forms["myForm"]["email"].value

} //end of fetchIPInfo
function enableBlockButton(address) {
    $("#blockButton")
        .empty()
        .prepend('<span class="glyphicon glyphicon-ban-circle"> </span>&nbsp&nbspSubmit Block')
        .removeClass("disabled")
        .button('refresh');

}
function enableInvestigateButton(address) {
    var sAddress = address.toString();
    var googleItem = "<li><a target=\"_blank\" href=\"http://www.google.com/#q=" + sAddress + "\">Google</a></li>";
    var mdlItem =    "<li><a target=\"_blank\" href=\"http://www.malwaredomainlist.com/mdl.php?search=" + sAddress + "&colsearch=All&quantity=50\">MDL</a></li>";
    var wotItem =    "<li><a target=\"_blank\" href=\"https://www.mywot.com/en/scorecard/" + sAddress + "\">WoT</a></li>";
    var coItem =     "<li><a target=\"_blank\" href=\"http://centralops.net/co/DomainDossier.aspx?dom_whois=true&dom_dns=true&traceroute=true&net_whois=true&svc_scan=true&addr=" + sAddress +"\">Central Ops</a></li>";
    var vtItem =     "<li><a target=\"_blank\" href=\"https://www.virustotal.com/en/ip-address/"+ sAddress +"/information/\">VirusTotal</a></li>";
    var rtItem =     "<li><a target=\"_blank\" href=\"https://www.robtex.com/ip/" + sAddress + ".html\">Robtex</a></li>";
    var dsItem =     "<li><a target=\"_blank\" href=\"https://www.dshield.org/ipinfo.html?ip=" + sAddress + "\">DShield</a></li>";
    var spamItem =   "<li><a target=\"_blank\" href=\"http://www.stopforumspam.com/ipcheck/" + sAddress +"\">Stop Spam</a></li>";

    $("#investigateAddressButton")
        .empty()
        //.fadeOut(200)
        .removeClass("btn-default")
        .addClass("btn-info")
        .addClass("btn-primary")
        .tooltip({
            title: "Ready to Investigate",
            placement:"bottom",
            delay: { "show": 600, "hide": 300 }
            })
        .prepend('<span class="glyphicon glyphicon-search" aria-hidden="true"> </span> Investigate')
        .removeClass("disabled")
        //.fadeIn(200);

    $("#investigateDropMenu")
        .empty()
        .append(googleItem)
        .append(dsItem)
        .append(coItem)
        .append(wotItem)
        .append(mdlItem)
        .append(vtItem)
        .append(rtItem)
        .append(spamItem);
    };

//////////////////////////
//Document Ready
//////////////////////////
$(document).ready(function () {
    // implement JSON.stringify serialization
    JSON.stringify = JSON.stringify || function (obj) {
        var t = typeof (obj);
        if (t != "object" || obj === null) {
            if (t == "string") obj = '"' + obj + '"';

            return String(obj);
        } else {
            // recurse array or object
            var n, v, json = [],
                arr = (obj && obj.constructor == Array);
            for (n in obj) {
                v = obj[n];
                t = typeof (v);
                if (t == "string") v = '"' + v + '"';
                else if (t == "object" && v !== null) v = JSON.stringify(v);
                json.push((arr ? "" : '"' + n + '":') + String(v));
            }
            return (arr ? "[" : "{") + String(json) + (arr ? "]" : "}");
        }
    };

    $("#internal_status").on("click", function(){
        $("#internal_status").popover('toggle');
    });

    $("#mdl_status").on("click", function(){
        $("#mdl_status").popover('toggle');
    });

    $("#ses_status").on("click", function(){
        $("#ses_status").popover('toggle');
    });

    $("#et_status").on("click", function(){
        $("#et_status").popover('toggle');
    });

    $("#phishtank_status").on("click", function(){
        $("#phishtank_status").popover('toggle');
    });

    $("#alexa_status").on("click", function(){
        $("#alexa_status").popover('toggle');
    });

    $("#address").on( "change", function ()  {
        var addr = $.trim(this.value);
        addr = addr.toString();

        enableInvestigateButton(addr);
        enableBlockButton(addr);

        //todo - should probably reset each button first
        UpdateWhoisTable(addr);
        UpdateMDLStatus(addr);
        UpdateAlexaStatus(addr);
        UpdateInternalStatus(addr);
        UpdateETStatus(addr);
        UpdatephishTankStatus(addr);
    }); //end of address onchange

}); //end of document ready
