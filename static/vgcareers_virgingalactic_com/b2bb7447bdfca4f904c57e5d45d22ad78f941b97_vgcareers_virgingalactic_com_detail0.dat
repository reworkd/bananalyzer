var phApp = phApp || {};
phApp.remediations = function () {
    var t = [];
    function e() {
        (function () {
            var e = {
                "ph-blog-list-v1-success": this.blogListImagesAltFix,
                "ph-blog-similar-v1-success": this.blogListImagesAltFix,
                "ph-facets-v1-success": this.eventFacets,
                "ph-email-event-v1-success": this.eventFacets,
                "ph-faceted-search-v1-succes": this.eventFacets,
                "ph-twitter-mentions-widget-v1-success": this.twitterImagesAltFix
            };
            phApp && phApp.phb && phApp.phb.eventAggregator && Object.keys(e).forEach(function (r) {
                t.push(phApp.phb.eventAggregator.subscribe(r, function (t) {
                    setTimeout(function () {
                        e[r].call(this, {})
                    }, 300)
                }))
            })
        }
        ).call(this, {})
    }
    function r(t) {
        var e = document.querySelector('[data-widget="ph-cvd-v1"]');
        if (t && e)
            t.parentElement.insertBefore(e, t);
        else if (e) {
            var r = document.querySelector("#skip-content, #ph-skip-content, .ae-skipto-main")
                , i = document.querySelector(".ph-header"),
                lkl = r.closest('.header-layout');
            r = lkl && lkl.firstElementChild || r;
            var a = ((r = r && r.parentElement) ? r.parentElement : i.parentElement,
                r || i);
            a && a.parentElement.insertBefore(e, a)
        }
    }
    function handleHeadingRoleForCaasWidget(widget) {
        setTimeout(function () {
            var headingBlock = widget && widget.querySelector('.ph-widget-box');
            if (headingBlock) {
                var widgetHeadingLevel = headingBlock.querySelector('[data-ph-component-name="h2-heading"]');
                var headingHeroWidget = headingBlock.querySelector('[data-ph-component-name="h1-heading"]');
                var headingList = headingBlock.querySelectorAll('[data-ph-component-name="heading"], [data-ph-component-name="h1-heading"]');
                var descriptionList = headingBlock.querySelectorAll('[data-ph-component-name="description"]');
                var primaryActionLinkList = headingBlock.querySelectorAll('[data-ph-component-name="primary-action-link"]');
                for (var j = 0; j < headingList.length; j++) {
                    headingList[j].removeAttribute('role');
                    headingList[j].removeAttribute('aria-level');
                    var headerExistList = headingList[j].querySelectorAll('h1,h2,h3,h4,h5,h6');

                    if (headingList[j] && !headingList[j].classList.contains('hide') && !headerExistList.length && descriptionList[j] && !descriptionList[j].classList.contains('hide') || primaryActionLinkList[j] && !primaryActionLinkList[j].classList.contains('hide')) {
                        var primaryActionLinkArialabelProperty = primaryActionLinkList[j].querySelector('.action-link');
                        if (!primaryActionLinkArialabelProperty.getAttribute("aria-label") && primaryActionLinkList[j] && !primaryActionLinkList[j].classList.contains('hide') && headingList[j] && !headingList[j].classList.contains('hide')) {
                            var primaryActionLinkArialabelValue = primaryActionLinkList[j].querySelector('.action-link> *:first-child').textContent;
                            var headingValue = headingList[j].firstChild && headingList[j].firstChild.textContent;
                            var primaryActionLinkArialabel = primaryActionLinkArialabelValue.concat(" ", headingValue);
                            primaryActionLinkArialabelProperty.setAttribute('aria-label', primaryActionLinkArialabel);
                        }
                        if (widgetHeadingLevel && !widgetHeadingLevel.classList.contains('hide') && !headingBlock.classList.contains('heading-block-hide')) {
                            headingList[j].setAttribute('aria-level', '3');
                            headingList[j].setAttribute('role', 'heading');
                        } else if (headingHeroWidget && headingHeroWidget.tagName == 'DIV') {
                            headingList[j].setAttribute('aria-level', '1');
                            headingList[j].setAttribute('role', 'heading');
                        } else {
                            if (!headingHeroWidget) {
                                headingList[j].setAttribute('aria-level', '2');
                                headingList[j].setAttribute('role', 'heading');
                            }
                        }
                    } else if (headingHeroWidget && headingHeroWidget.tagName == 'DIV') {
                        headingList[j].setAttribute('aria-level', '1');
                        headingList[j].setAttribute('role', 'heading');
                    }
                }
            }
        }, 3000);
    }
    
    function handleRoleForHeadings() {
        var widgets = document.querySelectorAll('.ph-widget');
        for (var i = 0; i < widgets.length; i++) {
            var headingBlock = widgets[i].querySelector('.ph-widget-box');
            if (headingBlock) {
                var widgetHeadingLevel = headingBlock.querySelector('[ctr-content-key="title"], [component-content-key="h2-heading"]');
                var headingHeroWidget = headingBlock.querySelector('[class^="ph-hero"]'); //('[component-content-key="h1-heading"]');
                var headingList = headingBlock.querySelectorAll('[component-content-key="heading"], [card-content-key="heading"], [component-content-key="h1-heading"]');
                var descriptionList = headingBlock.querySelectorAll('[component-content-key="description"], [card-content-key="description"]');
                var primaryActionLinkList = headingBlock.querySelectorAll('[component-content-key="primary-action-link"], [card-content-key="primary-action-link"]');
                for (var j = 0; j < headingList.length; j++) {
                    var headingRole = headingList[j].querySelector('[key-role], [card-content-key="heading"] > *:first-child, [component-content-key="heading"] > *:first-child, [component-content-key="h1-heading"] > *:first-child');
                    headingRole.removeAttribute('role');
                    headingRole.removeAttribute('aria-level');
    
                    // var primaryActionLinkArialabelProperty = primaryActionLinkList[j].querySelector('.action-link');
                    // var primaryActionLinkValue = primaryActionLinkList[j].querySelector('.action-link> *:first-child').innerHTML;
                    // // alert(primaryActionLinkValue);
                    // var headingValue = headingRole.querySelector('ppc-content').innerHTML;
                    // // alert(headingValue);
                    // var primaryActionLinkArialabel = primaryActionLinkValue.concat(" ", headingValue);
                    // // alert(primaryActionLinkArialabel);
                    var headerExistList = headingList[j].querySelectorAll('h1,h2,h3,h4,h5,h6');
                    if (headingRole && headingList[j] && !headingList[j].classList.contains('hide') && !headerExistList.length && descriptionList[j] && !descriptionList[j].classList.contains('hide') || primaryActionLinkList[j] && !primaryActionLinkList[j].classList.contains('hide')) {
                        // headingRole.setAttribute('role', 'heading');
                        // primaryActionLinkArialabelProperty.setAttribute('aria-label', primaryActionLinkArialabel);
                        // var primaryActionLinkArialabelProperty = primaryActionLinkList[j].querySelector('.action-link');
                        if (primaryActionLinkList[j] && primaryActionLinkList[j] && !primaryActionLinkList[j].classList.contains('hide') && headingList[j] && !headingList[j].classList.contains('hide')) {
                            var primaryActionLinkArialabelProperty = primaryActionLinkList[j].querySelector('.action-link');
                            // primaryActionLinkArialabelProperty.removeAttribute("aria-label");
                            if (!primaryActionLinkArialabelProperty.getAttribute("aria-label")) {
                                var primaryActionLinkArialabelValue = primaryActionLinkList[j].querySelector('.action-link> *:first-child').textContent;
                                // console.log(primaryActionLinkArialabelValue);
                                var headingValue = headingRole.querySelector('ppc-content').textContent;
                                console.log(headingValue);
                                var primaryActionLinkArialabel = primaryActionLinkArialabelValue.concat(" ", headingValue);
                                console.log(primaryActionLinkArialabel);
                                primaryActionLinkArialabelProperty.setAttribute('aria-label', primaryActionLinkArialabel);
                            }
                        }
                        if (widgetHeadingLevel && !widgetHeadingLevel.classList.contains('hide') && !headingBlock.classList.contains('heading-block-hide')) {
                            headingRole.setAttribute('aria-level', '3');
                            headingRole.setAttribute('role', 'heading');
                        } else if (headingHeroWidget && headingRole.tagName == 'SPAN') {
                            headingRole.setAttribute('aria-level', '1');
                            headingRole.setAttribute('role', 'heading');
                        } else {
                            // if (!headingHeroWidget) {
                            headingRole.setAttribute('aria-level', '2');
                            headingRole.setAttribute('role', 'heading');
                            // }
                        }
                    } else if (headingHeroWidget && headingRole.tagName == 'SPAN') {
                        headingRole.setAttribute('aria-level', '1');
                        headingRole.setAttribute('role', 'heading');
                    }
                }
            }
        }
    }

    return e.prototype.iframeTitleFix = function () {
        var t = document.querySelectorAll("iframe");
        if (t && t.length)
            for (var e = 0; e < t.length; e++)
                if (!t[e].getAttribute("title")) {
                    var r = t[e].getAttribute("src");
                    if (r) {
                        var i = (r = (r = r.replace(new RegExp("https:[/]{0,2}||http:[/]{0,2}"), "")).replace("www.", "")).split(".");
                        t[e].setAttribute("title", i[0])
                    } else
                        t[e].setAttribute("tabindex", -1),
                            t[e].setAttribute("aria-hidden", !0)
                }
    }
        ,
        e.prototype.staticLearnMoreSeeMore = function () {
            for (var t = document.querySelectorAll('div[data-widget="ph-html-v1"]'), e = 0; e < t.length; e++)
                for (var r = t[e].querySelectorAll(".ph-card"), i = 0; i < r.length; i++) {
                    for (var a = r[i].querySelector('[card-content-key="heading"], [component-content-key="heading"], [component-content-key="meta-label"], [card-content-key="meta-label"]'), l = r[i].querySelectorAll('[component-content-key="primary-action-link"] a, [card-content-key="primary-action-link"] a'), o = 0; o < l.length; o++)
                        if (a && l[o]) {
                            var n = (a.innerText || "").trim()
                                , u = l[o].innerText.trim() || "";
                            (d = (l[o].getAttribute("aria-label") || l[o].getAttribute("title") || l[o].getAttribute("data-ph-tevent-attr-trait75") || "").trim()) && -1 == d.indexOf(u) ? d = u + " " + d : (!d || d.toLowerCase() == u.toLowerCase() && u.toLowerCase() != n.toLowerCase()) && (d = u + " " + n),
                                l[o].setAttribute("aria-label", d.trim()),
                                l[o].removeAttribute("title")
                        }
                    for (var c = r[i].querySelectorAll("[href^='mailto']"), p = 0; p < c.length; p++)
                        c[p].getAttribute("title") || c[p].getAttribute("aria-label") || c[p].setAttribute("aria-label", "click here to access the mail client");
                    l = r[i].querySelectorAll("ppc-content a");
                    for (var g = 0; g < l.length; g++) {
                        var s = l[g].getAttribute("aria-label") || l[g].getAttribute("title") || ""
                            , b = l[g].innerText || "";
                        -1 == s.indexOf(b) && s && (b = b && s && s + " " + b),
                            b = b || s || "Click here to navigate to link",
                            l[g].setAttribute("aria-label", b.trim()),
                            l[g].removeAttribute("title")
                    }
                    for (var h = t[e].querySelectorAll('a[ph-cms-link="true"]'), A = 0; A < h.length; A++) {
                        var d;
                        if (!(d = (h[A].getAttribute("aria-label") || h[A].getAttribute("title") || h[A].getAttribute("data-ph-tevent-attr-trait75") || "").trim()))
                            if (d = h[A].getAttribute("ph-href") || h[A].getAttribute("data-ph-href"))
                                (s = (d = (d = d.split("?")[0]).split("/"))[d.length - 1]) || (s = d[d.length - 2] || d[0]),
                                    d = s.replace(/-/gi, " ");
                        h[A].setAttribute("aria-label", d.trim()),
                            h[A].removeAttribute("title")
                    }
                }
        }
        ,
        e.prototype.learnMoreFixesForNonStandard = function () {
            for (var t = document.querySelectorAll('[data-widget="ph-html-v1"] .common-inner-block,[data-widget="ph-html-v1"] .about-innercontent, [data-widget="ph-html-v1"] .staticContent'), e = 0; e < t.length; e++) {
                var r, i = t[e].querySelectorAll("a"), a = t[e].querySelector(".static-block-heading, h2");
                a && (r = a.innerText);
                for (var l = 0; l < i.length; l++) {
                    var o = i[l].getAttribute("aria-label") || i[l].getAttribute("title") || r || i[l].getAttribute("data-ph-tevent-attr-trait75")
                        , n = i[l].innerText;
                    o && -1 == o.indexOf(n) ? o = o + " " + n : (!o || o.toLowerCase() == n.toLowerCase() && n.toLowerCase() != headingText) && (o = headingText + " " + n),
                        i[l].setAttribute("aria-label", o.trim()),
                        i[l].removeAttribute("title")
                }
            }
        }
        ,
        e.prototype.polyfills = function () {
            Element.prototype.matches || (Element.prototype.matches = Element.prototype.msMatchesSelector || Element.prototype.webkitMatchesSelector),
                Element.prototype.closest || (Element.prototype.closest = function (t) {
                    var e = this;
                    do {
                        if (e.matches(t))
                            return e;
                        e = e.parentElement || e.parentNode
                    } while (null !== e && 1 === e.nodeType);
                    return null
                }
                )
        }
        ,
        e.prototype.globalSearchV3LabelMapping = function () {
            for (var t = document.querySelectorAll('div[data-widget="ph-global-search-v3"], div[data-widget="ph-global-search-v1"]'), e = ["default", "placeholder-gb", "glbl-search", "glb-search-mes"], r = 0; r < t.length; r++) {
                var i = t[r].getAttribute("original-view");
                if (-1 != e.indexOf(i))
                    for (var a = t[r].querySelectorAll("input"), l = 0; l < a.length; l++) {
                        var o = a[l].closest("section");
                        if (o) {
                            var n = a[l].getAttribute("name");
                            if (n) {
                                var u = o.querySelector('label[for="' + n + '"]');
                                if (u)
                                    u && (a[l].hasAttribute("id") || a[l].setAttribute("id", n));
                                else {
                                    var c = document.createElement("label");
                                    c.innerHTML = a[l].getAttribute("placeholder") || "",
                                        c.setAttribute("class", "sr-only"),
                                        c.style.position = "absolute",
                                        c.setAttribute("for", n),
                                        a[l].hasAttribute("id") || a[l].setAttribute("id", n),
                                        a[l].parentElement.insertBefore(c, a[l])
                                }
                            }
                        }
                    }
            }
        }
        ,
        e.prototype.dropzoneInput = function () {
            var t = document.querySelectorAll('input[type="file"].dz-hidden-input');
            if (t.length)
                for (var e = 0; e < t.length; e++)
                    t[e].setAttribute("aria-hidden", !0),
                        t[e].setAttribute("tabindex", "-1")
        }
        ,
        e.prototype.twitterImagesAltFix = function () {
            var t = document.querySelectorAll('[data-widget="ph-twitter-mentions-widget-v1"]');
            if (t && t.length)
                for (var e = 0; e < t.length; e++) {
                    var r = t[e].querySelectorAll("img");
                    if (r && r.length)
                        for (var i = 0; i < r.length; i++) {
                            (!r[i].getAttribute("alt") || r[i].getAttribute("alt") && -1 != ["img", "image"].indexOf(r[i].getAttribute("alt").toLowerCase())) && r[i].setAttribute("alt", "")
                        }
                }
        }
        ,
        e.prototype.virtualTourImgFix = function () {
            var t = document.querySelectorAll('div[data-widget="ph-virtual-tour-v1"]');
            if (t.length)
                for (var e = 0; e < t.length; e++) {
                    var r = t[e].querySelectorAll("img");
                    if (r.length)
                        for (var i = 0; i < r.length; i++)
                            r[i].hasAttribute("alt") || r[i].setAttribute("alt", "")
                }
        }
        ,
        e.prototype.blogListImagesAltFix = function () {
            var t = document.querySelectorAll('div[data-widget="ph-blog-list-v1"], div[data-widget="ph-blog-similar-v1"]');
            if (t.length)
                for (var e = 0; e < t.length; e++) {
                    var r = t[e].querySelectorAll(".blog-list-item")
                        , i = ["image"];
                    if (r.length)
                        for (var a = 0; a < r.length; a++)
                            for (var l = r[a].querySelector(".article-name"), o = r[a].querySelector(".author-name"), n = r[a].querySelectorAll("img"), u = 0; u < n.length; u++)
                                n[u].hasAttribute("alt") && -1 == i.indexOf(n[u].getAttribute("alt").trim().toLowerCase()) || (n[u].classList.contains("author-thumb") ? n[u].setAttribute("alt", o.innerText) : n[u].setAttribute("alt", l.innerText))
                }
        }
        ,
        e.prototype.shortHeaderHamburgerMenu = function () {
            for (var t = document.querySelectorAll(".ph-header"), e = 0; e < t.length; e++) {
                for (var r = t[e].querySelectorAll("a.mobile-menu, button.mobile-menu, .mobile-nav-controls a, .mobile-nav-icon a, .mobile-menu a, .navbar-toggle, .main-nav-toggle a"), i = 0; i < r.length; i++) {
                    l = (l = r[i].getAttribute("aria-label") || r[i].getAttribute("title") || r[i].getAttribute("data-ph-at-id") || "menu").replace(/-/gi, " "),
                        r[i].setAttribute("aria-label", l),
                        r[i].removeAttribute("title")
                }
                var a = t[e].querySelectorAll('[ph-tevent="logo_click"]');
                for (i = 0; i < a.length; i++) {
                    var l = a[i].getAttribute("aria-label") || a[i].getAttribute("title") || a[i].getAttribute("data-ph-tevent-attr-trait62") || a[i].getAttribute("data-ph-at-id") || "";
                    a[i].setAttribute("aria-label", l),
                        a[i].removeAttribute("title");
                    var o = a[i].querySelector("img");
                    if (o) {
                        var n = o.getAttribute("alt") || l || "";
                        o.setAttribute("alt", n)
                    }
                }
            }
        }
        ,
        e.prototype.headerAriaFixes = function () {
            for (var t = /icon-(.{1,} {0,})/, e = document.querySelectorAll(".ph-header"), r = 0; r < e.length; r++) {
                for (var i = e[r].querySelectorAll(".mobile-menu-block button"), a = 0; a < i.length; a++)
                    if (!i[a].hasAttribute("aria-label")) {
                        var l = i[a].getAttribute("title");
                        i[a].setAttribute("aria-label", l),
                            i[a].removeAttribute("title")
                    }
                for (var o = e[r].querySelectorAll("a"), n = 0; n < o.length; n++) {
                    var u, c = o[n].getAttribute("aria-label") || o[n].getAttribute("title") || o[n].getAttribute("data-ph-tevent-attr-trait62") || o[n].getAttribute("data-ph-tevent-attr-trait213") || o[n].innerText.trim();
                    if (!c && (u = o[n].querySelector(".icon")) && t.test(u.className)) {
                        var p = t.exec(u.className);
                        p && (c = p[1])
                    }
                    o[n].setAttribute("aria-label", c),
                        o[n].removeAttribute("title")
                }
                var g = e[r].querySelectorAll("img");
                for (n = 0; n < g.length; n++)
                    if (!g[n].hasAttribute("alt")) {
                        var s = (g[n].getAttribute("src") || "").split("/");
                        s = g[n].getAttribute("alt") || (s[s.length - 1] || "").split(".")[0],
                            g[n].setAttribute("alt", s)
                    }
            }
        }
        ,
        e.prototype.paragraphEmptyUserDefinedAnchorsNHeaders = function () {
            var t = document.querySelectorAll('div[original-view="ph-paragraph-cc-view1-option1"]');
            if (t.length)
                for (var e = 0; e < t.length; e++) {
                    var r = t[e].querySelectorAll("ppc-content a, ppc-content h1, ppc-content h2, ppc-content h3, ppc-content h4, ppc-content h5,  ppc-content h6");
                    if (r.length)
                        for (var i = 0; i < r.length; i++)
                            r[i].getAttribute("aria-label") || (r[i].innerText.trim().length ? r[i].setAttribute("aria-label", r[i].innerText) : r[i].setAttribute("aria-hidden", "true"))
                }
        }
        ,
        e.prototype.fyfAnchorsAriaLabelWithTitle = function () {
            var t = document.querySelectorAll('[data-widget="ph-find-your-fit-container-v1"]');
            if (t.length)
                for (var e = 0; e < t.length; e++) {
                    var r = t[e].querySelectorAll("a[title]");
                    if (r.length)
                        for (var i = 0; i < r.length; i++)
                            r[i].getAttribute("title").trim().length && !r[i].getAttribute("aria-label") && r[i].setAttribute("aria-label", r[i].getAttribute("title"))
                }
        }
        ,
        e.prototype.sliderPrimaryLinkArialabelFix = function () {
            for (var t = document.querySelectorAll('div[original-view="ph-media-large-testimonial-left-cc-slider-view2-option1"]'), e = 0; e < t.length; e++)
                for (var r = t[e].querySelectorAll('[card-name="ph-media-large-testimonial-left-cc-view2"]'), i = ["learn more", "read more", "see more"], a = 0; a < r.length; a++) {
                    var l = r[a].querySelector('[component-content-key="heading"]')
                        , o = r[a].querySelector('[component-content-key="meta-label"]')
                        , n = r[a].querySelector('[component-content-key="primary-action-link"] a')
                        , u = l || o;
                    if (u && n && (!n.getAttribute("aria-label") || -1 != i.indexOf(n.getAttribute("aria-label").toLowerCase()))) {
                        var c = u.innerText;
                        c.trim().length || (c = "Click here for ");
                        var p = c + " " + n.innerText;
                        n.setAttribute("aria-label", p)
                    }
                }
        }
        ,
        e.prototype.emptyHeadings = function () {
            for (var t = document.querySelectorAll('h1, h2, h3, h4, h5, h6, p, [role="heading"]'), e = 0; e < t.length; e++)
                t[e].innerText.trim().length || t[e].setAttribute("aria-hidden", !0)
        }
        ,
        e.prototype.candidateProfileFix = function () {
            var t = document.querySelectorAll('div[data-widget="ph-candidate-account-v1"]');
            if (t.length)
                for (var e = 0; e < t.length; e++) {
                    var r = t[e].querySelectorAll("label[for]");
                    if (r.length)
                        for (var i = 0; i < r.length; i++) {
                            var a, l = r[i].getAttribute("for"), o = r[i].closest("form");
                            o && (a = o.querySelector("input[name=" + l + "]")) && a.getAttribute("id") != l && a.setAttribute("id", l)
                        }
                }
        }
        ,
        e.prototype.footerFixes = function () {
            var t = document.querySelectorAll(".ph-footer");
            if (t)
                for (var e = 0; e < t.length; e++) {
                    var r = t[e].querySelectorAll(".social-icons a img, .social-icon-list li a img, .social-icons-block a img");
                    if (r.length)
                        for (var i = 0; i < r.length; i++) {
                            var a = r[i].closest("a");
                            if (0 == a.innerText.trim().length && !r[i].hasAttribute("alt")) {
                                var l = a.getAttribute("key-href") || a.getAttribute("data-ph-tevent-attr-trait213") || "";
                                r[i].setAttribute("alt", l)
                            }
                        }
                    for (var o = t[e].querySelectorAll("ppc-content a"), n = 0; n < o.length; n++) {
                        var u = o[n].getAttribute("aria-label") || o[n].getAttribute("title") || o[n].innerText;
                        o[n].setAttribute("aria-label", u),
                            o[n].removeAttribute("title")
                    }
                    for (var c = t[e].querySelectorAll(".image-out img"), p = 0; p < c.length; p++)
                        c[p].getAttribute("alt") || c[p].setAttribute("alt", "");
                    var g = t[e].querySelectorAll("a")
                        , s = /icon-([a-zA-Z]{1,} {0,})/;
                    for (i = 0; i < g.length; i++)
                        if (!g[i].getAttribute("aria-label") && !g[i].innerText.trim().length) {
                            var b = g[i].getAttribute("title");
                            if (b)
                                g[i].setAttribute("aria-label", b);
                            else {
                                var h = g[i].querySelector("i");
                                if (h && h.className && s.test(h.className)) {
                                    var A = s.exec(h.className);
                                    A && g[i].setAttribute("aria-label", A[1])
                                }
                            }
                        }
                    var d = t[e].querySelectorAll('[ph-tevent="logo_click"]');
                    for (i = 0; i < d.length; i++) {
                        var v = d[i].getAttribute("aria-label") || d[i].getAttribute("title") || d[i].getAttribute("data-ph-tevent-attr-trait62") || d[i].getAttribute("data-ph-at-id") || "";
                        d[i].setAttribute("aria-label", v),
                            d[i].removeAttribute("title");
                        var f = d[i].querySelector("img");
                        if (f) {
                            l = f.getAttribute("alt") || v || "";
                            f.setAttribute("alt", l)
                        }
                    }
                }
        }
        ,
        e.prototype.emailJobLabelFix = function () {
            var t = document.querySelectorAll('div[data-widget="ph-email-job-v1"]');
            if (t.length)
                for (var e = 0; e < t.length; e++) {
                    var r = t[e].querySelectorAll("label[for]");
                    if (r.length)
                        for (var i = 0; i < r.length; i++) {
                            var a = r[i].parentElement;
                            if (a) {
                                var l = r[i].getAttribute("for")
                                    , o = a.querySelector("input#" + l + ", input[name=" + l + "]");
                                if (!o) {
                                    var n = window.getComputedStyle(r[i])
                                        , u = window.getComputedStyle(a);
                                    "none" != n.display || r[i].classList.contains("sr-only") || "none" == u.display || (r[i].classList.add("sr-only"),
                                        r[i].style.display = "block",
                                        r[i].style.position = "absolute"),
                                        (o = r[i].parentElement.querySelector("input")) && "INPUT" == o.tagName && (o.setAttribute("name", l),
                                            o.setAttribute("id", l))
                                }
                            }
                        }
                }
        }
        ,
        e.prototype.fixInputsWithoutId = function () {
            for (var t = document.querySelectorAll("input[id]"), e = 0; e < t.length; e++) {
                var r = t[e];
                if (!r.getAttribute("name")) {
                    var i = r.closest("form");
                    if (i)
                        i.querySelector('label[for="' + r.getAttribute("id") + '"]') && r.setAttribute("name", r.getAttribute("id"))
                }
            }
        }
        ,
        e.prototype.noJobAnchor = function () {
            var t = document.querySelectorAll('div[data-widget="ph-job-cart-v2"]');
            if (t.length)
                for (var e = 0; e < t.length; e++) {
                    var r = t[e].querySelectorAll(".no-jobs-view a");
                    if (r.length)
                        for (var i = 0; i < r.length; i++)
                            if (!r[i].getAttribute("aria-label")) {
                                var a = r[i].getAttribute("title") || noJobAnchors[i].innerText;
                                a && r[i].setAttribute("aria-label", a)
                            }
                }
        }
        ,
        e.prototype.oAuthAriaLabelsFix = function () {
            for (var t = document.querySelectorAll('[data-widget="ph-oauthsignin-v1"]'), e = ["default"], r = 0; r < t.length; r++) {
                var i = t[r].getAttribute("original-view");
                if (-1 != e.indexOf(i)) {
                    var a = t[r].querySelector(".phs-signout-block .user-name");
                    if (a) {
                        var l = a.getAttribute("title")
                            , o = a.getAttribute("aria-label") || l || "dropdown";
                        a.setAttribute("aria-label", o),
                            a.removeAttribute("title")
                    }
                    var n = t[r].querySelector(".phs-signin-block .signin-link");
                    if (n) {
                        var u = n.getAttribute("title")
                            , c = n.getAttribute("aria-label") || u || "dropdown";
                        n.setAttribute("aria-label", c),
                            n.removeAttribute("title")
                    }
                }
            }
        }
        ,
        e.prototype.loaderImageAltFix = function () {
            for (var t = document.querySelectorAll(".ph-loading"), e = 0; e < t.length; e++) {
                var r = t[e].querySelector("img");
                r && !r.hasAttribute("alt") && r.setAttribute("alt", "")
            }
        }
        ,
        e.prototype.execAll = function () {
            for (var t in this)
                "function" == typeof this[t] && "execAll" != t && this[t].call(this, {})
        }
        ,
        e.prototype.eventFacets = function () {
            var t = document.querySelectorAll('div[data-widget="ph-email-event-v1"], div[data-widget="ph-facets-v1"], div[data-widget="ph-faceted-search-v1"], div[data-widget="ph-event-search-v1"]');
            if (t.length)
                for (var e = 0; e < t.length; e++) {
                    var r = t[e].querySelectorAll(".phs-facet-innersearch, .form-group, .phs-filter-panels, .form-group .has-feedback")
                        , i = [];
                    if (r.length)
                        for (var a = 0; a < r.length; a++) {
                            var l = r[a].querySelector('input[type="search"], input[type="text"]')
                                , o = r[a].querySelector("label");
                            if (l && o) {
                                var n = l.getAttribute("name");
                                if (!l.getAttribute("name") && o && o.getAttribute("for")) {
                                    var u = o.getAttribute("for");
                                    -1 != i.indexOf(u) ? (u += a,
                                        o.setAttribute("for", u)) : i.push(u),
                                        l.hasAttribute("id") || l.setAttribute("id", u)
                                } else
                                    l.getAttribute("name") && o.getAttribute("for") != l.getAttribute("name") && (-1 != i.indexOf(n) ? (n += a) : i.push(n),
                                        o.setAttribute("for", n),
                                        l.hasAttribute("id") || l.setAttribute("id", n))
                            }
                        }
                    for (var c = t[e].querySelectorAll("a"), p = 0; p < c.length; p++) {
                        var g = c[p].getAttribute("aria-label") || c[p].getAttribute("title") || c[p].getAttribute("data-ph-at-id") || "";
                        c[p].setAttribute("aria-label", g),
                            c[p].removeAttribute("title")
                    }
                }
        }
        ,
        e.prototype.emptyAltTags = function () {
            for (var t = document.querySelectorAll('ppc-content[type="image"], ppc-content.ppc-text'), e = /.[.]{1}png$|.[.]{1}jpeg$|.[.]{1}jpg$|.[.]{1}gif$/, r = 0; r < t.length; r++)
                for (var i = t[r].querySelectorAll("img"), a = 0; a < i.length; a++) {
                    var l = i[a].getAttribute("alt") || "";
                    if (e.test(i[a].getAttribute("alt"))) {
                        var o = l.split(".")[0];
                        l = o || ""
                    }
                    i[a].setAttribute("alt", l)
                }
        }
        ,
        e.prototype.inputLabelsForProfileCandidate = function () {
            for (var t = document.querySelectorAll('div[data-widget="ph-candidate-account-v1"], div[data-widget="ph-profile-update-v1"]'), e = ["default", "simple-form"], r = 0; r < t.length; r++) {
                var i = t[r].getAttribute("original-view");
                if (-1 != e.indexOf(i))
                    for (var a = t[r].querySelectorAll("input"), l = 0; l < a.length; l++) {
                        var o = a[l].getAttribute("id") || a[l].getAttribute("name");
                        if (!o) {
                            var n = a[l].parentElement.querySelectorAll("label");
                            n && 1 == n.length && (o = n[0].getAttribute("for"),
                                a[l].setAttribute("id", o),
                                a[l].setAttribute("name", o))
                        }
                        if (t[r].querySelector("label[for=" + o + "]")) {
                            var u = a[l].getAttribute("id") || a[l].getAttribute("name");
                            a[l].setAttribute("id", u),
                                a[l].getAttribute("name") || a[l].setAttribute("name", u)
                        } else {
                            var c = document.createElement("label");
                            c.innerHTML = a[l].getAttribute("placeholder") || "",
                                c.setAttribute("class", "sr-only"),
                                c.style.position = "absolute",
                                c.setAttribute("for", o),
                                a[l].hasAttribute("id") || a[l].setAttribute("id", o),
                                a[l].parentElement.insertBefore(c, a[l])
                        }
                    }
            }
        }
        ,
        e.prototype.locationMapv1ImagesAlt = function () {
            for (var t = document.querySelectorAll('div[data-widget="ph-location-map-v1"]'), e = 0; e < t.length; e++)
                for (var r = t[e].querySelectorAll(".phs-location-map-area img"), i = 0; i < r.length; i++)
                    r[i].getAttribute("alt") || r[i].setAttribute("alt", "")
        }
        ,
        e.prototype.languageSelector = function () {
            for (var t = document.querySelectorAll('div[data-widget="ph-language-selector-v1"]'), e = ["default"], r = 0; r < t.length; r++) {
                var i = t[r].getAttribute("original-view");
                if (-1 != e.indexOf(i))
                    for (var a = t[r].querySelectorAll(".phs-lang-select-area a"), l = 0; l < a.length; l++) {
                        var o = a[l].getAttribute("aria-label") || a[l].getAttribute("title") || a[l].getAttribute("data-ph-at-language-text");
                        a[l].setAttribute("aria-label", o),
                            a[l].removeAttribute("title")
                    }
            }
        }
        ,
        e.prototype.growWithOus = function () {
            for (var t = document.querySelectorAll('[data-widget="ph-grow-with-us-v1"]'), e = 0; e < t.length; e++) {
                t[e].getAttribute("original-view");
                var r = t[e].querySelector(".slider-actions .prev")
                    , i = t[e].querySelector(".slider-actions .next");
                if (r) {
                    var a = r.getAttribute("aria-label") || r.getAttribute("title") || r.innerText.trim() || r.getAttribute("ph-tevent");
                    r.setAttribute("aria-label", a)
                }
                if (i) {
                    var l = i.getAttribute("aria-label") || i.getAttribute("title") || i.innerText.trim() || i.getAttribute("ph-tevent");
                    i.setAttribute("aria-label", l)
                }
            }
        }
        ,
        e.prototype.reorderCookieForAlly = function () {
            if (phApp.ddo && phApp.ddo.siteConfig && phApp.ddo.siteConfig.data && phApp.ddo.siteConfig.data.ally && phApp.ddo.siteConfig.data.ally.reorderCookie) {
                var t = document.querySelector('section[ph-module="gdpr"]')
                    , e = t && t.querySelector('[data-widget="ph-cookie-popup-v2"]');
                if (t && e) {
                    var i = document.querySelector("#skip-content, #ph-skip-content, .ae-skipto-main")
                        , a = document.querySelector(".ph-header"),
                        lkl = i.closest('.header-layout');
                    i = lkl && lkl.firstElementChild || i;
                    var l = ((i = i && i.parentElement) ? i.parentElement : a.parentElement,
                        i || a);
                    l && l.parentElement.insertBefore(t, l),
                        r(t)
                } else
                    r(!1)
            } else
                r(!1)
        }
        ,
        e.prototype.addTitleForJobEvent = function () {
            switch (window.phApp && window.phApp.pageName) {
                case "job":
                    !function () {
                        if (!document.querySelector("title")) {
                            var t = document.createElement("title")
                                , e = document.querySelector('[data-ph-at-id="job-completion-info"]')
                                , r = e && e.innerText || "Job expired";
                            t.innerText = r;
                            var i = document.querySelector("head")
                                , a = i && i.firstElementChild;
                            a && a.parentNode.insertBefore(t, a)
                        }
                    }();
                    break;
                case "event":
                    !function () {
                        if (!document.querySelector("title")) {
                            var t = document.createElement("title")
                                , e = document.querySelector(".expire-job-view .widget-container h2")
                                , r = e && e.innerText || "Event expired";
                            t.innerText = r;
                            var i = document.querySelector("head")
                                , a = i && i.firstElementChild;
                            a && a.parentNode.insertBefore(t, a)
                        }
                    }()
            }
        },
        e.prototype.fullLinkModifier = function(){
            var links  = document.querySelectorAll('a[ph-cms-link], a[class="pcs-full-card-link"]');
            if(links.length){
                for(let i=0;i<links.length;i++){
                    let link = links[i];
                    link.setAttribute('role', 'link');
                    link.innerHTML = '';
                    let ariaLabel = link.getAttribute('aria-label');
                    if(ariaLabel && ariaLabel.trim().length > 0){
                        var sp = document.createElement('span');
                        sp.classList.add('sr-only');
                        sp.innerHTML = ariaLabel;
                        link.appendChild(sp);
                    }
                }
            }
        },
        e.prototype.addRolechangesForCaasWidgets = function () {
            window.addEventListener("ph:ex:widgetLoaded", function (event) {
                if (event && event.detail && event.detail.elem) {
                    handleHeadingRoleForCaasWidget(event.detail.elem);
                }
            });
            setTimeout(function(){
                if (document.readyState == 'complete') {
                    handleHeadingRoleForCaasWidget();
                    handleRoleForHeadings();
                } else {
                    window.addEventListener('load', function () {
                        handleHeadingRoleForCaasWidget();
                        handleRoleForHeadings();
                    });
                }
            },3000);
        },
        e.prototype.handlePhHrefToAvoidBlankHref = function(){
            var a = document.querySelectorAll('[ph-href]');
            for(var o = 0; o<a.length;o++){
                var urlSrc;
                var aEl = a[o];
                var hrefValue = aEl.getAttribute('href');
                var newValue = aEl.getAttribute('ph-href');

                if (aEl.getAttribute('key-href') && hrefValue && hrefValue.length){
                    newValue = hrefValue;
                }
                //to avoid to form a absolute URL	
                if (newValue.startsWith("/") || newValue.startsWith("javascript:void(0)") || newValue.startsWith("mailto:") || newValue.startsWith("tel:") || newValue.startsWith("#")) {
                    urlSrc = newValue;
                }//forming absolute url if newvalue fails
                else {
                    urlSrc = newValue.indexOf('//') == -1 ? phApp.baseUrl + newValue : newValue;
                }
                aEl.setAttribute('href', urlSrc);
            }
        }
        ,
        new e
}(),
    setTimeout(function () {
        phApp.remediations && phApp.remediations.execAll && phApp.remediations.execAll()
    }, 300);
