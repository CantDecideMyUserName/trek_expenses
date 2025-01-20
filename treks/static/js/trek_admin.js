django.jQuery(document).ready(function($) {
    // Get all required fields
    var startDateField = $('#id_starting_date');
    var durationField = $('#id_duration_days');
    var endDateField = $('#id_ending_date');
    var issueDateField = $('#id_issue_date');
    
    // Package fields
    var packageRateField = $('#id_package_rate');
    var packageNumbersField = $('#id_package_numbers');
    var packageDaysField = $('#id_package_days');
    
    // Guide fields
    var guideSalaryRateField = $('#id_guide_salary_rate');
    var guideSalaryDaysField = $('#id_guide_salary_days');
    
    // Assistant Guide fields
    var assistantSalaryRateField = $('#id_assistant_guide_salary_rate');
    var assistantSalaryDaysField = $('#id_assistant_guide_days');
    
    // Porter fields
    var porterSalaryRateField = $('#id_porter_salary_rate');
    var porterNumbersField = $('#id_porter_numbers');
    var porterDaysField = $('#id_porter_days');
    
    // Payment fields
    var extraExpensesField = $('#id_extra_expenses');
    var advancePaidField = $('#id_advance_paid');
    var balanceAmountField = $('#id_balance_amount');

    // Function to set today's date
    function setToday(field) {
        var today = new Date();
        var year = today.getFullYear();
        var month = String(today.getMonth() + 1).padStart(2, '0');
        var day = String(today.getDate()).padStart(2, '0');
        field.val(`${year}-${month}-${day}`);
    }

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

    // Function to auto-fill days fields based on duration
    function updateDays() {
        var duration = parseInt(durationField.val());
        if (duration > 0) {
            // Only update if fields are empty or haven't been manually changed
            if (!guideSalaryDaysField.data('manually-changed')) {
                guideSalaryDaysField.val(duration);
            }
            if (!assistantSalaryDaysField.data('manually-changed')) {
                assistantSalaryDaysField.val(duration);
            }
            if (!porterDaysField.data('manually-changed')) {
                porterDaysField.val(duration);
            }
            if (!packageDaysField.data('manually-changed')) {
                packageDaysField.val(duration);
            }
        }
    }

    // Function to calculate package total
    function calculatePackageTotal() {
        var rate = parseFloat(packageRateField.val()) || 0;
        var numbers = parseInt(packageNumbersField.val()) || 0;
        var days = parseInt(packageDaysField.val()) || 0;
        return rate * numbers * days;
    }

    // Function to calculate guide salary total
    function calculateGuideSalaryTotal() {
        var rate = parseFloat(guideSalaryRateField.val()) || 0;
        var days = parseInt(guideSalaryDaysField.val()) || 0;
        return rate * days;
    }

    // Function to calculate assistant guide salary total
    function calculateAssistantSalaryTotal() {
        var rate = parseFloat(assistantSalaryRateField.val()) || 0;
        var days = parseInt(assistantSalaryDaysField.val()) || 0;
        return rate * days;
    }

    // Function to calculate porter salary total
    function calculatePorterSalaryTotal() {
        var rate = parseFloat(porterSalaryRateField.val()) || 0;
        var numbers = parseInt(porterNumbersField.val()) || 0;
        var days = parseInt(porterDaysField.val()) || 0;
        return rate * numbers * days;
    }

    // Function to calculate total amount
    function calculateTotalAmount() {
        var packageTotal = calculatePackageTotal();
        var guideSalaryTotal = calculateGuideSalaryTotal();
        var assistantSalaryTotal = calculateAssistantSalaryTotal();
        var porterSalaryTotal = calculatePorterSalaryTotal();
        var extraExpenses = parseFloat(extraExpensesField.val()) || 0;
        
        return packageTotal + guideSalaryTotal + assistantSalaryTotal + porterSalaryTotal + extraExpenses;
    }

    // Function to update balance amount
    function updateBalanceAmount() {
        var totalAmount = calculateTotalAmount();
        var advancePaid = parseFloat(advancePaidField.val()) || 0;
        var balance = totalAmount - advancePaid;  // Changed from advancePaid - totalAmount
        balanceAmountField.val(balance);
    }
    
    // Track manual changes to days fields
    function trackManualChanges(field) {
        field.on('input', function() {
            $(this).data('manually-changed', true);
        });
    }

    // Set default dates if empty
    if (!startDateField.val()) {
        setToday(startDateField);
    }
    if (!issueDateField.val()) {
        setToday(issueDateField);
    }
    if (!durationField.val()) {
        durationField.val(1);  // Default duration
    }

    // Set up event listeners
    startDateField.on('change', updateEndDate);
    durationField.on('change', function() {
        updateEndDate();
        updateDays();
    });

    issueDateField.on('focus', function() {
        if (!$(this).val()) {
            setToday($(this));
        }
    });

    // Track manual changes to days fields
    trackManualChanges(guideSalaryDaysField);
    trackManualChanges(assistantSalaryDaysField);
    trackManualChanges(porterDaysField);
    trackManualChanges(packageDaysField);

    // Set up event listeners for amount calculations
    var calculateTotalFields = [
        packageRateField, packageNumbersField, packageDaysField,
        guideSalaryRateField, guideSalaryDaysField,
        assistantSalaryRateField, assistantSalaryDaysField,
        porterSalaryRateField, porterNumbersField, porterDaysField,
        extraExpensesField, advancePaidField
    ];

    calculateTotalFields.forEach(function(field) {
        field.on('input', updateBalanceAmount);
    });

    // Initial calculations
    updateEndDate();
    updateDays();
    updateBalanceAmount();
});