var _pageNameMap = {
    "404": "404_page_view",
    "home": "home_page_view",
    "category": "job_category_page_view",
    "job": "job_details_view",
    "search-results": "search_result_page_view",
    "apply": "apply_page_view",
    "glassdoorReviews": "glassdoor_reviews_page_view",
    "jobcart": "favorites_page_view",
    "jointalentcommunity": "jtc_page_view",
    "featuredOpportunities": "job_category_page_view",
    "businessUnit": "job_category_page_view",
    "event": "event_details_view",
    "events": "event_results_page_view",
    "saved-jobs": "favorites_page_view",
    "blogarticle": "blog_details_page",
    "chat-bot": "bot_container_view",
    "hvhapply": "hvhapply_page_view"
  };
  var isMovePhAppInfoDone = false;
  var pendingTrackEvents = [];
  
document.addEventListener("DOMContentLoaded", function(event) {
    if(phApp && phApp.ddo && phApp.ddo.siteConfig && !isMovePhAppInfoDone){
        movePhAppInfo();
    }
    if(phApp.pageName == 'home'){
        attachAudienceEventMetaData();
    }
});

function movePhAppInfo(){
    if(phApp && phApp.ddo && phApp.ddo.siteConfig && !isMovePhAppInfoDone){
        isMovePhAppInfoDone = true;
        var siteConfig = phApp.ddo.siteConfig.data || {};
        phApp.pageNameMap = siteConfig.pageNameMap;
        phApp.recommendedTrackingConfig = siteConfig.recommendedTrackingConfig;
        phApp.trackingConfig = siteConfig.trackingConfig;
        phApp.siteSettings = siteConfig.siteSettings;
        phApp.urlMap = siteConfig.urlMap;
        if(phApp.trackPending){
            var isEventEnabled;
            var siteSettings = siteConfig.siteSettings || {};
            var cookieMap = siteSettings.externalCookieConfig && siteSettings.externalCookieConfig.trackCookieMap;
            var arcCookeMap = siteSettings.externalCookieTrustArcConfig && siteSettings.externalCookieTrustArcConfig.trackCookieMap;

            if(cookieMap || arcCookeMap){
                isEventEnabled = true;
            }
            phenomevent.init(phApp.refNum, undefined, isEventEnabled);
            delete phApp.trackPending;
        }
    }
}

movePhAppInfo();

function attachAudienceEventMetaData() {
    var audienceElems = document.querySelectorAll('[data-audience-block] [data-widget],[data-audience-block] [data-ph-widget-id]');
    var dataWidgets = [];
    var dataWidgetPhIds = [];
    for (var auEl = 0; auEl < audienceElems.length; auEl++) {
        phApp.audience_state && audienceElems[auEl].setAttribute('data-event-audience', phApp.audience_state);
        phApp.pxPageState && audienceElems[auEl].setAttribute('data-event-pxpagestate', phApp.pxPageState);
        phApp.pxSegmentState && audienceElems[auEl].setAttribute('data-event-pxsegmentstate', phApp.pxSegmentState);
        phApp.pxstate && audienceElems[auEl].setAttribute('data-event-pxstate', phApp.pxstate);

        try {
            var dataWidget = audienceElems[auEl].getAttribute('data-widget');
            var dataWidgetPhId = audienceElems[auEl].getAttribute('data-ph-widget-id');

            if (dataWidget && dataWidgets.indexOf(dataWidget) == -1) {
                dataWidgets.push(dataWidget);
            }
            if (dataWidgetPhId && dataWidgetPhIds.indexOf(dataWidgetPhId) == -1) {
                dataWidgetPhIds.push(dataWidgetPhId);
            }
        } catch (e) {

        }
    }
    try {
        if (audienceElems.length) {
            if (dataWidgetPhIds.indexOf('b76bc5c38117d5f9474d32f8db41ce37') === -1) {
                raiseTrackEvent("px_audience_2_enabled", { 'widgets': dataWidgets });
            }
        } else {
            raiseTrackEvent("px_audience_2_not_enabled", { 'widgets': dataWidgets });
        }
    } catch (e) {

    }
}

function raiseTrackEvent(eventName, payload){
    var eventData = {}; 
    eventData.trait2 = phApp.refNum; 
    eventData.trait79 = phApp.locale; 
    eventData.trait65 = phApp.deviceType;
    eventData.trait76 = phApp.pageType || phApp.pageName;
    eventData.trait253 = phApp.pageName; 
    eventData.trait258 = phApp.siteType;
    eventData.experimentData = phApp.experimentData;
    if(phApp.pxSegmentState){
        eventData.trait323 = phApp.pxSegmentState;
    }
    if(phApp.pxstate){
        eventData.trait324 = phApp.pxstate;
    }
    eventData.params = payload || {};
    if (window.phenomevent) {
        phenomevent.track(eventName, eventData); 
    } else{
        pendingTrackEvents.push({
            'evName': eventName,
            'eventData': eventData
        });
        triggerMissedTrack();
    }
}

function triggerMissedTrack() {
    if(!window.phenomevent){
        setTimeout(() => {
            triggerMissedTrack();
        }, 750);
    }
    if (window.phenomevent && pendingTrackEvents.length) {
        pendingTrackEvents.forEach((eDa) => {
            window.phenomevent.track(eDa.evName, eDa.eventData);
        });
        pendingTrackEvents = [];
    }
}

function getQueryParam(queryParam){
    var reg = new RegExp( '[?&]' + queryParam + '=([^&#]*)', 'i' );
    var queryParamValue = reg.exec(window.location.href);
    return queryParamValue;
}

window.addEventListener('load', function() {

    try {
        if (window.localStorage) {
            var pageNameObj = { "pageName": phApp.pageName };
            var filteredPageNames = ["search-results"];
            var filteredPageTypes = ["category", "featuredOpportunities", "businessUnit"];
            if (filteredPageNames.indexOf(phApp.pageName) != -1 || filteredPageTypes.indexOf(phApp.pageType) != -1) {
                if (localStorage.getItem("pageName")) {
                    var lsPageNameObj = JSON.parse(this.localStorage.getItem("pageName"));
                    if (lsPageNameObj["pageName"] != "job") {
                        localStorage.setItem("pageName", JSON.stringify(pageNameObj));
                    }
                }
            }
            else {
                localStorage.setItem("pageName", JSON.stringify(pageNameObj));
            }
        }
    } catch (e) {
        if (window.phenomevent) {
            phenomevent.track('iframe_locale_storage_access_failed', {});
        }
    }
    
    var pageNameMap = phApp ? (phApp.pageNameMap || _pageNameMap) : _pageNameMap;
    var eventData = {}; 
    var missingJobSeqNum = false;
    if(phApp.experimentData && Object.keys(phApp.experimentData).length){
        var experimentId = Object.keys(phApp.experimentData)[0];
        var experimentPageName = experimentId && phApp.experimentData[experimentId]["pageName"];
        if(experimentPageName){
            phApp.pageName = experimentPageName;
        }
    }
    if(phApp && phApp.pageName && phApp.pageName != 'chatbot'){
        var eventName = pageNameMap[phApp.pageName];
        var eventStatus = true; 
        if(!eventName){
            eventName = pageNameMap[phApp.pageType]; 
        }
        if (phApp.pageType == 'category' || phApp.pageType == 'featuredOpportunities' || phApp.pageType == 'businessUnit') {
            eventData.trait14 = phApp.pageName; 
        } else {
            if (phApp.pageName == 'job') {
                if (phApp.ddo.jobDetail && phApp.ddo.jobDetail.data && phApp.ddo.jobDetail.data.job && phApp.ddo.jobDetail.data.job.jobSeqNo) {
                    eventData.trait5 = phApp.ddo.jobDetail.data.job.jobSeqNo;
                    eventData.trait14 = phApp.ddo.jobDetail.data.job.category;
                    eventData.trait282 = phApp.ddo.jobDetail.data.job.jobId;
                    phApp.ddo.jobDetail.data.job.refNum && (eventData.trait316 = phApp.ddo.jobDetail.data.job.refNum);
                    var refToken = 'referrerToken';
                    if(window.location.href.indexOf(refToken+'=') != -1){
                        eventData.trait281 = getQueryParam(refToken)[1]; //getting referral token
                    }

                } else {
                    missingJobSeqNum = true;
                    phApp.pendingJobPageViewEvent = true;
                }
            } 
            if (phApp.pageName == 'apply' || phApp.pageName == 'jointalentcommunity'|| phApp.pageName == 'apply-thankyou'|| phApp.pageName.toLowerCase() =='applythankyou') {
                eventStatus = false;
            }
            if(phApp.pageName == 'event'){
                if (phApp.ddo.eventDetail && phApp.ddo.eventDetail.data && phApp.ddo.eventDetail.data.eventScheduleId) {
                    eventData.trait269 = phApp.ddo.eventDetail.data.eventScheduleId;
                    eventData.trait14 = phApp.ddo.eventDetail.data.category;
                }
            }
        }
        if(!eventName){
            eventName = "static_page_view"; 
            eventData.trait13 = phApp.pageName; 
        }
        if(!phApp.pageType && !_pageNameMap[phApp.pageName]){
            phApp.pageType = 'content';
        }
        eventData.trait2 = phApp.refNum; 
        eventData.trait79 = phApp.locale; 
        eventData.trait65 = phApp.deviceType;
        eventData.trait76 = phApp.pageType || phApp.pageName;
        eventData.trait253 = phApp.pageName; 
        eventData.trait258 = phApp.siteType;
        eventData.experimentData = phApp.experimentData;
        let siteType = phApp.siteType;
        if(siteType == 'internal'){
           let res = phApp && phApp.ddo && phApp.ddo.getProfileDataFields;
           let phProfileId = '';
           if(res && res.status == 'success' && res.data){
               phProfileId = res.data.phProfileId || '';
           }
           if(phProfileId && phProfileId.length){
               eventData['phProfileId'] = phProfileId
           }
        }
        if(phApp.pxSegmentState){
            eventData.trait323 = phApp.pxSegmentState;
        }
        if(phApp.pxstate){
            eventData.trait324 = phApp.pxstate;
        }
        if (phApp.pageCategory) {
            eventData.pageCategory = phApp.pageCategory;
        }
        if (window.phenomevent && eventStatus && !missingJobSeqNum) {
            phenomevent.track(eventName, eventData); 
        } 
    }
});