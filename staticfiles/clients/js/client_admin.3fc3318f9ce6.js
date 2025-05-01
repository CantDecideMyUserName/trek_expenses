// Save this as clients/static/clients/js/client_admin.js
(function($) {
    $(document).ready(function() {
        console.log("Client admin JS loaded");
        
        // Get the relevant fields for the client model
        const startDateInput = $('#id_starting_date');
        const totalDaysInput = $('#id_number_of_days');
        const endDateInput = $('#id_ending_date');
        
        console.log("Date fields found:", {
            startDate: startDateInput.length > 0,
            totalDays: totalDaysInput.length > 0,
            endDate: endDateInput.length > 0
        });
        
        // Function to calculate the end date
        function calculateEndDate() {
            const startDateValue = startDateInput.val();
            const totalDaysValue = totalDaysInput.val();
            
            console.log("Calculating end date with:", {
                startDate: startDateValue,
                totalDays: totalDaysValue
            });
            
            if (startDateValue && totalDaysValue) {
                try {
                    // Parse the date (assuming YYYY-MM-DD format)
                    const [year, month, day] = startDateValue.split('-');
                    const startDate = new Date(year, month - 1, day);
                    
                    // Calculate end date (add totalDays - 1 days to start date)
                    const endDate = new Date(startDate);
                    endDate.setDate(startDate.getDate() + parseInt(totalDaysValue) - 1);
                    
                    // Format back to YYYY-MM-DD
                    const endYear = endDate.getFullYear();
                    const endMonth = String(endDate.getMonth() + 1).padStart(2, '0');
                    const endDay = String(endDate.getDate()).padStart(2, '0');
                    const formattedEndDate = `${endYear}-${endMonth}-${endDay}`;
                    
                    console.log("Setting end date to:", formattedEndDate);
                    endDateInput.val(formattedEndDate);
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
        
        // Your existing toggle code for trekking/peak climbing fields
        const trekkingCheckbox = $('#id_trekking');
        const peakClimbingCheckbox = $('#id_peak_climbing');
        
        // Get the fieldsets - adjust selectors based on your actual admin layout
        const trekkingFieldset = $('fieldset.module:nth-child(4)');
        const otherServicesFieldset = $('fieldset.module:nth-child(5)');
        
        // Function to toggle visibility of fieldsets
        function toggleFieldsets() {
            console.log("Toggle fieldsets called");
            const showTrekkingFields = trekkingCheckbox.prop('checked') || peakClimbingCheckbox.prop('checked');
            
            if (trekkingFieldset.length) {
                console.log("Found trekking fieldset");
                trekkingFieldset.css('display', showTrekkingFields ? 'block' : 'none');
            }
            
            if (otherServicesFieldset.length) {
                console.log("Found other services fieldset");
                otherServicesFieldset.css('display', showTrekkingFields ? 'none' : 'block');
            }
        }
        
        // Add event listeners for checkboxes
        trekkingCheckbox.on('change', toggleFieldsets);
        peakClimbingCheckbox.on('change', toggleFieldsets);
        
        // Initial toggle
        toggleFieldsets();
    });
})(django.jQuery);