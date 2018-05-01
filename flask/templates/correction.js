var temp=[];
function func1(num,num2,correct,record)
{
	// console.log(correct)

	x=(num).toString();
	var inputElems = document.getElementsByTagName("input");
	count=0;
	for (var j=0; j<x.length; j++)
	{
		 for (var i=0; i<inputElems.length; i++) 
		 {       
           if (inputElems[i].type == "checkbox" && inputElems[i].checked == true)
           {
        		if(inputElems[i].getAttribute("id")==x[j]);
        		count++;      
              	// console.log(record)
             	record[i].push(j);
             	// console.log(record[i])
           }

        }

	}
	if(x.length==count)
		correct[num2]=1;
	temp.push(correct);
	temp.push(record);
	// console.log(temp)
}
function func2()
{
  // console.log(record)
  // console.log(correct)
  console.log(temp[0]);
  window.open("{{ url_for('result',record=temp[1],correct=temp[0])}}");

}
