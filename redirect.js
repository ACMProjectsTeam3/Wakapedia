var host = "http://en.wakapedia.org/wiki/";
chrome.webRequest.onBeforeRequest.addListener(
    function(details) {
        var n = details.url.indexOf("/wiki/");

        return {redirectUrl: host + details.url.substring(n+6)};
    },
    {
        urls: [
            "*://en.wikipedia.org/*"
        ],
        types: ["main_frame", "sub_frame", "stylesheet", "script", "image", "object", "xmlhttprequest", "other"]
    },
    ["blocking"]
);
