var phPXHdlr = (function () {
    var PX_WIDGET_INIT_EVENT = 'personalisation_2_enabled';
    var ENABLED_WIDGETS_PER_PAGE = 'px_widgets_page_level_enabled_list';
    var PX_widget_impression_click = 'px_widget_impression_click';
    var PX_widget_impression = 'px_widget_impression';
    var pendingTrackEvents = [];
    var lazyObserver;
    var userAgent = navigator.userAgent;
    var isIe = userAgent && (userAgent.indexOf('Trident') != -1 || userAgent.indexOf('MSIE') != -1);
    var isInterSectionSupports = !isIe;

    var widgetMap = {
        "locationMap": "[data-widget='ph-location-overview-map-v2']",
        "agp": "[data-widget='ph-agp-overview-v1']",
        "blogList": "[data-ph-widget-id='1c0d513754c29bdf57f46c029c235bdb']"
    }

    function loadCaasScripts(platform, ignore){
        phApp.caasPlatform = phApp.caasPlatform || {};
        if(platform){
            phApp.caasPlatform.vendor = platform.vendor;
            phApp.caasPlatform.common = platform.common;
        }
        phApp.ddo.caasPageViews = phApp.ddo.caasPageViews || {"data":{"aliases":{},"settings": {},"views": {}},"status": "success"};
        !ignore && (phApp.ddo.caasContentV1 = phApp.ddo.caasContentV1 || {"data":{"common":{},"content": {},"modelMappings": {}},"status": "success"});
    }

    function loadScript(src, cb){
        var scriptTag = document.createElement('script');
            scriptTag.setAttribute("type", "text/javascript");
            scriptTag.setAttribute("src", src);
            scriptTag.setAttribute("async", "");
            scriptTag.setAttribute("defer", "");
			scriptTag.src = src;
            scriptTag.onload = function(){
                cb && cb();
            }
        var inserLocationTag = document.getElementsByTagName('script')[0];
            inserLocationTag && inserLocationTag.parentNode.insertBefore(scriptTag, inserLocationTag);
    }

    function createCntr(wdgts){
        var wdgt = document.createElement('section');
        var pageElem = document.querySelector('.ph-page');
        wdgt.setAttribute('class', 'px-dynamic-cntr-area');
        var completeWdgtsStr = '';
        var widgetIdsList = [];

        for(var wg = 0; wg < wdgts.length; wg++){
            if(!wdgts[wg].enabled){
                continue;
            }
            var wdgtsStr = '';
            var isElementAvailable = document.querySelector('[data-ph-widget-id="'+wdgts[wg].widgetId+'"]');
            if(!isElementAvailable && widgetMap[wdgts[wg].displayName]){
                isElementAvailable = document.querySelector(widgetMap[wdgts[wg].displayName]);
            }
            if(!isElementAvailable || (isElementAvailable && isElementAvailable.hasAttribute('data-auto-loaded'))){
                wdgtsStr += '<pcs-widget data-ph-widget-id="'+wdgts[wg].widgetId+'" data-auto-loaded data-aud-widget="true" data-event-auto-enabled-px="true" data-ph-content-id="'+wdgts[wg].contentId+'" data-audience-block style="padding: 15px" ';
                if(wdgts[wg].modelName){
                    wdgtsStr += 'data-event-content-type="'+wdgts[wg].modelName+'"';
                }
                if(wdgts[wg].widgetConfigMode){
                    wdgtsStr += 'widget-config-mode="'+wdgts[wg]['widgetConfigMode']+'"';
                }
                if(wdgts[wg].hasOwnProperty('ignoreWidgetTitle')){
                    wdgtsStr += 'ignore-widget-title="'+wdgts[wg]['ignoreWidgetTitle']+'"';
                }
                if(wdgts[wg].ignoreSlider){
                    wdgtsStr += 'ignore-slider="'+wdgts[wg]['ignoreSlider']+'"';
                }
                if(wdgts[wg].instanceId){
                    wdgtsStr += 'instance-id="'+wdgts[wg].instanceId+'" ';
                }else{
                    wdgtsStr += 'global-lookup-content="true" instance-id="'+wdgts[wg].widgetId+wg+'" '
                }
                if(phApp.pxSegmentState){
                    wdgtsStr += 'data-event-pxsegmentstate="'+phApp.pxSegmentState+'" ';
                }
    
                if(wdgts[wg].class){
                    wdgtsStr += 'class="'+wdgts[wg].class+'"';
                }

                if(wdgts[wg].singleColumnEnabled){
                    wdgtsStr += 'single-column-enabled="'+ wdgts[wg].singleColumnEnabled+'" ';
                }
                
                wdgts[wg] = handleSearchAndJob(wdgts[wg]);

                if(!wdgts[wg].selector){
                    if(wdgts[wg]["px-block"] && wdgts[wg]["px-block"] == 'block-2'){
                        wdgts[wg].selector = '';
                    }else {
                        wdgts[wg].selector = '[data-widget="ph-find-your-fit-container-v1"], [data-widget="ph-similar-jobs-v2"]';   
                    }
                }

                wdgtsStr += 'data-event-container-location='+wdgts[wg]["px-block"]+'></pcs-widget>';  

                if(wdgts[wg].selector){
                    var appendElemAtPosition = document.querySelector(wdgts[wg].selector);
                    if(appendElemAtPosition){
                        var el = document.createElement('div');
                        el.innerHTML = wdgtsStr;
                        if(!wdgts[wg].isAppenchild){
                            if(appendElemAtPosition && appendElemAtPosition.parentElement && appendElemAtPosition.parentElement.nextElementSibling){
                                appendElemAtPosition = appendElemAtPosition.parentElement.nextElementSibling;
                            }
                            appendElemAtPosition.parentElement.insertBefore(el.firstElementChild, appendElemAtPosition);
                        }
                        else{
                            appendElemAtPosition.appendChild(el.firstElementChild);
                        }

                        wdgtsStr = '';
                    }else if(wdgts[wg].isAppenchild){
                        wdgtsStr = '';
                    }
                }
                completeWdgtsStr += wdgtsStr;
            }
            widgetIdsList.push(wdgts[wg].widgetId);
        }
        raiseTrackEvent(ENABLED_WIDGETS_PER_PAGE, {'widgets': widgetIdsList});
        wdgt.innerHTML = completeWdgtsStr;
        pageElem.appendChild(wdgt);
    }

    function handleSearchAndJob(wdgt){
        var pageName = phApp.pageName && phApp.pageName.toLowerCase() || '';
        var pageType = phApp.pageType && phApp.pageType.toLowerCase() || '';
        if(pageName === 'search-results' || pageType === 'category'  || pageName.startsWith('job')){
            wdgt.selector = '[ph-page-state="no-results"], [ph-page-state="expired"]';
            wdgt.isAppenchild = true;
        }
        return wdgt;
    }

    function init(){
        if(phApp.siteType == 'internal')
        {
            return;
        }
        var refNum = phApp.refNum;
        reqObj = {
            "refNum": refNum,
            "locale": phApp.locale || 'en_us',
            "siteType": phApp.siteType,
            "channel": phApp.deviceType
        }

        makeRequest(reqObj, 'pxPageWidgetConfig').then(function(res){
            phApp.ddo = phApp.ddo || {};
            phApp.ddo.pxPageWidgetConfig = res;
            res = res && res.data || {};
            if(res && res.pageList && (res.pageList.length)){
                var widgetsList = getWidgetList(res);
                var pageName = phApp.pageName && phApp.pageName.toLowerCase();
                var pageType = window.phApp.pageType;
                if(res.pageList.indexOf(pageName) !== -1 || res.pageList.indexOf(pageType) !== -1){
                    createCntr(widgetsList);
                    var caasScr = document.querySelector('#platform_script_common');
                    var caasPlatScr = document.querySelector('#caas_bootstrapper');
                    if(!caasPlatScr || !caasScr){
                        makeRequest({}, 'caasPlatform').then(function(re){
                            if(re && re.data){
                                loadCaasScripts(re.data.platform);
                                loadScript(re.data.platform.bootstrap);
                            }
                        });
                    }else{
                        triggerAudWidgets();
                    }
                }
            }
        });

        raiseTrackEvent(PX_WIDGET_INIT_EVENT, {});
    }

    var audTim;
    function triggerAudWidgets(){
        clearTimeout(audTim);
        if(window.phw && window.phw.platform){
            var pageViewsScr = document.querySelector('[src*="caas-platform/page-views"]');
            if(!pageViewsScr){
                loadCaasScripts(undefined, true);
            }
            var autoLoadWdgts = document.querySelectorAll('[data-auto-loaded]');
            if(window.phw.platform.initiateAutoRenderWidgets){
                var wdg = window.phw.platform.initiateAutoRenderWidgets(autoLoadWdgts);
                if(wdg && wdg.then){
                    wdg.then(function(){
                        setTimeout(function(){
                            var autoLoadWidgts = document.querySelectorAll('[data-auto-loaded]');
                            for(var aWdgt = 0; aWdgt < autoLoadWidgts.length; aWdgt++){
                                autoLoadWidgts[aWdgt].addEventListener('click', function(ev){
                                    var widgetInfo = constructImpressionClickObj(ev.target);
                                    raiseTrackEvent(PX_widget_impression_click, widgetInfo);
                                });
                                lazyObserver.observe(autoLoadWidgts[aWdgt]);
                            }
                        }, 2000);
                    });   
                }
            }
        }else{
            audTim = setTimeout(function(){
                triggerAudWidgets();
            }, 30);
        }
    }

    function constructImpressionClickObj(el){
        var widgetInfo = PcsCommon.CommonService.widgetTrackData(el);
        try{
            var p = JSON.stringify(widgetInfo);
            if(p.indexOf('pcs-px-container-v1') !== -1){
                delete widgetInfo.parent;
                delete widgetInfo.px;
            }else{
                if(widgetInfo.params && widgetInfo.params.parent && widgetInfo.params.parent[0]){
                    var ppm = widgetInfo.params.parent[0].params || {};
                    widgetInfo.params.widgetId = ppm.widgetId || widgetInfo.params.widgetId;
                    widgetInfo.params.widgetName = ppm.widgetName || widgetInfo.params.widgetName;
                    widgetInfo.params.widgetview = ppm.widgetview || widgetInfo.params.widgetview;
                    widgetInfo.params.instanceId = ppm.instanceId || widgetInfo.params.instanceId;
                    delete widgetInfo.params.parent;
                }
            }
            widgetInfo = {... widgetInfo, ... widgetInfo.params};
            delete widgetInfo.params;
        }catch(e){

        }
        var wdgtEl = el.closest('[data-auto-loaded]');
        if(wdgtEl){
            widgetInfo['containerLocation'] = wdgtEl.getAttribute('data-event-container-location');
            widgetInfo['dataAutoLoaded'] = true;
        }
        return widgetInfo;
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

    function removeAudV2Wdgts(){
        var block = document.querySelector('[data-audience-block="px-block-1"]');
        if(block){
            block.innerHTML = '<div class=""><pcs-widget px-display-name="px container widget"></pcs-widget></div>';
        }
        var jobWigets = document.querySelectorAll('[data-widget*=near-by-jobs],[data-widget*=recently-viewed-jobs],[data-widget*=profile-recommendations],[data-widget*=recom-jobs-browsing-history],[data-ph-widget-id="73c392f15bd3bbc876c24fa7aae7befb"],[data-ph-widget-id="289214b02891bf353eaeb99fdfcf03d6"],[data-ph-widget-id="831545da6f94c09ac9db1bad3d47a306"],[data-ph-widget-id="a0b6b3ccbcfd07b297076f31d0a7886d"],[data-ph-widget-id="a137d47caff00a07bb6050a4b1a952f9"],[data-ph-widget-id="db202020aeb395cd57395cbcac857938"],[data-ph-widget-id="08a79eab684cfa7ac18445bd3151b63d"],[data-ph-widget-id="928360027545214f89f3c791fd1ed494"],[data-ph-widget-id="42d3f1691b0b53c17596bb589b2dc82d"],[data-ph-widget-id="3fe76af179ceaab279d11d3fd4b5118f"]');
        for (let i = 0; i < jobWigets.length; i++) {
            var secElem = jobWigets[i].parentElement;
            if (secElem && secElem.nodeName === "SECTION") {
                secElem.parentElement.removeChild(secElem);
            } else {
                jobWigets[i].parentElement.removeChild(jobWigets[i]);
            }
        }
    }

    function getWidgetList(res){
        var pageName = window.phApp.pageName && window.phApp.pageName.toLowerCase();
        var pageType = window.phApp.pageType;
        var pageId = window.phApp.pageId;
        var pxSegmentState = window.phApp.pxSegmentState;
        var widgetsList;

        if(res.pageLevelWidget){
            var pageIdLevelWidgetList = res.pageLevelWidget[pageId] && res.pageLevelWidget[pageId].widgetList;

            var segmentLevelWidgetList = res.pageLevelWidget[pxSegmentState] && res.pageLevelWidget[pxSegmentState].widgetList;

            var pageTypeLevelWidgetList = res.pageLevelWidget[pageType] && res.pageLevelWidget[pageType][pxSegmentState];
                pageTypeLevelWidgetList = pageTypeLevelWidgetList && pageTypeLevelWidgetList.widgetList;

            var pageNameLevelWidgetList = res.pageLevelWidget[pageName] && res.pageLevelWidget[pageName][pxSegmentState];
                pageNameLevelWidgetList = pageNameLevelWidgetList && pageNameLevelWidgetList.widgetList;


            if(pageIdLevelWidgetList){
                widgetsList = pageIdLevelWidgetList;
            }else if(pageTypeLevelWidgetList){
                widgetsList = pageTypeLevelWidgetList;
            }else if(pageNameLevelWidgetList){
                widgetsList = pageNameLevelWidgetList;
            }else if(segmentLevelWidgetList){
                widgetsList = segmentLevelWidgetList;
            }
        }

        return widgetsList = widgetsList || res.widgetList || [];
    }

    function getCsrfToken() {
        let csrfTokenDocEle = document.getElementById('X-CSRF-TOKEN');
        window.phApp.csrfToken = csrfTokenDocEle && csrfTokenDocEle.innerText || "";
        if (!window.phApp.csrfToken) {
            window.phApp.csrfToken = window.phApp.sessionParams && window.phApp.sessionParams.csrfToken;
        }
        return window.phApp.csrfToken;
    }

    function getDDOFromCache(ddoKey) {
        var ddo = window.phApp.ddo;
        return ddo[ddoKey];
    }

    function makeRequest(reqObj, ddoKey){
        var url = phApp.widgetApiEndpoint,
            xhr = new XMLHttpRequest();
        return new Promise((resolve, reject) => {
            var ddoResponse = getDDOFromCache(ddoKey);
            if (ddoResponse) {
                resolve(ddoResponse);
            } else {
                xhr.open("POST", url, true);
                reqObj['ddoKey'] = ddoKey;
                xhr.setRequestHeader("Content-type", "application/json");
                xhr.setRequestHeader("X-CSRF-TOKEN", getCsrfToken());
                xhr.onreadystatechange = function (e) {//Call a function when the state changes.
                    if (this.readyState == XMLHttpRequest.DONE || this.readyState === 4) {
                        if (this.status == 200) {
                            var resp = JSON.parse(xhr.responseText);
                            resp = resp[ddoKey];
                            if (resp && resp.status != 500) {
                                resp = resp[ddoKey] || resp;
                                window.phApp.loadingPage = false;
                            }
                        }
                        resolve(resp);
                    }
                }
                xhr.send(JSON.stringify(reqObj));
            }
        });
    }

    function isCrawlerUserAgent() {
        var userAgent = window.navigator.userAgent;
        var status = false;
        var crawlerUserAgents = getSiteSettings('crawlerUserAgents');
        if (crawlerUserAgents) {
            var pattern = new RegExp(crawlerUserAgents, 'i');
            status = pattern.test(userAgent.toLowerCase());
        }
        return status;
    }

    function getSiteSettings(key) {
        var ddo = phApp.ddo;
        var siteConfig = ddo && ddo.siteConfig;
        if (siteConfig && siteConfig.data) {
            if (key) {
                return siteConfig.data.siteSettings && siteConfig.data.siteSettings[key] || siteConfig.data[key];
            }
            return;
        }
        return siteConfig;
    };

    function lazyLoad() {
        if (isInterSectionSupports) {
            lazyObserver = new IntersectionObserver(function (entries, observer) {
                entries.forEach(function (entry) {
                    if (entry.isIntersecting) {
                        var lazyElem = entry.target;
                        var widgetInfo = constructImpressionClickObj(lazyElem);
                        var wdgtEl = lazyElem.closest('[data-auto-loaded]');
                        if(lazyElem && lazyElem.hasAttribute('data-auto-loaded')){
                            widgetInfo['containerLocation'] = lazyElem.getAttribute('data-event-container-location');
                            widgetInfo['dataAutoLoaded'] = true;
                        }else if(wdgtEl){
                            widgetInfo['containerLocation'] = wdgtEl.getAttribute('data-event-container-location');
                            widgetInfo['dataAutoLoaded'] = true;
                        }
                        raiseTrackEvent(PX_widget_impression, widgetInfo);
                        lazyObserver.unobserve(lazyElem);
                    }
                });
            }, { rootMargin: '0px 0px 30px 0px' });
        }
    }

    var newAudSett = getSiteSettings('navItems') || {};
    var isNewAudPxEnabled = newAudSett && newAudSett.audPxConfig && newAudSett.audPxConfig.newVersion &&  newAudSett.audPxConfig.newVersion === '4.0';
    var pageName = phApp.pageName && phApp.pageName.toLowerCase();
    if(phApp.pageName === 'chatbot'){
        var wdgt = document.querySelector('[data-widget="ph-cookie-popup-v2"]');
        var covidWgt = document.querySelector('[data-widget="ph-cvd-v1"]');
        if(wdgt){
            wdgt.parentElement.removeChild(wdgt);
        }
        if(covidWgt && covidWgt.parentElement){
            covidWgt.parentElement.removeChild(covidWgt);
        }
    }
    var pages = [
        "job",
        "search-results",
        "category",
        "home",
        "agp"
    ];
    if(isNewAudPxEnabled && (pageName != 'job' && (pages.indexOf(pageName) !== -1 || pages.indexOf(phApp.pageType) !== -1))){
        removeAudV2Wdgts();
    }
    function loadAud(){
        if((!isCrawlerUserAgent() && pageName !== 'chatbot')){
            if(isNewAudPxEnabled){
                lazyLoad();
                init();   
            }
        }
    }
    if (document.readyState == 'complete') {
        loadAud()
    } else {
        window.addEventListener('load', function () {
            loadAud();
        });
    }
}())