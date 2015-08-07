$(document).ready(function()
{
        $('#forgot_form').on('submit', function()
        {
            event.preventDefault();
            forgot_password();
            return false;
        });
});

function forgot_password()
{
    $.ajax(
        {

        }
    );
}