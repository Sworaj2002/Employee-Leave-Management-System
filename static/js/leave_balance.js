async function fetchLeaveBalance() {
    const response = await fetch('/api/leave_balance');
    const leaveBalances = await response.json();
    const leaveBalanceBody = document.getElementById('leave-balance-body');

    leaveBalances.forEach(balance => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${balance.employee_id}</td>
            <td>${balance.employee_name}</td>
            <td>${balance.total_leave}</td>
            <td>${balance.current_leave}</td>
            <td>${balance.remaining_leave}</td>
        `;
        leaveBalanceBody.appendChild(row);
    });
}

fetchLeaveBalance();
