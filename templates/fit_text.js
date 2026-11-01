// One font size per text style: the largest at which every card's text fits its box, so all cards match.
document.fonts.ready.then(() => {
  const groups = {title: 26, power: 24, desc: 22, quote: 20};
  for (const [cls, max] of Object.entries(groups)) {
    const els = [...document.querySelectorAll('.' + cls)];
    let s = max;
    const fits = () => els.every(e => e.scrollWidth <= e.clientWidth + 0.5 && e.scrollHeight <= e.clientHeight + 0.5);
    for (;; s -= 0.5) { els.forEach(e => e.style.fontSize = s + 'px'); if (fits() || s <= 10) break; }
  }
});
