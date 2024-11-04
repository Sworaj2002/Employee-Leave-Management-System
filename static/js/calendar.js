let currentDate = new Date();
let currentMonth = currentDate.getMonth();
let currentYear = currentDate.getFullYear();
let leaveRequests = [];

const monthNames = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
];

function renderCalendar() {
    const calendarElement = document.getElementById('calendar');
    const monthYearElement = document.getElementById('month-year'); // Get month-year element
    calendarElement.innerHTML = '';
    
    monthYearElement.innerText = `${monthNames[currentMonth]} ${currentYear}`;

    const firstDayOfMonth = new Date(currentYear, currentMonth, 1);
    const lastDayOfMonth = new Date(currentYear, currentMonth + 1, 0);
    const daysInMonth = lastDayOfMonth.getDate();
    const startDay = firstDayOfMonth.getDay();

    for (let i = 0; i < startDay; i++) {
        const emptyCell = document.createElement('div');
        emptyCell.classList.add('day');
        calendarElement.appendChild(emptyCell);
    }

    for (let day = 1; day <= daysInMonth; day++) {
        const dayCell = document.createElement('div');
        dayCell.classList.add('day');
        dayCell.innerHTML = `<div class="day-header">${day}</div>`;
        highlightLeaveDays(dayCell, day); 
        calendarElement.appendChild(dayCell);
    }
}

function highlightLeaveDays(dayCell, day) {
    leaveRequests.forEach(request => {
        const startDate = new Date(request.start_date);
        const endDate = new Date(request.end_date);

        if (currentYear === startDate.getFullYear() && currentMonth === startDate.getMonth()) {
            if (day >= startDate.getDate() && day <= endDate.getDate()) {
                dayCell.classList.add('leave');
                const leaveName = document.createElement('div');
                leaveName.classList.add('leave-name');
                leaveName.innerText = request.employee_name;
                dayCell.appendChild(leaveName);
            }
        }
    });
}

function prevMonth() {
    currentMonth--;
    if (currentMonth < 0) {
        currentMonth = 11;
        currentYear--;
    }
    renderCalendar();
}

function nextMonth() {
    currentMonth++;
    if (currentMonth > 11) {
        currentMonth = 0;
        currentYear++;
    }
    renderCalendar(); 
}

function fetchLeaveData() {
    fetch('/api/leave_data')
        .then(response => response.json())
        .then(data => {
            leaveRequests = data;
            renderCalendar();
        })
        .catch(error => console.error('Error fetching leave data:', error));
}

fetchLeaveData();
