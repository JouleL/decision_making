var fs = require('fs');

var file_reader = fs.readFileSync('data1.json', 'utf8');
//console.log(file_reader);
var mydata = JSON.parse(file_reader);
//console.log(mydata);
var variant, m1, m2, d1, d2, p1, p2, bildProb, noBuildProb, years;

function bestDecison() {
	let decision=[];
	let best;
	for (let i = 0; i<4; i++){
	best = parseFloat((mydata[i].D1 * mydata[i].P1 + mydata[i].D1 * mydata[i].P2) * mydata[i].years / mydata[i].M1);
    decision.push(best);
    mydata[i].coef = best;
    console.log("Ефективність варіанту " + mydata[i].var + " дорівнює = "+ decision[i]);
	}
	
	
	for (let i=0;i<4;i++){
		if (mydata[i].coef==Math.max.apply(Math, decision)) {
			console.log("Отже найкращий варіант буде: " + mydata[i].var + "\nЦіна: " + mydata[i].M1 + "\nПрибуток: " + mydata[i].D1 + "\nЙмовірність: " + mydata[i].P1 + "\nВтрата: " + mydata[i].D2 + "\nЙмовірність: " + mydata[i].P2 + "\nКількість років: " + mydata[i].years);
		}
	}

}

bestDecison();


