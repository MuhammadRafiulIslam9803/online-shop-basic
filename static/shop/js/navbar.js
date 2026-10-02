console.log("Navbar JS loaded");

const mobileMenuButton = document.getElementById("mobileMenuButton");
const mobileMenu = document.getElementById("mobileMenu");
const menuIcon = document.getElementById("menuIcon");

if (mobileMenuButton) {
    mobileMenuButton.addEventListener("click", function () {

        mobileMenu.classList.toggle("hidden");

        menuIcon.classList.toggle("fa-bars");
        menuIcon.classList.toggle("fa-xmark");
    });
}


// Mobile Categories

const mobileCategoryButton =
    document.getElementById("mobileCategoryButton");

const mobileCategories =
    document.getElementById("mobileCategories");

const categoryIcon =
    document.getElementById("categoryIcon");

if (mobileCategoryButton) {

    mobileCategoryButton.addEventListener("click", function () {

        mobileCategories.classList.toggle("hidden");

        categoryIcon.classList.toggle("fa-chevron-down");
        categoryIcon.classList.toggle("fa-chevron-up");

    });
}