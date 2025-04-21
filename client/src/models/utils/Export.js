// export.js

export function exportData(data, filename = 'data.json') {
    const jsonData = JSON.stringify(data, null, 2); // Преобразуем данные в формат JSON
    const blob = new Blob([jsonData], { type: 'application/json' }); // Создаём Blob объект
    const url = URL.createObjectURL(blob); // Генерируем URL для скачивания
  
    const a = document.createElement('a'); // Создаём ссылку для скачивания
    a.href = url;
    a.download = filename; // Название файла
  
    a.click(); // Имитируем клик по ссылке для скачивания
  
    // Очищаем URL после использования
    URL.revokeObjectURL(url);
  }
  