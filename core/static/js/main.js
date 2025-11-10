async function openNgoModal(ngoId) {
  const resp = await fetch(`/ngo/${ngoId}/profile/`, {
    headers: {'X-Requested-With': 'XMLHttpRequest'}
  });
  if (!resp.ok) return alert('Error fetching NGO profile');
  const data = await resp.json();
  document.getElementById('ngoName').textContent = data.name;
  document.getElementById('ngoEmail').textContent = data.email;
  document.getElementById('ngoContact').textContent = data.contact || 'N/A';
  const myModal = new bootstrap.Modal(document.getElementById('ngoModal'));
  myModal.show();
}