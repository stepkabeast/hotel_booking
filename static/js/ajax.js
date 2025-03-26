document.addEventListener('DOMContentLoaded', () => {
    const button = document.getElementById('check-button');
    const roomsList = document.getElementById('rooms-list');

    button.addEventListener('click', async () => {
        try {
            const response = await fetch('/check_rooms/', {
                method: 'GET',
            });
            const data = await response.json();

            roomsList.innerHTML = '';
            data.forEach((room_id) => {
                const li = document.createElement('li');
                li.textContent = room_id;
                roomsList.appendChild(li);
            });
        } catch (error) {
            alert('Произошла ошибка при получении данных.');
        }
    });
});