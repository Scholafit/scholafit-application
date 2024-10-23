// Wait for the DOM to load before executing the script
document.addEventListener("DOMContentLoaded", () => {
    const user = JSON.parse(sessionStorage.getItem('user')); 
    const firstname = user ? user.firstname : "Guest"; // Fallback if firstname is not found
    document.querySelector('.heading span').textContent = firstname;
    // Select the welcome message element and update its text
    const welcomeMessage = document.querySelector('.dashboard-welcome');
    welcomeMessage.textContent = `Good to see you, ${firstname}! Keep pushing towards your goals!`;
  });
  