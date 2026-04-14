const tabs = document.querySelectorAll('.tab-button');
const adminForm = document.getElementById('adminForm');
const studentForm = document.getElementById('studentForm');

function activateTab(target) {
    tabs.forEach(button => {
        const isActive = button.dataset.target === target;
        button.classList.toggle('active', isActive);
        button.setAttribute('aria-selected', isActive ? 'true' : 'false');
    });

    adminForm.classList.toggle('active', target === 'admin');
    studentForm.classList.toggle('active', target === 'student');
}

if (tabs.length) {
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            activateTab(tab.dataset.target);
        });
    });
}

window.addEventListener('DOMContentLoaded', () => {
    const activeTab = document.querySelector('.tab-button[aria-selected="true"]');
    activateTab(activeTab ? activeTab.dataset.target : 'student');
});
