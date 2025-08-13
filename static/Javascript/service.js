document.addEventListener('DOMContentLoaded', function() {
    const fullDates = JSON.parse(document.getElementById('full_dates').textContent);
    const dateStartInput = document.getElementById('date_start');
    const dateEndInput = document.getElementById('date_end');
    
    dateStartInput.addEventListener('input', function() {
        const selectedDate = new Date(this.value);
        const selectedDateString = selectedDate.toISOString().split('T')[0];
        if (fullDates.includes(selectedDateString)) {
            this.value = '';
            dateEndInput.value = '';
            alert('ไม่สามารถเลือกวันนี้ได้แล้ว เนื่องจากมีผู้ใช้บริการครบ 20 คนแล้ว');
        } else {
            const nextDay = new Date(selectedDate);
            nextDay.setDate(selectedDate.getDate() + 1);
            dateEndInput.value = nextDay.toISOString().split('T')[0];
        }
    });

    dateStartInput.addEventListener('click', function() {
        const today = new Date();
        const maxDate = new Date(today);
        maxDate.setMonth(today.getMonth() + 2);
        this.setAttribute('min', today.toISOString().split('T')[0]);
        this.setAttribute('max', maxDate.toISOString().split('T')[0]);
    });
});
