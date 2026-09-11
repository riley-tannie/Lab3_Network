async function executeCommand() {

    const ip = document
        .getElementById("routerIp")
        .value
        .trim();

    const command = document
        .getElementById("routerCommand")
        .value
        .trim();

    const output = document.getElementById("output");

    if (!ip || !command) {
        output.textContent =
            "Please enter both router IP and router command.";

        return;
    }

    output.textContent = "Connecting to router...";

try {

        const response = await fetch("/api/execute", {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                ip: ip,
                command: command
            })
        });

        const data = await response.json();

        if (data.success) {
            output.textContent = data.output;
        } else {
            output.textContent =
                "Error: " + data.message;
        }

    } catch (error) {

        output.textContent =
            "Connection error: " + error.message;
    }
}
