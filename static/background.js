chrome.runtime.onInstalled.addListener(() => {
    console.log("Extension installed");
});


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

console.log("EXtension ID", chrome.runtime.id);

chrome.runtime.onMessage.addListener(async (message, sender, sendResponse) => {
    if (message.action === "fetchData") {
        const taskResponse = await fetchData();
        console.log("Fetched tasks:", taskResponse);

        if (taskResponse && taskResponse.data && taskResponse.data.length > 0) {
            chrome.tabs.query( {}, (tabs) => {
                    const targetTab = tabs.find(tab => tab.url && tab.url.includes("http://127.0.0.1:8000"));
                    if (targetTab) {
                        console.log("Injecting content.js into tab:", targetTab.id);
                        
                        // Inject content.js dynamically
                        chrome.scripting.executeScript({
                            target: { tabId: targetTab.id },
                            files: ["content.js"]
                        }, () => {
                            console.log("content.js injected successfully.");
    
    
                            // Now send the message after injecting
                            chrome.tabs.sendMessage(targetTab.id, {
                                action: "updateTable",
                                tasks: taskResponse.data
                            });
                        });
                    } else {
                        console.warn("No matching tab found.");
                    }
                
                // if (tabs.length > 0) {
                //     console.log("Tab ID:", tabs[0].id);
                //     chrome.tabs.sendMessage(tabs[0].id, {
                //         action: "updateTable",
                //         tasks: taskResponse.data
                //     });
                // }
            });
        } else {
            console.warn("No tasks found or error fetching tasks");
        }

        sendResponse({ status: "success", tasks: taskResponse });
        return true; // Keep sendResponse async
    }
});
