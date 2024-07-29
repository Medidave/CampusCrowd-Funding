

// I MA STARTING THE JAVASCRIPT ON THIS DAY OF 6TH JUNE 2024

// THE SCRIPTS BELOW IS RESPONSIBLE FOR MAKING THE NAV ELEMENTS WHITE BASED ON THE URL
const home = document.querySelector('.home');
const home1 = document.querySelector('.home1');
const allCampaigns = document.querySelector('.allCampaigns');
const allCampaigns1 = document.querySelector('.allCampaigns1');
const createCampaign = document.querySelector('.createCampaign');
const createCampaign1 = document.querySelector('.createCampaign1');
const payments = document.querySelector('.payments');
const dashboard = document.querySelector('.dashboard');
const dashboard1 = document.querySelector('.dashboard1');
const logout = document.querySelector('.logout');
const login = document.querySelector('.login');
const show_search = document.querySelector('.show-on-all-campaings');

const pathname = window.location.pathname;

if (pathname.startsWith('/all-campaigns')) {
    allCampaigns.classList.add('active-link');
    allCampaigns1.classList.add('the-active');
    show_search.style.display = 'block';
}
else if (pathname.startsWith('/search_projects')) {
    allCampaigns.classList.add('active-link');
    allCampaigns1.classList.add('the-active');
    show_search.style.display = 'block';
}
else if (pathname.startsWith('/create-campaigns')) {
    createCampaign.classList.add('active-link');
    createCampaign1.classList.add('the-active');

}
else if (pathname.startsWith('/dashboard')) {
    dashboard.classList.add('active-link');
    dashboard1.classList.add('the-active');

}
else if (pathname.startsWith('/accounts/login/')) {
    logout.classList.add('active-link');
}
else if (pathname.startsWith('/users/login')) {
    login.classList.add('active-link');
}
else if (pathname.startsWith('/users/logout')) {
    login.classList.add('active-link');
}
else if (pathname.startsWith('/')) {
    home.classList.add('active-link');
    home1.classList.add('the-active');}

else {
    home1.classList.add('the-active');
}



const Campaign = document.querySelector('.Campaign');
const Perks = document.querySelector('.Perks');
const Updates = document.querySelector('.Updates');
const Chat = document.querySelector('.Chat');
const Chat1 = document.querySelector('.Chat1');
const FAQs = document.querySelector('.FAQs');


const pathname1 = window.location.pathname;

if (pathname1.startsWith('/campaign')) {
    Campaign.classList.add('active-project-home');
}
else if (pathname1.startsWith('/perks')) {
    Perks.classList.add('active-project-home');
}
else if (pathname1.startsWith('/updates')) {
    Updates.classList.add('active-project-home');
}
else if (pathname1.startsWith('/CHAT_ROOM')) {
    Chat.classList.add('active-project-home');
    Chat1.classList.add('active-project-home');
}
else if (pathname1.startsWith('/hints')) {
    FAQs.classList.add('active-project-home');
}
else {
    Perks.classList.add('active-project-home');
}


// PAYSTACK GATEWAY CODE INTEGRATION STARTS HERE 
const paymentForm = document.getElementById('paymentForm');
    paymentForm.addEventListener("submit", payWithPaystack, false);
    function payWithPaystack(e) {
        e.preventDefault();
        let handler = PaystackPop.setup({
            key: '{{ PAYSTACK_PUBLIC_KEY }}', // Replace with your public key
            email: document.getElementById("email-address").value,
            amount: document.getElementById("amount").value * 100,
            metadata: {
                custom_fields: [
                    {
                        display_name: "Anonymous Donation",
                        variable_name: "is_anonymous",
                        value: document.getElementById("is_anonymous").checked
                    }
                ]
            },
            callback: function(response) {
                let message = 'Payment complete! Reference: ' + response.reference;
                window.location.href = '/verify/' + response.reference;
            },
            onClose: function() {
                alert('Transaction was not completed, window closed.');
            },
        });
        handler.openIframe();
    }



