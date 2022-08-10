const partner = $("#nameContainer").data("partner");
const durationLabel = $("span#durationValue");

// Start traffic button in confirmation screen
$("#start-button").on('click', (event) => {
    event.preventDefault();
    const req = new XMLHttpRequest();
    req.onreadystatechange = handleError;
    const formData = new FormData(document.getElementById('start-form'));
    req.open("POST", `https://api.ddosclearinghouse.eu/${partner}/start`, false);
    req.withCredentials = true;
    req.send(formData);

    // Count down alert box
    const duration = $("input#duration").val()
    $("#count-down").html(duration);
    $("#count-down-alert").removeClass('collapse');

    const targetDate = new Date()
    targetDate.setSeconds(targetDate.getSeconds() + parseInt(duration));
    const countdown = setInterval(() => {
        const now = new Date().getTime();
        const distance = targetDate - now;
        const seconds = Math.ceil(distance / 1000);

        $("#count-down").html(seconds);

        if (distance < 0) {
            clearInterval(countdown);
            $("#count-down-alert").addClass('collapse');
        }
    }, 1000);
});

// Stop traffic button
$("#stop-button").on('click', (event) => {
    $("#count-down-alert").addClass('collapse');
    event.preventDefault();
    const req = new XMLHttpRequest();
    req.onreadystatechange = handleError;
    req.open("POST", `https://api.ddosclearinghouse.eu/${partner}/stop`, true);
    req.withCredentials = true;
    req.send();
    $("#staffic-stopped-alert").removeClass("collapse").delay(2500).queue(function (next) {
        $(this).addClass("collapse");
        next();
    });
});

String.prototype.capitalize = function() {
    return this.charAt(0).toUpperCase() + this.slice(1).toLowerCase();
}

// "Next" button under attack form
$("#to-confirm").on('click', (event) => {
    // Check if not already sending traffic (sort of)
    if (!$("#count-down-alert").hasClass('collapse')) {
        $("#alert-busy").removeClass("collapse").delay(5000).queue(function (next) {
            $(this).addClass("collapse");
            next();
        });
        return;
    }

    // Validate form contents
    const formData = new FormData(document.getElementById('start-form'));
    let parametersOk = true;

    const duration = $("input#duration").val();
    if (duration < 1 || duration > 120) {
        $("#alert-content").html("<strong>Invalid duration:</strong> should be between 1 and 120 seconds.")
        parametersOk = false;
    }

    const port = $("input#port").val();
    if (formData['protocol'] !== "icmp" && (port < 1 || port > 65535)) {
        $("#alert-content").html("<strong>Invalid port:</strong> should be between 1 and 65535.")
        parametersOk = false;
    }

    const data = $("input#data").val();
    if (formData['protocol'] !== "icmp" && (data < 0 || data > 1000)) {
        $("#alert-content").html("<strong>Invalid data size:</strong> should be between 1 and 1000 bytes per packet.")
        parametersOk = false;
    }

    if (!parametersOk) {
        // Show alert banner for 5 seconds.
        $("#alert-parameter").removeClass("collapse").delay(5000).queue(function (next) {
            $(this).addClass("collapse");
            next();
        });
        return;
    }

    // Insert form data into modal
    const table = $("table#modal-table")
    table.empty()
    for (const e of formData.entries()) {
        table.append(
            `<tr>
                <td>
                    ${e[0].capitalize()}:
                </td>
                <td style="padding-left: 10px">
                    \t${e[1].toUpperCase()}
                </td>
            </tr>`
        );
    }

    // Show modal
    $("#confirmationModal").modal("show");
});

function handleError() {
    if (this.readyState === 4) { // Ready
        if (this.status !== 200) {  // Status not OK
            alert("Something went wrong sending your request to the API: " + this.statusText);
        }
    }
}

// Duration slider live update number
$("input[type=range]#duration").on('change input', function () {
    const val = $(this).val()
    if (val === "1") {
        durationLabel.html(val + " second");
    } else {
        durationLabel.html(val + " seconds");
    }
})

// Show / hide protocol details on the right
$("select#protocol").on('change', function () {
    const val = $(this).val();
    const portInput = $("input#port");
    const dataInput = $("input#data");
    const icmpDetails = $("div#icmp-details");
    const ipDetails = $("div#ip-details");
    const rawipDetails = $("div#raw-ip-details");
    const tcpDetails = $("div#tcp-details");
    const udpDetails = $("div#udp-details");

    // Reset fields
    portInput.attr("disabled", false);
    dataInput.attr("disabled", false);
    icmpDetails.hide();
    ipDetails.hide();
    rawipDetails.hide();
    tcpDetails.hide();
    udpDetails.hide();

    const tcpInput = $(".tcp");
    const udpInput = $(".udp");
    const icmpInput = $(".icmp");
    const rawipInput = $(".rawip");

    tcpInput.attr('disabled', true);
    udpInput.attr('disabled', true);
    icmpInput.attr('disabled', true);
    rawipInput.attr('disabled', true);

    // Show relevant options
    if (val === "tcp") {
        ipDetails.show();
        udpDetails.show();
        tcpDetails.show();
        tcpInput.attr('disabled', false);
    } else if (val === "udp") {
        ipDetails.show();
        udpDetails.show();
        udpInput.attr('disabled', false);
    } else if (val === "rawip") {
        ipDetails.show();
        rawipDetails.show();
        rawipInput.attr('disabled', false);
    } else if (val === "icmp") {
        icmpDetails.show();
        icmpInput.attr('disabled', false);
    }
}).change();
