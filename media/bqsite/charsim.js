charCount = 0;

$(document).ready(function()
{       
    addCharPlate();       
    $('a#addChar').click(addCharPlate);   
    
});

function addCharPlate()
{
	ajax("/addchar", {charIndex:charCount}, initCharPanel)	
	charCount += 1;	
}


function initCharPanel(data)
{
	$('div.controlHeaderRow#charRows').append(data.htmlrow);
	var appendedData = $('div.CharContainer').append(data.html);	
	
	var charIndex = data.charIndex;
	
	getInputs(charIndex).each(function(index)
	{
		var obj = $(this);
		var id = obj.attr('id');
		
		if(id != 'charName')
        {
            obj.val(0);
            createInputCallback(obj, function(){sendInputs(charIndex)});
        }  
	});  
	
	var charName = "Character "+(parseInt(charIndex) + 1);
    var charNameBox = $('div.charBox#'+charIndex+' input[id=charName]');

    createInputCallback(charNameBox, modifyName);
    
    //charnamebox
    charNameBox.val(charName);
    $('div.charBox#'+charIndex+' input[id=charLevel]').val(1);
    
    $('#row'+charIndex).html(charName);

    //update target box
    $('select#target').each(function(index){
        $(this).html('');

        for(var i = 0; i < charCount; ++i)
        {
            var name = $('div.charBox#'+i+' input[id=charName]').val();
            $(this).append('<option id=\"'+i+'\">'+name+'</option>');
        }    
        
    });
    

    sendInputs(charIndex);
    
}

function modifyName()
{
    var parentBox = $(this).parents('div.charBox:first');
    var charIndex = parentBox.attr('id');
    var charName = $(this).val();

    $('div#row'+charIndex).html(charName);

    //update target dropdowns
    $('select#target').each(function(index){
        $(this).children('option[id='+charIndex+']:first').html(charName);
    });

}

function createInputCallback(obj, fn)
{
    obj.change(fn);    
    obj.keyup(fn);    
    //obj.focusout(fn);     
}

function getInputs(charIndex){return $('div#'+charIndex+' :input');}
function getValues(charIndex){return $('div#'+charIndex+' div.statValue');}
function formItem(charIndex, itemName){return $("div#"+charIndex + "> div div div input#"+itemName);}
function statItem(charIndex, itemName){return $("div#"+charIndex + "> div div div div#"+itemName);}


         
function updateCharBox(data)
{
    var charIndex = data.charIndex;
    delete data.charIndex;
    
    getValues(charIndex).each(function(index)
    {
    	var obj = $(this);
		var id = obj.attr('id');
		
		if(id in data)
			obj.html(data[id]);
    });
    
}

function ajax(pth, data, func)
{
	$.ajax(
	{
		type: 'POST',
		cache: false,
        data: data,
		dataType: 'json',
		url: '/charsim' + pth,
		success:func
	});
}

function sendInputs(charIndex)
{
    var data = {};
    data.charIndex = charIndex;

    getInputs(charIndex).each(function(index)
	{
		var obj = $(this);
		var id = obj.attr('id');

        if(obj.prop('type') == 'checkbox')
            data[id] = obj.prop('checked');
        else		
		if(id != 'charName')
        	data[id] = obj.val();  

	});
    
    var targetIndex = $('div#'+charIndex+' select[id=target] option:selected').attr('id');  
    
    getValues(targetIndex).each(function(index){
        var obj = $(this);
        var id = obj.attr('id');

        data['d'+id] = obj.html();
            
    });
        
   ajax('/update', data, updateCharBox);    

}
