const predictionForm = document.getElementById('predictionForm');

predictionForm.addEventListener('submit', function(event) {
  // Check if area, bhk, and age are valid numbers
  const area = document.getElementById('area').value;
  const bhk = document.getElementById('bhk').value;
  const age = document.getElementById('age').value;

  if (isNaN(area) || isNaN(bhk) || isNaN(age)) {
    event.preventDefault(); // Prevent form submission
    alert("Please enter valid numerical values for area, BHK, and age.");
  }
});
