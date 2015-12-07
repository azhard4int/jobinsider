//for adding the evaluation test template to the database.
$('#add_evaluation').on('submit', function(event)
       {
        $(".eva_heading_status").text("").show();
           event.preventDefault();

        $.ajax({
                url: '/private/members/evaluation/add_template/',
                type: 'POST',
                data:$('form#add_evaluation').serialize(),



            success: function (response) {
              message_display('Evaluation Test Added Successfully', 1)
                 var data = jQuery.parseJSON(response);
                console.log(data.status.evaluation_name);
                var eva_type;
                if (data.status.evaluation_type == 0) {

                   eva_type = "MCQ";
               } else eva_type = "True/False";

               var eva_status;
               if (data.status.evaluation_status == 0) {

                   eva_status = "Not Approved";
               } else eva_status = "Approved";





                edit_button='<td><div class="dropdown"><button value="' + data.status.evaluation_id + '" id="dropdown" class="btn btn-info dropdown-toggle" type="button" data-toggle="dropdown">Edit'+
                    '<span class="caret"></span></button>'+
                      '<ul class="dropdown-menu">'+
                      '<li><a class="editbutton" data-target="#editmodal" data-toggle="modal" href="#editmodal">Edit Template</a></li>'+
                      '<li><a href="testing/sample/' + data.status.evaluation_id + '">Edit Questions</a></li></td>';






                //edit_button = '<td><button value= "' + data.status.evaluation_id + '"  class="button123 btn btn-info btn-sm" data-toggle="modal" data-target="#myModal" type="button">Edit</button></td>';
               profile_button = '<td><button value= "' + data.status.evaluation_id + '"  class="profile_button btn btn-info" data-toggle="modal" data-target="#question_modal" type="button">Add Questions</button></td>';
               preview_button = '<td><button value= "' + data.status.evaluation_id + '" type="button" class="delete btn btn-info" >Preview</button></td>';
               delete_button = '<td><button value= "' + data.status.evaluation_id + '" type="button" class="delete btn btn-info" >Delete</button></td>';
               newline = '<tr><td> ' + data.status.evaluation_name + '</td> <td> ' + data.status.evaluation_catagory + '</td> <td> ' + eva_status + '</td> <td> ' + eva_type + '</td> <td> ' + data.status.evaluation_total_questions + edit_button + ' ' + profile_button + ' ' + preview_button +' '+ delete_button + '</tr>';
               $(newline).appendTo('.table > tbody:last').fadeIn('slow');

                $('#eva_title').val("");
                $('#eva_description').val("");
                $('#eva_rules').val("");
                $('#eva_cat').val("");
                $('#eva_type').val(0);
                $('#eva_number').val("");

            },


        });
    return false;
});



$(document).on('change', 'input:radio', function () {

       var selected=$("input[name='radio']:checked").val();
    try {
        if (selected == 1) {

            document.getElementById('option1').style.borderColor = "green";
        } else document.getElementById('option1').style.borderColor = "#DCDCDC";

        if (selected == 2) {

            document.getElementById('option2').style.borderColor = "green";
        } else document.getElementById('option2').style.borderColor = "#DCDCDC";

        if (selected == 3) {
            document.getElementById('option3').style.borderColor = "green";
        } else document.getElementById('option3').style.borderColor = "#DCDCDC";
        if (selected == 4) {

            document.getElementById('option4').style.borderColor = "green";
        } else document.getElementById('option4').style.borderColor = "#DCDCDC";
        if (selected == 5) {

            document.getElementById('option5').style.borderColor = "green";
        } else document.getElementById('option5').style.borderColor = "#DCDCDC";
    } catch(err){


    }

    });




var count;
var numberofquestion;
$('#add_question_button').on('click', function(event)

     {
         var selected=$("input[name='radio']:checked").val();
          alert(selected);
         if(selected == 1){
          $("#correct_answer").val($('#option1').val());
         }
         if(selected == 2){
          $("#correct_answer").val($('#option2').val());

         }
         if(selected == 3){
          $("#correct_answer").val($('#option3').val());

         }
         if(selected == 4){
          $("#correct_answer").val($('#option4').val());

         }
         if(selected == 5){
          $("#correct_answer").val($('#option5').val());

         }
         $("#heading3").text("").show();
         if(count <= numberofquestion) {
             count = count + 1;
         }
         console.log(count);
         $("#headingtop1").text("You have added: "+ count);
    event.preventDefault();
    $.ajax(
        {
            url: '/evaluation/addquestions/',
            type: 'POST',
            data:$('form#add_question').serialize(),



            success:function(response)
            {
              var data = jQuery.parseJSON(response);
                console.log(data.status);

                if(data.status == "True"){

                    $("#heading3").text("Successfully Added").delay(2000).fadeOut();
                    $('#question').val("");
                    $('#answer').val("");
                    $('#option1').val("");
                    $('#option2').val("");
                    $('#option3').val("");
                    $('#option4').val("");
                    $('#option5').val("");
                }
                if(data.status == "False"){
                     $("#heading3").text("You can not add more questions").delay(2000).fadeOut();
                }

            },
            error: function(response) {

        }
        }
    );
});


$(document).on('click', '#reset', function () {
    try {
        $('#question').val("");
        $('#correct_answer').val("");
        $('#option1').val("");
        $('#option2').val("");
        $('#option3').val("");
        $('#option4').val("");
        $('#option5').val("");
        $("#box" + 3).remove();
        $("#box" + 4).remove();
        $("#box" + 5).remove();
        $("#label" + 3).remove();
        $("#label" + 4).remove();
        $("#label" + 5).remove();
        document.getElementById('option1').style.borderColor = "#DCDCDC";
        document.getElementById('option2').style.borderColor = "#DCDCDC";
        document.getElementById('option3').style.borderColor = "#DCDCDC";
        document.getElementById('option4').style.borderColor = "#DCDCDC";
        document.getElementById('option5').style.borderColor = "#DCDCDC";

    } catch(Err){


    }

});
//this for getting the total number of questions
$('.add_button').on('click', function(event)
     {
            count=0;
            numberofquestion=0;
            event.preventDefault();
            var test_id = $(this).attr('value');
            console.log(test_id);
            test_template_id=$(this).val();
            test_id=$(this).closest(".dropdown").find('#dropdown').val();

            $('#question').val("");
            $('#answer').val("");
            $('#option1').val("");
            $('#option2').val("");
            $('#option3').val("");
            $('#option4').val("");
            $('#option5').val("");
            $('#hiddenvalue').val(test_id);
            $.ajax(
                {
                    url: '/evaluation/addquestions/',
                    type: 'GET',
                    data:{

                        'test_template_id':test_id,
                        "csrfmiddlewaretoken": document.getElementsByName('csrfmiddlewaretoken')[0].value
                    },
                    success:function(response)
                    {
                      var data = jQuery.parseJSON(response);
                        $("#headingtop1").text("You have added: "+ data.status.question_count);
                        count = data.status.question_count;
                        numberofquestion = data.status.total_questions;
                        $("#headingtop2").text("Total Number Questions  : "+ data.status.total_questions);
                    },
                    error: function(response) {
                }
                }
            );
});

//this is for adding and removing option2, option3 in modal
$('#question_modal').ready(function(){
     var counter = 3;
    $("#addoptions").click(function () {
        $("#heading3").text("").show();
	if(counter>5){
            $("#heading3").text("Not more than 5 options").delay(2000).fadeOut();
            return false;
	}

	var newTextBoxDiv = $(document.createElement('div'))
	     .attr("class", 'form-group').attr("id","box" + counter);
        var text='<input type="text" class = "form-control" " name="option' + counter +
	      '" id="option' + counter + '" value="" placeholder = "option">'
        var label='<label class = "col-sm-2 control-label">Option ' + counter + '</label>' + '<div class ="col-sm-10">'+ text +'</div>';
         var radio='<label id="label'+counter+'" class="btn btn-default">'+
               '<input type="radio" name="radio" id="radio" value="'+counter +'" autocomplete="off"> Option  ' + counter + '</label>';

        newTextBoxDiv.before().html(label);
     //$( "#inserthere").appendChild( radio );
     //   $(radio).insertAfter("#inserthere").last();
     //   $( "#inserthere" ).last().before( radio );
        $( "#inserthere" ).append( $(radio) );
     $( "#lastchild" ).first().before( newTextBoxDiv );
	counter++;
     });

     $("#removeoptions").click(function () {
         $("#heading3").text("").show();
	   if(counter==3){
          $("#heading3").text("Min options are 2").delay(2000).fadeOut();
          return false;
       }
	    counter--;
        $("#box" + counter).remove();
        $("#label" + counter).remove();
     });

  });
//this is for edit button

$('.editbutton').on('click', function(event)
     {
        test_template_id=$(this).closest(".dropdown").find('#dropdown').val();
         console.log(test_template_id);

        event.preventDefault();
        $.ajax(
            {
                url: '/private/members/evaluation/edit_user_template/',
                type: 'GET',
                data:{
                    'id':test_template_id,
                    "csrfmiddlewaretoken": document.getElementsByName('csrfmiddlewaretoken')[0].value
                },
                success:function(response)
                {

                    var data = jQuery.parseJSON(response);
                    console.log(data);
                    $("#edit_eva_title").val(data.status.evaluation_name);
                    $("#edit_eva_description").val(data.status.evaluation_description);
                    $("#edit_eva_rules").val(data.status.evaluation_rules);
                    $("#edit_eva_cat").val(data.status.evaluation_catagory);
                    if (data.status.evaluation_type == 0) {

                       $("#edit_eva_type").val(0);
                   } else eva_type = $("#edit_eva_type").val(1);
                    $("#edit_eva_number").val(data.status.evaluation_total_questions);
                    $("#evaluation_test_template_id").val(data.status.id);
                },
                error: function(response) {

            }
            }
        );
});
//this for updating and editing the Evaluation test template
//update button is in the evaluation_editmodal.html

$('#updatebutton').on('click', function(event)
     {
    event.preventDefault();

    $.ajax(
        {
            url: '/evaluation/edit-evaluation-test-template/',
            type: 'POST',
            data:$('form#edit_evaluation').serialize(),
            success:function(response)
            {
              var data = jQuery.parseJSON(response);
            },
            error: function(response) {
            }
        }
    );
});

//this is deleting evaluation tests
$('.delete').on('click', function(event)
     {
        test_template_id=$(this).closest(".dropdown").find('#dropdown').val();
        $(this).closest('tr').remove().delay(2000).fadeOut();
        event.preventDefault();
        $.ajax(
            {
                url: '/evaluation/delete-evaluation-test-template/',
                type: 'POST',
                data:{
                    'id':test_template_id,
                    "csrfmiddlewaretoken": document.getElementsByName('csrfmiddlewaretoken')[0].value

                },
                success:function(response)
                {
                    resp = JSON.parse(response);
                    if(resp.status==true)
                    {
                        $('#evaluation_test_box_'+test_template_id).remove('fast');
                        message_display('Evaluation Test Deleted Successfully', 1)
                    }

                },
                error: function(response) {
                }
            }
        );
});

$('.previewtest').on('click', function(event)
     {
         event.preventDefault();
         get_id=$(this).attr('value');
         $("div").remove("#removeoptions");
         $("#next_button").show();
         $("#remove_label").show();

         try{

    $.ajax(
        {
            url: '/evaluation/get-evaluation-test-questions/',
            type: 'GET',
            data:{
                'id':get_id,
                "csrfmiddlewaretoken": document.getElementsByName('csrfmiddlewaretoken')[0].value

            },
            success:function(response)
            {
              var data = jQuery.parseJSON(response);

                if(data.length==undefined){

                    alert("You have not add any questions to template");
                     $('#previewtest').modal('hide');
                }

                 question(data);
            },
            error: function(response) {
             //console.log(response);
        }
        }
    );
             } catch(e){



}
});


$('#next_button').on('click', function(event)
     {
         event.preventDefault();
         var selected=$("input[name='option']:checked").val();
         $("#current_answer").val(selected);
         $("div").remove("#removeoptions");
         $("#headingtest").text("");

    $.ajax(
        {
            url: '/evaluation/get-evaluation-test-questions/',
            type: 'POST',
            data:$('form#next_question_form').serialize(),
            success:function(response)
            {
             var data = jQuery.parseJSON(response);
                console.log(data);
                if(data.status =="Test is Finished"){


                    //$("button").remove("#next_button");
                    //$("label").remove("#remove_label");
                    $("#next_button").hide();
                    $("#remove_label").hide();
                    $('#headingtest').text("Test is Finished and You got "+data.final_marks+" out of "+data.questions);




                }
                if(data.status =="Test is incomplete"){
                  $('#headingtest').text("Test is incomplete");
                }
                question(data);

            },
            error: function(response) {
             //console.log(response);
        }
        }
    );
});



$('#close_button').on('click', function(event) {
    //location.reload();
//$("button").remove("#next_button");
//    $("label").remove("#remove_label");
});














//for populating testmodal
function question(data){

    if(data.length != undefined) {
        $('#previewtest').modal('show');
        var newdata = jQuery.parseJSON(data.options);
        $('#headingtest').text(data.question);
        $('#current_question_id').val(data.question_id);
        $('#test_id').val(data.test_id);
        w=1;
        for (x = 0; x < data.length;x++) {

            newradio = '<div class="radio" id="removeoptions">' +
                '<label>' +
                '<input id="'+w+'" name="option" value="' + newdata[x]['fields']['evaluation_question_option'] + '" type="radio"/>' +
                '' + newdata[x]['fields']['evaluation_question_option'] + '</label>' +
                '</div></div>';


            $("#current_question_id").first().after(newradio);
         w++;
        }


    }

}




$('.eva_add_template').on('click', function(event) {
        $("#add_evaluation").modal("show");
    }
);


$('.approve').on('click', function(event)
     {
        test_template_id=$(this).val();
         $(this).closest('tr').remove().delay(2000).fadeOut();

        event.preventDefault();
        $.ajax(
            {
                url: '/private/members/evaluation/approve_evaluation/',
                type: 'POST',
                data:{
                    'id':test_template_id,
                    "csrfmiddlewaretoken": document.getElementsByName('csrfmiddlewaretoken')[0].value

                },
                success:function(response)
                {
                    resp = JSON.parse(response);
                    if(resp.status=='True')
                    {
                          $(this).closest('tr').remove().delay(2000).fadeOut();
                        //$('#evaluation_test_box_'+test_template_id).remove('fast');
                        //message_display('Evaluation Test Deleted Successfully', 1)
                    }

                },
                error: function(response) {
                }
            }
        );
});


$('.reject').on('click', function(event)
     {
        test_template_id=$(this).val();
         $(this).closest('tr').remove().delay(2000).fadeOut();

        event.preventDefault();
        $.ajax(
            {
                url: '/private/members/evaluation/reject_evaluation/',
                type: 'POST',
                data:{
                    'id':test_template_id,
                    "csrfmiddlewaretoken": document.getElementsByName('csrfmiddlewaretoken')[0].value

                },
                success:function(response)
                {
                    resp = JSON.parse(response);
                    if(resp.status=='True')
                    {

                        //$('#evaluation_test_box_'+test_template_id).remove('fast');
                        //message_display('Evaluation Test Deleted Successfully', 1)
                    }

                },
                error: function(response) {
                }
            }
        );
});