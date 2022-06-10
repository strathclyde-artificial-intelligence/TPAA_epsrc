'use strict';

class Model {

	constructor() {

		this.problemObject;
		this.tokenObject;
		this.codeOutput;
	}

	fetchProblemObject(editor, problemNumber, setCode, setProblemStatement) {
		//fetching function for visiting currency
		let xhr = new XMLHttpRequest();
		const that = this;
		if(currentProblem == null) {
			//if the number has not been set or cleared we fetch the first problem
			problemNumber = numbers[0];
		}

		xhr.addEventListener("load", function() {
			let text = this.responseText;
			let jsonObj = JSON.parse(text);
			that.setProblemObject(jsonObj);
			view.setCode(editor, jsonObj.code);
			view.setProblemStatement(jsonObj.statement);
			view.displayProblemText();
			view.changeActiveButton("Problem");
		});

		let URL = "index.php/?func="+problemNumber;
		xhr.open("GET", URL, true);
		xhr.send();
	}

	setLocalStorage(nameOfCurrentProblem) {
		console.log(nameOfCurrentProblem);
		localStorage.setItem("currentProblem", nameOfCurrentProblem);
	}


	sendCodeRequest(codeRan, setCodeOutputBox, testString) {

		let test = codeRan + testString;
		console.log(test);
		let newData = btoa(test);
		const data = JSON.stringify({
		"language_id": 71,
		"source_code": newData, 
		"stdin": "SnVkZ2Uw"
	});

		const xhr = new XMLHttpRequest();
		xhr.withCredentials = false;
		const that = this;

		xhr.addEventListener("readystatechange", function () {
			
				if (this.readyState === this.DONE) {
					let object = this.responseText;
					that.fetchCodeResult(JSON.parse(object), setCodeOutputBox);
				}
		});

		xhr.open("POST", "https://judge0-ce.p.rapidapi.com/submissions?base64_encoded=true&fields=*");
		xhr.setRequestHeader("content-type", "application/json");
		xhr.setRequestHeader("Content-Type", "application/json");
		xhr.setRequestHeader("X-RapidAPI-Key", "1b2e2dc18fmsh22a79fc79be240fp129ea7jsn783b92950d99");
		xhr.setRequestHeader("X-RapidAPI-Host", "judge0-ce.p.rapidapi.com");

		xhr.send(data);
	}

	setTokenObject(tokenReceived) {
		this.tokenObject = tokenReceived;
	}

	fetchCodeResult(responseObject, setCodeOutputBox) {
		const data = null;
		const that = this;

		const xhr = new XMLHttpRequest();
		xhr.withCredentials = false;

		xhr.addEventListener("readystatechange", function () {

				if(this.readyState == this.DONE) {
					let collectedData = this.responseText;
					let data = JSON.parse(collectedData);
					console.log(data.stdout);
					that.setProblemOutput(atob(data.stdout));
					view.setCodeOutputBox(atob(data.stdout));
				}
		});

		xhr.open("GET", "https://judge0-ce.p.rapidapi.com/submissions/"+responseObject.token+"?base64_encoded=true&fields=*");
		xhr.setRequestHeader("X-RapidAPI-Key", "1b2e2dc18fmsh22a79fc79be240fp129ea7jsn783b92950d99");
		xhr.setRequestHeader("X-RapidAPI-Host", "judge0-ce.p.rapidapi.com");

		xhr.send(data);

	}


	getToken() {
		return this.tokenObject;
	}

	setProblemObject(jsonObj) {
		this.problemObject = jsonObj;
	}

	setProblemOutput(output) {
		this.codeOutput = output;
	}

	getProblemOutput() {
		return this.codeOutput;
	}

	getProblemObject() {
		return this.problemObject;
	}
}
