
frm.addEventListener('submit', (event) => {
  const lat = document.getElementById('lat').value;
  const lon = document.getElementById('lon').value;
  if (!lat || !lon) 
  {
    alert('Please enter both latitude and longitude');
    return; 
  }

  
  alert('Form submitted with Latitude: ' + lat + ' and Longitude: ' + lon);
});


