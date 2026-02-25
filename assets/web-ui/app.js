// OpenClaw Mission Control - Web UI
// Kanban board, real-time metrics, and theme support

class MissionControl {
    constructor() {
        this.tasks = this.loadTasks();
        this.currentTheme = localStorage.getItem('mc-theme') || 'dark';
        this.init();
    }

    init() {
        this.applyTheme(this.currentTheme);
        this.setupEventListeners();
        this.renderBoard();
        this.startAutoRefresh();
        this.fetchMetrics();
    }

    // Theme Management
    applyTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('mc-theme', theme);
        this.currentTheme = theme;
        
        const themeBtn = document.getElementById('themeToggle');
        themeBtn.textContent = theme === 'dark' ? '🌙' : '☀️';
    }

    toggleTheme() {
        const newTheme = this.currentTheme === 'dark' ? 'light' : 'dark';
        this.applyTheme(newTheme);
    }

    // Task Management
    loadTasks() {
        const saved = localStorage.getItem('mc-tasks');
        if (saved) {
            return JSON.parse(saved);
        }
        // Default tasks
        return {
            todo: [
                { id: 1, text: 'Review agent configs', created: Date.now() },
                { id: 2, text: 'Update SYSTEM.md', created: Date.now() },
            ],
            progress: [
                { id: 3, text: 'Mission Control v1.1', created: Date.now() },
            ],
            done: [
                { id: 4, text: 'Install Ollama', created: Date.now() },
                { id: 5, text: 'Deploy Zero-Cost Protocol', created: Date.now() },
            ]
        };
    }

    saveTasks() {
        localStorage.setItem('mc-tasks', JSON.stringify(this.tasks));
    }

    addTask(text, column = 'todo') {
        const task = {
            id: Date.now(),
            text,
            created: Date.now()
        };
        this.tasks[column].push(task);
        this.saveTasks();
        this.renderBoard();
        this.addActivity(`Added task: ${text}`);
    }

    moveTask(taskId, fromColumn, toColumn) {
        const taskIndex = this.tasks[fromColumn].findIndex(t => t.id === taskId);
        if (taskIndex > -1) {
            const [task] = this.tasks[fromColumn].splice(taskIndex, 1);
            this.tasks[toColumn].push(task);
            this.saveTasks();
            this.renderBoard();
            this.addActivity(`Moved task to ${toColumn}`);
        }
    }

    deleteTask(taskId, column) {
        this.tasks[column] = this.tasks[column].filter(t => t.id !== taskId);
        this.saveTasks();
        this.renderBoard();
    }

    // Rendering
    renderBoard() {
        const columns = ['todo', 'progress', 'done'];
        
        columns.forEach(col => {
            const list = document.getElementById(col + 'List');
            const count = document.getElementById('count' + col.charAt(0).toUpperCase() + col.slice(1));
            
            list.innerHTML = '';
            count.textContent = this.tasks[col].length;
            
            this.tasks[col].forEach(task => {
                const card = this.createTaskCard(task, col);
                list.appendChild(card);
            });
        });
    }

    createTaskCard(task, column) {
        const card = document.createElement('div');
        card.className = 'task-card';
        card.draggable = true;
        card.dataset.taskId = task.id;
        card.dataset.column = column;
        
        card.innerHTML = `
            <div class="task-text">${this.escapeHtml(task.text)}</div>
            <div class="task-actions">
                ${column !== 'todo' ? '<button class="task-btn" onclick="mc.moveTaskLeft(${task.id}, '${column}')">←</button>' : ''}
                ${column !== 'done' ? '<button class="task-btn" onclick="mc.moveTaskRight(${task.id}, '${column}')">→</button>' : ''}
                <button class="task-btn" onclick="mc.deleteTask(${task.id}, '${column}')">🗑</button>
            </div>
        `;
        
        // Drag events
        card.addEventListener('dragstart', (e) => {
            e.dataTransfer.setData('taskId', task.id);
            e.dataTransfer.setData('fromColumn', column);
            card.classList.add('dragging');
        });
        
        card.addEventListener('dragend', () => {
            card.classList.remove('dragging');
        });
        
        return card;
    }

    // Drag and Drop
    setupDragAndDrop() {
        const columns = document.querySelectorAll('.column-content');
        
        columns.forEach(col => {
            col.addEventListener('dragover', (e) => {
                e.preventDefault();
            });
            
            col.addEventListener('drop', (e) => {
                e.preventDefault();
                const taskId = parseInt(e.dataTransfer.getData('taskId'));
                const fromColumn = e.dataTransfer.getData('fromColumn');
                const toColumn = col.id.replace('List', '');
                
                if (fromColumn !== toColumn) {
                    this.moveTask(taskId, fromColumn, toColumn);
                }
            });
        });
    }

    // Activity Log
    addActivity(text) {
        const list = document.getElementById('activityList');
        const item = document.createElement('li');
        const time = new Date().toLocaleTimeString();
        item.textContent = `[${time}] ${text}`;
        list.insertBefore(item, list.firstChild);
        
        // Keep only last 10
        while (list.children.length > 10) {
            list.removeChild(list.lastChild);
        }
    }

    // Metrics API
    async fetchMetrics() {
        try {
            const response = await fetch('/api/status');
            if (response.ok) {
                const data = await response.json();
                this.updateMetrics(data);
            }
        } catch (e) {
            console.log('Metrics fetch failed:', e);
        }
    }

    updateMetrics(data) {
        // Update cost
        if (data.cost !== undefined) {
            document.getElementById('costToday').textContent = '$' + data.cost.toFixed(2);
        }
        
        // Update model
        if (data.model) {
            document.getElementById('currentModel').textContent = data.model.split('/').pop();
        }
        
        // Update cache
        if (data.cache !== undefined) {
            document.getElementById('cacheRate').textContent = data.cache + '%';
        }
        
        // Update sessions
        if (data.sessions !== undefined) {
            document.getElementById('sessionCount').textContent = data.sessions;
        }
    }

    startAutoRefresh() {
        setInterval(() => this.fetchMetrics(), 5000);
    }

    // Model Switching
    async switchModel(model) {
        try {
            const response = await fetch('/api/switch', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ model })
            });
            
            if (response.ok) {
                this.addActivity(`Switched to ${model}`);
                this.fetchMetrics();
                
                // Update UI
                document.querySelectorAll('.model-btn').forEach(btn => {
                    btn.classList.toggle('active', btn.dataset.model === model);
                });
            }
        } catch (e) {
            console.error('Model switch failed:', e);
        }
    }

    // Event Listeners
    setupEventListeners() {
        // Theme toggle
        document.getElementById('themeToggle').addEventListener('click', () => this.toggleTheme());
        
        // Refresh
        document.getElementById('refreshBtn').addEventListener('click', () => {
            this.fetchMetrics();
            this.addActivity('Manually refreshed');
        });
        
        // Add task modal
        document.getElementById('addTaskBtn').addEventListener('click', () => {
            document.getElementById('taskModal').classList.add('active');
        });
        
        document.querySelector('.close-btn').addEventListener('click', () => {
            document.getElementById('taskModal').classList.remove('active');
        });
        
        document.getElementById('saveTaskBtn').addEventListener('click', () => {
            const input = document.getElementById('taskInput');
            const column = document.getElementById('taskColumn').value;
            
            if (input.value.trim()) {
                this.addTask(input.value.trim(), column);
                input.value = '';
                document.getElementById('taskModal').classList.remove('active');
            }
        });
        
        // Model buttons
        document.querySelectorAll('.model-btn').forEach(btn => {
            btn.addEventListener('click', () => this.switchModel(btn.dataset.model));
        });
        
        // Drag and drop
        this.setupDragAndDrop();
        
        // Close modal on backdrop click
        document.getElementById('taskModal').addEventListener('click', (e) => {
            if (e.target === e.currentTarget) {
                e.target.classList.remove('active');
            }
        });
        
        // Enter key in modal
        document.getElementById('taskInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                document.getElementById('saveTaskBtn').click();
            }
        });
    }

    // Helpers
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    moveTaskLeft(taskId, column) {
        const cols = ['todo', 'progress', 'done'];
        const idx = cols.indexOf(column);
        if (idx > 0) {
            this.moveTask(taskId, column, cols[idx - 1]);
        }
    }

    moveTaskRight(taskId, column) {
        const cols = ['todo', 'progress', 'done'];
        const idx = cols.indexOf(column);
        if (idx < cols.length - 1) {
            this.moveTask(taskId, column, cols[idx + 1]);
        }
    }
}

// Command Runner
async function runCommand(command) {
    mc.addActivity(`Running: ${command}`);
    
    try {
        const response = await fetch(`/api/${command}`);
        if (response.ok) {
            const result = await response.text();
            mc.addActivity(`${command} completed`);
        }
    } catch (e) {
        mc.addActivity(`${command} failed: ${e.message}`);
    }
}

// Initialize
const mc = new MissionControl();
