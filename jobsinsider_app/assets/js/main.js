// admin panel start

var count_menu = 0;
$('.display_user_settings').on('click', function(event)
{
     //$('.user_profile_settings').slideToggle();
    event.preventDefault();
    if(count_menu==0)
    {
        $('.user_profile_settings').show();
        count_menu++
    }
    else{

        $('.user_profile_settings').hide();
        count_menu=0;
    }
    return false;

});

$('.next_btn').on('click', function(event)
{
    event.preventDefault();
    if($('#id_user_portrait').val()=='')
    {
        alert('Please upload your profile picture.');
    }
    if($('#id_user_title, #id_user_overview, #id_user_portrait').val()=='')
    {
        $('#id_user_title, #id_user_portrait').focus();
        $('#id_user_title, #id_user_portrait').css('border-color', 'red');
    }
    else{
        $('.basic_user_settings').hide('fast');
        $('.basic_user_settings_next').show('fast');
    }

    return false;
});
$('#id_user_title, #id_user_overview, #id_user_zipcode, #id_user_phone_no,' +
    ' #id_company_name, #id_company_location, #id_company_worktitle, ' +
    '#id_company_role, #id_company_from,#id_company_to, ' +
    '#id_user_institute, #id_user_degree, #id_company_name, ' +
    '#id_your_role, #id_company_url, #id_company_industry,' +
    '#id_job_title, #id_job_position, #id_salary_from, #id_salary_to').keyup(function(event)
{

    $(this).css('border-color', '#ccc');
    return false;
});

$('.prev_btn').on('click', function(event)
{
    event.preventDefault();
    $('.basic_user_settings').show('fast');
    $('.basic_user_settings_next').hide('fast');
    return false;
});

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


//admin panel

$('a.add_category_skill').on('click', function(event)
{
    event.preventDefault();
    var cat_val = $(this).attr('value');
     $('.category_value').attr('value', cat_val);
    //return false;
    //$.ajax(
    //    {
    //        type:'post',
    //        url:'/private/members/categories/get/?cat_id='+cat_val,
    //        data: {"csrfmiddlewaretoken": document.getElementsByName('csrfmiddlewaretoken')[0].value},
    //        success:function(data)
    //        {
    //            $('.category_value').attr(data.id);
    //        },
    //
    //    }
    //);

});

$('.addskill').on('click', function(event)
{
    event.preventDefault();
    $.ajax(
        {
            type:'post',
            url:'/private/members/skills/add/',
            data: $('#add_new_skill').serialize(),
            success:function(data)
            {
                resp = JSON.parse(data);
                if(resp.status==true)
                {
                    $('.info').html('Skill Successfully Added');
                }
            }
        }
    );
});

$('.add_edu_type').on('click', function(event)
{
    event.preventDefault();
    $.ajax(
        {
            type:'post',
            url:'/private/members/education/',
            data: $('#add_edu_type_form').serialize(),
            success:function(data)
            {
                resp = JSON.parse(data);
                if(resp.status==true)
                {
                    $('.info').html('Education Type Successfully Added');
                }
            }
        }
    );
});



$('.enable_edu_btn').on('click', function(event)
{
    valuedata = ($(this).attr('value'));
    $.ajax({
        url: '/private/members/categories/enable/?cat_id=' + valuedata,
        type: 'POST',
        data: {
            'category_id': valuedata,
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
        },
        success:function(response)
        {
            response = JSON.parse(response);
            if (response.status==true)
            {
                $('.display_message').html('Campaign Status Enabled');
                window.location.reload();
            }
        },
        error: function(response)
        {

        }
    });

});

$('.delete_edu_btn').on('click', function(event)
{
    valuedata = ($(this).attr('value'));
    $.ajax({
        url: '/private/members/education/delete/',
        type: 'POST',
        data: {
            'education_id': valuedata,
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
        },
        success:function(response)
        {
            response = JSON.parse(response);
            if (response.status==true)
            {
                $('.display_message').html('Education Type Deleted Successfully!');
                window.location.reload();
            }
        },
        error: function(response)
        {

        }
    });
});


$('.enable_edu_type_btn').on('click', function(event)
{
    valuedata = ($(this).attr('value'));
    $.ajax({
        url: '/private/members/education/enable/',
        type: 'POST',
        data: {
            'education_id': valuedata,
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
        },
        success:function(response)
        {
            response = JSON.parse(response);
            if (response.status==true)
            {
                $('.display_message').html('Education Type Enabled Successfully!');
                window.location.reload();
            }
        },
        error: function(response)
        {

        }
    });
});


$('.disable_edu_type_btn').on('click', function(event)
{
    valuedata = ($(this).attr('value'));
    $.ajax({
        url: '/private/members/education/disable/',
        type: 'POST',
        data: {
            'education_id': valuedata,
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
        },
        success:function(response)
        {
            response = JSON.parse(response);
            if (response.status==true)
            {
                $('.display_message').html('Education Type Disabled Successfully!');
                window.location.reload();

            }
        },
        error: function(response)
        {

        }
    });
});


$('.e_edit_btn').on('click', function(event)
{
    valuedata = ($(this).attr('value'));

    $.ajax({
        url: '/private/members/education/edit/',
        type: 'POST',
        data: {
            'education_id': valuedata,
            'status': 0,
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
        },
        success:function(data)
        {
            response = JSON.parse(data);
            if(response.edu_id==true)
            {
                window.location.reload();
            }
            $('.education_id_value').attr('value', valuedata)
            $('.e_e_name').attr('value', response.edu_id)

        },
        error: function(response)
        {

        }
    });
});

$('.edit_edu_type_btn').on('click', function(event)
{
    event.preventDefault();
    $.ajax(
        {
            type:'post',
            url:'/private/members/education/edit/',
            data: $('#edit_edu_type_form').serialize(),
            success:function(data)
            {
                resp = JSON.parse(data);
                if(resp.status==true)
                {
                    $('.info').html('Education Type Successfully Added');
                }
            }
        }
    );
});


//experience button

$('.add_exp_type').on('click', function(event)
{

    var type_value = $(this).attr('id');
    if(type_value=='experience_type')
    {
        data_url = '/private/members/experience/';
    }
    else{
        data_url = '/private/members/employment/';
    }

    event.preventDefault();
    $.ajax(
        {
            type:'post',
            url:data_url,
            data: $('#add_exp_type_form').serialize(),
            success:function(data)
            {
                resp = JSON.parse(data);
                if(resp.status==true)
                {
                    $('.info').html('Experience Type Successfully Added');
                }
            }
        }
    );
});

$('.experience_manage').on('click', function(event) {
    event.preventDefault();
    valuedata = ($(this).attr('value'));
    check_value = $(this).attr('id');
    if (check_value=='enable'){
        url_link = '/private/members/experience/enable/';
    }
    else if (check_value=='disable')
    {
        url_link = '/private/members/experience/disable/';
    }
    else if (check_value=='delete')
    {
        url_link = '/private/members/experience/delete/';

    }
    $.ajax(
        {
            type:'post',
            url:url_link,
            data: {
                'experience_id': valuedata,
                 csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
            },
            success:function(data)
            {
                resp = JSON.parse(data);
                if(resp.status==true)
                {
                    $('.info').html('Experience Type Successfully Added');
                    window.location.reload();
                }
            }
        }
    );

    return false;
});


$('.edit_exp_type_btn').on('click', function(event)
{
    event.preventDefault();
    $.ajax(
        {
            type:'post',
            url:'/private/members/experience/edit/',
            data: $('#edit_exp_type_form').serialize(),
            success:function(data)
            {
                resp = JSON.parse(data);
                if(resp.exp_id==true)
                {
                    $('.info').html('Experience Type Successfully Added');
                }
            }
        }
    );
});




$('.e_exp_btn').on('click', function(event)
{
    valuedata = ($(this).attr('value'));

    $.ajax({
        url: '/private/members/experience/edit/',
        type: 'POST',
        data: {
            'experience_id': valuedata,
            'status': 0,
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
        },
        success:function(data)
        {
            response = JSON.parse(data);
            if(response.exp_id==true)
            {
                window.location.reload();
            }
            $('.education_id_value').attr('value', valuedata)
            $('.e_e_name').attr('value', response.exp_id)

        },
        error: function(response)
        {

        }
    });
});


//employment type

$('.employment_manage').on('click', function(event) {
    event.preventDefault();
    valuedata = ($(this).attr('value'));
    check_value = $(this).attr('id');
    if (check_value=='enable'){
        url_link = '/private/members/employment/enable/';
    }
    else if (check_value=='disable')
    {
        url_link = '/private/members/employment/disable/';
    }
    else if (check_value=='delete')
    {
        url_link = '/private/members/employment/delete/';

    }
    $.ajax(
        {
            type:'post',
            url:url_link,
            data: {
                'employment_id': valuedata,
                 csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
            },
            success:function(data)
            {
                resp = JSON.parse(data);
                if(resp.status==true)
                {
                    $('.info').html('Experience Type Successfully Added');
                    window.location.reload();
                }
            }
        }
    );

    return false;
});

$('.countries_select_box').change(function(event)
{
    event.preventDefault();
    var value_data = $(this).val();
    $.ajax(
        {
            url:'/user/cities/',
            type:'POST',
            data:{
                'country_id': value_data,
                 csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
            },
            success:function(m)
            {
                resp = jQuery.parseJSON(m);
                list_obj = jQuery.parseJSON(resp.cities);
                var options_c='';
                $(list_obj).each(function(i)
                {
                    options_c += '<option value="'+ this.pk + '">'+ this.fields.city_name + "</option>";
                });
                $('.cities_select_box').html(options_c);
            }
        }
    );
    //alert(value_data);
});

//shortlisting candidates

$('.shorlist__candidate').on('click', function(e){
    e.preventDefault();
    var job_id = $('.job__advert__id').attr('value');
    $.ajax({
        url:'/company/shortlist/' + $(this).attr('value') + "/" +  job_id + "/",
        type: 'POST',
        data: {
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
        },
        success:function(m){
            var resp = JSON.parse(m);
            console.log(resp);
            if(resp.status==true){
                console.log('hoa');
                message_display('Candidate Added to Shortlisted Category', 1);
            }

        },
        error:function(m){
            message_display('Something Went Wrong, Please try again', 0);
        }

    });
    return false;
})

$('.shorlist__candidate__remove').on('click', function(e){
    e.preventDefault();
    var job_id = $('.job__advert__id').attr('value');
    $.ajax({
        url:'/company/shortlist_remove/' + $(this).attr('value') + "/" +  job_id + "/",
        type: 'POST',
        data: {
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
        },
        success:function(m){
            var resp = JSON.parse(m);
            console.log(resp);
            if(resp.status==true){
                console.log('hoa');
                message_display('Candidate Removed from Shortlisted Category', 1);
            }

        },
        error:function(m){
            message_display('Something Went Wrong, Please try again', 0);
        }

    });
    return false;
})