(() => {
  const app = document.getElementById('app');
  if (!app) return;
  const footer = document.querySelector('main>footer:not(.workspace-footer)');
  if (footer) {
    const details = document.createElement('details');
    details.className = 'source-details';
    const summary = document.createElement('summary');
    summary.textContent = 'Data sources & geometric solar model assumptions';
    const p = document.createElement('p');
    p.textContent = footer.textContent;
    details.append(summary, p);
    footer.replaceChildren(details);
  }
})();
