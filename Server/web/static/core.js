function programAlerts(){
	setInterval(checkAlerts, 1000);
}

function checkAlerts(){

	//checkHeigth();
	checkPitch();
	//checkRoll();
	//checkSpeed();

}

function checkSpeed(){

	var speedLimits = {
		speed_manual: "25",
		speed_automatic: "5",
		speed_warning: "20"
	};

	$.ajax({
		url: "http://localhost:5000/speedStatus",
		method: "POST",
		contentType: "application/json",
		data: JSON.stringify(speedLimits),
		dataType: "json",
		success: (function(data) {
			if(data["message"]["alert_message"] != "All normal"){
				if(data["message"]["alert_message"].startsWith("Alarma automatica"))
					alert(data["message"]["alert_message"]);
				else if(data["message"]["alert_message"].startsWith("Alarma manual"))
					if(confirm(data["message"]["alert_message"]) == true) sendAction(data["message"]["alert_message"]);
			}			
			if(data["message"]["notification_message"] != "All normal"){
				var textarea = document.getElementById('log');
				textarea.value += data["message"]["notification_message"];
				textarea.value += "\n";
			}
		})
	});

}
function checkRoll(){

	var rollLimits = {
		roll_manual: "20",
		roll_automatic: "30"
	};

	$.ajax({
		url: "http://localhost:5000/rollStatus",
		method: "POST",
		contentType: "application/json",
		data: JSON.stringify(rollLimits),
		dataType: "json",
		success: (function(data) {
			if(data["message"]["alert_message"] != "All normal"){
				if(data["message"]["alert_message"].startsWith("Alarma automatica"))
					alert(data["message"]["alert_message"]);
				else if(data["message"]["alert_message"].startsWith("Alarma manual"))
					if(confirm(data["message"]["alert_message"]) == true) sendAction(data["message"]["alert_message"]);
			}			
			if(data["message"]["notification_message"] != "All normal"){
				var textarea = document.getElementById('log');
				textarea.value += data["message"]["notification_message"];
				textarea.value += "\n";
			}
		})
	});

}

function checkPitch(){

	var pitchLimits = {
		pitch_manual: "20",
		pitch_automatic: "30"
	};

	$.ajax({
		url: "http://localhost:5000/pitchStatus",
		method: "POST",
		contentType: "application/json",
		data: JSON.stringify(pitchLimits),
		dataType: "json",
		success: (function(data) {
			console.log(data)
			if(data["message"]["alert_message"] != "All normal"){
				if(data["message"]["alert_message"].startsWith("Alarma automatica"))
					alert(data["message"]["alert_message"]);
				else if(data["message"]["alert_message"].startsWith("Alarma manual"))
					if(confirm(data["message"]["alert_message"]) == true) sendAction(data["message"]["alert_message"]);
			}			
			if(data["message"]["notification_message"] != "All normal"){
				var textarea = document.getElementById('log');
				textarea.value += data["message"]["notification_message"];
				textarea.value += "\n";
			}

		})
	});

}
function checkHeigth(){

	var heigthLimits = {
		heigth_manual: "20",
		heigth_automatic: "30"
	};

	$.ajax({
		url: "http://localhost:5000/heigthStatus",
		method: "POST",
		contentType: "application/json",
		data: JSON.stringify(heigthLimits),
		dataType: "json",
		success: (function(data) {
			if(data["message"]["alert_message"] != "All normal"){
				if(data["message"]["alert_message"].startsWith("Alarma automatica"))
					alert(data["message"]["alert_message"]);
				else if(data["message"]["alert_message"].startsWith("Alarma manual"))
					if(confirm(data["message"]["alert_message"]) == true) sendAction(data["message"]["alert_message"]);
			}			
			if(data["message"]["notification_message"] != "All normal"){
				var textarea = document.getElementById('log');
				textarea.value += data["message"]["notification_message"];
				textarea.value += "\n";
			}
		})
	});

}


function sendAction(message){

	var payload = {"message": message};

	$.ajax({
		url: "http://localhost:5000/sendAction",
		method: "POST",
		contentType: "application/json",
		data: JSON.stringify(payload),
		dataType: "json",
		success: (function(data) {})
	});

}
$(document).ready(programAlerts());

