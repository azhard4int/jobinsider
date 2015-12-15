 var over123;
 $(document).on('click', '.button123' ,function(event) {
        //e.preventDefault();
        event.preventDefault();
        $('.message_display').text(' ');
           // Find the row

        valuedata = $(this).val();
        over123 = $(this).val();


        $.ajax({
            url: "/private/members/users/edit_profile/?user_id=" + valuedata,
            //cache: 'false',
            type: "POST",
            dataType: "json",
            data: {
                "user_id": valuedata,
                "csrfmiddlewaretoken": document.getElementsByName('csrfmiddlewaretoken')[0].value},
                // success: function (user_info) {
                //     user_info = JSON.parse(user_info);
                //
                //     alert(user_info.username);
                //
                //},
             success: function (data) {
                     //data = JSON.parse(data);
                 for(keya in data)

                 {
                     $(".modalheading").text(data[keya].firstname+" "+ data[keya].lastname);
                     $('#n1').attr('value',data[keya].firstname);
                     $('#l1').attr('value',data[keya].lastname);
                     $('#u1').attr('value',data[keya].username);
                     $('#e1').attr('value',data[keya].email);

                     if(data[keya].status == true){
                         $('#combostatus').val('1');

                     } else $('#combostatus').val('0');

                     if(data[keya].staff == true){
                         $('#combo11').val('1');

                     } else $('#combo11').val('0');



                     if(data[keya].superuser == true){
                         $('#combo10').val('1');

                     } else $('#combo10').val('0');

                     profile_status = profilestatus(over123);

                     if(profile_status==0){
                         $('#status_user').val('0');
                     }else  $('#status_user').val('1');

                 }


                },



        });

    });



      $('#update_form').on('submit', function(event)
       {

           event.preventDefault();
           id = over123;
           name = $('#n1').val();
           lastname =$('#l1').val();
           username1 =$('#u1').val();
           email = $('#e1').val();
           status =  parseInt($('#combostatus').val());
           staff =  parseInt($('#combo11').val());
           superuser = parseInt($('#combo10').val());
           profile = parseInt($('#status_user').val());
        $.ajax({
        url: '/private/members/users/edit_profile/update_user/',
        type: 'POST',
        data: {
            'id':id,
            'first_name':name,
            'last_name':lastname,
            'username':username1,
            'email': email,
            'is_active': status,
            'is_staff': staff,
            'is_superuser': superuser,
            'profile_status':profile,
            "csrfmiddlewaretoken": document.getElementsByName('csrfmiddlewaretoken')[0].value

        },






          success:function(response) {
              response = JSON.parse(response);


              if (response.status == 'True') {
                  $('.message_display').text('saved');



              }

        },
        error: function(response)
        {

        }
        });
    return false;
});

 $('#add_form').on('submit', function(event)
       {
          $('.message_display_add').text(' ');
           $('.message_display_add').show();
           $('.modal-title').text("Add User");


           event.preventDefault();

           name = $('#n11').val();
           lastname =$('#l11').val();
           username123 =$('#u11').val();
           email = $('#e11').val();
           profile = $('#user_status_profile').val();

           status =  parseInt($('combo09').val());
           staff =  parseInt($('#combo101').val());
           superuser = parseInt($('#combo111').val());
           profile_status = parseInt($('user_status_profile'));

        $.ajax({
            url: '/private/members/users/edit_profile/add_user/',
            type: 'POST',
            data: {

                'first_name': name,
                'last_name': lastname,
                'username': username123,
                'email': email,
                'profile_status' :profile,
                "csrfmiddlewaretoken": document.getElementsByName('csrfmiddlewaretoken')[0].value

            },


            success: function (response) {
                var data = JSON.parse(response);

                try {
                    if (data.info.id != undefined) {

                         var usertype;
                               if(profile_status == 0){

                                   usertype = "Job Seeker"
                               } else usertype = "Company"




                        edit_button = '<td><button value= "' + data.info.id + '"  class="button123 btn btn-info btn-sm" data-toggle="modal" data-target="#myModal" type="button">Edit</button></td>';
                        profile_button = '<td><button value= "' + data.info.id + '" type="button" class="profile btn btn-info btn-sm" >Profile</button></td>';
                        delete_button = '<td><button value= "' + data.info.id + '" type="button" class="delete btn btn-info btn-sm" >Delete</button></td>';
                        newline = '<tr><td> ' + data.info.id + ' </td> <td> ' + data.info.username + '</td> <td> ' + data.info.firstname + '</td> <td> ' + data.info.lastname + '</td> <td> ' + data.info.email + '</td> <td> ' + data.info.active +' </td><td> '+ usertype +' </td> ' + edit_button + ' ' + profile_button + ' ' + delete_button + '</tr>';

                        //newline = '<tr><td> ' + data.info.id + ' </td> <td> ' + data.info.username + '</td> <td> ' + data.info.firstname + '</td> <td> ' + data.info.lastname + '</td> <td> ' + data.info.email + '</td> <td> '+ data.info.active +' </td> '+ usertype +' ' + edit_button + '<td>'+ profile_button + '</td>' + delete_button + '</tr>';


                       // $('.table > tbody:first').append(newline);
                        $(newline).insertBefore('table > tbody > tr:first');
                                    $('#n11').val("");
                                    $('#l11').val("");
                                    $('#u11').val("");
                                    $('#e11').val("");
                              $('.message_display_add').text('Saved');
                              $('.message_display_add').delay(2000).fadeOut('slow');
                    }
                }
                catch(err) {

                       if(err){

                           $('.message_display_add').text('Email or user exist');
                           $('.message_display_add').delay(2000).fadeOut('slow');
                       }
                    }


            },


        });
    return false;
});


$('.close_re').click(function() {
    location.reload();
    });
//$(myTable).empty();


     $(document).on('click', '#add_button', function () {
         $('.message_display_add').text('');

    });

///Delete button function
    $(document).on('click', 'button.delete', function () {
        $('.err').text(' ');
        $('.err').show();
     if (confirm('Are you sure ?')) {
         $(this).closest('tr').remove();
         {

             event.preventDefault();
             id = $(this).val();
             $.ajax({
                 url: '/private/members/users/edit_profile/delete_user/',
                 type: 'POST',
                 data: {
                     'id': id,
                     "csrfmiddlewaretoken": document.getElementsByName('csrfmiddlewaretoken')[0].value

                 },


                 success: function (response) {

                    response = JSON.parse(response);

                  $('.err').text('User is Deleted');
                  $('.err').delay(2000).fadeOut('slow');



                 },
                 error: function (response) {

                 }
             });
             return false;
         }
     }
});



 $(document).on('click', '#search', function () {


             event.preventDefault();
             $('.err').text(' ');
             $('.err').show();
             search = $('#searchbox').val();
              //if (/\s/.test(search)) {
              //      alert("space aa gae hai")
              //       }
           if(search != '') {

               $.ajax({
                   url: '/private/members/users/edit_profile/search/',
                   type: 'POST',
                   async : false,
                   data: {
                       'value': search,
                       "csrfmiddlewaretoken": document.getElementsByName('csrfmiddlewaretoken')[0].value

                   },

                   success: function (data) {
                       var aap = jQuery.parseJSON(data);

                       try {
                           $(".table").find("tr:gt(0)").remove();
                           var lens = (Object.keys(aap.user_info).length);

                           tableappend(aap,lens);

                       }
                       catch(e){

                       }

                       if(aap.status == "Not Found") {

                        $('.err').text(search + " " + "Not Found");
                         $('.err').delay(2000).fadeOut('slow');


                    }


                   },

               });
               return false;

           }
     else
           {
            message_display('Please enter the keyword in the search field', 0)
           }



});


// $(document).on('click', '#allusers', function () {
//
//
//     event.preventDefault();
//     $.ajax({
//         url: '/private/members/users/edit_profile/allusers/',
//         type: 'POST',
//         data: {
//             "csrfmiddlewaretoken": document.getElementsByName('csrfmiddlewaretoken')[0].value
//
//         },
//
//               success: function (data) {
//                       var aap = jQuery.parseJSON(data);
//                       console.log(aap);
//
//
//                       try {
//                           $(".table").find("tr:gt(0)").remove();
//                           var lens = (Object.keys(aap.user_info).length);
//
//                           tableappend(aap,lens);
//
//                       }
//                       catch(e){
//
//                       }
//
//
//
//
//
//
//
//                   },
//         error: function (response) {
//
//         }
//     });
//     return false;
//
//
//});


$(document).on('click', '#active', function () {


     event.preventDefault();
     id = $(this).val();
     $.ajax({
         url: '/private/members/users/edit_profile/activeusers/',
         type: 'POST',
         data: {
             "csrfmiddlewaretoken": document.getElementsByName('csrfmiddlewaretoken')[0].value

         },

success: function (data) {
                       var aap = jQuery.parseJSON(data);

                       try {
                           $(".table").find("tr:gt(0)").remove();
                           var lens = (Object.keys(aap.user_info).length);

                           tableappend(aap,lens);

                       }
                       catch(e){

                       }







                   },
         error: function (response) {

         }
     });
     return false;


});



//$(document).on('click', '#disable', function () {
//
//
//     event.preventDefault();
//     $.ajax({
//         url: '/private/members/users/edit_profile/nonactiveusers/',
//         type: 'POST',
//         data: {
//             "csrfmiddlewaretoken": document.getElementsByName('csrfmiddlewaretoken')[0].value
//
//         },
//
//success: function (data) {
//                       var aap = jQuery.parseJSON(data);
//
//                       try {
//                           $(".table").find("tr:gt(0)").remove();
//                           var lens = (Object.keys(aap.user_info).length);
//
//                           tableappend(aap,lens);
//
//                       }
//                       catch(e){
//
//                       }
//
//
//
//
//
//
//
//                   },
//         error: function (response) {
//
//         }
//     });
//     return false;
//
//
//});

//$(document).ready(function() {
//
//     event.preventDefault();
//     $.ajax({
//         url: '/private/members/users/edit_profile/allusers/',
//         type: 'POST',
//         data: {
//             "csrfmiddlewaretoken": document.getElementsByName('csrfmiddlewaretoken')[0].value
//
//         },
//
//   success: function (data) {
//                       var aap = jQuery.parseJSON(data);
//
//                       try {
//                           $(".table").find("tr:gt(0)").remove();
//                           var lens = (Object.keys(aap.user_info).length);
//
//                           tableappend(aap,lens);
//
//                       }
//                       catch(e){
//
//                       }
//
//
//
//
//
//
//
//                   },
//         error: function (response) {
//
//         }
//     });
//     return false;
//
//});
//
//




 function get_id(value){
     $.ajax({
                               url: '/private/members/users/edit_profile/get_id/',
                               type: 'POST',
                               async : false,
                               data: {
                                   'username': value,
                                   "csrfmiddlewaretoken": document.getElementsByName('csrfmiddlewaretoken')[0].value

                               },


                               success: function (data) {

                                   data = JSON.parse(data);
                                   final_id = data.user_info.id;



                               },

                               error: function (data) {

                               }



                           });

                        return final_id;

 };


 function tableappend(aap,lens){

     for (var j = 0; j <= lens; j++) {
         var mmore = jQuery.parseJSON(aap.user_info);
         value = mmore[j]['fields']['username'];
         newvalue = get_id(value);
         profile_status=profilestatus(newvalue);
         var usertype;
         if(profile_status == 0){
             usertype = "Job Seeker"
         } else usertype = "Company"
         edit_button = '<td><button value= "' + newvalue + '"  class="button123 btn btn-info btn-sm" data-toggle="modal" data-target="#user_editmodal" type="button">Edit</button></td>';
         profile_button = '<td><button value= "' + newvalue + '" type="button" class="profile btn btn-info btn-sm" >Profile</button></td>';
         delete_button = '<td><button value= "' + newvalue + '" type="button" class="delete btn btn-info btn-sm" >Delete</button></td>';
         //active = capitalise();
         // newline = '<tr><td> ' + newvalue + ' </td> <td> ' + mmore[j]['fields']['username'] + '</td> <td> ' + mmore[j]['fields']['first_name'] + '</td> <td> ' + mmore[j]['fields']['last_name'] + '</td> <td> ' + mmore[j]['fields']['email'] + '</td> <td> ' + (mmore[j]['fields']['is_active']) +' </td><td> '+ usertype +' </td> ' + edit_button + ' ' + profile_button + ' ' + delete_button + '</tr>';
         // $(newline).appendTo('.table > tbody:last');
}

 };
 function profilestatus(value){

     try {
         $.ajax({
             url: '/private/members/users/edit_profile/profilestatus/',
             type: 'POST',
             async: false,
             data: {
                 'id': value,
                 "csrfmiddlewaretoken": document.getElementsByName('csrfmiddlewaretoken')[0].value

             },


             success: function (data) {
                 console.log(data);
                 data = JSON.parse(data);
                 user_status = data.user_info.user_status;



             },

             error: function (data) {

             }


         });


     }

      catch(e){


      }
  return user_status;
 };

//$(document).on('click', '#companynew', function () {
//
//
//     event.preventDefault();
//     $.ajax({
//         url: '/private/members/users/edit_profile/companyfilter/',
//         type: 'POST',
//         data: {
//             "csrfmiddlewaretoken": document.getElementsByName('csrfmiddlewaretoken')[0].value
//
//         },
//
//success: function (data) {
//                        var aap = jQuery.parseJSON(data);
//
//                       try {
//                           $(".table").find("tr:gt(0)").remove();
//                           var lens = (Object.keys(aap.user_info).length);
//
//                           tableappend(aap,lens);
//
//                       }
//                       catch(e){
//
//                       }
//
//
//
//
//
//
//
//                   },
//         error: function (response) {
//
//         }
//     });
//     return false;
//
//
//
//});

//
//
// $(document).on('click', '#job_seeker', function () {
//
//
//     event.preventDefault();
//     $.ajax({
//         url: '/private/members/users/edit_profile/job_seekerfilter/',
//         type: 'POST',
//         data: {
//             "csrfmiddlewaretoken": document.getElementsByName('csrfmiddlewaretoken')[0].value
//
//         },
//
//success: function (data) {
//                        var aap = jQuery.parseJSON(data);
//
//                       try {
//                           $(".table").find("tr:gt(0)").remove();
//                           var lens = (Object.keys(aap.user_info).length);
//
//                           tableappend(aap,lens);
//
//                       }
//                       catch(e){
//
//                       }
//
//
//
//
//
//
//
//                   },
//         error: function (response) {
//
//         }
//     });
//     return false;
//
//
//
//});
//



// $(document).on('click', '.profile_button', function () {
//
//
//     event.preventDefault();
//     valuedata = $(this).val();
//     console.log(valuedata);
//     $.ajax({
//         url: '/private/members/users/edit_profile/profile_full/',
//         type: 'POST',
//         data: {
//             "id":valuedata,
//             "csrfmiddlewaretoken": document.getElementsByName('csrfmiddlewaretoken')[0].value
//
//         },
//
//                    success: function (data) {
//
//                                   data = JSON.parse(data);
//                                   console.log(data.user_info);
//                                   image1 = data.user_info.pic;
//                                   var res = image1.substr(38);
//
//
//                        $(".circle-image").css('background-image', 'url( "'+ res +'")');
//                        $("#h44").text(data.user_info.name+" "+ data.user_info.last);
//                        $('#name1').attr('value',data.user_info.name);
//                        $('#last1').attr('value',data.user_info.last);
//                        $('#email1').attr('value',data.user_info.email);
//                        $('#contact1').attr('value',data.user_info.contact);
//                        $('#address1').attr('value',data.user_info.address);
//
//
//
//
//
//
//
//
//
//                   },
//         error: function (response) {
//
//         }
//     });
//
//
//
//
//});
var base_url = 'http://jobinsider.xyz:8000/';

function getResults(pageValue)
{
    console.log(pageValue);
    $.ajax({
            'method':'GET',
            'url': base_url + 'private/members/users/?page='+pageValue,
            success: function(data)
              {
                  $('.table').html(data);
                  console.log(data)
              }
            }
        )

};



$('.edit_advertisement__btn').on('click', function(e)
{
    e.preventDefault();
    var advertisement_id = $(this).attr('value');
    $.ajax(
        {
            type: 'POST',
            url: '/private/members/advertisement/edit/',
            data:{
                'job_id': advertisement_id,
                "csrfmiddlewaretoken": document.getElementsByName('csrfmiddlewaretoken')[0].value
            },
            success: function (m) {
                $('#editAdvertisement').modal('toggle');
                $('#editAdvertisement').modal('show');
                $('#editAdvertisement .modal-body').html(m);
                tinymce.init({selector:'textarea'});
            },
            error: function (m) {
                
            }
        }
    );
    return false;
});

 function btn_save__advertisement()

 {
     var job_id = $('.job_id_form').attr('value');
     var form_data = $('#edit_advertisement_form').serialize();// new FormData(formElement);
     var job_description = (tinyMCE.activeEditor.getContent({format : 'raw'}));
     var csrfmdi = document.getElementsByName('csrfmiddlewaretoken')[0].value;
     $.ajax(
         {
             url:'/private/members/advertisement/edit_job/',
                type:'POST',
                data:{
                    'form_val': form_data,
                    'csrfmiddlewaretoken': csrfmdi,
                    'description': job_description,
                    job_id: job_id
                },
                success:function(m)
                {
                    resp = JSON.parse(m);
                    if(resp.status==true)
                    {
                        window.location.reload();
                        //window.location.href= '/company/settings-job/'+ resp.last_inserted;
                    }
                },
                error:function(m)
                {

                }
         }
     )
     return false;
 }

 $('.enable_job_advertisement').on('click',function(e)
 {
     e.preventDefault();
     var job_id = $(this).attr('value');
     var csrfmdi = document.getElementsByName('csrfmiddlewaretoken')[0].value;
     $.ajax(
         {
             url:'/private/members/advertisement/enable_job/',
                type:'POST',
                data:{
                    'csrfmiddlewaretoken': csrfmdi,
                    job_id: job_id
                },
                success:function(m)
                {
                    resp = JSON.parse(m);
                    if(resp.status==true)
                    {
                        window.location.reload();
                        //window.location.href= '/company/settings-job/'+ resp.last_inserted;
                    }
                },
                error:function(m)
                {

                }
         }
     );
     return false;
 });

 $('.disable_job_advertisement').on('click',function(e)
 {
     e.preventDefault();
     var job_id = $(this).attr('value');
     var csrfmdi = document.getElementsByName('csrfmiddlewaretoken')[0].value;
     $.ajax(
         {
             url:'/private/members/advertisement/disable_job/',
                type:'POST',
                data:{
                    'csrfmiddlewaretoken': csrfmdi,
                    job_id: job_id
                },
                success:function(m)
                {
                    resp = JSON.parse(m);
                    if(resp.status==true)
                    {
                        window.location.reload();
                        //window.location.href= '/company/settings-job/'+ resp.last_inserted;
                    }
                },
                error:function(m)
                {

                }
         }
     );
     return false;
 });

  $('.reject_job_advertisement').on('click',function(e)
 {
     e.preventDefault();
     var job_id = $(this).attr('value');
     var csrfmdi = document.getElementsByName('csrfmiddlewaretoken')[0].value;
     $.ajax(
         {
             url:'/private/members/advertisement/disable_job/',
                type:'POST',
                data:{
                    'csrfmiddlewaretoken': csrfmdi,
                    job_id: job_id
                },
                success:function(m)
                {
                    resp = JSON.parse(m);
                    if(resp.status==true)
                    {
                        window.location.reload();
                        //window.location.href= '/company/settings-job/'+ resp.last_inserted;
                    }
                },
                error:function(m)
                {

                }
         }
     );
     return false;
 });