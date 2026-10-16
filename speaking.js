/* Add local image paths here when speaking photographs are available. */
const speakingPhotos = [
  // { src: "assets/speaking/event-name.jpg", alt: "Describe the speaking event", caption: "Optional caption" },
];

const speakingGallery = document.getElementById("speaking-gallery");
const galleryGrid = document.getElementById("gallery-grid");

if (speakingGallery && galleryGrid) {
  speakingPhotos.filter((photo) => photo.src).forEach((photo) => {
    const figure = document.createElement("figure");
    figure.innerHTML = `<img src="${photo.src}" alt="${photo.alt || "Speaking event"}">${photo.caption ? `<figcaption>${photo.caption}</figcaption>` : ""}`;
    galleryGrid.append(figure);
  });
  if (galleryGrid.children.length) speakingGallery.hidden = false;
}
