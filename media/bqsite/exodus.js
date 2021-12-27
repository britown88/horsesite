$(document).ready(function()
{       
    $('input#send').click(addName);   
    
});

function addName()
{
    ajax("/update", {name:$('input#myname').val()}, dummy)  
    $('div#content').html("Thank you!")
}

function dummy(data){}

function ajax(pth, data, func)
{
    $.ajax(
    {
        type: 'POST',
        cache: false,
        data: data,
        dataType: 'json',
        url: "/exodus" + pth,
        success:func
    });
}
