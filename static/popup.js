// document.addEventListener("DOMContentLoaded", () => {
//     fetchData();
// });

document.addEventListener("DOMContentLoaded", function () {
    // Set default date to today
    let today = new Date().toISOString().split('T')[0];
    document.getElementById("dateInput").value = today;

    // Set default time to the current time
    let now = new Date();
    let hours = now.getHours().toString().padStart(2, '0');
    let minutes = now.getMinutes().toString().padStart(2, '0');
    let currentTime = `${hours}:${minutes}`;
    document.getElementById("fromTime").value = currentTime;
});

document.getElementById("closeModal").addEventListener("click", function () {
    document.getElementById("modal").style.display = "none";
});

document.getElementById("submitBtn").addEventListener("click", submitData);
// fetch post method
async function submitData() {
    const date = document.getElementById("dateInput").value;
    const from_time = document.getElementById("fromTime").value;
    const to_time = document.getElementById("toTime").value;
    const select_category = document.getElementById("selectInput").value;
    const task = document.getElementById("etask").value;
    const note = document.getElementById("taskNote").value; // Get the note value

    if (!date || !from_time || !to_time || !select_category || !task || !note) {
        alert("Please fill out all fields.");
        return;
    }

    const payload = {
        date: date,
        from_time: from_time,
        to_time: to_time,
        select_category: select_category,
        task: task,
        note: note,
    };

    try {
        const response = await fetch("http://127.0.0.1:8000/categery", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });

        const data = await response.json();
        if (response.ok) {
            alert("Task Created Successfully!");

            // Reset form fields
            document.getElementById("dateInput").value = "";
            document.getElementById("fromTime").value = "";
            document.getElementById("toTime").value = "";
            document.getElementById("selectInput").value = "";
            document.getElementById("etask").value = "";
            document.getElementById("taskNote").value = "";


            // Request updated tasks from background.js
            chrome.runtime.sendMessage({ action: "fetchData" }, (response) => {
                console.log("🔄 Updated tasks requested after new task submission", response.data);
            });
            // fetchAndUpdate();
            // fetchData();


        } else {
            alert("Error: " + data.detail);
        }
    } catch (error) {
        console.error("Error:", error);
        alert("Failed to create task.");
    }
}


// async function fetchData() {
//     try {
//         let response = await fetch("http://127.0.0.1:8000/categery/");
//         let fetchresponse = await response.json();
//         return fetchresponse.data;
//     } catch (error) {
//         console.error("Error fetching data:", error);
//     }
// }



//select option
document.addEventListener("DOMContentLoaded", function () {
    let apiUrl = "http://127.0.0.1:8000/task";
    let listContainer = document.getElementById("selectInput");
    let existingCategories = new Set();
    let selectInput = document.getElementById("selectInput");

    function fetchAndUpdate() {
        fetch(apiUrl)
            .then(response => response.json())
            .then(responseData => {
                console.log("API Response:", responseData);

                let categories = responseData.data;

                if (!Array.isArray(categories)) {
                    console.error("Expected an array but got:", categories);
                    return;
                }

                categories.forEach(category => {
                    if (!existingCategories.has(category.name)) {
                        let listItem = document.createElement("li");
                        listItem.className = "flex items-center justify-between hover:bg-red-100 rounded-lg h-15 w-100 py-2";
                        listItem.innerHTML = `
                    <span class="flex items-center gap-2 ml-6 font-semibold ">${category?.name}</span>
                      
                `;

                        listContainer.appendChild(listItem);
                        existingCategories.add(category.name);

                        // Add the category to the select dropdown
                        let option = document.createElement("option");
                        option.value = category.name;
                        option.textContent = category.name;
                        selectInput.appendChild(option);
                    }
                });
            })
            .catch(error => {
                console.error("Error fetching categories:", error);
            });
    }

    fetchAndUpdate(); // Initial call

});





