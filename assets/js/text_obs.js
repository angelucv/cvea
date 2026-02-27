const scrollText = document.querySelector('.scroll-text');
if (scrollText) {
  const observer = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting && !entry.target.classList.contains('show')) {
        entry.target.classList.add('show');
        observer.disconnect();
      }
    });
  });
  observer.observe(scrollText);
}
