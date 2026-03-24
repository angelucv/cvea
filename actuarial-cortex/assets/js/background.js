const nextSectionButton = document.querySelector('.btn-21');
const sections = document.querySelectorAll('.intro');
if (nextSectionButton && sections.length) {
  let currentSectionIndex = 0;
  nextSectionButton.addEventListener('click', () => {
    sections[currentSectionIndex].scrollIntoView({ behavior: 'smooth' });
    currentSectionIndex = (currentSectionIndex + 1) % sections.length;
  });
}
