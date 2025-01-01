async function makeDeposit() {
    window.location.href = '/deposit.html';
}
async function withdraw() {
    window.location.href = '/withdraw.html'; // Change URL to your withdraw page
}
async function transfer() {
    window.location.href = '/transfer.html'; // Change URL to your transfer page
}
// async function transactionHistory() {
//     window.location.href = '/transaction-history'; // Change URL to your transaction history page
// }
async function payBill() {
    window.location.href = '/payBill.html'; // Change URL to your pay bill page
}
async function buyAirtime() {
    window.location.href = '/buyAirtime.html'; // Change URL to your buy airtime page
}
async function transactionHistory() {
    window.location.href = '/transactionHistory.html'; // Change URL to your buy airtime page
}
async function balance() {
    window.location.href = '/balance.html'; // Change URL to your balance page
}
async function dashboard() {
    window.location.href = '/dasboard.html'
    
}

window.onload = function() {
    const token = localStorage.getItem('access_token');
    
    // If token doesn't exist, redirect to login page
    if (!token) {
        window.location.href = '/login';
    }
};