/**
 * Created by azhar on 8/30/15.
 */
/** classes made for the validations of the inputs
**/
//reg exp formaters


function validation_check(input_value)
{
    this.error = 0;
    this.success=0;
    this.obj_value =  input_value;
    if(this.obj_value=='')
    {
        this.error=1;
        return this.error;
    }

}


function date_input(input_value)
{
    this.error = 0;
    this.success=0;
    this.obj_value =  input_value;
    if(this.obj_value=='')
    {
        return this.error;
    }
    else{
        this.success=1;
        return this.success;
    }


}


// to get the field value by name

//to get the field value by class

//to get the field value by id

$('.datepicker').datepicker({
    format: 'yyyy-mm-dd',
    startDate: '0d'
});