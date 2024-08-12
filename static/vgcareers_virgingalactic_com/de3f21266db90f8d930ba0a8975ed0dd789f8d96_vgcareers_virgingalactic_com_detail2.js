function PhEnhancer() {
    // // To avoid showing the footer with broken styles
    // var footerElem = document.querySelector('.ph-footer');
    //     footerElem && (footerElem.style.visibility = 'hidden');
    var splElements = ["ph-search-results-v1", "ph-search-results-v2", "ph-facets-v1"];
    var recomWidget = ["ph-profile-recommendations-v2","ph-profile-recommendations-v1"];
    var templatingEngine, phVdom, actionAfterLoad;
    var parentWidgetMap = {};
    var userAgent = navigator.userAgent;
    var isIe = userAgent && (userAgent.indexOf('Trident') != -1 || userAgent.indexOf('MSIE') != -1);
    var isInterSectionSupports = !isIe;
    var widgetsIgnoreList = 
    [
        "ph-near-By-jobs-v2",
        "ph-recom-jobs-browsing-history-v3",
        "ph-people-also-viewed-v2",
        "ph-job-cart-v3",
        "ph-targeted-jobs-v2",
        "ph-similar-jobs-v2",
        "ph-recently-viewed-jobs-v3",
        "ph-profile-recommendations-v2"
    ]

    var isEnhancedAllWidgets = false;

    function fetchDOM() {
        var bodyElem = document.querySelector('body');
        phVdom = bodyElem.cloneNode(true);
    }

    function queryWidgetElem(selector) {

        if (selector) {
            var widgetElem;
            var sel = '[instance-id="' + selector + '"]'
            widgetElem = document.querySelector(sel);
            if (!widgetElem) {
                sel = '[as-element="' + selector + '"]'
                widgetElem = document.querySelector(sel);
            }
            return widgetElem;
        }
    }
    function swapAsElement(key, widgetElem) {

    }

    function attachEventListeners() {
        var actionableElems = document.querySelectorAll('[phae]');
        if (actionableElems) {
            var actionableElemsLen = actionableElems.length;
            for (var j = 0; j < actionableElemsLen; j++) {
                var actionableElem = actionableElems[j];
                var actionRef = actionableElem.getAttribute("phae");
                var actionType = actionableElem.getAttribute("phae-type");
                var widgetElem = queryWidgetElem(actionRef, actionableElem);

                if (widgetElem) {
                    swapAsElement('as-element', widgetElem);
                }
                actionType = actionType || 'focus';
                actionableElem.addEventListener(actionType, handleLoadWidget)
            }
        }

        document.addEventListener('keyup', renderAllWidgets);
        document.addEventListener('getUserProfileData', loadRecomWidget);
    }

    function getSections(root, elems) {
        //console.time('toplevel-queryselect>getSections')
        if (root) {
            var children = root.children;
            var childElemCount = root.childElementCount;
            for (var i = 0; i < childElemCount; i++) {
                var childElem = children[i]
                if (childElem && childElem.classList.contains('ph-widget')) {
                    elems.push(childElem)
                } else {
                    if (childElem.childElementCount) {
                        getSections(childElem, elems)
                    }
                }
            }
        }
        //console.timeEnd('toplevel-queryselect>getSections')
    }

    function renderAllWidgets(ev) {
        if (isEnhancedAllWidgets) {
            return;
        }
        var keys = [37, 38, 39, 40, 9, 13];
        var keyNameList = ['ArrowDown', 'ArrowUp', 'ArrowLeft', 'ArrowRight', 'Tab', 'Enter'];

        var keyCode = ev.keyCode || ev.which || '';
        var keyName = ev.code || ev.key;

        if (keys.indexOf(keyCode) !== -1 || keyNameList.indexOf(keyName) !== -1) {
            enhanceAllWidgets();
            isEnhancedAllWidgets = true;
            document.removeEventListener('keyup', renderAllWidgets);
        }
    }

    function enhanceAllWidgets() {
        if (isEnhancedAllWidgets) {
            return;
        }
        isEnhancedAllWidgets = true;
        var widgetsList = [];
        getSections(document, widgetsList);

        for (var ju = 0; ju < widgetsList.length; ju++) {
            var widgetEnhanced = widgetsList[ju].querySelector('.au-target');
            if (!widgetEnhanced) {
                timerFn(ju, widgetsList[ju]);
            }
        }

        var asLitElems = document.querySelectorAll('[as-lit-tmpl]');
        for (var k = 0; k < asLitElems.length; k++) {
            var widgetEnhanced = widgetsList[k].querySelector('.au-target');
            if (!widgetEnhanced && widgetsList[k].parentElement) {
                timerFn(k, widgetsList[k].parentElement);
            }
        }
    }

    function timerFn(i, wgt) {
        setTimeout(function () {
            var fElem = wgt.firstElementChild && wgt.firstElementChild.getAttribute('data-widget');
            if (fElem && wgt.firstElementChild.nodeName == 'DIV') {
                wgt = wgt.firstElementChild;
            }
            enhanceElem(wgt);
        }, i * 100);
    }

    function loadFramework() {
        if (!window.localAurelia) {
            require(['aurelia-framework',
                'aurelia-loader-default',
                'aurelia-pal-browser',
                "components",
                'aurelia-templating',
                'aurelia-task-queue',
                'aurelia-logging', 'aurelia-templating-binding', 'aurelia-polyfills'], function (AF, ALD, PAL, e, AT, ATQ) {
                    require(['ph-common'], function (PHC) {
                        //e.default.push('aurelia-templating-resources')
                        require(e.default, function (WM) {
                            PAL.initialize()
                            taskQueue = new ATQ.TaskQueue()
                            var loader = new ALD.DefaultLoader();
                            var aurelia = new AF.Aurelia(loader);
                            aurelia.loader.loadModule('aurelia-framework')
                            window.localAurelia = aurelia;
                            aurelia.use.defaultBindingLanguage().defaultResources().plugin("ph-common").globalResources(e.default)
                            var aStart = aurelia.start();
                            aStart.then(function () {
                                handlePostFrameWorkInitiation();
                            })
                        })
                    })
                })
        }
    }

    function handlePostFrameWorkInitiation() {
        var q = window.localAurelia.loader.moduleRegistry['aurelia-framework'];
        templatingEngine = window.localAurelia.container.get(q.TemplatingEngine);
        if (phApp && phApp.siteType && phApp.siteType === 'internal') {
            var bodyElem = document.querySelector('body');
            loadLazyImages();
            enhanceElem(bodyElem);
            revertFooterVisibility();
            return;
        }
        loadSpecialElements();
        setResetHeaderWidgets();
        loadHeaderWidgets();
        setTimeout(function () {
            attachAudienceEventMetaData();
            loadWidgets('body > section, .ph-page [as-element], .ph-footer');
            initiatePageState();
            loadLazyImages();
            handleSliders();
            handleStickyElem();
        }, 50);
    }

    function attachAudienceEventMetaData(){
        var audienceElems = document.querySelectorAll('[data-audience-block] [data-widget], [data-ph-widget-id]');
        for(var auEl = 0; auEl < audienceElems.length; auEl++){
            phApp.audience_state && audienceElems[auEl].setAttribute('data-event-audience', phApp.audience_state);
            phApp.pxPageState && audienceElems[auEl].setAttribute('data-event-pxpagestate', phApp.pxPageState);
            phApp.pxSegmentState && audienceElems[auEl].setAttribute('data-event-pxsegmentstate', phApp.pxSegmentState);
            phApp.pxstate && audienceElems[auEl].setAttribute('data-event-pxstate', phApp.pxstate);
        }
    }

    function loadWidgets(selector) {
        var wdgts = document.querySelectorAll(selector);
        var wdgtsLen = wdgts.length;
        for (var i = 0; i < wdgtsLen; i++) {
            var wdgt = wdgts[i];
            var ignoreIntersection = wdgt && wdgt.getAttribute('data-ignore-lazy-intersection');
            // var isVideoAvailable = wdgt && isVideoExist(wdgt);
            if (wdgt && isInterSectionSupports && phApp.env != 'editor' && !ignoreIntersection) {
                var asLitTmpl = wdgt.getAttribute('as-lit-tmpl');
                var dataWidget = wdgt.getAttribute('data-widget') || '';
                var widgets = ['ph-global-search-v1', 'ph-global-search-v3', 'ph-cookie-popup-v2', 'ph-find-your-fit-container-v1','ph-cvd-v1', 'ph-generic-apply-v1'];
                var isOnetrust = wdgt.closest('[ph-module="onetrust"]');
                var isGenericApply = (dataWidget == "ph-generic-apply-v1");
                if (!asLitTmpl && !isOnetrust && !isGenericApply) {
                    asLitTmpl = wdgt.querySelector('[as-lit-tmpl]');
                    if (!asLitTmpl) {
                        var dataWidget = wdgt.getAttribute('data-widget');
                        if(widgetsIgnoreList.indexOf(dataWidget) != -1){
                            wdgt.setAttribute('data-ignore-widget-impression', true);
                        }
                        observeElem(wdgt)
                    } else {
                        parentWidgetMap[wdgt.getAttribute('as-lit-tmpl'), wdgt]
                    }
                }
                if(!isCrawlerUserAgent() && (widgets.indexOf(dataWidget) != -1 && (wdgt.hasAttribute('as-lit-tmpl') || isOnetrust || isGenericApply))){
                    wdgt.removeAttribute('as-lit-tmpl');
                    var isGlobalSearch = ['ph-global-search-v1', 'ph-global-search-v3'].indexOf(dataWidget) != -1;
                    if(isGlobalSearch){
                       var wgt = wdgt.parentElement && wdgt.parentElement.closest('[data-widget]');
                       wdgt = wgt || wdgt;
                    }
                    wdgt.parentElement.closest('[data-widget]')
                    setTimeForWidget(wdgt);
                }
            } else {
                enhanceElem(wdgt);
            }
        }
        revertFooterVisibility();
    }

    function setTimeForWidget(wdgt){
        setTimeout(function(){
            enhanceElem(wdgt);
        }, 500);
    }

    function initiatePageState() {
        if (phApp && phApp.phb && phApp.phb.eventAggregator && phApp.phb.eventAggregator.subscribe) {
            phApp.phb.eventAggregator.subscribe('pageState', function (p) {
                if (p) {
                    handlePageState(p.pageState);
                }
            });
        }
        handlePageState();
    }

    function handlePageState(pageState) {
        var state = phApp && phApp.pageState || pageState;
        if (state) {
            var stateElems = document.querySelectorAll('[ph-page-state]');
            for (var ies = 0; ies < stateElems.length; ies++) {
                var stateName = stateElems[ies].getAttribute('ph-page-state');
                if (state != stateName) {
                    stateElems[ies].parentElement.removeChild(stateElems[ies]);
                } else if (state) {
                    stateElems[ies].classList.remove('hide');
                }
            }
            return;
        }
    }

    function revertFooterVisibility() {
        // To avoid showing the footer with broken styles
        // var footerElem = document.querySelector('.ph-footer');
        //     footerElem && (footerElem.style.visibility = 'visible');
    }

    function loadSpecialElements(elements) {
        elements = elements || splElements;
        for (var i = 0; i < elements.length; i++) {
            var splElemTag = elements[i]
            if (splElemTag) {
                var splElem = document.querySelector('[as-element="' + splElemTag + '"]')
                if (splElem) {
                    enhanceElem(splElem)
                }
            }
        }
    }

    function enhanceElem(elem) {
        if (isElementEnhace(elem)) {
            templatingEngine.enhance({
                container: window.localAurelia.container,
                element: elem,
                resources: window.localAurelia.resources
            });
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

    function isElementEnhace(elem) {
        var isSliderWidget, nestedWdgt;
        try{
            nestedWdgt = elem.parentElement && elem.parentElement.closest('[ph-card-slider-v1], [ph-media-gallery-v1]');
            if(nestedWdgt){
                isSliderWidget = true;
            }
        }catch(e){

        }
        return elem && !elem.au && !elem.getAttribute('as-bridged') && !elem.querySelector('[data-ph-card-slider-v1]') && !elem.querySelector('.au-target') && !isSliderWidget;
    }

    function handleLoadWidget(evt) {
        if (evt.target) {
            var widgetTag = evt.target.getAttribute('phae');
            var actionType = evt.target.getAttribute('phae-type');
            var dataPhId = evt.target.getAttribute('data-ph-id');
            var wdgtElem = evt.target.closest('[instance-id]');
            var instanceId = wdgtElem && wdgtElem.getAttribute('instance-id');

            if (!widgetTag) {
                var tagRefEle = evt.target.closest('[phae]')
                widgetTag = tagRefEle.getAttribute('phae');
                dataPhId = tagRefEle.getAttribute('data-ph-id');
                if (widgetTag) {
                    actionType = tagRefEle.getAttribute('phae-type');
                }
            }
            actionType = actionType || 'focus'
            evt.target.removeEventListener(actionType, handleLoadWidget)
            if (templatingEngine) {
                actionAfterLoad = {
                    dataPhId: dataPhId,
                    actionType: actionType
                }
                var selector = '[instance-id="' + instanceId + '"]';
                var elemToEnhance = phVdom.querySelector(selector)
                if (!elemToEnhance) {
                    selector = '[instance-id="' + widgetTag + '"]'
                    elemToEnhance = phVdom.querySelector(selector)
                }
                if (!elemToEnhance) {
                    selector = '[as-element="' + widgetTag + '"]'
                }
                elemToEnhance = phVdom.querySelector(selector)
                if (elemToEnhance && !elemToEnhance.au) {
                    swapAsElement('as-element-silent', elemToEnhance)
                    if (parentWidgetMap[selector]) {
                        elemToEnhance = parentWidgetMap[selector]
                    }
                    enhanceElem(elemToEnhance)
                    setTimeout(function () {
                        var elemToPatch = document.querySelector(selector)
                        elemToPatch.parentElement.replaceChild(elemToEnhance, elemToPatch)
                        applyActionAfterLoad(elemToEnhance);
                    }, 10)
                }
            }
        }

    }

    function applyActionAfterLoad(elemToEnhance) {
        if (actionAfterLoad) {
            var dataPhId = actionAfterLoad.dataPhId;
            var actionType = actionAfterLoad.actionType
            if (dataPhId) {
                var selector = '[data-ph-id="' + dataPhId + '"]'
                var actionableElem = elemToEnhance.querySelector(selector);
                if (actionableElem) {
                    switch (actionType) {
                        case 'focus':
                            setTimeout(function () {
                                actionableElem.focus();
                            }, 240);
                            break;
                        case 'click':
                            actionableElem.click();
                            setTimeout(function () {
                                if (actionableElem.classList.contains('au-target')) {
                                    actionableElem.focus();
                                }
                            }, 240);
                            break;
                        default:
                            break;
                    }
                }
            }
            actionAfterLoad = undefined
        }
    }

    function isVideoExist(elem) {
        return elem.querySelector('[ph-video-v1]');
    }

    function loadLazyImages() {
        var lazyImgTags = document.querySelectorAll('[ph-data-src]');
        var lazyImgTagsLen = lazyImgTags.length;
        for (var i = 0; i < lazyImgTagsLen; i++) {
            var lazyImgTag = lazyImgTags[i];
            var phSrc = lazyImgTag.getAttribute('ph-src');
            if(phSrc){
                var phSrcValue = getImageUrl(phSrc);
                lazyImgTag.removeAttribute('ph-src');
                lazyImgTag.setAttribute("src", phSrcValue);
            }else{
                lazyImgTag.setAttribute("src", lazyImgTag.getAttribute('ph-data-src'));
            }
            lazyImgTag.removeAttribute('ph-data-src');
        }
    }

    function getImageUrl(e) {
        var t = this;
        if (e && -1 != e.indexOf("://"))
            return e;
        var i = ["cdnUrl", "refNum", "locale", "deviceType"]
          , o = "";
        return i.forEach(function(e, i) {
            var n = getParam(e);
            n && n.trim().length > 0 && (o += n,
            "/" !== n[n.length - 1] && (o += "/"))
        }),
        o + e
    }

    function getParam (e) {
        return this.phApp[e]
    }

    function handleSliders() {
        var sliderTags = document.querySelectorAll('[ph-card-slider-v1]')
        var sliderTagsLen = sliderTags.length;
        for (var i = 0; i < sliderTagsLen; i++) {
            var sliderTag = sliderTags[i]
            if (sliderTag && !sliderTag.au) {
                var listCards = sliderTag.querySelectorAll('.ph-card');
                for (var eachCard = 0; eachCard < listCards.length; eachCard++) {
                    listCards[eachCard].removeAttribute('role');
                }
            }
        }
    }

    function setResetHeaderWidgets() {
        var widgetTags = document.querySelectorAll('.ph-header [data-widget]:not([type="static"])');
        var widgetTagsLen = widgetTags.length;
        for (var i = 0; i < widgetTagsLen; i++) {
            var widgetTag = widgetTags[i];
            if (!widgetTag.hasAttribute('data-as-element')) {
                var widgeName = widgetTag.getAttribute('as-element');
                widgetTag.setAttribute('data-as-element', widgeName);
                widgetTag.removeAttribute('as-element');
            } else {
                var widgeName = widgetTag.getAttribute('data-as-element');
                widgetTag.setAttribute('as-element', widgeName);
                widgetTag.removeAttribute('data-as-element');
            }
        }
    }

    function loadHeaderWidgets() {
        var widgetTag = document.querySelector('.ph-header > [as-element]');
        widgetTag && enhanceElem(widgetTag);

        setResetHeaderWidgets();

        var widgetTags = document.querySelectorAll('.ph-header [as-element]:not([type="static"])');
        var widgetTagsLen = widgetTags.length;
        for (var i = 0; i < widgetTagsLen; i++) {
            var widgetTag = widgetTags[i];
            if (widgetTag && !widgetTag.au) {
                triggerEnhanceWithTimer(widgetTag, i);
            }
        }
    }

    function triggerEnhanceWithTimer(widgetTag, i) {
        setTimeout(function () {
            enhanceElem(widgetTag)
        }, 10 * (i + 1))
    }

    function lazyLoad() {
        if (isInterSectionSupports) {
            lazyObserver = new IntersectionObserver(function (entries, observer) {
                entries.forEach(function (entry) {
                    if (entry.isIntersecting) {
                        var lazyElem = entry.target;
                        var asLitTmpl = lazyElem.getAttribute('as-lit-tmpl');
                        if (!asLitTmpl) {
                            enhanceElem(lazyElem)
                        }
                        lazyObserver.unobserve(lazyElem);
                    }
                });
            }, { rootMargin: '0px 0px 30px 0px' });
        }
    }

    function handleStickyElem() {
        var stickyElem = document.querySelector('[ph-sticky]');
        if (stickyElem) {
            document.addEventListener("scroll", initiateScrollSticky.bind(this, stickyElem));
            window.addEventListener("resize", checkIfRealResize.bind(this, stickyElem));
        }
    }

    function checkIfRealResize() {
        if(window.innerWidth !== document.documentElement.clientWidth){
            setBodyHeight();
        }
    }

    var nextElementSibling;
    function initiateScrollSticky(element) {
        var e = element.offsetTop || 0;
        element.offsetTop || (e = element.offsetParent && element.offsetParent.offsetTop || 0),
            element && window.pageYOffset > e ? element.classList.contains("ph-sticky-block-fixed") || (this.currentStickyHeight = element.offsetHeight,
                element.classList.add("ph-sticky-block-fixed"),
                setBodyHeight(element, !0)) : (element.classList.remove("ph-sticky-block-fixed"),
                    element.style.top = null,
                    nextElementSibling && nextElementSibling.style && nextElementSibling.style.paddingTop && (nextElementSibling.style.paddingTop = null))
    }

    function setBodyHeight(element, e) {
        if (element.classList.contains("ph-sticky-block-fixed") || e) {
            var t = fetchPosition(element);
            if (t && (element.style.top = t + "px"),
                !nextElementSibling) {
                var i = element;
                for (nextElementSibling = i.nextElementSibling; i && "BODY" != i.nodeName && !nextElementSibling;)
                    i = i.parentElement,
                        nextElementSibling = i && i.nextElementSibling
            }
            nextElementSibling && (nextElementSibling.style.paddingTop = (element.offsetHeight + t) + "px")
        }
    }

    function fetchPosition(element) {
        for (var e = document.querySelectorAll(".pcs-sticky-header, .ph-sticky-header, .ph-sticky-block-fixed"), t = 0, i = 0; i < e.length; i++)
            element !== e[i] && (t += e[i].offsetHeight);
        return t
    }

    function observeElem(elem) {
        lazyObserver.observe(elem)
    }

    function elementClosestPolyfill() {
        if (!Element.prototype.matches) {
            Element.prototype.matches =
                Element.prototype.msMatchesSelector ||
                Element.prototype.webkitMatchesSelector;
        }

        if (!Element.prototype.closest) {
            Element.prototype.closest = function (s) {
                var el = this;

                do {
                    if (Element.prototype.matches.call(el, s)) return el;
                    el = el.parentElement || el.parentNode;
                } while (el !== null && el.nodeType === 1);
                return null;
            };
        }
    }

    function loadRecomWidget(){
        loadSpecialElements(recomWidget);
        document.removeEventListener('getUserProfileData', loadRecomWidget);
    }

    function init() {
        document.body.removeAttribute("aurelia-app");
        elementClosestPolyfill()
        lazyLoad()
        fetchDOM()
        attachEventListeners();
        setTimeout(function () {
            loadFramework()
        }, 50);
    }

    return {
        init: init,
        loadFramework: loadFramework
    }
}

window.phEnhancer = new PhEnhancer();
if (window.P) {
    P.config({
        longStackTraces: !1,
        warnings: {
            wForgottenReturn: !1
        }
    }) 
}

if (phApp.siteType !== 'internal') {
    phEnhancer.init()
} else {
    document.body.removeAttribute("aurelia-app");
    phEnhancer.loadFramework();
}
