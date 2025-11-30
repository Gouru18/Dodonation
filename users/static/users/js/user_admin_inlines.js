document.addEventListener('DOMContentLoaded', function() {
    var roleSelect = document.getElementById('id_role');
    if (!roleSelect) return;

    var ngoInline = document.getElementById('ngo_profile-group');
    var donorInline = document.getElementById('donor_profile-group');

    function toggleInlines() {
        var v = roleSelect.value;
        if (ngoInline) ngoInline.style.display = (v === 'ngo') ? '' : 'none';
        if (donorInline) donorInline.style.display = (v === 'donor') ? '' : 'none';
    }

    roleSelect.addEventListener('change', toggleInlines);
    // initial state
    toggleInlines();
});
