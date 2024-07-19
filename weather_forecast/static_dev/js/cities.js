const url = 'http://127.0.0.1:8000/api/v1/cities/';
let cities = [];
fetch(url)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        cities = data
    })
    .catch(error => {
        console.error('There has been a problem with your fetch operation:', error);
    });
const cityInput = document.getElementById('searchBox');
const suggestionsContainer = document.getElementById('autocomplete-list');


cityInput.addEventListener('input', function () {
    const inputValue = this.value.toLowerCase();

    const filteredCities = cities
        .filter((city) => city.name.toLowerCase().startsWith(inputValue))
        .slice(0, 10);

    suggestionsContainer.innerHTML = '';

    if (filteredCities.length > 0) {
        filteredCities.forEach((city) => {
            const suggestion = document.createElement('li');
            suggestion.textContent = city.name;
            suggestion.addEventListener('click', () => {
                // cityInput.value = '';
                suggestionsContainer.innerHTML = '';
                const currentUrl = window.location.href;
                const newUrl = currentUrl.split('/').slice(0, 3).join('/') + '/geo/' + city.id;
                window.location.href = newUrl;
            });
            suggestionsContainer.appendChild(suggestion);
        });
        suggestionsContainer.style.display = 'block';
    } else {
        suggestionsContainer.style.display = 'none';
    }

    document.addEventListener('click', function (event) {
        if (!event.target.closest('#cityInput, .suggestions')) {
            suggestionsContainer.style.display = 'none';
        }
    });
});