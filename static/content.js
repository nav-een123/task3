chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    console.log("📩 Message received in content.js:", message);

    if (message.action === "updateTable") {
        console.log("🎯 Forwarding message to body.html");

        // Ensure the message is correctly forwarded to the webpage
        window.postMessage({ action: "updateTable", tasks: message.tasks }, "*");

        sendResponse({ status: "success", forwarded: true });
    }
});

// Request initial data when the page loads
chrome.runtime.sendMessage({ action: "fetchData" });
