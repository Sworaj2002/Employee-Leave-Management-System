document.getElementById('leave-request-form').addEventListener('submit', function(event) {
    event.preventDefault(); 
    const employeeId = document.getElementById('employee-id').value;
    const employeeName = document.getElementById('employee-name').value;
    const leaveType = document.getElementById('leave-type').value;
    const startDate = document.getElementById('start-date').value;
    const endDate = document.getElementById('end-date').value;
    const reason = document.getElementById('reason').value;

   
    fetch('/submit_leave_request', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            employee_id: employeeId,
            employee_name: employeeName,
            leave_type: leaveType,
            start_date: startDate,
            end_date: endDate,
            reason: reason
        })
    })
    .then(response => response.json())
    .then(data => {
        
        document.body.insertAdjacentHTML('beforeend', `<p>${data.message}</p>`);
        document.getElementById('leave-request-form').reset();
        fetchLeaveRequests();
    })
    .catch(error => console.error('Error:', error));
});

function fetchLeaveRequests() {
    fetch('/get_leave_requests')
    .then(response => response.json())
    .then(data => {
        displayLeaveRequests(data);
    })
    .catch(error => console.error('Error fetching leave requests:', error));
}

function displayLeaveRequests(requests) {
    const requestsContainer = document.getElementById('requests-container');
    requestsContainer.innerHTML = '';

    requests.forEach(request => {
        const requestElement = document.createElement('div');
        requestElement.innerHTML = `
            <p>
                ${request.employee_name} (${request.leave_type})<br>
                From: ${request.start_date} To: ${request.end_date}<br>
                Reason: ${request.reason}<br>
                <button onclick="approveLeave(${request.id})">Approve</button>
                <button onclick="rejectLeave(${request.id})">Reject</button>
                <span id="status-${request.id}"></span>
            </p>
        `;
        requestsContainer.appendChild(requestElement);
    });
}

function approveLeave(id) {
    document.getElementById(`status-${id}`).innerText = 'Approved';
}

function rejectLeave(id) {
    document.getElementById(`status-${id}`).innerText = 'Rejected';
}
function showPopup(event) {
    event.preventDefault(); 
    document.getElementById('popup').style.display = 'flex';
}

function closePopup() {
    document.getElementById('popup').style.display = 'none';
    document.getElementById('leave-request-form').submit();
}

fetchLeaveRequests();