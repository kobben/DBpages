var isOpen;
var theLightboxIMG;
var theLightbox;
var theMask;
var theTitle;
function simpleLightbox(theURL, thePadding, showTitle) {
    function closeLightbox() {
        if (isOpen) {
            document.removeEventListener("click", closeLightbox);
            document.removeEventListener("scroll", closeLightbox);
            theLightbox.removeChild(theLightboxIMG);
            theLightbox.removeChild(theTitle);
            document.body.removeChild(theLightbox);
            document.body.removeChild(theMask);
            isOpen = false;
        }
    }
    if (isOpen) closeLightbox();
    theMask = document.body.appendChild(document.createElement('div'));
    theMask.id = "lightboxmask";
    theMask.style.top = 0 + window.pageYOffset + "px";
    theMask.style.left = 0  + window.pageXOffset + "px";
    theLightbox = document.body.appendChild(document.createElement('div'));
    theLightbox.id = "lightbox";
    theLightboxIMG = theLightbox.appendChild(document.createElement("IMG"));
    theTitle = theLightbox.appendChild(document.createElement("div"));
    theTitle.id = "theTitle";
    theLightboxIMG.src = theURL;
    theLightboxIMG.onload = function () {
        // calc original IMG width & ratio
        var imgH = this.height;
        var imgW = this.width;
        var imgAspect = imgW / imgH;
        var theMargin = 20;

        var boxH = window.innerHeight - (theMargin * 2) - (thePadding * 2) - 10;
        var boxCY = Math.round(window.innerHeight / 2);
        var boxW = window.innerWidth - (theMargin * 2) - (thePadding * 2) - 10;
        var boxCX = Math.round(window.innerWidth / 2);
        var boxAspect = boxW / boxH;
        if (boxAspect > imgAspect)
            scaleFactor = boxH / imgH;
        else
            scaleFactor = boxW / imgW;
        if (scaleFactor > 1) scaleFactor = 1; //only shrink, don't grow if fits
        H = imgH * scaleFactor;
        W = imgW * scaleFactor;
        T = boxCY - Math.round((imgH * scaleFactor) / 2);
        L = boxCX - Math.round((imgW * scaleFactor) / 2);
        theLightboxIMG.height = H;
        theLightboxIMG.width = W;
        theLightbox.style.padding = thePadding + "px";
        theLightbox.style.top = T + window.pageYOffset + "px";
        theLightbox.style.left = L  + window.pageXOffset + "px";
        theLightbox.style.height = H + "px";
        theLightbox.style.width = W + "px";
        theLightbox.style.display = 'block';
        theMask.style.display = 'block';
        console.log(theURL + ', ' + theLightbox.style.top + ', '+ theLightbox.style.left +
            ', '+ theLightbox.style.height + ', '+ theLightbox.style.width);
        if (showTitle) {
            var Txt = theURL + " (" + imgW + "x" + imgH + "px @ " + Math.round(scaleFactor * 100) + "%)";
            theTitle.innerText = Txt;
        } else {
            theTitle.innerText = "";
        }
        document.addEventListener("click", closeLightbox);
        document.addEventListener("scroll", closeLightbox);
        isOpen = true;
    }
}
