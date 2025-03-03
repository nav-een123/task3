chrome.runtime.onInstalled.addListener(() => {
    console.log("Extension installed");
});


//get data
// document.addEventListener("DOMContentLoaded", fetchData);

async function fetchData() {
    try {
        let response = await fetch("http://127.0.0.1:8000/categery/");
        let fetchresponse = await response.json();
        return fetchresponse; // Return full response
    } catch (error) {
        console.error("Error fetching data:", error);
        return null;
    }
}


chrome.runtime.onMessage.addListener(async (message, sender, sendResponse) => {
    if (message.action === "fetchData") {
        const taskResponse = await fetchData();
        console.log("Fetched tasks:", taskResponse);

        if (taskResponse && taskResponse.data && taskResponse.data.length > 0) {
            chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
                if (tabs.length > 0) {
                    chrome.tabs.sendMessage(tabs[0].id, {
                        action: "updateTable",
                        tasks: taskResponse.data
                    });
                }
            });
        } else {
            console.warn("No tasks found or error fetching tasks");
        }

        sendResponse({ status: "success", tasks: taskResponse });
        return true; // Keep sendResponse async
    }
});
