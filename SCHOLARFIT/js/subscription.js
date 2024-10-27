// Ensure utils.js and apiService.js are correctly imported
import { saveToSessionStorage, getItemFromSessionStorage } from './utils.js';
import { subscribe, verifyPayment } from './apiService.js';

// Define the function to handle the subscription button click event
export const clickSubscribeButton = () => {
    const subscribePremiumButton = document.getElementById('subcribe-premium'); 

    if (!subscribePremiumButton) {
        console.error('Subscribe button not found.');
        return;
    }

    subscribePremiumButton.addEventListener('click', async (event) => {
        event.preventDefault();
        
        const user = getItemFromSessionStorage('user');
        
        if (!user || !user.profileId || !user.email) {
            alert('User data is missing or incomplete.');
            return;
        }

        const data = {
            profile_id: user.profileId,
            email: user.email,
            amount: 5000
        };

        try {
            const response = await subscribe(data);
            console.log('Subscription response:', response);


            if (response.error && response.status !== 201) {
                alert(`Error: ${response.error.code}`);
                return;
            }

            const { authorization_url: authUrl, reference } = response.data;

            saveToSessionStorage('reference', { "reference": reference });

            const popup = window.open(
                authUrl,
                '_blank',
                'width=800,height=600,scrollbars=yes'
            );
            verifyPayment();
            // Redirect the user to the authorization URL (Paystack)
            //window.location.replace(authUrl);
        } catch (error) {
            console.error('Subscription failed:', error);
            alert('An error occurred during subscription. Please try again.');
        }
    });
};

// Ensure the function is executed after the DOM loads
document.addEventListener('DOMContentLoaded', clickSubscribeButton);
