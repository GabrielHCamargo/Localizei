// Configuração do mapa
const map = L.map('map');

/**
 * Inicializa o mapa com a localização do usuário
 * @param {GeolocationPosition} position - Objeto de posição geográfica
 */
function initMap(position) {
    const latitude = position.coords.latitude;
    const longitude = position.coords.longitude;
    map.setView([latitude, longitude], 15);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    const marker = L.marker([latitude, longitude]).addTo(map);

    marker.bindPopup("Você está aqui!").openPopup();
}

/**
 * Trata erros de geolocalização
 * @param {GeolocationPositionError} error - Objeto de erro de geolocalização
 */
function handleLocationError(error) {
    console.error("Erro ao obter localização:", error.message);
    setDefaultMapView();
}

/**
 * Define a visualização padrão do mapa (São Paulo)
 */
function setDefaultMapView() {
    map.setView([-23.55052, -46.633308], 12);
}

/**
 * Inicializa a geolocalização
 */
function initGeolocation() {
    if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition(initMap, handleLocationError);
    } else {
        console.log("Geolocalização não suportada pelo navegador");
        setDefaultMapView();
    }
}

/**
 * Busca o endereço correspondente a um CEP utilizando a API ViaCEP
 * @param {string} cep - O CEP a ser consultado
 */
function fetchAddressByCep(cep) {
    const url = `https://viacep.com.br/ws/${cep}/json/`;

    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            if (data.erro) {
                console.error('CEP não encontrado.');
                alert('CEP não encontrado.');
                return;
            }

            const { logradouro, bairro, localidade, uf } = data;
            const address = [logradouro, bairro, localidade, uf].filter(Boolean).join(', ');

            updateAddressFields(logradouro, localidade, uf);
            fetchGeocode(address);
            sendCepDataToApi(cep, { logradouro, bairro, localidade, uf });
        })
        .catch(error => {
            console.error('Houve um problema com a requisição Fetch:', error);
        });
}

/**
 * Atualiza os campos de endereço no HTML
 * @param {string} street - Logradouro
 * @param {string} city - Cidade
 * @param {string} state - Estado
 */
function updateAddressFields(street, city, state) {
    document.getElementById('street').value = street;
    document.getElementById('city').value = city;
    document.getElementById('state').value = state;
}

/**
 * Envia dados do CEP para a API
 * @param {string} cep - CEP
 * @param {Object} cepData - Dados do CEP
 */
function sendCepDataToApi(cep, cepData) {
    fetch(`/api/cep/${cep}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(cepData)
    })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            if (data.message === true) {
                updateAddressCount();
            }
        })
        .catch((error) => console.error('Erro:', error));
}

/**
 * Atualiza o contador de endereços
 */
function updateAddressCount() {
    const addressCountElement = document.getElementById('address-count');
    const currentCount = parseInt(addressCountElement.textContent, 10);
    addressCountElement.textContent = currentCount + 1;
}

/**
 * Busca as coordenadas geográficas de um endereço utilizando o serviço Nominatim do OpenStreetMap
 * @param {string} address - O endereço a ser geocodificado
 */
function fetchGeocode(address) {
    const geocodeUrl = `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(address)}`;

    fetch(geocodeUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            if (data.length === 0) {
                console.error('Endereço completo não encontrado. Tentando buscar apenas a cidade...');
                const cityMatch = address.match(/([^,]+),\s*([^,]+)$/);
                if (cityMatch) {
                    const city = cityMatch[1].trim();
                    return fetchGeocode(city);
                } else {
                    console.error('Não foi possível extrair a cidade do endereço.');
                    alert('Endereço não encontrado.');
                    return;
                }
            }

            const { lat, lon } = data[0];
            updateMapView(lat, lon, address);
        })
        .catch(error => {
            console.error('Houve um problema com a requisição Fetch:', error);
        });
}

/**
 * Atualiza a visualização do mapa
 * @param {number} lat - Latitude
 * @param {number} lon - Longitude
 * @param {string} address - Endereço
 */
function updateMapView(lat, lon, address) {
    map.setView([lat, lon], 15);

    map.eachLayer(function (layer) {
        if (layer instanceof L.Marker) {
            map.removeLayer(layer);
        }
    });

    const marker = L.marker([lat, lon]).addTo(map);
    marker.bindPopup(`Endereço: ${address}`).openPopup();
}

/**
 * Manipula a aplicação de filtros
 */
function handleApplyFilters() {
    const postalCodeInput = document.getElementById('postal-code');
    const postalCode = postalCodeInput.value.trim();
    if (postalCode) {
        fetchAddressByCep(postalCode);
        document.getElementById('map').scrollIntoView({ behavior: 'smooth' });
        updateRecentCount();
    } else {
        alert('Por favor, insira um CEP válido.');
    }
}

/**
 * Atualiza o contador de buscas recentes
 */
function updateRecentCount() {
    const recentCountElement = document.getElementById('recent-count');
    const currentCount = parseInt(recentCountElement.textContent, 10);
    recentCountElement.textContent = currentCount + 1;
}

/**
 * Alterna o estado de favorito
 */
function toggleFavorite() {
    const cep = document.getElementById('postal-code').value;
    const favoriteButton = document.getElementById('favorite-map');
    const isFavorite = favoriteButton.getAttribute('data-favorite') === 'true';

    fetch(`/api/favorite/${cep}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
    })
        .then(response => response.json())
        .then(data => {
            if (data.message === true) {
                updateFavoriteUI(favoriteButton, isFavorite);
            } else {
                alert('Para favoritar, você precisa estar logado.');
            }
        })
        .catch(error => {
            console.error('Erro ao favoritar:', error);
            alert('Ocorreu um erro ao favoritar. Tente novamente.');
        });
}

/**
 * Atualiza a interface do usuário para favoritos
 * @param {HTMLElement} favoriteButton - Botão de favorito
 * @param {boolean} isFavorite - Estado atual de favorito
 */
function updateFavoriteUI(favoriteButton, isFavorite) {
    favoriteButton.setAttribute('data-favorite', (!isFavorite).toString());
    favoriteButton.style.color = isFavorite ? 'gray' : 'currentColor';

    const favoriteCountElement = document.getElementById('favorite-count');
    const currentCount = parseInt(favoriteCountElement.textContent, 10);
    favoriteCountElement.textContent = isFavorite ? currentCount - 1 : currentCount + 1;
}

/**
 * Inicializa a interface do usuário
 */
function initUI() {
    const menuToggle = document.getElementById('menu-toggle');
    const sidebar = document.getElementById('sidebar');
    const closeSidebar = document.getElementById('close-sidebar');
    const profileButton = document.querySelector('.profile-button');
    const applyFiltersButton = document.getElementById('apply-filters');
    const favoriteButton = document.getElementById('favorite-map');

    menuToggle.addEventListener('click', () => {
        sidebar.classList.add('active');
        closeSidebar.style.display = 'block';
    });

    closeSidebar.addEventListener('click', () => {
        sidebar.classList.remove('active');
        closeSidebar.style.display = 'none';
    });

    profileButton.addEventListener('click', () => {
        window.location.href = '/meus-enderecos';
    });

    applyFiltersButton.addEventListener('click', handleApplyFilters);

    favoriteButton.addEventListener('click', toggleFavorite);
}

// Inicialização
document.addEventListener('DOMContentLoaded', () => {
    initGeolocation();
    initUI();
});