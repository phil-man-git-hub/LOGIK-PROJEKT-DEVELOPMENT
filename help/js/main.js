document.addEventListener('DOMContentLoaded', () => {
    const navLinks = document.querySelectorAll('.nav-tree a');
    const iframe = document.querySelector('iframe[name="content-frame"]');
    const searchInput = document.getElementById('search-input');
    const treeToggles = document.querySelectorAll('.tree-toggle');

    // Handle Active Link Highlighting
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            navLinks.forEach(l => l.classList.remove('active'));
            link.classList.add('active');
        });
    });

    // Handle Collapsible Sections
    treeToggles.forEach(toggle => {
        toggle.addEventListener('click', () => {
            const submenu = toggle.nextElementSibling;
            if (submenu) {
                const isHidden = submenu.style.display === 'none';
                submenu.style.display = isHidden ? 'block' : 'none';
            }
        });
    });

    // Basic Search Functionality
    searchInput.addEventListener('input', (e) => {
        const term = e.target.value.toLowerCase();
        navLinks.forEach(link => {
            const text = link.textContent.toLowerCase();
            const parentLi = link.parentElement;
            if (text.includes(term)) {
                parentLi.style.display = 'block';
            } else {
                parentLi.style.display = 'none';
            }
        });

        // Hide empty groups
        treeToggles.forEach(toggle => {
            const group = toggle.parentElement;
            const hasVisibleItems = Array.from(group.querySelectorAll('ul li')).some(li => li.style.display !== 'none');
            group.style.display = hasVisibleItems ? 'block' : 'none';
        });
    });
});
