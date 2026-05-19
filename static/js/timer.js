let timer;
let seconds = 0;
let isRunning = false;

const display = document.getElementById('timer-display');
const startBtn = document.getElementById('startBtn');
const stopBtn = document.getElementById('stopBtn');
const resetBtn = document.getElementById('resetBtn');
const logForm = document.getElementById('log-form');
const mooSound = document.getElementById('mooSound');

function formatTime(s) {
    const hrs = Math.floor(s / 3600);
    const mins = Math.floor((s % 3600) / 60);
    const secs = s % 60;
    return `${hrs.toString().padStart(2, '0')}:${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
}

function updateDisplay() {
    display.textContent = formatTime(seconds);
}

startBtn.addEventListener('click', () => {
    if (!isRunning) {
        isRunning = true;
        startBtn.classList.add('hidden');
        stopBtn.classList.remove('hidden');
        
        timer = setInterval(() => {
            seconds++;
            updateDisplay();
        }, 1000);
    }
});

stopBtn.addEventListener('click', () => {
    clearInterval(timer);
    isRunning = false;
    startBtn.classList.remove('hidden');
    stopBtn.classList.add('hidden');
    mooSound.play();
    document.getElementById('id_duration_minutes').value = Math.max(1, Math.round(seconds / 60));
    logForm.classList.remove('hidden');
});

resetBtn.addEventListener('click', () => {
    clearInterval(timer);
    seconds = 0;
    isRunning = false;
    updateDisplay();
    startBtn.classList.remove('hidden');
    stopBtn.classList.add('hidden');
    logForm.classList.add('hidden');
});

document.getElementById('cancelBtn').addEventListener('click', () => {
    logForm.classList.add('hidden');
});