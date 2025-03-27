document.addEventListener('DOMContentLoaded', () => {
    const button = document.getElementById('check-button');
    const roomsList = document.getElementById('rooms-list');

    button.addEventListener('click', async () => {
        try {
            const selectedCategory = document.getElementById('room-category-select').value;
            console.log("Selected Category:", selectedCategory);
            const url = '/check_rooms/?category=' + encodeURIComponent(selectedCategory);
            const response = await fetch(url, {
                method: 'GET',
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();

            roomsList.innerHTML = ''; // Очищаем содержимое списка

            // Выводим каждое значение room_number
            data.forEach((room) => {
                const li = document.createElement('li');
                li.textContent = room.room_number; // Доступ к полю room_number
                roomsList.appendChild(li);
            });
        } catch (error) {
            console.error('Error:', error);
            alert('Произошла ошибка при получении данных.');
        }
    });
});