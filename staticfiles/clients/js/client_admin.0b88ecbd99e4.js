// Save this as static/js/client_admin.js
django.jQuery(document).ready(function($) {
    // Get the date fields
    var startDateField = $('#id_starting_date');
    var durationField = $('#id_number_of_days');
    var endDateField = $('#id_ending_date');
    
    // Function to update end date based on start date and duration
    function updateEndDate() {
        var startDate = new Date(startDateField.val());
        var duration = parseInt(durationField.val());
        
        if (!isNaN(startDate.getTime()) && duration > 0) {
            var endDate = new Date(startDate);
            endDate.setDate(startDate.getDate() + duration - 1);
            
            // Format date as YYYY-MM-DD
            var year = endDate.getFullYear();
            var month = String(endDate.getMonth() + 1).padStart(2, '0');
            var day = String(endDate.getDate()).padStart(2, '0');
            
            endDateField.val(`${year}-${month}-${day}`);
        }
    }
    
    // Set up event listeners
    startDateField.on('change', updateEndDate);
    durationField.on('change', updateEndDate);
    durationField.on('input', updateEndDate);
    
    // Initial calculation
    updateEndDate();
    
    // Toggle fieldsets based on checkboxes (if needed)
    const trekkingCheckbox = $('#id_trekking');
    const peakClimbingCheckbox = $('#id_peak_climbing');
    
    // Function to toggle visibility of fieldsets
    function toggleFieldsets() {
        const showTrekkingFields = trekkingCheckbox.prop('checked') || peakClimbingCheckbox.prop('checked');
        
        // Get the fieldsets - adjust selectors based on your actual layout
        const trekkingFieldset = $('fieldset.module:nth-child(4)');
        const otherServicesFieldset = $('fieldset.module:nth-child(5)');
        
        if (trekkingFieldset.length) {
            trekkingFieldset.css('display', showTrekkingFields ? 'block' : 'none');
        }
        
        if (otherServicesFieldset.length) {
            otherServicesFieldset.css('display', showTrekkingFields ? 'none' : 'block');
        }
    }
    
    // Add event listeners for checkboxes
    trekkingCheckbox.on('change', toggleFieldsets);
    peakClimbingCheckbox.on('change', toggleFieldsets);
    
    // Initial toggle
    toggleFieldsets();
});