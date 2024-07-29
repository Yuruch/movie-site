document.querySelectorAll(".star-rating .star").forEach(star => {
  star.addEventListener("click", () => {
    const ratingValue = star.getAttribute("data-value");
    document.getElementById("rating-value").value = ratingValue;

    document.querySelectorAll(".star-rating .star").forEach(s => {
      s.classList.remove("selected");
    });

    document.querySelectorAll(".star-rating .star").forEach(s => {
      if (parseInt(s.getAttribute("data-value")) <= parseInt(ratingValue)) {
        s.classList.add("selected");
      }
    });
  });
});