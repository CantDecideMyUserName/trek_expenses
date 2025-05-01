// Save this as clients/static/clients/js/client_admin.js
(function($) {
    $(document).ready(function() {
        // PART 1: Toggle fieldsets based on checkboxes
        const trekkingCheckbox = $('#id_trekking');
        const peakClimbingCheckbox = $('#id_peak_climbing');
        
        // Get the fieldsets - adjust selectors based on your actual admin layout
        const trekkingFieldset = $('fieldset.module:nth-child(4)');
        const otherServicesFieldset = $('fieldset.module:nth-child(5)');
        
        // Function to toggle visibility of fieldsets
        function toggleFieldsets() {
            const showTrekkingFields = trekkingCheckbox.prop('checked') || peakClimbingCheckbox.prop('checked');
            
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
        
        // PART 2: Auto-calculate ending date
        // Get the date input fields
        const startDateInput = $('#id_starting_date');
        const totalDaysInput = $('#id_number_of_days');
        const endDateInput = $('#id_ending_date');
        
        // Make the end date field read-only but still visible
        endDateInput.attr('readonly', true);
        
        // Function to calculate the end date
        function calculateEndDate() {
            // Check if both fields have values
            if (startDateInput.val() && totalDaysInput.val()) {
                try {
                    // Parse the start date
                    const startDateStr = startDateInput.val();
                    console.log("Start date string:", startDateStr);
                    
                    // Handle different date formats (YYYY-MM-DD or MM/DD/YYYY)
                    let startDate;
                    if (startDateStr.includes('-')) {
                        // YYYY-MM-DD format
                        const [year, month, day] = startDateStr.split('-');
                        startDate = new Date(parseInt(year), parseInt(month) - 1, parseInt(day));
                    } else if (startDateStr.includes('/')) {
                        // MM/DD/YYYY format
                        const [month, day, year] = startDateStr.split('/');
                        startDate = new Date(parseInt(year), parseInt(month) - 1, parseInt(day));
                    } else {
                        // Try direct parsing
                        startDate = new Date(startDateStr);
                    }
                    
                    console.log("Parsed start date:", startDate);
                    
                    // Parse the number of days
                    const totalDays = parseInt(totalDaysInput.val());
                    console.log("Total days:", totalDays);
                    
                    // Calculate the end date (add totalDays - 1 days to start date)
                    const endDate = new Date(startDate);
                    endDate.setDate(startDate.getDate() + totalDays - 1);
                    console.log("Calculated end date:", endDate);
                    
                    // Format the date as YYYY-MM-DD
                    const year = endDate.getFullYear();
                    const month = String(endDate.getMonth() + 1).padStart(2, '0');
                    const day = String(endDate.getDate()).padStart(2, '0');
                    const formattedDate = `${year}-${month}-${day}`;
                    
                    console.log("Formatted end date:", formattedDate);
                    
                    // Set the end date value
                    endDateInput.val(formattedDate);
                } catch (error) {
                    console.error("Error calculating end date:", error);
                }
            }
        }
        
        // Add event listeners for date calculation
        startDateInput.on('change', calculateEndDate);
        totalDaysInput.on('change', calculateEndDate);
        totalDaysInput.on('input', calculateEndDate);
        
        // Calculate on page load
        calculateEndDate();
    });
})(django.jQuery);