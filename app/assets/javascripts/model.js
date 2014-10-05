var grades = ["A+", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-", "F"];

function saveCookie(data) {
	// I promise this works
	document.cookie = "grades=" + [].concat.apply([], data.semesters.map(function (x) { return x["classes"]; })).filter(function (x) { return x["transcript"] != null; }).map(function (x) { var a = {}; a[x.course_code] = x.transcript[0].grade; return a; } ).reduce(function (a, b) { return $.extend(a, b); } );
}

function updateHistogram(past_class, future_class, past_grade) {
    return $.getJSON('/models/' + past_class + '/' + future_class, function(data) {
        if (!jQuery.isEmptyObject(data)) {
        	var gradehist = [];
        	for (var i = 0; i < grades.length; i++) {
                console.log(data.histogram);
        		for (var j = 0; j < data.histogram[past_grade][grades[i]]; j++) {
                    gradehist.push(i);
                }
        	}
            console.log(gradehist);
        	histogram(gradehist);
        }
        else {
            console.log("not enough data");
        }
    });
}

function histogram(values) {
    // Normalize
    var total = 0;
    $.each(values,function() {
        total += this;
    });

    var bar_height = 300;
    $("#barAp").height((values[0] / total * bar_height) + "%");
    $("#barA").height((values[1] / total * bar_height) + "%");
    $("#barAm").height((values[2] / total * bar_height) + "%");
    $("#barBp").height((values[3] / total * bar_height) + "%");
    $("#barB").height((values[4] / total * bar_height) + "%");
    $("#barBm").height((values[5] / total * bar_height) + "%");
    $("#barCp").height((values[6] / total * bar_height) + "%");
    $("#barC").height((values[7] / total * bar_height) + "%");
    $("#barCm").height((values[8] / total * bar_height) + "%");
    $("#barDp").height((values[9] / total * bar_height) + "%");
    $("#barD").height((values[10] / total * bar_height) + "%");
    $("#barDm").height((values[11] / total * bar_height) + "%");
    $("#barF").height((values[12] / total * bar_height) + "%");

    $("#percentA").text(Math.round((values[0] + values[1] + values[2]) * 100 / total) + "%");
    $("#percentB").text(Math.round((values[3] + values[4] + values[5]) * 100 / total) + "%");
    $("#percentC").text(Math.round((values[6] + values[7] + values[8]) * 100 / total) + "%");
    $("#percentD").text(Math.round((values[10] + values[11] + values[12]) * 100 / total) + "%");
    $("#percentF").text(Math.round(values[12] * 100 / total) + "%");
    // A formatter for counts.
    /*
    d3.select("svg").remove();
    
    // A formatter for counts.
    var formatCount = d3.format(",.0f");

    var margin = {top: 10, right: 30, bottom: 30, left: 30},
        width = 960 - margin.left - margin.right,
        height = 500 - margin.top - margin.bottom;

    var x = d3.scale.linear()
        .domain([0, 12])
        .range([0, width]);

    // Generate a histogram using twenty uniformly-spaced bins.
    var data = d3.layout.histogram()
        .bins(x.ticks(12))
        (values);

    console.log(data)

    var y = d3.scale.linear()
        .domain([0, d3.max(data, function(d) { return d.y; })])
        .range([height, 0]);

    var xAxis = d3.svg.axis()
        .scale(x)
        .orient("bottom");

    var svg = d3.select("#canvas").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    var bar = svg.selectAll(".bar")
        .data(data)
      .enter().append("g")
        .attr("class", "bar")
        .attr("transform", function(d) { return "translate(" + x(d.x) + "," + y(d.y) + ")"; });

    bar.append("rect")
        .attr("x", 1)
        .attr("width", x(data[0].dx) - 1)
        .attr("height", function(d) { return height - y(d.y); })
        .attr("fill");

    bar.append("text")
        .attr("dy", ".75em")
        .attr("y", 6)
        .attr("x", x(data[0].dx) / 2)
        .attr("text-anchor", "middle")
        .attr("fill", "blue")
        .text(function(d) { return formatCount(d.y); });

    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);
    */
}

function myClasses() {
    var select = document.getElementById("select1");
    return $.getJSON('/courses.json', function(data) {
        for (var i = 0; i < data.length; i++) {
            var opt = data[i].name;
            var el = document.createElement("option");
            el.textContent = opt;
            el.value = opt;
            select.appendChild(el);
            console.log(data[i].name);
        }
    });
}

function allClasses() {
    var select = document.getElementById("select2");
    return $.getJSON('/courses.json', function(data) {
        for (var i = 0; i < data.length; i++) {
            var opt = data[i].name;
            var el = document.createElement("option");
            el.textContent = opt;
            el.value = opt;
            select.appendChild(el);
            console.log(data[i].name);
        }
    });
}

function draw() {
    var class1 = $("#select1 option:selected").text();
    var class2 = $("#select2 option:selected").text();
    updateHistogram(class1, class2, "A-")
}

function moveSelects() {
    $("#select1").appendTo("#newselectlocation");
    $("#select2").appendTo("#newselectlocation");
}
