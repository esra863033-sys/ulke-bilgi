document.getElementById('countryInput').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        getCountry();
    }
});

function getCountry() {
    const countryName = document.getElementById('countryInput').value;
    const resultDiv = document.getElementById('result');
    const errorDiv = document.getElementById('error');

    if (!countryName) return;

    // Backend'e istek atıyoruz (app.py içindeki /search route'u)
    fetch(`/search?country=${countryName}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Ülke bulunamadı');
            }
            return response.json();
        })
        .then(data => {
            // Hata mesajını gizle
            errorDiv.style.display = 'none';
            resultDiv.style.display = 'block';

            // Verileri yerleştir
            document.getElementById('flag').src = data.flag;
            document.getElementById('countryName').textContent = data.name;
            document.getElementById('capital').textContent = data.capital;
            document.getElementById('population').textContent = data.population;
            document.getElementById('continent').textContent = data.continent;
            document.getElementById('region').textContent = data.region;
            document.getElementById('currency').textContent = data.currency;
            document.getElementById('language').textContent = data.languages;
            document.getElementById('mapLink').href = data.maps;
        })
        .catch(err => {
            resultDiv.style.display = 'none';
            errorDiv.style.display = 'block';
            errorDiv.textContent = "HATA: Girdiğiniz ülke bulunamadı veya bir sorun oluştu.";
        });
}
