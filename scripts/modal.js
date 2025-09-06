function openModal(src) {
  const modal = document.getElementById("modal");
  const modalImg = document.getElementById("modal-image");
  modal.style.display = "block";
//   modalImg.src = src.replace('.webp', '.png'); // show full PNG if you want
    modalImg.src = src; // keep the webp

}

function closeModal() {
  document.getElementById("modal").style.display = "none";
}
