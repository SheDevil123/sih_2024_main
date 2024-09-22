// Get references to checkboxes and table elements
const checkboxes = document.querySelectorAll('input[name="template-type"]');
const templatesTable = document.getElementById('templates-table');
const headingsTableBody = document.getElementById("headings-table").querySelector("tbody");
// Event listener for all checkboxes
checkboxes.forEach(checkbox => {
    checkbox.addEventListener("change", function () {
        toggleTableDisplay(); // Check if the table should be shown or hidden

        // Handle the specific logic for each checkbox (e.g., Initial Setup, Services, Network, etc.)
        if (this.id === "initial-setup" && this.checked) {
            populateInitialSetup();
        } else if (this.id === "initial-setup" && !this.checked) {
            clearInitialSetup();
        }

        if (this.id === "services" && this.checked) {
            populateServices();
        } else if (this.id === "services" && !this.checked) {
            clearServices();
        }

        if (this.id === "network" && this.checked) {
            populateNetwork();
        } else if (this.id === "network" && !this.checked) {
            clearNetwork();
        }

        if (this.id === "host-based-firewall" && this.checked) {
            populateHostBasedFirewall();
        } else if (this.id === "host-based-firewall" && !this.checked) {
            clearHostBasedFirewall();
        }

        if (this.id === "access-control") {
            if (this.checked) {
                populateAccessControl();
            } else {
                clearAccessControl();
            }
        }

        if (this.id === "logging-and-auditing") {
            if (this.checked) {
                populateLoggingAndAuditing();
            } else {
                clearLoggingAndAuditing();
            }
        }

        // Add event listener for "System Maintenance" checkbox
        if (this.id === "system-maintenance") {
            if (this.checked) {
                populateSystemMaintenance();
            } else {
                clearSystemMaintenance();
            }
        }
    });
});

// Function to toggle the visibility of the table based on selected checkboxes
function toggleTableDisplay() {
    const isAnyCheckboxChecked = Array.from(checkboxes).some(checkbox => checkbox.checked);
    if (isAnyCheckboxChecked) {
        templatesTable.style.display = 'block'; // Show the table if any checkbox is selected
    } else {
        templatesTable.style.display = 'none'; // Hide the table if no checkbox is selected
        headingsTableBody.innerHTML = ''; // Clear the table contents
    }
}

// Function to populate the checklist items for "Initial Setup"
function populateInitialSetup() {
    const checklistItems = [
        "1.1 Filesystem",
        "1.2 Package Management",
        "1.3 Mandatory Access Control",
        "1.4 Configure Bootloader",
        "1.5 Configure Additional Process Hardening",
        "1.6 Configure Command Line Warning Banners",
        "1.7 Configure GNOME Display Manager"
    ];

    checklistItems.forEach(item => {
        const row = document.createElement("tr");
        const itemId = item.replace(/\s+/g, '-').toLowerCase();
        row.innerHTML = `
            <td><input type="checkbox" class="heading-checkbox" id="${itemId}"></td>
            <td>${item}</td>
        `;

        headingsTableBody.appendChild(row);

        // Add event listener to each detailed topic checkbox
        document.getElementById(itemId).addEventListener('change', function () {
            if (this.checked) {
                window[`display${itemId.charAt(0).toUpperCase() + itemId.slice(1).replace(/-/g, '')}Details`]();
            } else {
                window[`remove${itemId.charAt(0).toUpperCase() + itemId.slice(1).replace(/-/g, '')}Details`]();
            }
        });
    });
}

// Function to clear the checklist items for "Initial Setup"
function clearInitialSetup() {
    const rows = Array.from(headingsTableBody.querySelectorAll("tr"));
    rows.forEach(row => {
        if (row.querySelector('td').innerText.startsWith("1.1") || row.querySelector('td').innerText.startsWith("1.2") || row.querySelector('td').innerText.startsWith("1.3") || row.querySelector('td').innerText.startsWith("1.4") || row.querySelector('td').innerText.startsWith("1.5") || row.querySelector('td').innerText.startsWith("1.6") || row.querySelector('td').innerText.startsWith("1.7")) {
            row.remove(); // Remove the "Initial Setup" related rows
        }
    });
}

// Function to populate the checklist items for "Services"
function populateServices() {
    const checklistItems = [
        "2.1 Configure Server Services",
        "2.2 Configure Client Services",
        "2.3 Configure Time Synchronization",
        "2.4 Job Schedulers"
    ];

    checklistItems.forEach(item => {
        const row = document.createElement("tr");
        const itemId = item.replace(/\s+/g, '-').toLowerCase();
        row.innerHTML = `
            <td><input type="checkbox" class="heading-checkbox" id="${itemId}"></td>
            <td>${item}</td>
        `;

        headingsTableBody.appendChild(row);

        // Add event listener to each detailed topic checkbox
        document.getElementById(itemId).addEventListener('change', function () {
            if (this.checked) {
                window[`display${itemId.charAt(0).toUpperCase() + itemId.slice(1).replace(/-/g, '')}Details`]();
            } else {
                window[`remove${itemId.charAt(0).toUpperCase() + itemId.slice(1).replace(/-/g, '')}Details`]();
            }
        });
    });
}

// Function to clear the checklist items for "Services"
function clearServices() {
    const rows = Array.from(headingsTableBody.querySelectorAll("tr"));
    rows.forEach(row => {
        if (row.querySelector('td').innerText.startsWith("2.1") || row.querySelector('td').innerText.startsWith("2.2") || row.querySelector('td').innerText.startsWith("2.3") || row.querySelector('td').innerText.startsWith("2.4")) {
            row.remove(); // Remove the "Services" related rows
        }
    });
}

// Function to populate the checklist items for "Network"
function populateNetwork() {
    const checklistItems = [
        "3.1 Configure Network Devices",
        "3.2 Configure Network Kernel Modules",
        "3.3 Configure Network Kernel Parameters"
    ];

    checklistItems.forEach(item => {
        const row = document.createElement("tr");
        const itemId = item.replace(/\s+/g, '-').toLowerCase();
        row.innerHTML = `
            <td><input type="checkbox" class="heading-checkbox" id="${itemId}"></td>
            <td>${item}</td>
        `;

        headingsTableBody.appendChild(row);

        // Add event listener to each detailed topic checkbox
        document.getElementById(itemId).addEventListener('change', function () {
            if (this.checked) {
                window[`display${itemId.charAt(0).toUpperCase() + itemId.slice(1).replace(/-/g, '')}Details`]();
            } else {
                window[`remove${itemId.charAt(0).toUpperCase() + itemId.slice(1).replace(/-/g, '')}Details`]();
            }
        });
    });
}

// Function to clear the checklist items for "Network"
function clearNetwork() {
    const rows = Array.from(headingsTableBody.querySelectorAll("tr"));
    rows.forEach(row => {
        if (row.querySelector('td').innerText.startsWith("3.1") || row.querySelector('td').innerText.startsWith("3.2") || row.querySelector('td').innerText.startsWith("3.3")) {
            row.remove(); // Remove the "Network" related rows
        }
    });
}

// Function to populate the checklist items for "Host Based Firewall"
function populateHostBasedFirewall() {
    const checklistItems = [
        "4.1 Configure Uncomplicated Firewall",
        "4.2 Configure nftables",
        "4.3 Configure iptables"
    ];

    checklistItems.forEach(item => {
        const row = document.createElement("tr");
        const itemId = item.replace(/\s+/g, '-').toLowerCase();
        row.innerHTML = `
            <td><input type="checkbox" class="heading-checkbox" id="${itemId}"></td>
            <td>${item}</td>
        `;

        headingsTableBody.appendChild(row);

        // Add event listener to each detailed topic checkbox
        document.getElementById(itemId).addEventListener('change', function () {
            if (this.checked) {
                window[`display${itemId.charAt(0).toUpperCase() + itemId.slice(1).replace(/-/g, '')}Details`]();
            } else {
                window[`remove${itemId.charAt(0).toUpperCase() + itemId.slice(1).replace(/-/g, '')}Details`]();
            }
        });
    });
}

// Function to clear the checklist items for "Host Based Firewall"
function clearHostBasedFirewall() {
    const rows = Array.from(headingsTableBody.querySelectorAll("tr"));
    rows.forEach(row => {
        if (row.querySelector('td').innerText.startsWith("4.1") || row.querySelector('td').innerText.startsWith("4.2") || row.querySelector('td').innerText.startsWith("4.3")) {
            row.remove(); // Remove the "Host Based Firewall" related rows
        }
    });
}

// Function to populate the checklist items for "Access Control"
function populateAccessControl() {
    const checklistItems = [
        "5.1 Configure User Accounts",
        "5.2 Configure User Privileges",
        "5.3 Configure Group Accounts",
        "5.4 Configure Sudo Access"
    ];

    checklistItems.forEach(item => {
        const row = document.createElement("tr");
        const itemId = item.replace(/\s+/g, '-').toLowerCase();
        row.innerHTML = `
            <td><input type="checkbox" class="heading-checkbox" id="${itemId}"></td>
            <td>${item}</td>
        `;

        headingsTableBody.appendChild(row);

        // Add event listener to each detailed topic checkbox
        document.getElementById(itemId).addEventListener('change', function () {
            if (this.checked) {
                window[`display${itemId.charAt(0).toUpperCase() + itemId.slice(1).replace(/-/g, '')}Details`]();
            } else {
                window[`remove${itemId.charAt(0).toUpperCase() + itemId.slice(1).replace(/-/g, '')}Details`]();
            }
        });
    });
}

// Function to clear the checklist items for "Access Control"
function clearAccessControl() {
    const rows = Array.from(headingsTableBody.querySelectorAll("tr"));
    rows.forEach(row => {
        if (row.querySelector('td').innerText.startsWith("5.1") || row.querySelector('td').innerText.startsWith("5.2") || row.querySelector('td').innerText.startsWith("5.3") || row.querySelector('td').innerText.startsWith("5.4")) {
            row.remove(); // Remove the "Access Control" related rows
        }
    });
}

// Function to populate the checklist items for "Logging and Auditing"
function populateLoggingAndAuditing() {
    const checklistItems = [
        "6.1 Configure Filesystem Integrity Checking",
        "6.2 System Logging",
        "6.3 System Auditing"
    ];

    checklistItems.forEach(item => {
        const row = document.createElement("tr");
        const itemId = item.replace(/\s+/g, '-').toLowerCase();
        row.innerHTML = `
            <td><input type="checkbox" class="heading-checkbox" id="${itemId}"></td>
            <td>${item}</td>
        `;

        headingsTableBody.appendChild(row);

        // Add event listener to each detailed topic checkbox
        document.getElementById(itemId).addEventListener('change', function () {
            if (this.checked) {
                window[`display${itemId.charAt(0).toUpperCase() + itemId.slice(1).replace(/-/g, '')}Details`]();
            } else {
                window[`remove${itemId.charAt(0).toUpperCase() + itemId.slice(1).replace(/-/g, '')}Details`]();
            }
        });
    });
}

// Function to clear the checklist items for "Logging and Auditing"
function clearLoggingAndAuditing() {
    const rows = Array.from(headingsTableBody.querySelectorAll("tr"));
    rows.forEach(row => {
        if (row.querySelector('td').innerText.startsWith("6.1") || row.querySelector('td').innerText.startsWith("6.2") || row.querySelector('td').innerText.startsWith("6.3")) {
            row.remove(); // Remove the "Logging and Auditing" related rows
        }
    });
}

// Function to populate the checklist items for "System Maintenance"
function populateSystemMaintenance() {
    const checklistItems = [
        "7.1 System File Permissions",
        "7.2 Local User and Group Settings"
    ];

    checklistItems.forEach(item => {
        const row = document.createElement("tr");
        const itemId = item.replace(/\s+/g, '-').toLowerCase();
        row.innerHTML = `
            <td><input type="checkbox" class="heading-checkbox" id="${itemId}"></td>
            <td>${item}</td>
        `;

        headingsTableBody.appendChild(row);

        // Add event listener to each detailed topic checkbox
        document.getElementById(itemId).addEventListener('change', function () {
            if (this.checked) {
                window[`display${itemId.charAt(0).toUpperCase() + itemId.slice(1).replace(/-/g, '')}Details`]();
            } else {
                window[`remove${itemId.charAt(0).toUpperCase() + itemId.slice(1).replace(/-/g, '')}Details`]();
            }
        });
    });
}

// Function to clear the checklist items for "System Maintenance"
function clearSystemMaintenance() {
    const rows = Array.from(headingsTableBody.querySelectorAll("tr"));
    rows.forEach(row => {
        if (row.querySelector('td').innerText.startsWith("7.1") || row.querySelector('td').innerText.startsWith("7.2")) {
            row.remove(); // Remove the "System Maintenance" related rows
        }
    });
}


function GetSelected() {
    //Reference the Table.
    var grid = document.getElementById("headings-table");

    //Reference the CheckBoxes in Table.
    var checkBoxes = grid.getElementsByTagName("INPUT");
    var message = "";

    //Loop through the CheckBoxes.
    for (var i = 0; i < checkBoxes.length; i++) {
        if (checkBoxes[i].checked) {
            var row = checkBoxes[i].parentNode.parentNode;
            message += row.cells[1].innerHTML;
            message += "\n";
        }
    }

    //Display selected Row data in Alert Box.
    alert(message);
    $.ajax({
        url: '/selection_processing',
        type: 'POST',
        data: { 'idk': message},
        success:function(request){
                window.location.href = "/scan_running";
        },
        error: function(error) {
            console.log(error);
        }
    });
}