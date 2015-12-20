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
            var email = document.getElementsByName('email')[0].value;
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
});
$('.send_invitation').on('click', function(event)
{
    event.preventDefault();
    wait_it('body');
    var invitation_message = $('#interview_message').val();
    var from_date = $('.from_interview_date').val();
    var from_time = $('.from_interview_time').val();
    var to_date = $('.to_interview_date').val();
    var to_time = $('.to_interview_time').val();
    var job_id = $('.job_id_value').val();
    var candidate_id = $('.candidate_id_value').val();
    $.ajax(
        {
            url: '/company/schedule_interview/'+ candidate_id+ '/' + job_id + '/',
            type:'POST',
            data:{
                csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
                'from_date': from_date,
                'from_time': from_time,
                'to_date':to_date,
                'to_time': to_time,
                'invitation': invitation_message
            },
            success:function(m)
            {
                wait_it_hide('body');
                var resp = JSON.parse(m);
                if(resp.status==true)
                {
                    message_display('Invitation Sent Successfully', 1);
                }
                else{
                    message_display(resp.response, 0);
                }
            },
            error:function(m)
            {
                wait_it_hide('body');
            }
        }
    );
    return false;
});
$('.send_message_btn').on('click', function(e)
{
    e.preventDefault();
    $.ajax({
        url: '/company/message/',
        type:'POST',
        data: $('.sendMessageForm').serialize(),
        success:function(m)
        {
            var resp = JSON.parse(m);
            if(resp.status==true)
            {
                message_display('Message Sent Successfully', '1');
                setTimeout(function(){
                       window.location.reload(1);
                    }, 1000);

            }
        },
        error:function(m){
            message_display('Something went wrong, Notify administrators!', 0)
        }

    });
    return false;
});
$('.left_active_message').on('click', function(e)
{
    e.preventDefault();
    $('.send_composed_message').attr('value', $(this).attr('value'));
    $.ajax(
        {
            url:'/company/messages/',
            type:'POST',
            data:{
                csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
                candidate_id: $(this).attr('value')
            },
            success:function(m)
            {
                $('.message_main_data').html(m);
            },
            error:function(m)
            {
                $('.message_main_data').html('');
            }
        }
    );
    return false;
});
$('.send_composed_message').on('click', function(e)
{
    e.preventDefault();
    $.ajax({
        url: '/company/composedmessage/',
        type:'POST',
        data: {
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
            candidate_id: $(this).attr('value'),
            subject_message: '',
            content_message:$('.composer_editor').text()
        },
        success:function(m)
        {
            $('.u_message').append(m);
            var elem = document.getElementsByClassName('u_message');
            elem.scrollTop = elem.scrollHeight;
            $('.composer_editor').html('');
        },
        error:function(m){
            console.log(m)
        }

    });
    return false;
});
$('.profile_settings_overview').hover(function(e)
{
    e.preventDefault();
    return false;
});

//profile changes button
$('.profile_changes_btn').on('click', function(e)
{
    e.preventDefault();
    var data = new FormData($('#user_profile_settings').get(0));
    $.ajax(
        {
            url: '/user/u/profile_settings/',
            type: 'POST',
            data:data,
            cache:false,
            processData: false,
            contentType: false,
            success:function(m)
            {
                resp = JSON.parse(m);
                console.log(resp);
                if(resp.status==true)
                {
                    message_display('Settings Saved Successfully!', 1)
                }
            },
            error:function(m)
            {
                message_display('Something went wrong, Notify administrators!', 0)
            }
        }
    );
    return false;
});

//edit user settings page - employment details

$('.edit_employment_details').on('click', function(e)
{
    e.preventDefault();
    var employment_id = $(this).attr('value');
    $('.edit_company_description').attr('value',employment_id);
    $('.job_employment_id').attr('value',employment_id);

    $.ajax(
        {
            url: '/user/u/profile_settings/employment/',
            type: 'POST',
            data: {
                csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
                employment_id:employment_id
            },
            success:function(m)
            {
                resp = JSON.parse(m);
                $('#company_name').attr('value', resp.data.company_name);
                $('#company_worktitle').attr('value', resp.data.company_work_title);
                $('#company_from').attr('value', resp.data.company_from);
                $('#company_to').attr('value', resp.data.company_to);
                $('#company_overview').text(resp.data.company_description);

                $('.details_employment').show();
            },
            error:function(m)
            {

            }
        }
    );
    return false;
});

//posting the edited data for employment

$('.edit_company_description').on('click', function(e)
{
    e.preventDefault();
    $.ajax(
        {
            url: '/user/u/profile_settings/employment/edit/',
            type: 'POST',
            data: $('#edit_company_description_form').serialize(),
            success:function(m)
            {
                resp = JSON.parse(m);
                if(resp.status==true)
                {
                    message_display('Employment Details Successfully Updated!', 1)
                }
            },
            error:function(m)
            {

            }

        }
    );
    return false;
});

//delete employment details

$('.delete_employment_details').on('click', function(e)
{
    e.preventDefault();
    var employment_id = $(this).attr('value');
    $.ajax(
        {
            url: '/user/u/profile_settings/employment/delete/',
            type: 'POST',
            data: {
                csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
                employment_id:employment_id
            },
            success:function(m)
            {
                resp = JSON.parse(m);
                if(resp.status==true) {
                    message_display('Employment Details Deleted Successfully!', 1)
                }
            },
            error:function(m)
            {
            }
        });
});

//get user education details and show form
$('.edit_education_details').on('click', function(e)
{
    e.preventDefault();
    var education_id = $(this).attr('value');
    $('.education_id').attr('value',education_id);

    $.ajax(
        {
            url: '/user/u/profile_settings/education/',
            type: 'POST',
            data: {
                csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
                education_id:education_id
            },
            success:function(m)
            {
                resp = JSON.parse(m);
                $('#user_institute').attr('value', resp.data.user_institute);
                $('#user_degree').attr('value', resp.data.user_degree);
                $('#degree_from').attr('value', resp.data.degree_from);
                $('#degree_to').attr('value', resp.data.degree_to);
                //$('#company_overview').text(resp.data.company_description);
                //
                $('.details_education').show();
            },
            error:function(m)
            {

            }
        }
    );
    return false;
});


//edit user education details

$('.edit_education_description').on('click', function(e)
{
    e.preventDefault();
    $.ajax(
        {
            url: '/user/u/profile_settings/education/edit/',
            type: 'POST',
            data: $('#edit_education_description_form').serialize(),
            success:function(m)
            {
                resp = JSON.parse(m);
                if(resp.status==true)
                {
                    message_display('Education Details Successfully Updated!', 1)
                }
            },
            error:function(m)
            {

            }

        }
    );
    return false;
});

//delete education form

$('.delete_education_details').on('click', function(e)
{
    e.preventDefault();
    var education_id = $(this).attr('value');
    $.ajax(
        {
            url: '/user/u/profile_settings/education/delete/',
            type: 'POST',
            data: {
                csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
                education_id:education_id
            },
            success:function(m)
            {
                resp = JSON.parse(m);
                if(resp.status==true) {
                    message_display('Education Details Deleted Successfully!', 1)
                }
            },
            error:function(m)
            {
            }
        });
});


//add education form in the django

$('.display_add_education').on('click', function(e)
{
    e.preventDefault();
    $('.user_education_form').show();
    return false;
});
$('.edu_close_btn ').on('click', function(e)
{
    e.preventDefault();
    $('.user_education_form').hide();
    return false;
});
$('.display_add_employment').on('click', function(e)
{
    e.preventDefault();
    $('.add_employment_col').show();
    return false;
});
$('.emp_close_btn ').on('click', function(e)
{
    e.preventDefault();
    $('.add_employment_col').hide();
    return false;
});

//resume show box
$('.update_resume_user').on('click', function(e)
{
    e.preventDefault();
    $('.user_resume_box').show();
    return false;
});

//resume close box
$('.close_resume').on('click', function(e)
{
    e.preventDefault();
    $('.user_resume_box').hide();
    return false;
});

//resume upload

$('.upload_resume_btn').on('click', function(e)
{
    e.preventDefault();
    var data = new FormData($('#user_resume').get(0));
    $.ajax(
        {
            url: '/user/u/profile_settings/resume/',
            type: 'POST',
            data:data,
            cache:false,
            processData: false,
            contentType: false,
            success:function(m)
            {
                resp = JSON.parse(m);
                console.log(resp);
                if(resp.status==true)
                {
                    message_display('Settings Saved Successfully!', 1)

                }
            },
            error:function(m)
            {
                message_display('Something went wrong, Notify administrators!', 0)
            }
        }
    );
    return false;
});


//evaluation test display


$('#evaluation_test_label').change(function(e){
    e.preventDefault();

    if(this.checked)
    {
        this.value = 1;
        //$('.apply_datepicker').show();
        $.ajax(
            {
                url: '/company/create-job/evaluation/',
                type: 'POST',
                data: {
                    "csrfmiddlewaretoken": document.getElementsByName('csrfmiddlewaretoken')[0].value,

                },
                success:function(m)
                {
                    var resp = JSON.parse(m);
                    var html = '<select name="evaluation_template" style="margin-left:-15px;" class="evaluation_template form-control">"';
                    for(var i=0; i<resp.length; i++)
                    {

                        html+='<option value="'+ resp[i].pk + '">' + resp[i].fields.evaluation_name + '</option>';
                    }
                    html+='</select>';
                    $('.evaluation_test_selectbox').html(html);
                    $('.evaluation_test_selectbox').show();

                },
                error:function(m)
                {

                }
            }
        )
    }
    else{
        this.value = 0;
        $('.evaluation_test_selectbox').hide();
    }
    return false;
});

//for the applied filters

var applied_candidates = function()
{
    var countries =  null;
    var gender = null;
};
applied_candidates.by_countries = function(country_id)
{
    this.countries = country_id;
    var jobid = $('.job__advert__id').attr('value');
    console.log(jobid);
    $.ajax({
        url:'/company/candidates/applied/',
        type:'POST',
        data:{
            "csrfmiddlewaretoken": document.getElementsByName('csrfmiddlewaretoken')[0].value,
            'country_id': this.countries,
            'job_id': jobid
        },
        success: this.extract,
        errors:this.is_error
    })
};
applied_candidates.by_cities = function(e, city_id)
{
    var cities = [];
    if($(e.checked))
    {
        if( $.inArray(city_id, this.cities) == -1)
        {
            cities.push(city_id);
            city_id = cities[0];
            var jobid = $('.job__advert__id').attr('value');
            $.ajax(
                {
                    url: '/company/candidates/applied_city/',
                    type: 'POST',
                    data: {
                        "csrfmiddlewaretoken": document.getElementsByName('csrfmiddlewaretoken')[0].value,
                        'city_id': city_id,
                        'job_id': jobid,
                        'country_id': this.countries,

                    },
                    success: this.extract,
                    errors:this.is_error
                });
        }
    }
    else
    {
        if( $.inArray(city_id, this.cities) != -1)
        {
            cities.pop(city_id);
        }
    }

};
applied_candidates.by_gender = function(gender){
    this.gender = gender;
    var jobid = $('.job__advert__id').attr('value');
    $.ajax(
        {
            url: '/company/candidates/applied_gender/',
            type: 'POST',
            data: {
                "csrfmiddlewaretoken": document.getElementsByName('csrfmiddlewaretoken')[0].value,
                'gender': this.gender,
                'job_id': jobid,
                'country_id': this.countries,
            },
            success: this.extract,
            errors:this.is_error
        });
}

applied_candidates.extract = function(m)
{
    $('.applied_candidate_listview').html(m);
}
applied_candidates.is_error = function(m)
{
}


//job alert poriton
$('.alert_user_job').on('click', function(e)
{
    e.preventDefault();
    var category_id = $('#category_job_alert').val();
    $.ajax(
        {
            url: '/user/job_alert/',
            type: 'POST',
            data:{
                "csrfmiddlewaretoken": document.getElementsByName('csrfmiddlewaretoken')[0].value,
                'category_id': category_id
            },
            success:function(m)
            {
                resp = JSON.parse(m);
                if(resp.status==true)
                {
                    message_display('Job alert has been added successfully!', 1)
                }
                else{
                    message_display('Job alert already exists!', 0)
                }

            },
            error:function(m)
            {
                message_display('Something went wrong notify administrators!', 0)
            }


        }
    );
    return false;
});

//evaluation test for job

$('.apply_with_evaluation').on('click', function(e)
{
    e.preventDefault();
    $('#pre_test').modal('show');
    var evaluation_test_id  = $(this).data('evaluation-id');
     $('.test_description').empty();
     $('.test_rules').empty();
     $('.pre_test_catagory').empty();
     $('.pre_test_type').empty();
     $('.pre_questions').empty();
     $('.pre_test_time').empty();
     $("#start_test").val(evaluation_test_id);
        $.ajax(
            {
                url: '/evaluation/info/',
                type: 'POST',
                data:{
                    'id':evaluation_test_id,
                    "csrfmiddlewaretoken": document.getElementsByName('csrfmiddlewaretoken')[0].value

                },
                success:function(response)
                {
                    $('#pre_test').modal('show');
                    resp = JSON.parse(response);

                    $('.test_description').append(resp.list.evaluation_description);
                    $('.test_rules').append(resp.list.evaluation_rules);
                    $('.pre_test_catagory').append(resp.list.evaluation_catagory);

                    var type;
                    if(resp.list.evaluation_type==0){
                        type ="MCQ"

                    }else type="True/False";

                    $('.pre_test_type').append(type);
                    $('.pre_questions').append(resp.list.evaluation_total_questions);
                    $('.pre_test_time').append(resp.list.evaluation_time+' mins');


                },
                error: function(response) {
                }
            }
        );
    return false;
});


//adming evaluation

$('.schedule_interview_btn').on('click', function(e)
{
    var schedule_date = $('.schedule_interviews_date').val();
    e.preventDefault();
    $.ajax(
        {
            url: '/company/shortlisted_candidates_date/',
            type: 'POST',
            data:{
                'scheduled_date':schedule_date,
                "csrfmiddlewaretoken": document.getElementsByName('csrfmiddlewaretoken')[0].value
            },
            success:function(response)
            {
                console.log(response);
                resp = JSON.parse(response);
                if(resp.status==true)
                {
                    $('.schedule_interviews_date_data').html(resp.html);
                }
                else{
                    alert('Please Enter Your Date First');
                }

            },
            error: function(response) {
             //console.log(response);
            }
        }
    );
    return false;

});

$('.predefined_template ').on('click', function(e)
{
    e.preventDefault();
    //'Dear {{first_name}}' +
    //    '\n\n' +
    var email = 'You have been selected for interview at {{from_time}} - {{to_time}}.' +
        '\n\n' +
        'It would be good if you bring your Resume too.';
    $('#interview_message').html(email);
    return false;
});
$('.clear_template').on('click', function(e)
{
    e.preventDefault();
    $('#interview_message').html('');
    return false;
});

$('.applied_posted_job').on('click', function(e)
{
    e.preventDefault();
    var job_id = ($(this).attr('value'));
    $.ajax(
        {
            type: 'POST',
            url: '/company/candidates/all/',
            data:
            {
                'job_id': job_id,
                'csrfmiddlewaretoken': document.getElementsByName('csrfmiddlewaretoken')[0].value
            },
            success:function(m)
            {
                $('.applied_candidate_listview').html(m);
            },
            error:function(m)
            {

            }
        }
    );
    return false;
});

//on all applied candidates page - shortlist addition and removal function

$('.shorlist__candidate__all').on('click', function(e){
    e.preventDefault();
    var job_id = $(this).data('job_id');
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

$('.shorlist__candidate__remove__all').on('click', function(e){
    e.preventDefault();
    var job_id = $(this).data('job_id');
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
                message_display('Candidate Removed from Shortlisted Category', 1);
            }

        },
        error:function(m){
            message_display('Something Went Wrong, Please try again', 0);
        }

    });
    return false;
});
$('id_company_from').datepicker(
    {
        //autoclose: True
    }
);
    $("#id_company_from").datepicker({
        onSelect: function(selected) {
          $("#id_company_to").datepicker("option","minDate", selected)
        }
    });
    $("#id_company_to").datepicker({
        onSelect: function(selected) {
           $("#id_company_from").datepicker("option","maxDate", selected)
        }
    });
