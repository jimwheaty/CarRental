function setInfo(userData){
	var d=new Date(userData.joined);
	document.getElementById("Name").innerHTML = userData.user;
	document.getElementById("Date").innerHTML = d.toLocaleString('el-GR',{weekday:'long', year:'numeric', month:'long',day:'numeric'});
	document.getElementById("Contrib").innerHTML = userData.cont;
}
function setHistory(entries){
	var i;
	var container = document.getElementById("hBox");
	for (i=0;i<entries.length;i++){
		var newDiv = document.createElement("div");
		newDiv.setAttribute('class','hSub');
		var pic=document.createElement("img");
		pic.setAttribute('src',entries[i].image);
		newDiv.appendChild(pic);
		pic.setAttribute('style',"float:left;width:100px;height:100px;")
		createEntry(entries[i],newDiv);
		container.appendChild(newDiv);
	}
}
function createEntry(entry,element){
	var j=0;
	var para = document.createElement("p");
	para.setAttribute('class','small');
	var node = document.createTextNode("Εταιρεία Ενοικίασης: "+entry.company);
	para.appendChild(node);
	element.appendChild(para);

	var para = document.createElement("p");
	para.setAttribute('class','small');
	var node = document.createTextNode("Κατασκευαστής και Μοντέλο: "+entry.manuf+ ' '+entry.model);
	para.appendChild(node);
	element.appendChild(para);
	
	var d1=new Date(entry.leaseStart);
	var d2=new Date(entry.leaseEnd);
	var para = document.createElement("p");
	para.setAttribute('class','small');
	var node = document.createTextNode("Περίοδος Ενοικίασης: "+d1.toLocaleString('el-GR',{year:'numeric', month:'numeric',day:'numeric'})+ ' - '+d2.toLocaleString('el-GR',{year:'numeric', month:'numeric',day:'numeric'}));
	para.appendChild(node);
	element.appendChild(para);

	var para = document.createElement("p");
	para.setAttribute('class','small');
	var node = document.createTextNode("Τιμή ανά ημέρα: "+entry.payPerDay+'€');
	para.appendChild(node);
	element.appendChild(para);
}

