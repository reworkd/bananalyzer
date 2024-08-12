(function () {
    var script = document.createElement("script")
    script.type = "text/javascript";
    script.async = !0;
    script.src = "undefined" !== typeof PHENOMTRACK_URL ? PHENOMTRACK_URL : "file:" === document.location.protocol && "//"+phApp.phenomTrackURL.match(/^\/\//) ? "https://"+phApp.phenomTrackURL : "//"+phApp.phenomTrackURL;
    var p = document.getElementsByTagName("head")[0];
    p.parentNode.insertBefore(script, p)
    script.onload = function (){
        if(phApp && phApp.ddo && phApp.ddo.siteConfig && phApp.ddo.siteConfig.data){
            var isEventEnabled;
            var siteSettings = phApp.ddo.siteConfig.data.siteSettings || {};
            var cookieMap = siteSettings.externalCookieConfig && siteSettings.externalCookieConfig.trackCookieMap;
            var arcCookeMap = siteSettings.externalCookieTrustArcConfig && siteSettings.externalCookieTrustArcConfig.trackCookieMap;

            if(cookieMap || arcCookeMap){
                isEventEnabled = true;
            }

            phenomevent.init(phApp.refNum, undefined, isEventEnabled,phApp.nonTxmCookieConcern);
        }else{
            phApp.trackPending = phenomevent.init;
        }
    }
})();