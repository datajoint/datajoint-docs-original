// show dropdown content when clicking the menu-text 
function dropmenu() {
    var ddMenu = document.getElementById("dropdown-menu")

    ddMenu.classList.toggle("show");
}

// // close the menu when clicking outside the menu
// window.onclick = function (event) {
//     if (!event.target.matches('.dropdown-versions')) {
//         console.log("clicked outside the menu")
//         var ddMenu = document.getElementById("dropdown-menu")

//         if (ddMenu.classList.contains('show')) {
//             ddMenu.classList.remove('show');
//         }
        
//     }
// }