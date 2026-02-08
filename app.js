// TaskFlow - Main Application

const tasks = [];

function addTask(title) {
    tasks.push({
        id: tasks.length + 1,
        title: title,
        completed: false
    });
    renderTasks();
}

function renderTasks() {
    const list = document.getElementById('task-list');
    list.innerHTML = '<h2>My Tasks</h2>';

    tasks.forEach(task => {
        const div = document.createElement('div');
        div.className = 'task-item';
        div.textContent = task.title;
        list.appendChild(div);
    });
}

console.log('TaskFlow loaded!');
