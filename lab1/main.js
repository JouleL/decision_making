var fs = require('fs');

var file_reader = fs.readFileSync('matrix1.txt', 'utf8');
console.log(file_reader);
var min_each_row=[];
var max_of_min;
var line_element;
var lines = file_reader.split('\n');
console.log(lines);
var best1;
var min_of_min;
var max_each_row=[];
//Vald
console.log("Критерій Вальда\n");

for (var i = 0; i<lines.length-1; i++) {
	line_element = lines[i].split(' ');
	min_each_row.push(Math.min.apply(Math, line_element));
 }
console.log("Мінімальні значення рядків:" + min_each_row);
min_of_min = Math.min.apply(Math, min_each_row);
max_of_min = Math.max.apply(Math, min_each_row);
console.log("Найвище мінімальне значення:" + max_of_min);

for (var i = 0; i<lines.length-1; i++) {
	line_element = lines[i].split(' ');
	if (Math.min.apply(Math, line_element) == max_of_min && Math.min.apply(Math, line_element) != min_of_min){
		best1 = lines[i];
		break;
	}
}
console.log("Найкраще рішення:"+best1);


//Laplace
console.log("\nКритерій Лапласа\n");
var each_row_sum = 0;
 var parsing;
var divided_sum = [];
var divided_sum2;
var max_value;
var best2;

for (var i = 0; i<lines.length-1; i++) {
	console.log(lines[i]);
	line_element = lines[i].split(' ');
	for (var j = 0; j < line_element.length; j++) {
		//console.log("Елемент дорівнює " + line_element[j]);
		parsing = parseInt(line_element[j]);
		each_row_sum = each_row_sum+parsing;
	}
	divided_sum.push(each_row_sum/(line_element.length));
	console.log("Поділена сума "+ (i+1) +" рядка дорівнює = " + divided_sum[i]);
	//sums.push(divided_sum);
	each_row_sum = 0;
}

max_value = Math.max.apply(Math, divided_sum);
console.log("\nНайвище значення:" + max_value);

for (var i = 0; i<lines.length-1; i++) {
	line_element = lines[i].split(' ');
	for (var j = 0; j < line_element.length; j++) {
		parsing = parseInt(line_element[j]);
		each_row_sum = each_row_sum+parsing;
	}
	divided_sum2 = each_row_sum/line_element.length;
	if (divided_sum2 == max_value){
		best2 = line_element;
	}
	each_row_sum = 0;
}

console.log("Найкраще рішення:"+best2);


//Hurwitz
var hur_values = [];
var hur_values_max;
var k;
var best3;
console.log("\nКритерій Гурвіца\n");

for (var i = 0; i<lines.length-1; i++) {
	line_element = lines[i].split(' ');
	max_each_row.push(Math.max.apply(Math, line_element));
}

 console.log("Мінімальні значення рядків:" + min_each_row);
 console.log("Мaксимальні значення рядків:" + max_each_row);
 
 console.log("\nКоефіцієнт 0.8:");
k=0.8;
 for (var i = 0; i < lines.length-1; i++) {
            hur_values[i] = k * min_each_row[i] + (1 - k) * max_each_row[i];
        }
hur_values_max = Math.max.apply(Math, hur_values);

for (var i = 0; i < hur_values.length; i++) {
    if (hur_values[i]==hur_values_max) {
    	best3 = lines[i];
    }
}
console.log("Значення розраховані по формулі:"+hur_values);
console.log("Найкраще рішення:"+best3);



 console.log("\nКоефіцієнт 0.2:");
k=0.2;
 for (var i = 0; i < lines.length-1; i++) {
            hur_values[i] = k * min_each_row[i] + (1 - k) * max_each_row[i];
        }

hur_values_max = Math.max.apply(Math, hur_values);

for (var i = 0; i < hur_values.length; i++) {
    if (hur_values[i]==hur_values_max) {
    	best3 = lines[i];
    }
}
console.log("Значення розраховані по формулі:"+hur_values);
console.log("Найкраще рішення:"+best3);

//Критерій Байєса – Лапласа

console.log("\nКритерій Байєса – Лапласа\n");
var bl_values = [];
var coef = [0.5, 0.35, 0.15];
var bl_max_value;
for (var i = 0; i < lines.length-1; i++) {
	bl_values.push(0);
}

for (let i = 0; i < lines.length-1; i++) {
	line_element = lines[i].split(' ');
            for (let j = 0; j < line_element.length; j++) {
            	parsing = parseFloat(line_element[j]);
                bl_values[i] = bl_values[i] + coef[j]*line_element[j];
            }
}

bl_max_value = Math.max.apply(Math, bl_values);

for (var i = 0; i < bl_values.length; i++) {
    if (bl_values[i]==bl_max_value) {
    	best3 = lines[i];
    }
}
console.log("Значення розраховані по формулі:" + bl_values);
console.log("Найкраще рішення:"+best3);
