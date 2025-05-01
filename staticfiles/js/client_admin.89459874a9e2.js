// Save this as static/js/client_admin.js
django.jQuery(document).ready(function($) {
    // Try multiple approaches to find the fields
    
    // Approach 1: Direct ID targeting
    function updateEndDateWithIds() {
        console.log("Attempting calculation with direct IDs");
        var startingDate = $('#id_starting_date').val();
        var totalDays = $('#id_number_of_days').val() || $('#id_total_days').val();
        
        if (startingDate && totalDays) {
            try {
                // Parse date (in YYYY-MM-DD format)
                var [year, month, day] = startingDate.split('-');
                var startDate = new Date(year, month - 1, day);
                
                // Calculate end date
                var endDate = new Date(startDate);
                endDate.setDate(startDate.getDate() + parseInt(totalDays) - 1);
                
                // Format as YYYY-MM-DD
                var endYear = endDate.getFullYear();
                var endMonth = String(endDate.getMonth() + 1).padStart(2, '0');
                var endDay = String(endDate.getDate()).padStart(2, '0');
                var formattedEndDate = `${endYear}-${endMonth}-${endDay}`;
                
                $('#id_ending_date').val(formattedEndDate);
                return true;
            } catch (error) {
                console.error("Error with direct ID targeting:", error);
            }
        }
        return false;
    }
    
    // Approach 2: Field label targeting
    function updateEndDateWithLabels() {
        console.log("Attempting calculation with label-based targeting");
        
        // Find fields based on their labels
        var startDateField = $('label:contains("Starting date")').next('input');
        var durationField = $('label:contains("Total days")').next('input');
        var endDateField = $('label:contains("Ending date")').next('input');
        
        if (startDateField.length && durationField.length && endDateField.length) {
            try {
                var startDate = new Date(startDateField.val());
                var duration = parseInt(durationField.val());
                
                if (!isNaN(startDate.getTime()) && duration > 0) {
                    var endDate = new Date(startDate);
                    endDate.setDate(startDate.getDate() + duration - 1);
                    
                    var endYear = endDate.getFullYear();
                    var endMonth = String(endDate.getMonth() + 1).padStart(2, '0');
                    var endDay = String(endDate.getDate()).padStart(2, '0');
                    var formattedEndDate = `${endYear}-${endMonth}-${endDay}`;
                    
                    endDateField.val(formattedEndDate);
                    return true;
                }
            } catch (error) {
                console.error("Error with label-based targeting:", error);
            }
        }
        return false;
    }
    
    // Approach 3: Field order targeting
    function updateEndDateWithFieldOrder() {
        console.log("Attempting calculation with field order targeting");
        
        // Assuming the fields are date-days-date in sequence
        var dateInputs = $('input[type="text"][id*="date"]');
        
        if (dateInputs.length >= 2) {
            var startDateField = dateInputs.eq(0);
            var endDateField = dateInputs.eq(1);
            var daysField = $('input[type="number"]').first();
            
            if (startDateField.length && daysField.length && endDateField.length) {
                try {
                    var startDate = new Date(startDateField.val());
                    var duration = parseInt(daysField.val());
                    
                    if (!isNaN(startDate.getTime()) && duration > 0) {
                        var endDate = new Date(startDate);
                        endDate.setDate(startDate.getDate() + duration - 1);
                        
                        var endYear = endDate.getFullYear();
                        var endMonth = String(endDate.getMonth() + 1).padStart(2, '0');
                        var endDay = String(endDate.getDate()).padStart(2, '0');
                        var formattedEndDate = `${endYear}-${endMonth}-${endDay}`;
                        
                        endDateField.val(formattedEndDate);
                        return true;
                    }
                } catch (error) {
                    console.error("Error with field order targeting:", error);
                }
            }
        }
        return false;
    }
    
    // Function to try all approaches
    function updateEndDate() {
        if (updateEndDateWithIds()) return;
        if (updateEndDateWithLabels()) return;
        if (updateEndDateWithFieldOrder()) return;
        
        console.log("All calculation approaches failed");
    }
    
    // Find all form fields
    $('input').each(function() {
        var fieldId = $(this).attr('id');
        if (fieldId) {
            if (fieldId.includes('date')) {
                $(this).on('change', updateEndDate);
            } else if (fieldId.includes('day') || fieldId.includes('duration') || fieldId.includes('number')) {
                $(this).on('change', updateEndDate);
                $(this).on('input', updateEndDate);
            }
        }
    });
    
    // Run calculation on page load
    updateEndDate();
    
    // Add a small delay to ensure all fields are properly loaded
    setTimeout(updateEndDate, 500);
    
    // // Add a debug button that will always be visible
    // $('body').append('<button id="force_calculate" style="position: fixed; bottom: 10px; right: 10px; z-index: 9999; background-color: red; color: white; padding: 10px;">Calculate End Date</button>');
    
    $('#force_calculate').on('click', function(e) {
        e.preventDefault();
        console.log("Manual calculation triggered");
        updateEndDate();
    });
});