function hasClass(element, cls) {
    return (' ' + element.className + ' ').indexOf(' ' + cls + ' ') > -1;
}


/*====== Header Mobile Menu functionality Start ======*/

function toggle_menu() {
    // debugger;
    var navBar = document.getElementsByClassName('header-menu')[0];
    // var menuIcon = document.getElementsByClassName('icon-menu')[0];
    var menuIcon = document.querySelector('.mobile-menu');
    
    if (navBar && !hasClass(navBar, 'show') && window.innerWidth <= 1024) {
        menuIcon.firstElementChild.classList.add('icon-cancel');
        menuIcon.firstElementChild.classList.remove('icon-menu');
        // menuIcon.classList.add('icon-cancel');
        navBar.classList.add("show");
        menuIcon.setAttribute('aria-expanded','true');
        // menuIcon.classList.add("icon-cancel");
        document.body.style.overflow = 'hidden';
        navBar.focus();
      
    } else {
        menuIcon.firstElementChild.classList.remove('icon-cancel');
        menuIcon.firstElementChild.classList.add('icon-menu');
        // menuIcon.classList.remove('icon-cancel');
        navBar.classList.remove("show");
        menuIcon.setAttribute('aria-expanded','false');
        // menuIcon.classList.remove("icon-cancel");
        document.body.style.overflow = 'scroll';
    }

}

/*====== Header Mobile Menu functionality End ======*/
function dropDown(){
    var DropDownBtn = document.getElementsByClassName('subnav-dropdown')[0];
    var dropDownListParent = document.getElementsByClassName('drop-down')[0];
    var subMenuNav = document.getElementsByClassName('sub-navigation')[0];
    if(DropDownBtn && subMenuNav.classList.contains('show') == true ){
        dropDownListParent.classList.remove('active');
        DropDownBtn.setAttribute('aria-expanded','false');
        subMenuNav.classList.remove('show');
        subMenuNav.setAttribute('aria-hidden','true');
        dropDownListParent.children[0].getElementsByTagName('i')[0].classList.add('icon-down-arrow');
        dropDownListParent.children[0].getElementsByTagName('i')[0].classList.remove('icon-up-arrow');
    }
    else{
        dropDownListParent.classList.add('active');
        DropDownBtn.setAttribute('aria-expanded','true');
        subMenuNav.classList.add('show');
        subMenuNav.setAttribute('aria-hidden','false');
        dropDownListParent.children[0].getElementsByTagName('i')[0].classList.add('icon-up-arrow');
        dropDownListParent.children[0].getElementsByTagName('i')[0].classList.remove('icon-down-arrow');
    }
}
//to hide dropdown click outside
function persona_focuse_close_menu(){
    dropDown();
}

/*====== Header Mobile Menu functionality End ======*/
document.addEventListener('DOMContentLoaded', setFocus(500));

function setFocus(setTime) {
    setTimeout(function() {
        var getJobcart = phApp.pageName;
        if(getJobcart == "jobcart"){
            document.querySelector("[as-element='ph-job-cart-count-v3']").classList.add('active');
        }
        var getCI = phApp.pageName;
        if(getCI == "candidate-account"){
            document.querySelector("[as-element='ph-social-connect-v1']").classList.add('active');
        }
        var getLogo = document.querySelector('.mobile-logo a');
        if (getLogo || jobCartEle) {
            getLogo.addEventListener('focus', function() {
                if (window.innerWidth <= 767) {
                    if (document.querySelector('.nav').classList.contains('show') == true) {
                        toggle_menu();
                    }
                }
            })
        } else {
            setFocus(500)
        }
    }, setTime);
}

/*====== Header Mobile Menu functionality End ======*/
function dropDown(event){
    // var DropDownBtn = document.getElementsByClassName('subnav-dropdown')[0];
    var getArrowIcon = document.querySelector('.nav-list-items .icon');
    var subItemsMenu = document.querySelectorAll('.sub-navigation');
    var areaOfExpert;
    var parentElement;
    if (event && event.type == "blur") {
        areaOfExpert = document.querySelector('.nav-main-bar .nav-list-items.active button');
    } else {
        areaOfExpert = event.currentTarget;
    }
    if (!areaOfExpert) {
 
    }
     var listItem = areaOfExpert.parentElement;
     var subItems = listItem && listItem.getElementsByClassName('sub-navigation')[0];
     // var subItemsParent = subItems.parentElement;
 
     if(areaOfExpert.length >= 0){
         for (var i = 0; i < areaOfExpert.length; i++) {
             var element = areaOfExpert[i];
             var buttonDatPhValue = element.getAttribute('data-ph-id');
             var buttonAreaDataPhValue = areaOfExpert.getAttribute('data-ph-id');
             if (buttonAreaDataPhValue != buttonDatPhValue) {
                 element.setAttribute('aria-expanded', 'false');
             }
         }
     }
     if(subItemsMenu.length >= 0){
         for (var i = 0; i < subItemsMenu.length; i++) {
             var element = subItemsMenu[i];
             var subMenuDataPhValue = element.getAttribute('data-ph-id');
             var subMenuItemsDataValue = subItems.getAttribute('data-ph-id')
             if (subMenuDataPhValue != subMenuItemsDataValue) {
                 element.classList.remove("show");
                 element.setAttribute('aria-hidden', 'true');
                 element.parentElement.classList.remove('active');
             }
         }
 
     }

     if (subItems.classList.contains('show')){
        subItems.classList.remove("show");
        listItem.classList.remove('active');
        subItems.setAttribute('aria-hidden','true');
        areaOfExpert.setAttribute('aria-expanded','false');
        getArrowIcon.classList.remove('icon-up-arrow')
        getArrowIcon.classList.add('icon-down-arrow')
    } else {
        subItems.classList.add("show");
        listItem.classList.add('active');
        getArrowIcon.classList.remove('icon-down-arrow')
        getArrowIcon.classList.add('icon-up-arrow')
        subItems.setAttribute('aria-hidden','false');
        areaOfExpert.setAttribute('aria-expanded','true');
    }
}

//to hide dropdown click outside
function persona_focuse_close_menu(event){
    // dropDown();
    setTimeout(function(){
        var activeEle = document.activeElement;
        var areaOfExpert = document.querySelector('.nav-main-bar .nav-list-items.active button');
        if(areaOfExpert){
            var listItem = areaOfExpert.parentElement;
            var subItems = listItem && listItem.getElementsByClassName('sub-navigation')[0];
            if(!subItems.contains(activeEle)){
                dropDown(event);
            }
        }
    }, 500)
}

// Header desktop menu  active color

document.addEventListener('DOMContentLoaded', function() {
    // var getTopNav = document.querySelector('.top-nav .list-items');
    // var childListItem = getTopNav.children;
    var getSkiptContent=document.getElementById('skip-content');
    var getPhpageEle=document.querySelector('.ph-page');
    var getUrlLocation = window.location.href;
    var getCurrentPage = getUrlLocation.split(phApp.baseUrl)[1];
    var getHeader = document.querySelector('.ph-header');
    var getPageAnchor = getHeader.querySelector('[data-ph-href="'+getCurrentPage+'"]');
    if(!getPageAnchor){
        getPageAnchor = getHeader.querySelector('[ph-href="'+getCurrentPage+'"]');
    }
    // if(getPageAnchor){
    //     getPageAnchor.parentElement.classList.add('active');
    //     var getBtnMenu=getPageAnchor.parentElement.parentElement.previousElementSibling;
    //     if(getBtnMenu){
    //         if(getBtnMenu.nodeName == "BUTTON"){
    //             getBtnMenu.classList.add('active');
    //         }            
    //     }
    // }
    document.addEventListener( "click", function(e){
        var getHeader = document.querySelector('.ph-header');
        var getSubNavDropDown = getHeader.querySelector('.subnav-dropdown');
        var personaNavBar = document.querySelector('.ph-navigation .main-nav .nav-list-items.active');
        var getSubmenu = getHeader.querySelector('.drop-down .sub-navigation');
        var currentTartget = e.target;
        var getAttribute = currentTartget.getAttribute("data-ph-id");
        var isButtonEle;
        
        if (getSubNavDropDown) {
            isButtonEle = getSubNavDropDown.querySelector('[data-ph-id="' + getAttribute + '"]') || (getSubNavDropDown.getAttribute("data-ph-id") == getAttribute) || getSubmenu.querySelector('[data-ph-id="' + getAttribute + '"]');

        }
        var subItemsMenu = document.querySelectorAll('.main-nav .sub-navigation');

        if (subItemsMenu.length >= 0 && personaNavBar && !personaNavBar.contains(e.target)) {

            for (var i = 0; i < subItemsMenu.length; i++) {
                var element = subItemsMenu[i];
                element.classList.remove("show");
                element.setAttribute('aria-hidden', 'true');
                element.parentElement.classList.remove('active');  
                var dropDownListParent = document.getElementsByClassName('drop-down')[0]
                dropDownListParent.children[0].getElementsByTagName('i')[0].classList.add('icon-down-arrow'); 
                dropDownListParent.children[0].getElementsByTagName('i')[0].classList.remove('icon-up-arrow');
            }
        }

       if(!isButtonEle){
            if(getSubmenu && getSubmenu.classList.contains('show')){
                var dropDownListParent = document.getElementsByClassName('drop-down')[0];
                getSubmenu.classList.remove('show');
                getSubmenu.parentElement.classList.remove('active');
                dropDownListParent.children[0].getElementsByTagName('i')[0].classList.remove('icon-up-arrow');
                dropDownListParent.children[0].getElementsByTagName('i')[0].classList.add('icon-down-arrow');
            }
            else{
            }
        }
        return true;
    })
    // skip to main
    // if(getSkiptContent){
    //     document.getElementById('skip-content').addEventListener('focus',function(){
    //         document.querySelector('.skip-main').style.height="40px";
    //         });
    //     document.getElementById("skip-content").addEventListener("focusout", function(){
    //         document.querySelector('.skip-main').style.height="auto";
    //     });
    // }
    setTimeout(function(){
        // var createNewEle=document.createElement("DIV");
        // var nodeText_El = ("<a id='acc-skip-content'>-</a>");
        var removeRole = document.querySelector('.ph-component-cntr.ph-widget-box');
        var removeRoleInJd = document.querySelector('.banner-block');
        var removeRoleInTestimonialSlider = document.querySelector('.ph-container-content-block.ph-static-slider');
        var removeHeadingRoleInTestimonialSlider = document.querySelector('.ph-component-cntr.ph-widget-box');



        // createNewEle.innerHTML=nodeText_El;
        // createNewEle.setAttribute('class','skipTobody')
        // getPhpageEle.appendChild(createNewEle);
        // getPhpageEle.insertBefore(createNewEle,getPhpageEle.firstChild);
        if(getPhpageEle){
            getPhpageEle.setAttribute('role','main');
        }
        if(removeRole){
            removeRole.removeAttribute('role');
        }
        if(removeRoleInJd){
            removeRoleInJd.removeAttribute('role');
        }
        if(removeRoleInTestimonialSlider){
            removeRoleInTestimonialSlider.firstElementChild.removeAttribute('role');
        }
        if(removeHeadingRoleInTestimonialSlider){
            removeHeadingRoleInTestimonialSlider.removeAttribute('role');
        }
        
    },500);
    // skip to main end
});

document.addEventListener('DOMContentLoaded', function() {
    var getPhpageEle=document.querySelector('.ph-page');
 
	setTimeout(function(){
		var removeRole = document.querySelector('.ph-component-cntr.ph-widget-box');
		var removeRoleInJd = document.querySelector('.banner-block');
		var removeRoleInTestimonialSlider = document.querySelector('.ph-container-content-block.ph-static-slider');
		var removeHeadingRoleInTestimonialSlider = document.querySelector('.ph-component-cntr.ph-widget-box');
	
		if(getPhpageEle){
            getPhpageEle.setAttribute('role','main');
            getPhpageEle.setAttribute('id','acc-skip-content');
		}
		if(removeRole){
			removeRole.removeAttribute('role');
		}
		if(removeRoleInJd){
			removeRoleInJd.removeAttribute('role');
		}
		if(removeRoleInTestimonialSlider){
			removeRoleInTestimonialSlider.firstElementChild.removeAttribute('role');
		}
		if(removeHeadingRoleInTestimonialSlider){
			removeHeadingRoleInTestimonialSlider.removeAttribute('role');
		}
		
	},500);
    
});