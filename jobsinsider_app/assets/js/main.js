$(document).ready(function()
{

        //form validations through javascript for frontend

        function changeFocus()
        {
            $('input:text').blur(function () {
                $(this).css('border-color', 'red');
            });

        }

        function passwordCheck(password_value)
        {
            if(password_value==''){
                $('.error_message').html('Please enter password');
                $('.error_message').show();
                $('input[type=text][name=password]').focus();
                $('input[type=text][name=password]:focus').attr('background-color','red');
                return false;

            }
            if(password_value.length<=5)
            {
                $('.error_message').html('Password should be greater than 5 characters.');
                $('.error_message').show();
                $('input[type=text][name=password]').focus();
                $('input[type=text][name=password]:focus').attr('background-color','red');
                return false;
            }

        }

        function usernameCheck(username_value)
        {
            if(username_value==''){
                $('.error_message').html('Please enter username');
                $('.error_message').show();
                $('input[type=text][name=username]').focus();
                $('input[type=text][name=username]:focus').attr('background-color','red');
                return false;
            }
        }

        function emailCheck(email_value)
        {
            if(email_value==''){
                $('.error_message').html('Please enter username');
                $('.error_message').show();
                $('input[type=text][name=username]').focus();
                $('input[type=text][name=username]:focus').attr('background-color','red');
                return false;
            }
        }

        $('#login_user').on('submit', function()
        {
            event.preventDefault();
            var username = document.getElementsByName('username')[0].value;
            var password = document.getElementsByName('password')[0].value;
            username_detect = usernameCheck(username);
            password_detect = passwordCheck(password);
            login_account();
            return false;
        });

        $('#forgot_form').on('submit', function()
        {
            event.preventDefault();
            var email = document.getElementsByName('username')[0].value;
            emaildetect = emailCheck(email);
            forgot_password();
            return false;
        });

         $('#register_form').on('submit', function()
        {
            event.preventDefault();
            var username = document.getElementsByName('username')[0].value;
            var first_name = document.getElementsByName('first_name')[0].value;
            var last_name = document.getElementsByName('last_name')[0].value;
            var password = document.getElementsByName('password')[0].value;
            var email = document.getElementsByName('email')[0].value;

            username_detect = usernameCheck(username);
            if(first_name==''){
                $('.error_message').html('Please enter username');
                $('.error_message').show();
                $('input[type=text][name=first_name]').focus();
                $('input[type=text][name=first_name]:focus').attr('background-color','red');
                return false;

            }
            if(last_name==''){
                $('.error_message').html('Please enter last name');
                $('.error_message').show();
                $('input[type=text][name=last_name]').focus();
                $('input[type=text][name=last_name]:focus').attr('background-color','red');
                return false;

            }
            password_detect = passwordCheck(password);
            if(email==''){
                $('.error_message').html('Please enter email');
                $('.error_message').show();
                $('input[type=text][name=email]').focus();
                $('input[type=text][name=email]:focus').attr('background-color','red');
                return false;

            }

            register_account();
            return false;
        });

        //currently not using this function
         $('#set_password').on('submit', function()
        {
            var password = document.getElementsByName('password')[0].value;
            password_detect = passwordCheck(password);

            forgot_set();
            return false;
        });



});
