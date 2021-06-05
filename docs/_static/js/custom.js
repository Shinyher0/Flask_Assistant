// noinspection DuplicatedCode

function renderSearch() {
    // Delete text above
    document.querySelector("span.caption-text").remove()

    // Hide stuff aboce
    document.querySelectorAll('input[type="submit"]').forEach(i => i.setAttribute("type", "hidden"));
    // a.setAttribute('type', 'hidden');

    // Customize search btn
    document.querySelectorAll('input[type="text"]').forEach(b => {
        b.style.fontWeight = 300;
        b.style.fontSize = "1em";
        b.style.color = "#2D2D2D";
        b.style.border = "None";
        b.style.backgroundColor = "transparent";
        b.style.fontFamily = "IBM Plex Sans,serif";
        b.style.fontWeight = "bold";
        b.style.padding = "1em";
        b.setAttribute('placeholder', 'Search...');
    });
}

function renderLeftNav() {
    document.querySelectorAll("p.caption").forEach(caption => caption.style.textTransform = "capitalize");
}


function uniformNavLink() {
    let navs = document.querySelectorAll(".nav-link");
    for (let i = 0; i < navs.length; i++) {
        if (navs[i].classList.contains("external") === false) {
            navs[i].classList.add("external");
            navs[i].style.textTransform = "capitalize";
        }
    }
}

window.onload = function () {
    renderSearch();
    renderLeftNav();
    uniformNavLink();
}
