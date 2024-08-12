(function () {
    window.phae = window.phae || {};

    var counter = 0;
    var handlerCfg = {
        'ph-global-search-v1': handleGlobalSearch,
        'ph-global-search-v3': handleGlobalSearch,
        'ph-find-your-fit-container-v1': handleFYF,
        'ph-cookie-popup-v2': handleCookie,
        'ph-cvd-v1': handleCvd,
        'ph-job-details-v1': handleJob
    }

    var postRenderCfg = {
        'ph-cookie-popup-v2': handleBodyCookie,
        'ph-cvd-v1': handleBodyCvd,
        'ph-global-search-v3': handlePostGlobalSearch,
    }
    //handlers returning 2 or 3 means, skip pre-rendering and load full widgte
    var pageState = []
    var tokenAvailable = phApp && phApp.ddo && phApp.ddo.fyfTokenStatus && phApp.ddo.fyfTokenStatus.tokenAvailable;

    function handleGlobalSearch(elem) {
        var asLitTmpl = elem.getAttribute('as-lit-tmpl');
        if (asLitTmpl) {
            var setDataMode = phApp && phApp.ddo && phApp.ddo.siteConfig && phApp.ddo.siteConfig.data && phApp.ddo.siteConfig.data.globalSearchFeature && phApp.ddo.siteConfig.data.globalSearchFeature.v1 && phApp.ddo.siteConfig.data.globalSearchFeature.v1.dataMode;
            var dataMode = elem.getAttribute('data-mode') || setDataMode;
            pageState.push(asLitTmpl + '-' + dataMode);
        }
        return 1;
    }

    function handlePostGlobalSearch(elem){
        var eagerLoad = window.phApp.ddo || {};
        if(!(eagerLoad.getAgpMetaData && eagerLoad.eagerLoadRefineSearch)){
            var el = elem.querySelectorAll('.search-text-block')[1];
            var str = el && el.getAttribute('if.bind');
            var showTitle = elem && (elem.getAttribute('show-title') || elem.getAttribute('show-title.bind'));
            var showCaption = elem && (elem.getAttribute('show-caption') || elem.getAttribute('show-caption.bind'));
            if(el && (str == '!(agpData && agpData.bannerText && agpData.totalHits >0)' && (showTitle == 'true' || showCaption == 'true'))){
                el.classList.remove('phcriticalhide');
                try{
                    if(!showTitle){
                        var titlEle = el.querySelector('[if\\.bind="showTitle"]');
                        titlEle && titlEle.classList.add('hide');
                    }
                    if(!showCaption){
                        var capEle = el.querySelector('[if\\.bind="showCaption"]');
                        capEle && capEle.classList.add('hide');
                    }
                }catch(e){

                }
            }
        }else{
            var el = elem.querySelectorAll('.search-text-block')[0];
            var str = el && el.getAttribute('if.bind');
            if(el && str == 'agpData && agpData.bannerText && agpData.totalHits >0'){

            }
        }
    }

    function handleFYF(elem) {
        var asLitTmpl = elem.getAttribute('as-lit-tmpl');
        if (tokenAvailable) {
            if (asLitTmpl) {
                return 2;
            }
        } else {
            pageState.push(asLitTmpl + '-newuser');
        }
        return 1;
    }

    function handleCookie(elem){
        var cookie = document.cookie || '';
        var isHide = window.getComputedStyle(elem).display == 'none';
        var settings = phApp && phApp.ddo && phApp.ddo.siteConfig && phApp.ddo.siteConfig.data && phApp.ddo.siteConfig.data.siteSettings && phApp.ddo.siteConfig.data.siteSettings || {};
        cookie = (cookie.indexOf('PHPPPE_GCC=a') != -1) || (cookie.indexOf('PHPPPE_GCC=d') != -1);
        
        var disableCookiePrerender = settings.gdpr && settings.gdpr.disableCookiePrerender; 
        var isGdprEnabled = !(settings.externalCookieConfig || settings.externalCookieTrustArcConfig) && settings.gdpr && settings.gdpr.enabled;

        var isCookieEnabled = elem && elem.getAttribute('as-element');
        if (!cookie && isGdprEnabled && isCookieEnabled && !isHide && !disableCookiePrerender) {
            return 1;
        }
        return 2;
    }

    function handleJob(){
        return 3;
    }

    function handleBodyCookie(elem) {
        var bodyElem = document.querySelector('body');
        if (elem) {
            var sticky = elem.querySelector('.ph-sticky-header');
            var height = sticky && sticky.offsetHeight || 0;
            var bodyTop = window.getComputedStyle(document.body).paddingTop || window.getComputedStyle(document.body).marginTop;
            var top = parseInt((bodyTop || "0px").replace('px', ''));
            var cvd = '[as-element^="ph-cvd"][placement="header"] .ph-sticky-header';
            var cvdBanner = document.querySelector(cvd);
            var offset = cvdBanner && cvdBanner['offsetHeight'] || 0;
            
            sticky && (sticky['style'].top = offset + 'px');
            sticky && (bodyElem.style.paddingTop = (height + top) + 'px');

            var STICKY_HEADER_SELCTOR = '[as-element*="header"] .ph-sticky-header, .header-layout .pcs-sticky-header ,.header-layout .ph-sticky-block-fixed';
            var stickyHeader = document.querySelector(STICKY_HEADER_SELCTOR);
            if(elem.contains(stickyHeader)){
                stickyHeader = undefined;
            }
            if(stickyHeader) {
                var stickyTop = (stickyHeader.style.top || '0px');
                stickyTop = parseInt(stickyTop.replace(stickyTop, 'px'));
                stickyHeader['style'].top = (stickyTop + height) + 'px';
            };
        }
        var showCookieSettings = phApp.ddo && phApp.ddo.siteConfig && phApp.ddo.siteConfig.data && phApp.ddo.siteConfig.data.siteSettings && phApp.ddo.siteConfig.data.siteSettings.gdpr && phApp.ddo.siteConfig.data.siteSettings.gdpr.showCookieSettings;
        var showDecline = phApp.ddo && phApp.ddo.siteConfig && phApp.ddo.siteConfig.data && phApp.ddo.siteConfig.data.siteSettings && phApp.ddo.siteConfig.data.siteSettings.gdpr && phApp.ddo.siteConfig.data.siteSettings.gdpr.showDecline;
        if(showCookieSettings){
            var cookBtn = elem.querySelector('.cookie-button-area .cookie-settings');
            cookBtn && (cookBtn.classList.remove('phcriticalhide'));
        }
        if(showDecline){
            var decBtn = elem.querySelector('.cookie-button-area .primary-button');
            decBtn && (decBtn.classList.remove('phcriticalhide'));
        }
    }

    function getSiteSettings(key){
    	var siteConfig = phApp && phApp.ddo && phApp.ddo['siteConfig'];
    	if(siteConfig && siteConfig.data){
    		if(key){
    			return siteConfig.data.siteSettings[key] || siteConfig.data[key];
    		}
    		return siteConfig.data.siteSettings;
    	}
	}

    function handleCvd(elem){
        var cookie = document.cookie || '';
        cookie = cookie.indexOf('PHPPPE_CVD');
        var isCvdEnabled = elem && elem.getAttribute('as-element');

        var ignoreCovidWidget = getSiteSettings('ignoreCovidWidgetPagesList') || [];
        var ignoreCvd = false;
        var pageName = phApp.pageName;
        if(ignoreCovidWidget.indexOf(pageName) != -1){
            ignoreCvd = true;
        }

        if (cookie == -1 && elem && isCvdEnabled && !ignoreCvd) {
            return 1;
        }
        return 2;
    }

    function handleBodyCvd(elem) {
        var bodyElem = document.querySelector('body');
        if (elem) {
            var sticky = elem.querySelector('.ph-sticky-header');
            var height = sticky && sticky.offsetHeight || 0;
            var bodyTop = window.getComputedStyle(document.body).paddingTop || window.getComputedStyle(document.body).marginTop;
            var top = parseInt((bodyTop || "0px").replace('px', ''));
            sticky && (bodyElem.style.paddingTop = (height + top) + 'px');
            var STICKY_HEADER_SELCTOR = '[as-element*="header"] .ph-sticky-header, .header-layout .pcs-sticky-header ,.header-layout .ph-sticky-block-fixed';
            var stickyHeader = document.querySelector(STICKY_HEADER_SELCTOR);
            if(elem.contains(stickyHeader)){
                stickyHeader = undefined;
            }
            stickyHeader && (stickyHeader['style'].top = height);

            var ppcElems = elem.querySelectorAll('ppc-content a');
            for(var paEl = 0; paEl < ppcElems.length; paEl++){
                ppcElems[paEl].setAttribute('phae', 'ph-cvd-v1');
                ppcElems[paEl].setAttribute('phae-type', 'click');
                ppcElems[paEl].setAttribute('phae-main', paEl);
            }
        }
    }


    function init() {
        var elem = document.querySelector('.ph-page');
        // var headerElem = document.querySelector('.ph-header');
        var elems = [];

        // checkViewportElems(headerElem, elems, 20);
        checkViewportElems(elem, elems, 2);
        checkViewPortSlider();
        applyFontforLcpElems();

        var preRenderElems = document.querySelectorAll('[as-lit-tmpl]');
        var preRenderElemsLen = preRenderElems.length;
        for (var i = 0; i < preRenderElemsLen; i++) {
            var preRenderElem = preRenderElems[i]
            if (preRenderElem) {
                var asElem = preRenderElem.getAttribute('data-widget');
                var asLitTmpl = preRenderElem.getAttribute('as-lit-tmpl');
                if (asElem) {
                    var handler = handlerCfg[asElem]
                    var shouldSkipPrerender = false;
                    if (handler) {
                        shouldSkipPrerender = handler(preRenderElem)
                    }
                    if(shouldSkipPrerender == 3){
                        continue;
                    }
                    else if (shouldSkipPrerender == 2) {
                        preRenderElem.removeAttribute('as-lit-tmpl')
                        preRenderElem.innerHTML = ''
                    } else if(shouldSkipPrerender == 1){
                        var tmplElem = document.getElementById(asLitTmpl)
                        if (tmplElem) {
                            var htmlstr = tmplElem.innerHTML || '';
                            htmlstr = htmlstr.replace(/au-target/g, 'au-target1');
                            htmlstr = htmlstr.replace(/href/g, 'data-href');
                            preRenderElem.innerHTML = htmlstr
                        }
                        applyFontforLcpElems(preRenderElem, asElem);
                        var stateElems = preRenderElem.querySelectorAll('[phae-state]');
                        var stateElemsLen = stateElems.length;
                        for (var j = 0; j < stateElemsLen; j++) {
                            var stateElem = stateElems[j]
                            if (stateElem) {
                                var stateVal = stateElem.getAttribute('phae-state')
                                var lookup = asLitTmpl + '-' + stateVal;
                                if (pageState.indexOf(lookup) != -1) {
                                    stateElem.classList.remove('phcriticalhide')
                                }else{
                                    stateElem.parentElement.removeChild(stateElem);
                                }
                            }
                        }
                        updateWidgetBundleLiterals(preRenderElem, asElem);

                    }
                    if(shouldSkipPrerender == 1){
                        var postHandler = postRenderCfg[asElem];
                        postHandler && postHandler(preRenderElem);
                    }
                }
            }
        }        
        // To avoid showing the footer with broken styles
        var bodyElem = document.querySelector('body');
            bodyElem && (bodyElem.style.visibility = 'visible');
    }

    function applyFontforLcpElems(elem, elemTag){
        if(isCrawlerUserAgent()){
            if(elemTag == 'ph-cookie-popup-v2'){
                var m = elem.querySelectorAll('[data-ph-at-id="cookie-text"]')
                for(var i = 0;i<m.length;i++){
                    m[i].style.fontFamily = 'sans-serif';
                }
            }
            if(!elemTag){
                var footerElem = document.querySelector('.ph-footer');
                footerElem && (footerElem.style.visibility = 'hidden');

                var elems = document.querySelectorAll('[id^="ph-job-details-v1-"]');
                for(var je = 0;je<elems.length;je++){
                    var tmpEl = document.createElement('div');
                    tmpEl.innerHTML = elems[je].innerHTML;
                    var fElems = tmpEl.querySelectorAll('[class="job-title"],[class="jd-info"]');
                    for(var e = 0;e<fElems.length;e++){
                        fElems[e].style.fontFamily = 'sans-serif';
                    }
                    if(fElems.length){
                        elems[je].innerHTML = tmpEl.innerHTML;
                    }
                    if(elems[je].innerHTML.indexOf('jobDetail.description') != -1){
                        var id = elems[je].getAttribute('id') ||  '';
                        var viewName = id.replace('ph-job-details-v1-', '');
                        var viewElem = document.querySelector('div[view="'+viewName+'"]');
                        if(viewElem){
                            var jobData = getDDOFromCache('jobDetail') || {};
                            var description = jobData.data && jobData.data.job && jobData.data.job.description || '';
                            viewElem.innerHTML = description;
                        }
                    }
                }
                setTimeout(function(){
                    footerElem.style.visibility = 'visible';
                }, 3500);
            }
        }
    }

    function updateWidgetBundleLiterals(elem, asElem){
        var stateElems = elem && elem.querySelectorAll('[phae-bind-literal]');
        var tranKey = elem.getAttribute('original-view');
        var literal = phApp && phApp.translations && phApp.translations[asElem+'-'+tranKey];
        if(stateElems.length && literal){
            for(var i = 0;i < stateElems.length; i++){
                var key = stateElems[i].getAttribute('phae-bind-literal') || '';
                key = key && key.split(',');
                if(key.length){
                    var widgetLiteral = literal[key[0]];
                    if(widgetLiteral && key[1]){
                        stateElems[i].setAttribute(key[1].trim(), widgetLiteral);
                    }else if(widgetLiteral){
                        stateElems[i].innerHTML = widgetLiteral;
                    }
                }                
            }
        }
    }

    function checkViewPortSlider(){
        var widgetElems = document.querySelectorAll('.ph-page div[data-widget="ph-html-v1"]');
        for(var el = 0; el < widgetElems.length; el++){
            var eachElem = widgetElems[el];
            var slideElem = eachElem && eachElem.querySelector("[ph-card-slider-v1]");
            if(slideElem && (slideElem.getAttribute('pha-load-on-event') != 'true' && slideElem.getAttribute('pha-phslide-ignore-slider') != 'true') && !eachElem.getAttribute('data-ignore-lazy-intersection')){
                var listCards = slideElem.querySelectorAll('.ph-card');
                for(var eachCard = 0; eachCard < listCards.length; eachCard++){
                    listCards[eachCard].style.display = "none";
                    listCards[eachCard].removeAttribute('role');
                }
                // slideElem.classList.remove('ph-slide-loader');
                slideElem.setAttribute("data-ph-card-slider-v1","");
                slideElem.removeAttribute("ph-card-slider-v1","");
                if (document.readyState == 'complete') {
                    enhanceSlider();
                } else {
                    window.addEventListener('load', function () {
                        enhanceSlider();
                    });
                }
                break;
            }
            if(el == 2){
                break;
            }
        }
    }
    
    function checkViewportElems(root, elems, viewPortElems){
        if(root){
            var children = root.children;
            var childElemCount = root.childElementCount;    
            for (var i = 0; i < childElemCount; i++) {
                var childElem = children[i]
                if (childElem && childElem.classList.contains('ph-widget') && viewPortElems) {
                    var type = childElem.getAttribute('type') || (childElem.firstElementChild && childElem.firstElementChild.getAttribute('type')) || '';
                    if(childElem.nodeName === 'SECTION' && (type != 'static')){
                        var asElem = childElem.querySelector('[as-element]');
                        var widgetName = asElem && asElem.getAttribute('as-element');
                        var ignoreWidgets = ['ph-cookie-popup-v2', 'ph-cvd-v1', 'ph-html-v1'];
                        if(asElem && ignoreWidgets.indexOf(widgetName) == -1){
                            elems.push(childElem);
                            viewPortElems = viewPortElems -1;
                            constructWidgetScriptId(asElem);
                        }else if(asElem && widgetName === 'ph-cookie-popup-v2'){
                            var isCookiePopup = handleCookie(asElem);
                            if(isCookiePopup == 1){
                                constructWidgetScriptId(asElem);
                            }
                        }else if(asElem && widgetName === 'ph-cvd-v1'){
                            var isCvd = handleCvd(asElem);
                            if(isCvd == 1){
                                constructWidgetScriptId(asElem);
                            }
                        }

                    }else if (childElem.childElementCount) {
                        checkViewportElems(childElem, elems, viewPortElems);
                    }
                } else if(viewPortElems){
                    if (childElem.childElementCount) {
                        checkViewportElems(childElem, elems, viewPortElems);
                    }
                }else{
                    return;
                }
            }
        }
    }

    function constructWidgetScriptId(asElem){
        var widgetName = asElem.getAttribute('as-element');
        var viewName = asElem.getAttribute('view');
        var scrId = widgetName + '-' + viewName;
        var scrElem = document.querySelector('#'+ scrId);
        var scrText = scrElem && scrElem.innerHTML;
        if(scrText && (scrText.indexOf('phcriticalhide') !== -1 || scrText.indexOf('data-pre-render') !== -1 )){
            asElem.setAttribute('as-lit-tmpl', scrId);
        }
    }

    function enhanceSlider() {
        var widgetElems = document.querySelectorAll('[data-ph-card-slider-v1]');
        for (var el = 0; el < widgetElems.length; el++) {
            var wdgetSection = widgetElems[el].closest('section');
            loadLazyImages(wdgetSection);
            var cloneWdgtSec = wdgetSection.cloneNode(true);
            var elem = cloneWdgtSec.querySelector('[data-ph-card-slider-v1]');
            if(elem){
                elem.removeAttribute('data-ph-card-slider-v1');
                elem.setAttribute('ph-card-slider-v1', "");
                elem.classList.add('ph-slide-loader');
      
                var listCards = elem.querySelectorAll('.ph-card');
                for(var eachCard = 0; eachCard < listCards.length; eachCard++){
                    listCards[eachCard].style.display = null;
                }
                var isEnhanced = false;
                var slickInter = setInterval(function(){
                    if(window.localAurelia && !isEnhanced){
                        var cntrHeadElem = cloneWdgtSec.querySelector('.ph-container-heading-block');
                        if(cntrHeadElem){
                            enhanceElem(cntrHeadElem);
                        }
                        var enhanceElement;
                        if(elem.parentElement){
                            enhanceElement = elem.parentElement;
                        }
                        enhanceElem(enhanceElement);
                        isEnhanced = true;
                    }
                    counter = counter + 1;
                    if((window.Slick || elem.slick) && counter < 15){
                        clearInterval(slickInter);
                        wdgetSection.parentElement.replaceChild(cloneWdgtSec, wdgetSection);
                    }else if(counter >= 15){
                        clearInterval(slickInter);
                        wdgetSection.parentElement.replaceChild(cloneWdgtSec, wdgetSection);
                        enhanceElem(cloneWdgtSec);
                    }
                }, 260);
            }
        }
    }

    function enhanceElem(elem){
        var q = window.localAurelia.loader.moduleRegistry['aurelia-framework'];
        if(q && q.TemplatingEngine){
            var templatingEngine = window.localAurelia.container.get(q.TemplatingEngine);
            templatingEngine.enhance({
                container: window.localAurelia.container,
                element: elem,
                resources: window.localAurelia.resources
            });
        }
    }

    function loadLazyImages(widgetElem){
        var lazyImgTags = widgetElem.querySelectorAll('[ph-data-src]');
        var lazyImgTagsLen = lazyImgTags.length;
        for(var i=0; i<lazyImgTagsLen; i++){
            var lazyImgTag = lazyImgTags[i]
            lazyImgTag.setAttribute("src", lazyImgTag.getAttribute('ph-data-src'));
            lazyImgTag.removeAttribute('ph-data-src');
        }
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

    var userAgent = navigator.userAgent;
    var isIe = userAgent && (userAgent.indexOf('Trident') != -1 || userAgent.indexOf('MSIE') != -1);
    var m = document.querySelectorAll('[au-target-id], .au-target');
    for(var a = 0; a < m.length; a++){
        m[a].classList.remove('au-target');
        m[a].removeAttribute('au-target-id');
    }
    if(phApp && phApp.siteType == 'internal' && phApp.pageName == 'myhome') {
        var scriptName = 'ph-im-widget-personalization';
        var scriptSrc = phApp.cdnUrl + "/common/js/vendor/"+scriptName+".js";
        var scriptTag = document.createElement('script');
            scriptTag.setAttribute("type", "text/javascript");
            scriptTag.setAttribute("async", "");
            scriptTag.setAttribute("defer", "");
			scriptTag.src = scriptSrc;
        var inserLocationTag = document.getElementsByTagName('script')[0];
            inserLocationTag && inserLocationTag.parentNode.insertBefore(scriptTag, inserLocationTag);
    }
    if(phApp && phApp.siteType && phApp.siteType !== 'internal' && !isIe && phApp.env != 'editor'){
        handleBodyHtml();
        handleDynamicWidgets();
        handleDeviceHeight();
        handleRemoveDeviceHeight();
        handleCaasHeaderHeight();
        init();
        handleAnchorPoint();
    }else{
        var bodyElem = document.querySelector('body');
        bodyElem && (bodyElem.style.visibility = 'visible');
    }
    loadPxHdlrScript();
    

    // To make this as priority adding to last of head tag
    var styletg = document.createElement('style');
        styletg.innerHTML = '.phcriticalhide {display: none !important} .show.aurelia-hide{display: none !important}';
        document.querySelector('head').appendChild(styletg);
    
    function handleDeviceHeight(){
        var phPageElem = document.querySelector('.ph-page');
        if(phPageElem && phApp.deviceType == 'desktop'){
            phPageElem.style.minHeight = "600px";
        }else if(phPageElem && phApp.deviceType == 'mobile'){
            phPageElem.style.minHeight = "350px";
        }
    }

    function loadPxHdlrScript(){
        var scr = document.createElement('script');
        var scriptUrl = getSiteSettings('pxScrVerionUrl') || '';
        var hed = document.querySelector('head');

        if(scriptUrl){
            if(!scriptUrl.startsWith('http')){
                scriptUrl = window.phApp.cdnUrl + '/' + scriptUrl;
            }

            scr.setAttribute('src', scriptUrl);
            scr.setAttribute("async", "");
            scr.setAttribute("defer", "");
            hed.appendChild(scr);
        }
    }

    function handleRemoveDeviceHeight(){
        if (document.readyState == 'complete') {
            removeDeviceHeight();
        } else {
            window.addEventListener('load', function () {
                removeDeviceHeight();
            });
        }
    }

    function removeDeviceHeight(){
        setTimeout(function(){
            var phPageElem = document.querySelector('.ph-page');
            if(phPageElem && phApp.deviceType == 'desktop'){
                phPageElem.style.minHeight = null;
            }else if(phPageElem && phApp.deviceType == 'mobile'){
                phPageElem.style.minHeight = null;
            }
        }, 1000);
    }



    function handleCaasHeaderHeight(){
        var elem = document.querySelector('.header-layout');
        if(elem){
            var el = elem.querySelector('pcs-widget');
                if(el){
                    el.style.height = '72px';
                    el.style.overflow = 'hidden';
                    el.style.display = 'block';
                }
        }
    }
 
    function handleAnchorPoint(){
        try{
            if(phApp && phApp.ddo && 
                phApp.ddo.siteConfig && phApp.ddo.siteConfig.data && 
                phApp.ddo.siteConfig.data.smoothAnchorSettings && 
                phApp.ddo.siteConfig.data.smoothAnchorSettings.isLazyIgnored){
                var anchorPt = document.querySelector('[ph-scroll]');
                if(window.location && window.location.hash || anchorPt){
                    var lazyImages = document.querySelectorAll('[loading]');
                    for(var im = 0; im < lazyImages.length; im++){
                        lazyImages[im].removeAttribute('loading');
                    }
                }
            }
        }catch(e){

        }
    }

    function getDDOFromCache(ddoKey) {
        const ddo = this.phApp.ddo;
        return ddo[ddoKey];
    }

    function formatParams(params) {
        return "?" + Object
            .keys(params)
            .map(function (key) {
                return key + "=" + encodeURIComponent(params[key])
            })
            .join("&")
    }

    function handleBodyHtml(){
        var pageBodyHtml = window.pageBodyHtml;
        if(pageBodyHtml){
            var bodyElem = document.querySelector('body');
            bodyElem.innerHTML = pageBodyHtml;
        }
    }

    function handleDynamicWidgets(){
        var head = document.querySelector('head');
        var pageWidgetHtml = window.pageDynamicWidgets;
        if(pageWidgetHtml && head){
            var tempElem = document.createElement('div');
                tempElem.innerHTML = pageWidgetHtml;
                for(var i = 0;i < tempElem.children.length; i++){
                    head.appendChild(tempElem.children[i].cloneNode(true));
                }
        }
    }
}())