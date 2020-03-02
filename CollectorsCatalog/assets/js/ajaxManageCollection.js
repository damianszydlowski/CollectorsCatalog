$('.js-manage-collection-link').on('click', function (event) {
    $this = $(this);
    $management = $this.closest('.collectible-managable-item');
    event.preventDefault();
    $.ajax({
        url: $(this).data('action-url'),
        method: 'POST',
        headers: {'X-CSRFToken': $management.data('csrf')},
        dataType: 'json',
        data: {
            'user': $management.data('user-id'),
            'collectible': $management.data('collectible-id')
        },
        success: function (response) {
            if (response['status']) {
                if (response['remove']) {
                    $management.remove();
                } else {
                    $this.attr('data-uk-icon', 'icon:check; ratio: 0.8');
                }
            }
        }
    })
});
