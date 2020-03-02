$('.js-watch-user').on('click', function (event) {
    $this = $(this);
    event.preventDefault();
    $.ajax({
        url: $(this).data('action-url'),
        method: 'POST',
        headers: {'X-CSRFToken': $this.data('csrf')},
        dataType: 'json',
        data: {
            'target': $this.data('target-user-id'),
        },
        success: function (response) {
            if (response['status']) {
                $this.html('<p>Obserwujesz</p>');
            } else {
                alert(response['message'])
            }
        }
    })
});
