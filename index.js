const items = document.querySelectorAll(".accordion button");
const icon = document.querySelector(".fa-plus");
const minus = document.querySelector(".icon")

function toggleAccordion() {
  const itemToggle = this.getAttribute("aria-expanded");

  for (i = 0; i < items.length; i++) {
    items[i].setAttribute("aria-expanded", "false");
  }

  if (itemToggle == "false") {
    this.setAttribute("aria-expanded", "true");
    minus.style.content = '-';
  }
}

items.forEach((item) => item.addEventListener("click", toggleAccordion));