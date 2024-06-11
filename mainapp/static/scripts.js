function deleteEntry(id) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    $.ajax({
        url: '/notes/',
        headers: { 'X-CSRFToken': csrftoken },
        method: 'POST',
        data: {'id': id},
        success: function(response) {
            if (response.success) {
                alert('Entry deleted successfully!');
                location.reload();
            } else {
                alert('Failed to delete entry.');
            }
        }
    });
}