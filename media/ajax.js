// using jQuery
var rows = new Array()
var lineCount, logY
var scrolling

$(document).ready(function()
{
	for(i = 0; i < 10; ++i)
	{
		rows[i] = $('#row'+(i+1));
		rows[i].css('opacity', i*0.1);
	}

	ajax('/getLineCount', getLineCount);
	scrolling = false;	
	logY = $('#log').position().top;
	
	setInterval(interval, 100);
	
	$("button#update").click(function()
	{
		$("button#update").attr("disabled", "disabled");
		ajax('/update', update);
	});
});

var newList = new Array();

function ajax(pth, func)
{
	$.ajax(
	{
		type: 'POST',
		cache: false,
		dataType: 'json',
		url: '/amishbot' + pth,
		success:func
	})
}


function refresh(data)
{
	newLines = data.lineCount - lineCount;

	if(data.allowUpdate)
		$("button#update").removeAttr("disabled");
	else
		$("button#update").attr("disabled", "disabled");
	
	var str = data.minTillUpdate + ":" + (data.secTillUpdate < 10 ? '0' : '') + data.secTillUpdate;
	$("span#updTime").html(str);

	if(!scrolling)
	{
		if(newLines > 0)
		{
		scrolling = true;
		
		newList = new Array()
		for(i = 0; i < 9; ++i)
			newList[i] = rows[i+1].html();
		newList[9] = data.lines[9-(newLines-1)];


		d = $('#log').innerHeight()/10;
		$("#log").animate(
			{
				top: '-='+d,
				opacity: '-='+0.1
			}, 
			{
				easing:'linear',
				queue:false, 
				duration:250, 
				complete:function(){
					$("#log").css('top', logY);
					$("#log").css('opacity', 1.0);
					scrolling = false;
					for (i=0; i<10; i++)
						rows[i].html( newList[i]);
					}
			})
		lineCount++;
		}
		else if(newList.length == 0)
			for(i = 0; i<10;++i)
			{
				newList[i] = data.lines[i];
				rows[i].html(data.lines[i]);
			}
	}


}

function getLineCount(data)
{
	lineCount = data.lineCount;
}

function update(data)
{
}

function interval()
{
	ajax('', refresh);
}




